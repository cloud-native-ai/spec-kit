#!/usr/bin/env python3
"""
语雀文档上传工具（upsert 版）

将文档内容上传到目标语雀知识库，支持 upsert：
- 若目标知识库已存在同 source_url 的文档（通过派生 slug 识别），则覆盖更新
- 否则新建文档并加入目录
- 无需本地状态，多端/多 AI 实例环境通用

使用方法：
    python3 yuque_upload.py \
        --token <TOKEN> \
        --target-repo <group_login/book_slug> \
        --title <文档标题> \
        --body-file <文档内容文件> \
        --format <markdown|lake> \
        --source-url <源文档URL>

slug 派生规则：
    source_url 末段路径去掉 query/fragment，加 "kb-" 前缀
    示例：yuque.com/g/b/yxl1tgidfqs00g73 → kb-yxl1tgidfqs00g73
"""

import argparse
import json
import re
import urllib.request
import urllib.error
import urllib.parse
import ssl
import sys
import time
import os


class YuqueClient:
    """语雀 API 客户端"""

    BASE_URL = "https://yuque-api.antfin-inc.com/api/v2"
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # 秒

    def __init__(self, token: str):
        self.token = token
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def _request(self, method: str, endpoint: str, data: dict = None, retries: int = MAX_RETRIES) -> dict:
        """带重试机制的请求方法"""
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "X-Auth-Token": self.token,
            "Content-Type": "application/json",
            "User-Agent": "YuqueKBCollector/2.1",
        }

        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        last_error = None
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=60, context=self.ssl_context) as response:
                    return json.loads(response.read().decode())
            except urllib.error.HTTPError as error:
                last_error = error
                error_body = error.read().decode() if error.fp else ""
                # 如果是4xx错误，不重试
                if 400 <= error.code < 500:
                    raise Exception(f"API Error {error.code}: {error_body}")
                # 5xx错误重试
                if attempt < retries - 1:
                    print(f"   ⚠️ 请求失败，{self.RETRY_DELAY}秒后重试 ({attempt + 1}/{retries})...")
                    time.sleep(self.RETRY_DELAY)
                    continue
                raise Exception(f"API Error {error.code}: {error_body}")
            except urllib.error.URLError as error:
                last_error = error
                # 网络错误重试
                if attempt < retries - 1:
                    print(f"   ⚠️ 网络错误，{self.RETRY_DELAY}秒后重试 ({attempt + 1}/{retries})...")
                    time.sleep(self.RETRY_DELAY)
                    continue
                raise Exception(f"Network Error: {error}")
        
        # 如果所有重试都失败
        raise Exception(f"Request failed after {retries} attempts: {last_error}")

    def post(self, endpoint: str, data: dict) -> dict:
        return self._request("POST", endpoint, data)

    def put(self, endpoint: str, data: dict) -> dict:
        return self._request("PUT", endpoint, data)

    def get_doc(self, group_login: str, book_slug: str, doc_slug: str):
        """按 slug 查询文档，存在返回 doc 对象，不存在返回 None（不抛异常）"""
        try:
            result = self._request("GET", f"/repos/{group_login}/{book_slug}/docs/{doc_slug}", retries=1)
            return result.get("data")
        except Exception as e:
            if "404" in str(e):
                return None
            raise

    def create_doc(self, group_login: str, book_slug: str, title: str, body: str,
                   doc_format: str = "markdown", slug: str = None) -> dict:
        """新建文档，可指定 slug"""
        data = {
            "title": title,
            "body": body,
            "format": doc_format,
            "public": 0,
        }
        if slug:
            data["slug"] = slug
        result = self.post(f"/repos/{group_login}/{book_slug}/docs", data)
        return result.get("data", {})

    def update_doc(self, group_login: str, book_slug: str, doc_slug: str,
                   title: str, body: str, doc_format: str = "markdown") -> dict:
        """覆盖更新已有文档内容"""
        data = {"title": title, "body": body, "format": doc_format}
        result = self.put(f"/repos/{group_login}/{book_slug}/docs/{doc_slug}", data)
        return result.get("data", {})

    def add_to_toc(self, group_login: str, book_slug: str, doc_id: int) -> dict:
        data = {
            "action": "appendNode",
            "action_mode": "child",
            "type": "DOC",
            "doc_ids": [doc_id],
        }
        result = self.put(f"/repos/{group_login}/{book_slug}/toc", data)
        return result.get("data", {})


def derive_slug(source_url: str):
    """
    从 source_url 派生确定性 slug，用于 upsert 唯一标识。
    规则：取 URL 路径最后一段（去掉 query/fragment），加 "kb-" 前缀。
    示例：https://yuque.com/g/b/yxl1tgidfqs00g73?view=doc → kb-yxl1tgidfqs00g73
    返回 None 表示无法派生（source_url 为空或格式异常）。
    """
    if not source_url:
        return None
    try:
        parsed = urllib.parse.urlparse(source_url)
        # 取路径最后一段，去除空段
        segments = [s for s in parsed.path.split("/") if s]
        if not segments:
            return None
        raw_slug = segments[-1]
        # 只保留字母、数字、连字符，避免非法字符
        clean_slug = re.sub(r"[^a-zA-Z0-9\-]", "", raw_slug)
        if not clean_slug:
            return None
        return f"kb-{clean_slug}"
    except Exception:
        return None


def upload_document(token: str, title: str, body: str, doc_format: str,
                    source_url: str, target_repo: str, index: int = 0, total: int = 1):
    """上传文档到目标知识库并加入目录"""
    client = YuqueClient(token)

    # 批量上传时显示进度
    if total > 1:
        print(f"\n{'=' * 60}")
        print(f"📄 批量上传进度: [{index}/{total}]")
        print(f"{'=' * 60}")
    else:
        print("=" * 60)
        print("📄 语雀知识库收集器")
        print("=" * 60)

    target_parts = target_repo.split("/")
    if len(target_parts) != 2:
        print("❌ 目标知识库格式错误，应为 group_login/book_slug")
        return None
    target_group, target_book = target_parts

    print(f"\n📖 源文档: {source_url}")
    print(f"📚 目标知识库: {target_group}/{target_book}")
    print(f"   标题: {title}")
    print(f"   格式: {doc_format}")

    # 1. 派生 slug，决定 upsert 行为
    target_slug = derive_slug(source_url)

    if target_slug:
        # 有可派生的 slug → 先查询是否已存在
        print(f"\n🔍 检查文档是否已存在（slug: {target_slug}）...")
        existing_doc = client.get_doc(target_group, target_book, target_slug)

        if existing_doc:
            # 已存在 → 覆盖更新
            doc_id = existing_doc.get("id")
            print(f"   ♻️  发现已有文档（ID: {doc_id}），执行覆盖更新...")
            client.update_doc(target_group, target_book, target_slug, title, body, doc_format)
            doc_slug = target_slug
            action = "更新"
        else:
            # 不存在 → 新建（携带固定 slug）
            print(f"   ➕ 未找到同源文档，执行新建...")
            new_doc = client.create_doc(target_group, target_book, title, body, doc_format, slug=target_slug)
            doc_id = new_doc.get("id")
            doc_slug = new_doc.get("slug")
            print(f"   ✅ 文档创建成功 (ID: {doc_id})")
            print(f"   📂 正在加入目录...")
            client.add_to_toc(target_group, target_book, doc_id)
            print(f"   ✅ 已加入目录")
            action = "新建"
    else:
        # source_url 为空或无法派生 → 直接新建（兜底，行为与旧版一致）
        print(f"\n🚀 正在上传到目标知识库（无 source_url，直接新建）...")
        new_doc = client.create_doc(target_group, target_book, title, body, doc_format)
        doc_id = new_doc.get("id")
        doc_slug = new_doc.get("slug")
        print(f"   ✅ 文档创建成功 (ID: {doc_id})")
        print(f"   📂 正在加入目录...")
        client.add_to_toc(target_group, target_book, doc_id)
        print(f"   ✅ 已加入目录")
        action = "新建"

    # 2. 输出结果
    target_url = f"https://yuque.antfin.com/{target_group}/{target_book}/{doc_slug}"

    if total > 1:
        print(f"\n✅ [{index}/{total}] {action}完成")
    else:
        print(f"\n{'=' * 60}")
        print(f"✅ 文档{action}完成！")
        print(f"{'=' * 60}")
        print(f"   📖 源文档: {source_url}")
        print(f"   📚 目标文档: {target_url}")
        print(f"   操作类型: {action}")
        print(f"{'=' * 60}")

    return {
        "source_url": source_url,
        "target_url": target_url,
        "doc_id": doc_id,
        "doc_slug": doc_slug,
        "action": action,
    }


def main():
    parser = argparse.ArgumentParser(description="语雀文档上传工具（优化版）")
    parser.add_argument("--token", required=True, help="语雀 API Token")
    parser.add_argument("--target-repo", required=True, help="目标知识库 (group_login/book_slug)")
    parser.add_argument("--title", help="文档标题")
    parser.add_argument("--body-file", help="文档内容文件路径")
    parser.add_argument("--body-content", help="文档内容（直接传入，避免临时文件）")
    parser.add_argument("--format", default="markdown", help="文档格式 (markdown/lake/html)")
    parser.add_argument("--source-url", default="", help="源文档 URL（仅用于记录）")
    parser.add_argument("--batch-file", help="批量上传文件（JSON格式，包含多个文档信息）")

    args = parser.parse_args()

    # 批量上传模式
    if args.batch_file:
        return batch_upload(args)
    
    # 单个文档上传模式
    if not args.title:
        print("❌ 单个文档上传必须指定 --title")
        return 1

    # 检查内容来源
    if args.body_content:
        # 直接使用传入的内容
        body = args.body_content
        temp_file = None
    elif args.body_file:
        # 从文件读取内容
        with open(args.body_file, "r", encoding="utf-8") as file:
            body = file.read()
        temp_file = args.body_file
    else:
        print("❌ 必须指定 --body-file 或 --body-content")
        return 1

    try:
        result = upload_document(
            token=args.token,
            title=args.title,
            body=body,
            doc_format=args.format,
            source_url=args.source_url,
            target_repo=args.target_repo,
        )
        
        # 清理临时文件
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"   🧹 已清理临时文件: {temp_file}")
            except Exception as cleanup_error:
                print(f"   ⚠️ 清理临时文件失败: {cleanup_error}")
        
        return 0
        
    except Exception as error:
        print(f"\n❌ 上传失败: {error}")
        import traceback
        traceback.print_exc()
        
        # 即使失败也尝试清理临时文件
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"   🧹 已清理临时文件: {temp_file}")
            except Exception as cleanup_error:
                print(f"   ⚠️ 清理临时文件失败: {cleanup_error}")
        
        return 1


def batch_upload(args):
    """批量上传文档"""
    print("=" * 60)
    print("📄 语雀知识库收集器 - 批量上传模式")
    print("=" * 60)
    
    # 读取批量上传文件
    try:
        with open(args.batch_file, "r", encoding="utf-8") as file:
            batch_data = json.load(file)
    except Exception as error:
        print(f"❌ 读取批量上传文件失败: {error}")
        return 1
    
    if not isinstance(batch_data, list):
        print("❌ 批量上传文件格式错误，应为JSON数组")
        return 1
    
    total_docs = len(batch_data)
    if total_docs == 0:
        print("❌ 批量上传文件中没有文档")
        return 1
    
    print(f"\n📚 准备批量上传 {total_docs} 个文档到 {args.target_repo}")
    print(f"{'=' * 60}")
    
    success_count = 0
    failed_count = 0
    failed_docs = []
    
    for index, doc_info in enumerate(batch_data, 1):
        print(f"\n📄 处理文档 [{index}/{total_docs}]")
        
        # 验证文档信息
        if not all(key in doc_info for key in ["title", "content"]):
            print(f"   ❌ 文档信息不完整，跳过")
            failed_count += 1
            failed_docs.append({
                "index": index,
                "title": doc_info.get("title", "unknown"),
                "error": "文档信息不完整"
            })
            continue
        
        try:
            result = upload_document(
                token=args.token,
                title=doc_info["title"],
                body=doc_info["content"],
                doc_format=doc_info.get("format", args.format),
                source_url=doc_info.get("source_url", ""),
                target_repo=args.target_repo,
                index=index,
                total=total_docs
            )
            success_count += 1
            
        except Exception as error:
            print(f"   ❌ 上传失败: {error}")
            failed_count += 1
            failed_docs.append({
                "index": index,
                "title": doc_info["title"],
                "error": str(error)
            })
    
    # 输出批量上传结果
    print(f"\n{'=' * 60}")
    print(f"📊 批量上传完成")
    print(f"{'=' * 60}")
    print(f"   总计: {total_docs} 个文档")
    print(f"   ✅ 成功: {success_count} 个")
    print(f"   ❌ 失败: {failed_count} 个")
    
    if failed_docs:
        print(f"\n❌ 失败文档列表:")
        for failed_doc in failed_docs:
            print(f"   [{failed_doc['index']}] {failed_doc['title']}: {failed_doc['error']}")
    
    print(f"{'=' * 60}")
    
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    exit(main())
