#!/usr/bin/env python3
"""
语雀文档管理工具

功能：
- 创建 / 读取 / 更新 / 删除文档
- 搜索文档或知识库

注：评论相关操作已拆分到 scripts/yuque_comment.py。

使用方法：
    # 创建文档
    python yuque_doc.py --token <TOKEN> --repo <group_login/book_slug> create --title "标题" --file content.md

    # 读取文档
    python yuque_doc.py --token <TOKEN> --repo <group_login/book_slug> read --slug <doc_slug>

    # 更新文档
    python yuque_doc.py --token <TOKEN> --repo <group_login/book_slug> update --slug <doc_slug> --file content.md

    # 搜索文档
    python yuque_doc.py --token <TOKEN> --repo <group_login/book_slug> search --query "关键词"
"""

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request


class YuqueClient:
    """语雀 API 客户端"""
    
    BASE_URL = "https://yuque-api.antfin-inc.com/api/v2"
    
    def __init__(self, token: str):
        self.token = token
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "X-Auth-Token": self.token,
            "Content-Type": "application/json",
        }
        
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            raise Exception(f"API Error {e.code}: {error_body}")
    
    def get(self, endpoint: str) -> dict:
        return self._request("GET", endpoint)
    
    def post(self, endpoint: str, data: dict) -> dict:
        return self._request("POST", endpoint, data)
    
    def put(self, endpoint: str, data: dict) -> dict:
        return self._request("PUT", endpoint, data)
    
    def delete(self, endpoint: str) -> dict:
        return self._request("DELETE", endpoint)
    
    def create_doc(self, group_login: str, book_slug: str, title: str, body: str) -> dict:
        data = {
            "title": title,
            "body": body,
            "format": "markdown",
            "public": 0,
        }
        result = self.post(f"/repos/{group_login}/{book_slug}/docs", data)
        return result.get("data", {})
    
    def get_doc(self, group_login: str, book_slug: str, doc_slug: str) -> dict:
        result = self.get(f"/repos/{group_login}/{book_slug}/docs/{doc_slug}")
        return result.get("data", {})
    
    def update_doc(self, group_login: str, book_slug: str, doc_slug: str, 
                   title: str = None, body: str = None) -> dict:
        data = {}
        if title:
            data["title"] = title
        if body:
            data["body"] = body
        result = self.put(f"/repos/{group_login}/{book_slug}/docs/{doc_slug}", data)
        return result.get("data", {})
    
    def delete_doc(self, group_login: str, book_slug: str, doc_slug: str) -> dict:
        result = self.delete(f"/repos/{group_login}/{book_slug}/docs/{doc_slug}")
        return result.get("data", {})

    def search(self, query: str, scope: str = None, search_type: str = "doc",
               page: int = 1, creator: str = None) -> dict:
        """
        搜索文档或知识库

        参数:
            query: 搜索关键词，最大 200 字符
            scope: 搜索范围 (group_login 或 group_login/book_slug)，不填为当前用户/团队
            search_type: 搜索类型 (doc=文档, repo=知识库)
            page: 页码 1-100
            creator: 作者 login（可选）

        返回:
            包含 data 和 meta 的字典
        """
        # scope 的形式是 group_login 或 group_login/book_slug，
        # 保留 `/` 不编码（OpenAPI 规范中 scope 是这种原样格式）
        params = [("q", query), ("type", search_type), ("page", page)]
        if scope:
            params.append(("scope", scope))
        if creator:
            params.append(("creator", creator))
        # 用 quote_via=quote 保留斜杠
        url = f"/search?{urllib.parse.urlencode(params, quote_via=lambda s, *a, **kw: urllib.parse.quote(s, safe='/'))}"

        result = self.get(url)
        return {
            "data": result.get("data", []),
            "meta": result.get("meta", {})
        }


def cmd_create(client: YuqueClient, group_login: str, book_slug: str, args):
    """创建文档"""
    # 读取文件内容
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            body = f.read()
    else:
        body = args.body or ""
    
    try:
        result = client.create_doc(group_login, book_slug, args.title, body)
        print(f"✅ 创建文档成功")
        print(f"   ID: {result.get('id')}")
        print(f"   Slug: {result.get('slug')}")
        print(f"   URL: https://yuque.antfin.com/{group_login}/{book_slug}/{result.get('slug')}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")


def cmd_read(client: YuqueClient, group_login: str, book_slug: str, args):
    """读取文档"""
    try:
        result = client.get_doc(group_login, book_slug, args.slug)
        print(f"标题: {result.get('title')}")
        print(f"ID: {result.get('id')}")
        print(f"字数: {result.get('word_count')}")
        print(f"创建时间: {result.get('created_at')}")
        print(f"更新时间: {result.get('updated_at')}")
        print("-" * 40)
        
        if args.format == "markdown":
            print(result.get("body", ""))
        elif args.format == "html":
            print(result.get("body_html", ""))
        else:
            print(result.get("body", ""))
    except Exception as e:
        print(f"❌ 读取失败: {e}")


def cmd_update(client: YuqueClient, group_login: str, book_slug: str, args):
    """更新文档"""
    body = None
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            body = f.read()
    
    try:
        result = client.update_doc(group_login, book_slug, args.slug, args.title, body)
        print(f"✅ 更新文档成功")
        print(f"   更新时间: {result.get('updated_at')}")
    except Exception as e:
        print(f"❌ 更新失败: {e}")


def cmd_delete(client: YuqueClient, group_login: str, book_slug: str, args):
    """删除文档"""
    if not args.force:
        confirm = input(f"确定要删除文档 '{args.slug}' 吗？(y/N): ")
        if confirm.lower() != "y":
            print("已取消")
            return
    
    try:
        client.delete_doc(group_login, book_slug, args.slug)
        print(f"✅ 删除文档成功")
    except Exception as e:
        print(f"❌ 删除失败: {e}")







def cmd_search(client: YuqueClient, group_login: str, book_slug: str, args):
    """搜索文档或知识库"""
    scope = f"{group_login}/{book_slug}" if args.in_repo else group_login
    search_type = getattr(args, "type", None) or "doc"
    page = getattr(args, "page", None) or 1
    creator = getattr(args, "creator", None)
    
    try:
        result = client.search(args.query, scope, search_type, page, creator)
        data = result.get("data", [])
        meta = result.get("meta", {})
        total = meta.get("total", len(data))
        
        print(f"共 {total} 个结果")
        if total > len(data):
            print(f"（当前显示第 {page} 页，每页 20 条）\n")
        else:
            print()
        
        for item in data:
            if search_type == "doc":
                print(f"📄 {item.get('title')}")
                print(f"   ID: {item.get('id')}")
                print(f"   Slug: {item.get('slug')}")
                if item.get("book"):
                    print(f"   知识库: {item['book'].get('name')}")
            else:  # repo
                print(f"📚 {item.get('name')}")
                print(f"   ID: {item.get('id')}")
                print(f"   Slug: {item.get('slug')}")
            print()
    except Exception as e:
        print(f"❌ 搜索失败: {e}")


def main():
    parser = argparse.ArgumentParser(description="语雀文档管理工具")
    parser.add_argument("--token", required=True, help="语雀 API Token")
    parser.add_argument("--repo", required=True, help="目标知识库 (group_login/book_slug)")
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建文档")
    create_parser.add_argument("--title", required=True, help="文档标题")
    create_parser.add_argument("--file", help="Markdown 文件路径")
    create_parser.add_argument("--body", help="文档内容（与 --file 二选一）")
    
    # read 命令
    read_parser = subparsers.add_parser("read", help="读取文档")
    read_parser.add_argument("--slug", required=True, help="文档 slug")
    read_parser.add_argument("--format", choices=["markdown", "html"], default="markdown", help="输出格式")
    
    # update 命令
    update_parser = subparsers.add_parser("update", help="更新文档")
    update_parser.add_argument("--slug", required=True, help="文档 slug")
    update_parser.add_argument("--title", help="新标题")
    update_parser.add_argument("--file", help="新内容文件")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除文档")
    delete_parser.add_argument("--slug", required=True, help="文档 slug")
    delete_parser.add_argument("--force", action="store_true", help="跳过确认")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索文档或知识库")
    search_parser.add_argument("--query", required=True, help="搜索关键词（最大 200 字符）")
    search_parser.add_argument("--type", choices=["doc", "repo"], default="doc", help="搜索类型：doc=文档, repo=知识库")
    search_parser.add_argument("--in-repo", action="store_true", help="仅在当前知识库搜索")
    search_parser.add_argument("--page", type=int, default=1, help="页码（1-100）")
    search_parser.add_argument("--creator", help="按作者 login 过滤")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # 解析知识库路径
    repo_parts = args.repo.split("/")
    if len(repo_parts) != 2:
        print("错误: --repo 格式应为 group_login/book_slug")
        return 1
    
    group_login, book_slug = repo_parts
    client = YuqueClient(args.token)
    
    # 执行命令
    commands = {
        "create": cmd_create,
        "read": cmd_read,
        "update": cmd_update,
        "delete": cmd_delete,
        "search": cmd_search,
    }
    
    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(client, group_login, book_slug, args)
    
    return 0


if __name__ == "__main__":
    exit(main())
