#!/usr/bin/env python3
"""
语雀文档评论管理工具

功能：
- 获取文档评论列表（支持 lastId 分页）
- 查看单条评论详情
- 创建 / 更新 / 删除评论
- 支持按文档 slug 自动解析 doc_id

使用方法：
    # 查看文档评论列表
    python yuque_comment.py --token <TOKEN> --repo <group_login/book_slug> list --slug <doc_slug>

    # 查看单条评论详情
    python yuque_comment.py --token <TOKEN> --repo <group_login/book_slug> show --comment-id 304742631

    # 创建评论（按 slug）
    python yuque_comment.py --token <TOKEN> --repo <group_login/book_slug> create --slug <doc_slug> --body "内容"

    # 回复某条评论
    python yuque_comment.py --token <TOKEN> --repo <group_login/book_slug> create --doc-id 12345 --body "回复内容" --parent-id 304742631

    # 更新评论
    python yuque_comment.py --token <TOKEN> --repo <group_login/book_slug> update --comment-id 304742631 --body "新内容"

    # 删除评论
    python yuque_comment.py --token <TOKEN> --repo <group_login/book_slug> delete --comment-id 304742631
"""

import argparse
import json
import re
import urllib.error
import urllib.parse
import urllib.request


class YuqueCommentClient:
    """语雀评论 API 客户端"""

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

    # ---- 内部辅助：通过 slug 解析 doc_id ----
    def resolve_doc_id_by_slug(self, group_login: str, book_slug: str, doc_slug: str) -> int:
        result = self.get(f"/repos/{group_login}/{book_slug}/docs/{doc_slug}")
        return (result.get("data") or {}).get("id")

    # ---- 评论 API ----
    def list_comments(self, doc_id: int, last_id: int = None) -> list:
        """
        获取文档的评论列表。

        参数:
            doc_id: 文档 ID（数字）
            last_id: 上一个评论 ID，用于分页（PageSize 固定 20）
        """
        params = {"commentable_id": doc_id}
        if last_id:
            params["lastId"] = last_id
        url = f"/comments?{urllib.parse.urlencode(params)}"
        result = self.get(url)
        return result.get("data", [])

    def show_comment(self, comment_id: int) -> dict:
        """获取单条评论详情"""
        result = self.get(f"/comments/{comment_id}")
        return result.get("data", {})

    def create_comment(self, doc_id: int, body: str,
                       fmt: str = "markdown", parent_id: int = None) -> dict:
        """
        创建评论。

        参数:
            doc_id: 文档 ID（commentable_id）
            body: 评论内容
            fmt: 内容格式 markdown / lake / text
            parent_id: 回复的评论 ID，可选
        """
        data = {
            "commentable_id": doc_id,
            "body": body,
            "format": fmt,
        }
        if parent_id:
            data["parent_id"] = parent_id
        result = self.post("/comments", data)
        return result.get("data", {})

    def update_comment(self, comment_id: int, body: str, fmt: str = "markdown") -> dict:
        """更新评论"""
        data = {"body": body, "format": fmt}
        result = self.put(f"/comments/{comment_id}", data)
        return result.get("data", {})

    def delete_comment(self, comment_id: int) -> dict:
        """删除评论"""
        result = self.delete(f"/comments/{comment_id}")
        return result.get("data", {})


def _resolve_doc_id(client: YuqueCommentClient, group_login: str, book_slug: str,
                    doc_id: int, slug: str):
    """把 --slug 解析为 doc_id；若两个都没提供返回 None"""
    if doc_id:
        return doc_id
    if slug:
        try:
            resolved = client.resolve_doc_id_by_slug(group_login, book_slug, slug)
            if not resolved:
                print(f"❌ 无法获取文档 '{slug}' 的 ID")
                return None
            return resolved
        except Exception as e:
            print(f"❌ 获取文档失败: {e}")
            return None
    print("❌ 必须指定 --doc-id 或 --slug")
    return None


def _read_body(args) -> str:
    """从 --body / --file 读取评论内容"""
    if getattr(args, "file", None):
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read()
    return getattr(args, "body", None) or ""


def cmd_list(client: YuqueCommentClient, group_login: str, book_slug: str, args):
    """获取文档评论列表"""
    doc_id = _resolve_doc_id(client, group_login, book_slug,
                             getattr(args, "doc_id", None),
                             getattr(args, "slug", None))
    if not doc_id:
        return

    try:
        comments = client.list_comments(doc_id, getattr(args, "last_id", None))
        if not comments:
            print("暂无评论")
            return

        print(f"共 {len(comments)} 条评论\n")
        for comment in comments:
            user = comment.get("user", {}) or {}
            parent_id = comment.get("parent_id")
            prefix = "  ↳ 回复" if parent_id else "💬"

            # 从 body_html 中提取纯文本
            body_html = comment.get("body_html", "")
            body_text = re.sub(r"<[^>]+>", "", body_html).strip()

            print(f"{prefix} [{user.get('name', '未知')}] ({comment.get('created_at', '')[:16]})")
            print(f"   {body_text}")
            if parent_id:
                print(f"   (回复评论 #{parent_id})")
            print(f"   ID: {comment.get('id')}")
            print()
    except Exception as e:
        print(f"❌ 获取评论失败: {e}")


def cmd_show(client: YuqueCommentClient, group_login: str, book_slug: str, args):
    """查看单条评论详情"""
    try:
        c = client.show_comment(args.comment_id)
        user = c.get("user", {}) or {}
        print(f"ID: {c.get('id')}")
        print(f"作者: {user.get('name', '未知')} (login: {user.get('login', '')})")
        print(f"格式: {c.get('format')}")
        print(f"创建时间: {c.get('created_at')}")
        print(f"更新时间: {c.get('updated_at')}")
        if c.get("parent_id"):
            print(f"回复: #{c.get('parent_id')}")
        print("-" * 40)
        print(c.get("body", ""))
    except Exception as e:
        print(f"❌ 查看评论失败: {e}")


def cmd_create(client: YuqueCommentClient, group_login: str, book_slug: str, args):
    """创建评论"""
    doc_id = _resolve_doc_id(client, group_login, book_slug,
                             getattr(args, "doc_id", None),
                             getattr(args, "slug", None))
    if not doc_id:
        return

    body = _read_body(args)
    if not body:
        print("❌ 必须指定 --body 或 --file")
        return

    try:
        result = client.create_comment(doc_id, body, args.format, args.parent_id)
        print("✅ 创建评论成功")
        print(f"   ID: {result.get('id')}")
        print(f"   创建时间: {result.get('created_at')}")
    except Exception as e:
        print(f"❌ 创建评论失败: {e}")


def cmd_update(client: YuqueCommentClient, group_login: str, book_slug: str, args):
    """更新评论"""
    body = _read_body(args)
    if not body:
        print("❌ 必须指定 --body 或 --file")
        return

    try:
        result = client.update_comment(args.comment_id, body, args.format)
        print("✅ 更新评论成功")
        print(f"   更新时间: {result.get('updated_at')}")
    except Exception as e:
        print(f"❌ 更新评论失败: {e}")


def cmd_delete(client: YuqueCommentClient, group_login: str, book_slug: str, args):
    """删除评论"""
    if not args.force:
        confirm = input(f"确定要删除评论 #{args.comment_id} 吗？(y/N): ")
        if confirm.lower() != "y":
            print("已取消")
            return
    try:
        client.delete_comment(args.comment_id)
        print("✅ 删除评论成功")
    except Exception as e:
        print(f"❌ 删除评论失败: {e}")


def _add_doc_ref_group(sub_parser):
    """为子命令添加 --doc-id / --slug 互斥参数"""
    grp = sub_parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--doc-id", type=int, help="文档 ID（数字）")
    grp.add_argument("--slug", help="文档 slug（自动解析为 doc_id）")


def main():
    parser = argparse.ArgumentParser(description="语雀文档评论管理工具")
    parser.add_argument("--token", required=True, help="语雀 API Token")
    parser.add_argument("--repo", required=True, help="目标知识库 (group_login/book_slug)")

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # list 命令
    list_parser = subparsers.add_parser("list", help="获取文档评论列表")
    _add_doc_ref_group(list_parser)
    list_parser.add_argument("--last-id", type=int, help="上一个评论 ID（分页用）")

    # show 命令
    show_parser = subparsers.add_parser("show", help="查看单条评论详情")
    show_parser.add_argument("--comment-id", type=int, required=True, help="评论 ID")

    # create 命令
    create_parser = subparsers.add_parser("create", help="创建评论")
    _add_doc_ref_group(create_parser)
    create_parser.add_argument("--body", help="评论内容")
    create_parser.add_argument("--file", help="从文件读取评论内容")
    create_parser.add_argument("--format", choices=["markdown", "lake", "text"],
                               default="markdown", help="内容格式")
    create_parser.add_argument("--parent-id", type=int, help="回复的评论 ID（可选）")

    # update 命令
    update_parser = subparsers.add_parser("update", help="更新评论")
    update_parser.add_argument("--comment-id", type=int, required=True, help="评论 ID")
    update_parser.add_argument("--body", help="新评论内容")
    update_parser.add_argument("--file", help="从文件读取评论内容")
    update_parser.add_argument("--format", choices=["markdown", "lake", "text"],
                               default="markdown", help="内容格式")

    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除评论")
    delete_parser.add_argument("--comment-id", type=int, required=True, help="评论 ID")
    delete_parser.add_argument("--force", action="store_true", help="跳过确认")

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
    client = YuqueCommentClient(args.token)

    commands = {
        "list": cmd_list,
        "show": cmd_show,
        "create": cmd_create,
        "update": cmd_update,
        "delete": cmd_delete,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(client, group_login, book_slug, args)

    return 0


if __name__ == "__main__":
    exit(main())
