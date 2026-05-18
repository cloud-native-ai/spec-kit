#!/usr/bin/env python3
"""
语雀批量同步工具

功能：
- 将本地 Markdown 目录批量同步到语雀知识库
- 自动创建目录分组（TITLE 节点）
- 自动将文档加入对应目录
- 支持增量同步

使用方法：
    python yuque_sync.py --token <TOKEN> --repo <group_login/book_slug> --local-dir <path>

示例：
    python yuque_sync.py --token xxx --repo team/docs --local-dir ./doc-repo
"""

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error


class YuqueClient:
    """语雀 API 客户端"""
    
    BASE_URL = "https://yuque-api.antfin-inc.com/api/v2"
    
    def __init__(self, token: str):
        self.token = token
        self.request_count = 0
        self.last_request_time = 0
    
    def _request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        """发送 API 请求"""
        # 频率控制：每秒最多 50 次
        current_time = time.time()
        if current_time - self.last_request_time < 0.02:  # 50ms 间隔
            time.sleep(0.02)
        
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "X-Auth-Token": self.token,
            "Content-Type": "application/json",
        }
        
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                self.last_request_time = time.time()
                self.request_count += 1
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
    
    def verify_token(self) -> bool:
        """验证 Token 是否有效"""
        try:
            self.get("/hello")
            return True
        except Exception:
            return False
    
    def get_toc(self, group_login: str, book_slug: str) -> list:
        """获取知识库目录结构"""
        result = self.get(f"/repos/{group_login}/{book_slug}/toc")
        return result.get("data", [])
    
    def create_doc(self, group_login: str, book_slug: str, title: str, body: str) -> dict:
        """创建文档"""
        data = {
            "title": title,
            "body": body,
            "format": "markdown",
            "public": 0,
        }
        result = self.post(f"/repos/{group_login}/{book_slug}/docs", data)
        return result.get("data", {})
    
    def update_toc(self, group_login: str, book_slug: str, toc_data: dict) -> list:
        """更新目录结构，返回更新后的完整目录列表"""
        result = self.put(f"/repos/{group_login}/{book_slug}/toc", toc_data)
        return result.get("data", [])
    
    def search_doc(self, query: str, scope: str) -> list:
        """搜索文档"""
        result = self.get(f"/search?q={query}&type=doc&scope={scope}")
        return result.get("data", [])


class LocalDocScanner:
    """本地文档扫描器"""
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
    
    def scan(self) -> list:
        """扫描本地目录，返回文档列表"""
        docs = []
        for md_file in sorted(self.base_dir.rglob("*.md")):
            rel_path = md_file.relative_to(self.base_dir)
            docs.append({
                "path": str(rel_path),
                "abs_path": str(md_file),
                "title": self._extract_title(md_file),
                "parent_dirs": list(rel_path.parent.parts),
            })
        return docs
    
    def _extract_title(self, file_path: Path) -> str:
        """使用文件名作为标题（不含扩展名）"""
        return file_path.stem


class YuqueSyncer:
    """语雀同步器"""
    
    def __init__(self, client: YuqueClient, group_login: str, book_slug: str):
        self.client = client
        self.group_login = group_login
        self.book_slug = book_slug
        self.toc_cache = {}  # path -> uuid 映射
        self.doc_id_map = {}  # path -> doc_id 映射
        self.title_to_path = {}  # title -> path 映射
    
    def sync(self, local_docs: list, dry_run: bool = False):
        """执行同步（方案B：先创建分组，再创建文档并直接添加到对应分组）"""
        print(f"开始同步 {len(local_docs)} 个文档到 {self.group_login}/{self.book_slug}")
        
        if dry_run:
            print("[DRY RUN 模式]")
            for doc in local_docs:
                parent = "/".join(doc["parent_dirs"]) if doc["parent_dirs"] else "根目录"
                print(f"  将创建文档: {doc['title']} (位于: {parent})")
            return
        
        # 第一步：创建目录分组结构
        print("\n第一步：创建目录分组结构...")
        dir_uuid_map = self._create_toc_groups(local_docs)
        
        # 第二步：创建文档并直接添加到对应分组
        print("\n第二步：创建文档并添加到对应分组...")
        self._create_docs_with_toc(local_docs, dir_uuid_map)
        
        print(f"\n同步完成！")
        print(f"API 调用次数: {self.client.request_count}")
    
    def _create_toc_groups(self, local_docs: list) -> dict:
        """创建目录分组结构，返回 dir_path -> uuid 的映射"""
        # 收集所有需要的目录
        all_dirs = set()
        for doc in local_docs:
            if doc["parent_dirs"]:
                for i in range(len(doc["parent_dirs"])):
                    dir_path = "/".join(doc["parent_dirs"][:i+1])
                    all_dirs.add(dir_path)
        
        if not all_dirs:
            print("  无需创建分组（所有文档都在根目录）")
            return {}
        
        print(f"需要创建 {len(all_dirs)} 个分组")
        
        # 按层级排序（先创建父目录）
        sorted_dirs = sorted(all_dirs, key=lambda x: x.count("/"))
        
        # 创建目录节点
        dir_uuid_map = {}
        
        for dir_path in sorted_dirs:
            parts = dir_path.split("/")
            dir_name = parts[-1]
            parent_path = "/".join(parts[:-1]) if len(parts) > 1 else ""
            
            # 获取父节点 uuid
            parent_uuid = dir_uuid_map.get(parent_path)
            
            # 创建 TITLE 节点
            try:
                toc_data = {
                    "action": "appendNode",
                    "action_mode": "child",
                    "type": "TITLE",
                    "title": dir_name,
                }
                
                # 如果有父节点，指定 target_uuid
                if parent_uuid:
                    toc_data["target_uuid"] = parent_uuid
                
                result = self.client.update_toc(self.group_login, self.book_slug, toc_data)
                
                # 找到新创建的节点
                found = False
                for item in result:
                    if item.get("title") == dir_name and item.get("type") == "TITLE":
                        if parent_uuid:
                            if item.get("parent_uuid") == parent_uuid:
                                dir_uuid_map[dir_path] = item["uuid"]
                                print(f"  创建分组: {dir_path}")
                                found = True
                                break
                        else:
                            if not item.get("parent_uuid"):
                                dir_uuid_map[dir_path] = item["uuid"]
                                print(f"  创建分组: {dir_path}")
                                found = True
                                break
                
                if not found:
                    for item in result:
                        if item.get("title") == dir_name and item.get("type") == "TITLE":
                            dir_uuid_map[dir_path] = item["uuid"]
                            print(f"  使用已存在分组: {dir_path}")
                            break
                
            except Exception as e:
                print(f"  创建分组失败: {dir_path} - {e}")
        
        return dir_uuid_map
    
    def _create_docs_with_toc(self, local_docs: list, dir_uuid_map: dict):
        """创建文档并直接添加到对应分组"""
        created_count = 0
        
        for i, doc in enumerate(local_docs, 1):
            # 读取文档内容
            with open(doc["abs_path"], "r", encoding="utf-8") as f:
                body = f.read()
            
            # 获取父分组 uuid
            parent_path = "/".join(doc["parent_dirs"]) if doc["parent_dirs"] else ""
            parent_uuid = dir_uuid_map.get(parent_path) if parent_path else None
            
            try:
                # 创建文档
                result = self.client.create_doc(
                    self.group_login,
                    self.book_slug,
                    doc["title"],
                    body
                )
                doc_id = result.get("id")
                
                if not doc_id:
                    print(f"  创建文档失败（无ID）: {doc['title']}")
                    continue
                
                # 立即添加到目录
                toc_data = {
                    "action": "appendNode",
                    "action_mode": "child",
                    "type": "DOC",
                    "doc_ids": [doc_id],
                }
                
                if parent_uuid:
                    toc_data["target_uuid"] = parent_uuid
                
                self.client.update_toc(self.group_login, self.book_slug, toc_data)
                
                created_count += 1
                parent_display = parent_path if parent_path else "根目录"
                print(f"  创建文档: {doc['title']} -> {parent_display}")
                
                if created_count % 10 == 0:
                    print(f"  已完成 {created_count}/{len(local_docs)} 个文档")
                
            except Exception as e:
                print(f"  创建文档失败: {doc['title']} - {e}")
        
        print(f"创建完成！共创建 {created_count} 个文档并添加到目录")


def main():
    parser = argparse.ArgumentParser(description="语雀批量同步工具")
    parser.add_argument("--token", required=True, help="语雀 API Token")
    parser.add_argument("--repo", required=True, help="目标知识库 (group_login/book_slug)")
    parser.add_argument("--local-dir", required=True, help="本地 Markdown 目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不实际执行")
    
    args = parser.parse_args()
    
    # 解析知识库路径
    repo_parts = args.repo.split("/")
    if len(repo_parts) != 2:
        print("错误: --repo 格式应为 group_login/book_slug")
        return 1
    
    group_login, book_slug = repo_parts
    
    # 验证本地目录
    if not os.path.isdir(args.local_dir):
        print(f"错误: 目录不存在: {args.local_dir}")
        return 1
    
    # 初始化客户端
    client = YuqueClient(args.token)
    
    # 验证 Token
    print("验证 Token...")
    if not client.verify_token():
        print("错误: Token 无效")
        return 1
    print("Token 验证成功")
    
    # 扫描本地文档
    print(f"扫描本地目录: {args.local_dir}")
    scanner = LocalDocScanner(args.local_dir)
    local_docs = scanner.scan()
    print(f"找到 {len(local_docs)} 个 Markdown 文件")
    
    # 执行同步
    syncer = YuqueSyncer(client, group_login, book_slug)
    syncer.sync(local_docs, dry_run=args.dry_run)
    
    return 0


if __name__ == "__main__":
    exit(main())
