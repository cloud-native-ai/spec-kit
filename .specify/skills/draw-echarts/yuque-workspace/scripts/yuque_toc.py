#!/usr/bin/env python3
"""
语雀目录管理工具

功能：
- 查看知识库目录结构
- 创建目录分组 / 外链节点
- 将文档加入目录
- 移动 / 编辑 / 删除目录节点

使用方法：
    # 查看目录结构（完整显示 UUID 便于后续操作）
    python yuque_toc.py --token <TOKEN> --repo <group_login/book_slug> list

    # 创建分组（根目录）
    python yuque_toc.py --token <TOKEN> --repo <group_login/book_slug> create-group --title "分组名称"

    # 创建子分组
    python yuque_toc.py --token <TOKEN> --repo <group_login/book_slug> create-group --title "子分组" --parent "父分组"

    # 将文档加入目录
    python yuque_toc.py --token <TOKEN> --repo <group_login/book_slug> add-doc --doc-id 12345 --parent "分组名"

    # 移动节点
    python yuque_toc.py --token <TOKEN> --repo <group_login/book_slug> move --node <node_uuid> --target <target_uuid> --mode child

    # 编辑节点
    python yuque_toc.py --token <TOKEN> --repo <group_login/book_slug> edit --node <node_uuid> --title "新标题"

    # 删除节点
    python yuque_toc.py --token <TOKEN> --repo <group_login/book_slug> remove --node <node_uuid>
"""

import argparse
import json
import urllib.error
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
    
    def put(self, endpoint: str, data: dict) -> dict:
        return self._request("PUT", endpoint, data)
    
    def get_toc(self, group_login: str, book_slug: str) -> list:
        result = self.get(f"/repos/{group_login}/{book_slug}/toc")
        return result.get("data", [])
    
    def update_toc(self, group_login: str, book_slug: str, toc_data: dict) -> list:
        """更新目录结构，返回更新后的完整目录列表"""
        result = self.put(f"/repos/{group_login}/{book_slug}/toc", toc_data)
        return result.get("data", [])


_TYPE_ICONS = {"TITLE": "📁", "DOC": "📄", "LINK": "🔗"}


def cmd_list(client: YuqueClient, group_login: str, book_slug: str, args):
    """列出目录结构"""
    toc = client.get_toc(group_login, book_slug)

    for item in toc:
        level = item.get("level", 0)
        indent = "  " * level
        icon = _TYPE_ICONS.get(item.get("type", ""), "•")
        extra = ""
        if item.get("type") == "DOC" and item.get("doc_id"):
            extra = f" doc_id={item['doc_id']}"
        elif item.get("type") == "LINK" and item.get("url"):
            extra = f" url={item['url']}"
        uuid_display = item.get("uuid", "") if args.full_uuid else item.get("uuid", "")[:8] + "..."
        print(f"{indent}{icon} {item.get('title', '')} [{item.get('type')}]{extra} (uuid: {uuid_display})")

    print(f"\n共 {len(toc)} 个节点")


def _find_node_by_title(toc: list, title: str, node_type: str = None) -> dict:
    """根据标题查找节点；node_type 可选 'TITLE' / 'DOC' / 'LINK'"""
    for item in toc:
        if item.get("title") == title:
            if node_type is None or item.get("type") == node_type:
                return item
    return None


def cmd_create_group(client: YuqueClient, group_login: str, book_slug: str, args):
    """创建分组（TITLE 节点）

    根据 OpenAPI 规范：创建场景下 target_uuid 可省略（默认添加到根节点）。
    """
    toc_data = {
        "action": "appendNode",
        "action_mode": "child",
        "type": "TITLE",
        "title": args.title,
    }

    if args.parent:
        toc = client.get_toc(group_login, book_slug)
        parent = _find_node_by_title(toc, args.parent, "TITLE")
        if not parent:
            print(f"错误: 找不到父分组 '{args.parent}'")
            return
        toc_data["target_uuid"] = parent["uuid"]

    try:
        result = client.update_toc(group_login, book_slug, toc_data)
        print(f"✅ 创建分组成功: {args.title}")
        if isinstance(result, list):
            matches = [i for i in result
                       if i.get("title") == args.title and i.get("type") == "TITLE"]
            if matches:
                print(f"   UUID: {matches[-1]['uuid']}")
    except Exception as e:
        print(f"❌ 创建分组失败: {e}")


def cmd_create_link(client: YuqueClient, group_login: str, book_slug: str, args):
    """创建外链节点（LINK 节点）"""
    toc_data = {
        "action": "appendNode",
        "action_mode": "child",
        "type": "LINK",
        "title": args.title,
        "url": args.url,
        "open_window": 1 if args.new_window else 0,
    }

    if args.parent:
        toc = client.get_toc(group_login, book_slug)
        parent = _find_node_by_title(toc, args.parent, "TITLE")
        if not parent:
            print(f"错误: 找不到父分组 '{args.parent}'")
            return
        toc_data["target_uuid"] = parent["uuid"]

    try:
        client.update_toc(group_login, book_slug, toc_data)
        print(f"✅ 创建外链节点成功: {args.title} -> {args.url}")
    except Exception as e:
        print(f"❌ 创建外链节点失败: {e}")


def cmd_add_doc(client: YuqueClient, group_login: str, book_slug: str, args):
    """将文档加入目录

    创建场景：target_uuid 可省略（默认根节点），必须使用 doc_ids 数组。
    """
    toc_data = {
        "action": "appendNode",
        "action_mode": "child",
        "type": "DOC",
        "doc_ids": [args.doc_id],
    }

    if args.parent:
        toc = client.get_toc(group_login, book_slug)
        parent = _find_node_by_title(toc, args.parent, "TITLE")
        if not parent:
            print(f"错误: 找不到父分组 '{args.parent}'")
            return
        toc_data["target_uuid"] = parent["uuid"]

    try:
        client.update_toc(group_login, book_slug, toc_data)
        print("✅ 文档已加入目录")
    except Exception as e:
        print(f"❌ 操作失败: {e}")


def cmd_move(client: YuqueClient, group_login: str, book_slug: str, args):
    """移动节点：target_uuid 和 node_uuid 都必填"""
    toc_data = {
        "action": "appendNode",
        "action_mode": args.mode,
        "node_uuid": args.node,
        "target_uuid": args.target,
    }
    try:
        client.update_toc(group_login, book_slug, toc_data)
        print(f"✅ 节点已移动 (mode={args.mode})")
    except Exception as e:
        print(f"❌ 移动失败: {e}")


def cmd_edit(client: YuqueClient, group_login: str, book_slug: str, args):
    """编辑节点：node_uuid 必填，可选 title / url / open_window / visible"""
    toc_data = {
        "action": "editNode",
        "action_mode": "child",
        "node_uuid": args.node,
    }
    if args.title is not None:
        toc_data["title"] = args.title
    if args.url is not None:
        toc_data["url"] = args.url
    if args.open_window is not None:
        toc_data["open_window"] = args.open_window
    if args.visible is not None:
        toc_data["visible"] = args.visible

    try:
        client.update_toc(group_login, book_slug, toc_data)
        print("✅ 节点已更新")
    except Exception as e:
        print(f"❌ 编辑失败: {e}")


def cmd_remove(client: YuqueClient, group_login: str, book_slug: str, args):
    """删除节点（不会删除关联文档）

    action_mode=sibling 仅删除当前节点；child 删除当前节点及所有子节点。
    """
    if not args.force:
        confirm = input(f"确定要删除节点 {args.node} 吗？(y/N): ")
        if confirm.lower() != "y":
            print("已取消")
            return

    toc_data = {
        "action": "removeNode",
        "action_mode": "child" if args.with_children else "sibling",
        "node_uuid": args.node,
    }
    try:
        client.update_toc(group_login, book_slug, toc_data)
        print("✅ 节点已删除")
    except Exception as e:
        print(f"❌ 删除失败: {e}")


def main():
    parser = argparse.ArgumentParser(description="语雀目录管理工具")
    parser.add_argument("--token", required=True, help="语雀 API Token")
    parser.add_argument("--repo", required=True, help="目标知识库 (group_login/book_slug)")
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出目录结构")
    list_parser.add_argument("--full-uuid", action="store_true", help="显示完整的 UUID")

    # create-group 命令
    create_group_parser = subparsers.add_parser("create-group", help="创建分组 (TITLE 节点)")
    create_group_parser.add_argument("--title", required=True, help="分组标题")
    create_group_parser.add_argument("--parent", help="父分组标题（可选）")

    # create-link 命令
    create_link_parser = subparsers.add_parser("create-link", help="创建外链节点 (LINK 节点)")
    create_link_parser.add_argument("--title", required=True, help="节点标题")
    create_link_parser.add_argument("--url", required=True, help="外链 URL")
    create_link_parser.add_argument("--parent", help="父分组标题（可选）")
    create_link_parser.add_argument("--new-window", action="store_true", help="在新窗口打开")

    # add-doc 命令
    add_doc_parser = subparsers.add_parser("add-doc", help="将文档加入目录")
    add_doc_parser.add_argument("--doc-id", required=True, type=int, help="文档 ID")
    add_doc_parser.add_argument("--parent", help="父分组标题（可选）")

    # move 命令
    move_parser = subparsers.add_parser("move", help="移动目录节点")
    move_parser.add_argument("--node", required=True, help="要移动的节点 UUID")
    move_parser.add_argument("--target", required=True, help="目标节点 UUID")
    move_parser.add_argument("--mode", choices=["child", "sibling"], default="child",
                             help="child=作为子节点, sibling=作为兄弟节点")

    # edit 命令
    edit_parser = subparsers.add_parser("edit", help="编辑目录节点")
    edit_parser.add_argument("--node", required=True, help="节点 UUID")
    edit_parser.add_argument("--title", help="新标题")
    edit_parser.add_argument("--url", help="新 URL（仅 LINK 类型）")
    edit_parser.add_argument("--open-window", type=int, choices=[0, 1], help="是否新窗口打开")
    edit_parser.add_argument("--visible", type=int, choices=[0, 1], help="是否可见")

    # remove 命令
    remove_parser = subparsers.add_parser("remove", help="删除目录节点（不会删除文档）")
    remove_parser.add_argument("--node", required=True, help="要删除的节点 UUID")
    remove_parser.add_argument("--with-children", action="store_true",
                               help="同时删除所有子节点（action_mode=child）")
    remove_parser.add_argument("--force", action="store_true", help="跳过确认")

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
        "list": cmd_list,
        "create-group": cmd_create_group,
        "create-link": cmd_create_link,
        "add-doc": cmd_add_doc,
        "move": cmd_move,
        "edit": cmd_edit,
        "remove": cmd_remove,
    }
    
    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(client, group_login, book_slug, args)
    
    return 0


if __name__ == "__main__":
    exit(main())
