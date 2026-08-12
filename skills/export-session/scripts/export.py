#!/usr/bin/env python3
"""
export-session: 把当前 AI Agent 会话相关的全部原始文件打包成 zip 到项目根目录 .session-export/

支持的工具与内容(含子 agent / 派生会话补全):
  - Claude Code: 主 {sid}.jsonl + {sid}/subagents/* + {sid}/tool-results/*
  - Qwen Code:   主 chats/{sid}.jsonl + {sid}.runtime.json + subagents + fork 派生 + tmp 工具结果
  - Codex CLI:   state_5.sqlite(source∈cli/exec)→ rollout {sid}.jsonl + 递归 spawn 子 agent
  - Codex App:   state_5.sqlite(source=vscode)→ 同结构,与 Codex CLI 分开导出
  - Qoder:       ~/.qoder/projects/<enc>/transcript/{sid}.jsonl
  - Qoder CLI:   ~/.qoder/projects/<enc>/{sid}.jsonl + {sid}/ 状态目录 + logs/sessions 段日志
  - qoderwork:   ~/.qoderwork/projects/<enc>/{sid}.jsonl + {sid}/ 状态目录 + logs/sessions 段日志
  - OpenCode:    从 SQLite 还原(session+message+part,按 parent_id 递归含子会话)
  - oh-my-pi:    ~/.omp/agent/sessions/<enc>/<ts>_{sid}.jsonl
  - Kimi Code:   ~/.kimi-code/sessions/<ws>/session_<uuid>/ 整目录(state.json、
                 agents/*/wire.jsonl、logs/);user-history/ 为项目级跨会话聚合,不收

会话定位一律以文件内真实 cwd 字段 / SQLite 的 cwd|directory 列精确匹配,
不依赖各工具有损且互不一致的目录名编码。当前客户端优先按安装位置/进程链识别
(见 _client_bias);同 cwd 出现多个候选会话/工具时,多因子锁定当前会话:
显式会话 id 环境变量(Claude CLAUDE_(CODE_)SESSION_ID / Codex CODEX_THREAD_ID) >
运行时属主 pid 命中本进程祖先链(Qwen runtime.json) > 会话内容末条时间戳最新。

平台支持 macOS / Linux / Windows,平台差异全部收敛在少数几处(其余逻辑共用):
  - 路径比较: Windows 大小写不敏感且 '/' 与 '\\' 混用,一律走 _same_path 规范化后比较,
    不做裸字符串相等(SQLite 的 cwd 列同理: 精确查询未命中时回扫全表按 _same_path 比对);
  - 进程祖先链: Windows 无 ps,改用 CreateToolhelp32Snapshot(纯 ctypes)取 pid/ppid/exe 名;
    node/npm 安装的 CLI 进程名一律 node.exe,exe 名识别不出客户端时再查一次命令行;
  - 控制终端(tty): Windows 无此概念,oh-my-pi 的 per-tty 会话记录信号在 Windows 上不可用,
    自动降级到其余因子(内容时间戳等);
  - 存储根: OpenCode 数据目录跨平台候选探测(_resolve_opencode_db),Codex 支持 CODEX_HOME;
  - 超长路径: Windows MAX_PATH 限制下给 >255 的路径加 \\\\?\\ 前缀,避免深层会话目录打包失败。

退出码: 0 成功 / 2 参数无效 / 3 无会话 / 4 工具未安装 / 5 IO/SQLite 错误
"""
import argparse
import hashlib
import io
import json
import os
import re
import sqlite3
import sys
import zipfile
from pathlib import Path

HOME = Path.home()
IS_WINDOWS = os.name == "nt"


# ---------------- 跨平台路径 ----------------

def _norm_path(p):
    """路径规范化为可比较形式:转绝对路径,消除 '.'/'..'/重复分隔符/尾部分隔符,
    再经 os.path.normcase 统一形态(Windows 折大小写与 '/'→'\\',POSIX 为恒等)。
    Windows 文件系统大小写不敏感,各工具写进 jsonl/SQLite 的 cwd 可能是 'C:/x'、
    'C:\\x'、'c:\\x' 任一形态,裸字符串相等会漏匹配。空/非字符串/异常返 None。"""
    if not isinstance(p, str) or not p:
        return None
    try:
        return os.path.normcase(os.path.abspath(os.path.normpath(p)))
    except (OSError, ValueError):
        return None


def _same_path(a, b):
    """两路径是否指向同一位置(规范化后比较);任一不可规范化即 False。"""
    na, nb = _norm_path(a), _norm_path(b)
    return na is not None and na == nb


def _os_path(p):
    """交给文件系统调用的实际路径:Windows 上给超 MAX_PATH(260)的路径加 '\\\\?\\' 前缀,
    否则未开启长路径支持的系统会 OSError。前缀要求完全限定且无 '.'/'..',故先 abspath;
    UNC 走 '\\\\?\\UNC\\'。非 Windows / 短路径 / 已带前缀原样返回。

    适用范围是**读取侧**(各 agent 的存储目录):其路径由工具生成、嵌套深且不可控
    (projects/<长编码目录名>/<uuid>/subagents/agent-<uuid>.jsonl),遍历根、stat、open、
    zip 写入必须全程带前缀,只包其中一环无效(前面的 rglob/stat 会先失败)。
    写出侧(<项目根>/.session-export/)由用户自己控制且层级浅,不做包装;
    SQLite 库路径也不包装,它经 _sqlite_ro_uri 进 URI,前缀会被当成路径内容。"""
    if not IS_WINDOWS:
        return str(p)
    s = os.path.abspath(str(p))
    if len(s) < 256 or s.startswith("\\\\?\\"):
        return s
    return ("\\\\?\\UNC\\" + s[2:]) if s.startswith("\\\\") else ("\\\\?\\" + s)


def _file_uri_to_path(uri):
    """file:// URI → 本地路径。Windows 上 urlparse('file:///C:/x').path 为 '/C:/x',
    须去掉前导 '/'(POSIX 的 '/Users/x' 不能去,故按盘符形态判断);
    UNC(file://server/share)还原为 '\\\\server\\share'。非 file/空返 None。"""
    from urllib.parse import urlparse, unquote
    if not isinstance(uri, str) or not uri:
        return None
    pr = urlparse(uri)
    if pr.scheme and pr.scheme != "file":
        return None
    path = unquote(pr.path or "")
    if not path:
        return None
    if pr.netloc:
        if IS_WINDOWS:
            return "\\\\" + pr.netloc + path.replace("/", "\\")
        return "//" + pr.netloc + path
    if IS_WINDOWS and re.match(r"^/[A-Za-z]:", path):
        path = path[1:]
    return path


def _sqlite_ro_uri(path):
    """本地路径 → SQLite 只读 URI(file:...?mode=ro),_file_uri_to_path 的反向。
    路径须先百分号转义再进 URI:'%XX' 会被 SQLite 解码、'?' 起查询串、'#' 起片段,
    直接拼接会把 'C:\\bob#work\\a.db' 截断成 'C:\\bob'、'v1%2Ffinal' 解成 'v1/final'。
    分隔符与盘符冒号保持原样,'/a/b'、'C:\\a\\b'、UNC '\\\\srv\\share\\b' 逐字符不变
    (故不能用 Path.as_uri():它把 UNC 转成 'file://srv/...',authority 非空会被 SQLite 拒绝)。"""
    from urllib.parse import quote
    return "file:" + quote(str(path), safe="/\\:") + "?mode=ro"


# ---------------- 通用辅助 ----------------

def _safe_float(v):
    """SQLite 时间字段可能是 int/float/str(ISO)/None，统一转 float，失败返 0.0"""
    if v is None or v == "":
        return 0.0
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _read_cwd_from_jsonl(path, max_lines=200):
    """读 jsonl 前若干行，返回第一个出现的顶层 cwd 字段；找不到返 None。
    大会话开头可能有大量无 cwd 的 summary / queue-operation / runtime-config 行，故窗口放宽。
    只认非空字符串:调用方要拿它去 sha256 求 Qwen tmp 目录名,畸形 jsonl 里的数字 cwd
    会在 encode 时抛错、把整次导出带崩,而它本该只是跳过一个可选目录。"""
    try:
        with open(_os_path(path), encoding="utf-8", errors="ignore") as f:
            for _ in range(max_lines):
                line = f.readline()
                if not line:
                    break
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict) and isinstance(obj.get("cwd"), str) and obj["cwd"]:
                    return obj["cwd"]
    except OSError:
        return None
    return None


def _list_jsonl_projects(root, cwd, rel_glob):
    """遍历 root 下每个项目子目录，用文件内真实 cwd 字段精确匹配当前 cwd。

    rel_glob 是子目录内会话文件的相对 glob：
      Claude '*.jsonl' / Qoder 'transcript/*.jsonl' / Qwen 'chats/*.jsonl' / QoderCLI '*.jsonl'。
    一个项目目录对应一个 cwd，找该目录第一个能读出 cwd 的文件作为归属判据，
    从而彻底规避各工具目录名编码规则的差异与有损问题。
    返回 [(sessionId, path, mtime)] 按 mtime 降序。"""
    root = Path(_os_path(root))
    if not root.exists():
        return []
    out = []
    for proj in root.iterdir():
        if not proj.is_dir():
            continue
        files = sorted(proj.glob(rel_glob),
                       key=lambda p: p.stat().st_mtime, reverse=True)
        if not files:
            continue
        probe_cwd = None
        for probe in files:
            probe_cwd = _read_cwd_from_jsonl(probe)
            if probe_cwd is not None:
                break
        if not _same_path(probe_cwd, cwd):
            continue
        for f in files:
            out.append((f.stem, f, f.stat().st_mtime))
    out.sort(key=lambda t: t[2], reverse=True)
    return out


def _open_zip_atomic(dst):
    """打开一个临时 .part 文件用于写 zip；调用者拿到 (zf, tmp_path)，写完后调 _commit_zip"""
    tmp = dst.with_name(dst.name + ".part")
    if tmp.exists():
        try:
            tmp.unlink()
        except OSError:
            pass
    zf = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    return zf, tmp


def _commit_zip(zf, tmp, dst):
    """关闭 zip 并原子 rename 到 dst；失败时清理 .part"""
    try:
        zf.close()
        os.replace(tmp, dst)
    except Exception:
        try:
            zf.close()
        except Exception:
            pass
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
        raise


def _abort_zip(zf, tmp):
    """异常路径清理未提交的 zip"""
    try:
        zf.close()
    except Exception:
        pass
    if tmp.exists():
        try:
            tmp.unlink()
        except OSError:
            pass


def _strip_chatcmpl(v):
    """chatcmpl-<uuid> 里 <uuid> 即百炼 request-id;非该形态返 None"""
    if isinstance(v, str) and v.startswith("chatcmpl-"):
        return v[len("chatcmpl-"):]
    return None


def _assistant_request_ids(src_path, id_key):
    """通用:从 claude 风格 jsonl 的 assistant 行按 id_key 取 chatcmpl-<uuid>,
    剥前缀为 request_id;按 request_id 去重、时间升序。id_key 为 message 内字段名。"""
    out, seen = [], set()
    try:
        with open(_os_path(src_path), encoding="utf-8", errors="ignore") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not (isinstance(d, dict) and d.get("type") in ("assistant", "message")):
                    continue
                m = d.get("message") if isinstance(d.get("message"), dict) else {}
                if d.get("type") == "message" and m.get("role") != "assistant":
                    continue
                rid = _strip_chatcmpl(m.get(id_key))
                if not rid or rid in seen:
                    continue
                seen.add(rid)
                out.append({"timestamp": d.get("timestamp"),
                            "request_id": rid, "model": m.get("model")})
    except OSError:
        return out
    return sorted(out, key=lambda r: r.get("timestamp") or "")


def _zip_write_jsonl(zf, arcname, records):
    """把 records(dict 列表)按 JSONL 写入 zip;空则不写。返回写入文件数(0/1)。"""
    if not records:
        return 0
    buf = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records)
    zf.writestr(arcname, buf)
    return 1


def _add_dir_to_zip(zf, directory, arc_prefix):
    """把 directory 下所有文件加入 zip，arcname = arc_prefix/<相对路径>；跳过符号链接。返回文件数。"""
    directory = Path(directory)
    if not directory.is_dir() or directory.is_symlink():
        return 0
    # 从带前缀的根开始遍历,子路径自动继承前缀,rglob/stat/open/write 全程一致
    root = Path(_os_path(directory))
    n = 0
    for f in sorted(root.rglob("*")):
        if f.is_symlink() or not f.is_file():
            continue
        rel = f.relative_to(root).as_posix()
        zf.write(f, arcname=f"{arc_prefix}/{rel}")
        n += 1
    return n


def _maybe_parse_json_field(d, key):
    """SQLite 里存成字符串的 JSON 字段，尽量解析成对象，失败保持原样"""
    if isinstance(d.get(key), str):
        try:
            d[key] = json.loads(d[key])
        except (json.JSONDecodeError, TypeError):
            pass


def _ts_to_epoch(v):
    """把一条 timestamp 值转 epoch 秒:数字(秒/毫秒/微秒/纳秒)或 ISO8601 字符串;失败返 None。
    数字按量级归一:逐级 /1000 直到落入合理 epoch 秒区间(< 1e11 ≈ 公元 5138 年),
    从而兼容 s(~1.7e9)/ms(~1.7e12)/us(~1.7e15)/ns(~1.7e18) 混用;单档阈值(如只按 1e12
    判毫秒)会把 us/ns 判成远未来,让该会话冒充最新。bool 是 int 子类须先排除,非正数视为无效。"""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        f = float(v)
        if f <= 0:
            return None
        while f >= 1e11:
            f /= 1000.0
        return f
    if isinstance(v, str) and v:
        try:
            from datetime import datetime
            return datetime.fromisoformat(v.replace("Z", "+00:00")).timestamp()
        except ValueError:
            return None
    return None


def _content_last_activity(path, max_bytes=64 * 1024, max_scan=32 * 1024 * 1024):
    """读 jsonl 尾部，返回内容里最后(最大)的 timestamp(epoch 秒);找不到返 None。
    比文件 mtime 更能反映真实对话活动(mtime 会被备份/同步/改名等非内容操作扰动)。
    尾部窗口可能整块落在一条超大行(如超大工具结果)内、扫不到任何顶层 timestamp,
    此时逐步放大窗口(×8)直至覆盖全文,避免误返 None 后退化到不可信的 mtime。
    放大设 max_scan 上限(默认 32MB):防止病态'全文无顶层 timestamp'的超大文件被整体读入内存。"""
    try:
        size = Path(_os_path(path)).stat().st_size
    except OSError:
        return None
    window = max_bytes
    while True:
        try:
            with open(_os_path(path), "rb") as f:
                if size > window:
                    f.seek(size - window)
                data = f.read()
        except OSError:
            return None
        best = None
        for line in data.decode("utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line[0] != "{":
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                ep = _ts_to_epoch(obj.get("timestamp"))
                if ep is not None and (best is None or ep > best):
                    best = ep
        # 本窗口找到,或已读完全文,或达扫描上限→返回;否则放大窗口重试
        if best is not None or window >= size or window >= max_scan:
            return best
        window *= 8


def _state_json_updated(src_path):
    """qoder-cli / qoderwork 在同名 {sid}/state.json 里维护可靠的 updatedAt(ISO8601)。
    该文件小、不含超大行,不受 _content_last_activity 尾部窗口局限,也免疫 mtime 扰动,
    是这两个产品(无会话 id 环境变量/无属主 pid)最稳的'最近活跃'来源。
    返 epoch 秒;非 jsonl / 无该文件 / 无字段 → None。Qoder IDE(transcript/ 布局)无此同名目录,不受影响。"""
    if not (isinstance(src_path, Path) and src_path.suffix == ".jsonl"):
        return None
    sj = Path(_os_path(src_path.parent / src_path.stem / "state.json"))
    if not sj.is_file():
        return None
    try:
        d = json.loads(sj.read_text(encoding="utf-8", errors="ignore"))
    except (OSError, json.JSONDecodeError):
        return None
    return _ts_to_epoch(d.get("updatedAt")) if isinstance(d, dict) else None


def _session_recency(src, fallback_ts):
    """会话'最近活跃'时间(epoch 秒):综合两路更可靠信号取最大——
      1) 同名 {sid}/state.json 的 updatedAt(qoder-cli/qoderwork,小文件、稳、免疫尾部超大行);
      2) 会话内容末条 timestamp(_content_last_activity,通用)。
    二者皆取不到(src 非 jsonl 如 OpenCode 的 DB / 解析失败)时退回 fallback_ts(通常为 mtime)。"""
    if isinstance(src, Path) and src.suffix == ".jsonl" and Path(_os_path(src)).is_file():
        cands = [t for t in (_state_json_updated(src), _content_last_activity(src))
                 if t is not None]
        if cands:
            return max(cands)
    return fallback_ts


def _find_model_value(obj):
    """从一条 jsonl 记录取模型名:top-level model(runtime-config)、message.model(assistant)
    或 payload.model(Codex 的 turn_context)。"""
    if isinstance(obj, dict):
        v = obj.get("model")
        if isinstance(v, str) and v:
            return v
        msg = obj.get("message")
        if isinstance(msg, dict) and isinstance(msg.get("model"), str) and msg["model"]:
            return msg["model"]
        payload = obj.get("payload")
        if isinstance(payload, dict) and isinstance(payload.get("model"), str) and payload["model"]:
            return payload["model"]
    return None


def _last_model(src_path):
    """会话最后声明的模型:扫描整个 jsonl,返回最后一个 model 值(top-level model 或 message.model);
    无则 None。会话中途切换模型时以最终使用的模型为准。"""
    last = None
    try:
        with open(_os_path(src_path), encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line[0] != "{":
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                m = _find_model_value(d)
                if m:
                    last = m
    except OSError:
        return None
    return last


def _sanitize_model(model):
    """模型名净化为文件名安全片段:非 [A-Za-z0-9._-] → '-',压缩连续 '-',截断 40;空返 'unknown-model'。"""
    if not model:
        return "unknown-model"
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", model)
    s = re.sub(r"-{2,}", "-", s).strip("-.")[:40].strip("-.")
    return s or "unknown-model"


def _zip_name(prefix, model, session_id):
    """统一 zip 命名:{tool}+{model}+{sessionId}.zip(以 '+' 分隔三字段)。
    三字段自身都可能含 '-'(如 qoder-cli / claude-sonnet-4 / uuid),用 '-' 做分隔无法回解;
    改用不在净化集 [A-Za-z0-9._-] 内、且 macOS/Windows 文件系统与 shell 均安全的 '+',
    回解 split('+') 恰得 3 段。model 已净化不含 '+';prefix/session_id 理论不含 '+',仍顺手去掉作保险。"""
    prefix = prefix.replace("+", "-")
    session_id = str(session_id).replace("+", "-")
    return f"{prefix}+{_sanitize_model(model)}+{session_id}.zip"


# ---------------- Claude Code ----------------

def claudecode_available():
    return (HOME / ".claude" / "projects").exists()


def claudecode_list(cwd):
    root = HOME / ".claude" / "projects"
    items = _list_jsonl_projects(root, cwd, "*.jsonl")

    # 在 Claude Code 子进程里跑时，CLAUDE_(CODE_)SESSION_ID 精确指向当前会话。
    current_sid = _env_session_id("claude-code")
    if current_sid:
        # a) 当前会话就在本 cwd 列表里 → 置顶(确保导出当前会话而非同项目其它会话)
        for i, (sid, _, _) in enumerate(items):
            if sid == current_sid:
                items.insert(0, items.pop(i))
                return items
        # b) 本 cwd 完全无会话(如 skill 从子目录被调用)才全局按 sid 兜底;
        #    若本 cwd 已有其它会话(说明在导另一个项目)则不覆盖,保持 --project 语义。
        if not items:
            hits = sorted(Path(_os_path(root)).glob(f"*/{current_sid}.jsonl"))
            if hits:
                p = hits[0]
                items.insert(0, (p.stem, p, p.stat().st_mtime))
    return items


def _claude_request_ids(src_path, session_id):
    """从 Claude Code 会话(含 subagents)提取请求标识:request_id 取 assistant 消息体的
    message.id(msg_*)。流式下同一次调用多行重复同一 message.id,按 message.id 去重、时间升序。"""
    files = [src_path]
    subdir = src_path.parent / session_id / "subagents"
    if subdir.is_dir():
        files += sorted(Path(_os_path(subdir)).glob("*.jsonl"))
    seen = {}
    for fp in files:
        try:
            with open(_os_path(fp), encoding="utf-8", errors="ignore") as f:
                for line in f:
                    try:
                        d = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if not isinstance(d, dict):
                        continue
                    m = d.get("message") if isinstance(d.get("message"), dict) else {}
                    mid = m.get("id")
                    if not mid or mid in seen:
                        continue
                    seen[mid] = {
                        "timestamp": d.get("timestamp"),
                        "request_id": mid,
                        "model": m.get("model"),
                    }
        except OSError:
            continue
    return sorted(seen.values(), key=lambda r: r.get("timestamp") or "")


def claudecode_pack(src_path, session_id, out_dir):
    """主 jsonl + 同名子目录(subagents/、tool-results/) 打包成 zip"""
    dst = Path(out_dir) / _zip_name("claude-code", _last_model(src_path), session_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    sibling_dir = src_path.parent / session_id

    n = 0
    zf, tmp = _open_zip_atomic(dst)
    try:
        zf.write(_os_path(src_path), arcname=src_path.name)
        n += 1
        n += _add_dir_to_zip(zf, sibling_dir, session_id)
        # 排查用:提取 API requestId(req_*),放 zip 最外层
        n += _zip_write_jsonl(zf, "request-ids.jsonl",
                              _claude_request_ids(src_path, session_id))
        _commit_zip(zf, tmp, dst)
    except Exception:
        _abort_zip(zf, tmp)
        raise
    return dst.resolve(), n


# ---------------- Qwen Code ----------------

def _qwen_root():
    # Qwen 支持 QWEN_HOME 覆盖全局目录；默认 ~/.qwen
    env = os.environ.get("QWEN_HOME")
    return Path(env) if env else HOME / ".qwen"


def _qwen_project_hash(cwd):
    """Qwen 以 sha256(cwd) 十六进制作为 ~/.qwen/tmp 下的项目目录名(已比对实际目录确认)"""
    return hashlib.sha256(cwd.encode("utf-8")).hexdigest()


def qwen_available():
    return (_qwen_root() / "projects").exists()


def qwen_list(cwd):
    return _list_jsonl_projects(_qwen_root() / "projects", cwd, "chats/*.jsonl")


def _jsonl_forked_from(path):
    """返回该 jsonl 中记录的 forkedFrom.sessionId(取首个出现)，无则 None"""
    try:
        with open(_os_path(path), encoding="utf-8", errors="ignore") as f:
            for _ in range(50):
                line = f.readline()
                if not line:
                    break
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ff = o.get("forkedFrom") if isinstance(o, dict) else None
                if isinstance(ff, dict) and ff.get("sessionId"):
                    return ff["sessionId"]
    except OSError:
        return None
    return None


def _qwen_request_ids(src_path):
    """从 Qwen 会话 jsonl 的 ui_telemetry/api_response 事件提取 response_id(排查用)。
    返回 [{timestamp, response_id, model, status_code, duration_ms}];无则 []。"""
    out = []
    try:
        with open(_os_path(src_path), encoding="utf-8", errors="ignore") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not (isinstance(d, dict) and d.get("type") == "system"
                        and d.get("subtype") == "ui_telemetry"):
                    continue
                ev = d.get("systemPayload", {}).get("uiEvent", {})
                if ev.get("event.name") == "qwen-code.api_response" and ev.get("response_id"):
                    resp = ev.get("response_id")
                    # chatcmpl-<uuid> 里 <uuid> 即百炼返回的 request-id;剥掉前缀
                    rid = resp[len("chatcmpl-"):] if resp.startswith("chatcmpl-") else resp
                    out.append({
                        "timestamp": ev.get("event.timestamp"),
                        "request_id": rid,
                        "model": ev.get("model"),
                        "status_code": ev.get("status_code"),
                        "duration_ms": ev.get("duration_ms"),
                    })
    except OSError:
        return out
    return out


def qwen_pack(src_path, session_id, out_dir):
    """主 chats/{sid}.jsonl + 子 agent transcript + fork 派生会话 + tmp 外置工具结果。

    子 agent:  <projectDir>/subagents/<sid>/agent-*.jsonl(+.meta.json)
    fork/branch: 同 chats/ 下 forkedFrom.sessionId==sid 的其它 jsonl
    工具结果:  ~/.qwen/tmp/<sha256(cwd)>/tool-results/* 与 <tmp>/*.output(有 24h 时效)
    运行时元数据: 同目录 <sid>.runtime.json(pid/work_dir/qwen_version 等)
    """
    dst = Path(out_dir) / _zip_name("qwen-code", _last_model(src_path), session_id)
    dst.parent.mkdir(parents=True, exist_ok=True)

    n = 0
    zf, tmp = _open_zip_atomic(dst)
    try:
        zf.write(_os_path(src_path), arcname=src_path.name)
        n += 1
        # 同名运行时元数据 <sid>.runtime.json(与主 jsonl 同目录)
        runtime = src_path.parent / (src_path.stem + ".runtime.json")
        if Path(_os_path(runtime)).is_file():
            zf.write(_os_path(runtime), arcname=runtime.name)
            n += 1
        # 排查用:提取大模型接口返回的 response_id,放 zip 最外层
        n += _zip_write_jsonl(zf, "request-ids.jsonl",
                              _qwen_request_ids(src_path))
        # 布局A(projects/<id>/chats/<sid>.jsonl):补子 agent / fork 派生 / tmp 工具结果。
        # 布局B/C(chats|tmp/<hash>/ 下的 checkpoint/json):文件自包含,只打其本身即可。
        if "projects" in src_path.parts and src_path.parent.name == "chats":
            project_dir = src_path.parent.parent
            chats_dir = src_path.parent
            n += _add_dir_to_zip(zf, project_dir / "subagents" / session_id,
                                 f"{session_id}/subagents")
            for jf in sorted(Path(_os_path(chats_dir)).glob("*.jsonl")):
                if jf != src_path and _jsonl_forked_from(jf) == session_id:
                    zf.write(_os_path(jf), arcname=f"{session_id}/forks/{jf.name}")
                    n += 1
            cwd = _read_cwd_from_jsonl(src_path)
            if cwd:
                tmpdir = _qwen_root() / "tmp" / _qwen_project_hash(cwd)
                n += _add_dir_to_zip(zf, tmpdir / "tool-results",
                                     f"{session_id}/tool-results")
                if tmpdir.is_dir():
                    for f in sorted(Path(_os_path(tmpdir)).glob("*.output")):
                        if f.is_file():
                            zf.write(_os_path(f), arcname=f"{session_id}/tool-results/{f.name}")
                            n += 1
        _commit_zip(zf, tmp, dst)
    except Exception:
        _abort_zip(zf, tmp)
        raise
    return dst.resolve(), n


# ---------------- Qoder ----------------

# Qoder IDE 的 transcript 不记模型;模型在审计日志的 startup 事件里按 session_id 记录。
QODER_AUDIT_LOG = HOME / ".qoder" / "audit" / "audit.jsonl"


def qoder_available():
    return (HOME / ".qoder" / "projects").exists()


def _qoder_audit_model(session_id):
    """Qoder IDE 回退:从 ~/.qoder/audit/audit.jsonl 按 session_id 回查模型,
    取最后一条带 model 的记录(值为 Qoder 档位别名,如 ultimate)。无则 None。"""
    if not QODER_AUDIT_LOG.exists():
        return None
    last = None
    try:
        with open(_os_path(QODER_AUDIT_LOG), encoding="utf-8", errors="ignore") as f:
            for line in f:
                if session_id not in line or '"model"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(d, dict) or d.get("session_id") != session_id:
                    continue
                m = d.get("model")
                if isinstance(m, str) and m:
                    last = m
    except OSError:
        return None
    return last


def qoder_list(cwd):
    return _list_jsonl_projects(HOME / ".qoder" / "projects", cwd,
                                "transcript/*.jsonl")


# ---- Qoder IDE 精确信号: workspaceStorage/<hash>/state.vscdb ----
# Qoder IDE 的 transcript 既不记模型、也无会话 id 环境变量/属主 pid;但 IDE 在 VS Code 风格的
# workspaceStorage 里维护了两类精确状态: (a) 当前活动会话(aicoding.chat.tabs/views),
# (b) 每会话模型(chat.modelConfig.session.<sid>)。据 cwd 反查该工作区库即可精确锁定并取真实模型。

def _qoder_user_dir():
    """Qoder IDE 的 User 配置目录(含 workspaceStorage),按平台定位;不存在返 None。
    Qoder 基于 VS Code,沿用其各平台约定:macOS Library/Application Support、
    Windows %APPDATA%(缺失时退回 ~/AppData/Roaming)、Linux ~/.config。"""
    if sys.platform == "darwin":
        p = HOME / "Library" / "Application Support" / "Qoder" / "User"
    elif IS_WINDOWS:
        appdata = os.environ.get("APPDATA")
        base = Path(appdata) if appdata else HOME / "AppData" / "Roaming"
        p = base / "Qoder" / "User"
    else:
        p = HOME / ".config" / "Qoder" / "User"
    return p if p and p.is_dir() else None


def _qoder_workspace_db(cwd):
    """据 cwd 反查 Qoder IDE 该工作区的 state.vscdb:遍历 workspaceStorage/*/workspace.json,
    其 folder(file:// URI)解码后等于 cwd 者即是。返库路径;无匹配/无库返 None。"""
    user = _qoder_user_dir()
    if not user:
        return None
    ws_root = user / "workspaceStorage"
    if not ws_root.is_dir():
        return None
    for wj in Path(_os_path(ws_root)).glob("*/workspace.json"):
        try:
            folder = json.loads(wj.read_text(encoding="utf-8", errors="ignore")).get("folder")
        except (OSError, json.JSONDecodeError, AttributeError):
            continue
        if not isinstance(folder, str) or not folder:
            continue
        # file:// URI → 本地路径需按平台还原(Windows 上 .path 会多一个前导 '/'),
        # 再用 _same_path 比较(Windows 盘符大小写/分隔符形态不定)
        if _same_path(_file_uri_to_path(folder), cwd):
            # 库路径只经 _sqlite_ro_uri 打开,故按 ws_root 重建为不带 '\\?\' 前缀的形态
            db = ws_root / wj.parent.name / "state.vscdb"
            return db if db.is_file() else None
    return None


def _vscdb_get(db_path, key):
    """只读读取 VS Code 风格 state.vscdb 的 ItemTable[key];缺失/出错返 None。"""
    try:
        conn = sqlite3.connect(_sqlite_ro_uri(db_path), uri=True)
        try:
            r = conn.execute("SELECT value FROM ItemTable WHERE key = ?", (key,)).fetchone()
        finally:
            conn.close()
    except sqlite3.Error:
        return None
    return r[0] if r else None


def _qoder_active_session(cwd):
    """Qoder IDE 当前活动会话 id:优先 aicoding.chat.tabs(activeTabId→该 tab.sessionId),
    退回 aicoding.chat.views(active:true 的 sessionId)。取不到返 None。"""
    db = _qoder_workspace_db(cwd)
    if not db:
        return None
    raw = _vscdb_get(db, "aicoding.chat.tabs")
    if raw:
        try:
            d = json.loads(raw)
            active = d.get("activeTabId")
            for t in d.get("tabs", []):
                if isinstance(t, dict) and t.get("tabId") == active and t.get("sessionId"):
                    return t["sessionId"]
        except (json.JSONDecodeError, TypeError, AttributeError):
            pass
    raw = _vscdb_get(db, "aicoding.chat.views")
    if raw:
        try:
            for v in json.loads(raw):
                if isinstance(v, dict) and v.get("active") and v.get("sessionId"):
                    return v["sessionId"]
        except (json.JSONDecodeError, TypeError):
            pass
    return None


def _qoder_state_model(cwd, session_id):
    """Qoder IDE 该会话真实模型:读 state.vscdb 的 chat.modelConfig.session.<sid>
    (值为裸模型名如 'qwen3.7-max',个别版本可能是 JSON)。比 transcript(不记)/audit(仅档位别名)更准;取不到返 None。"""
    db = _qoder_workspace_db(cwd)
    if not db:
        return None
    raw = _vscdb_get(db, f"chat.modelConfig.session.{session_id}")
    if not isinstance(raw, str) or not raw.strip():
        return None
    raw = raw.strip()
    if raw.startswith("{"):
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            return None
        m = (d.get("model") or d.get("modelId") or d.get("modelID")) if isinstance(d, dict) else None
        return m if isinstance(m, str) and m else None
    return raw.strip('"') or None


def qoder_pack(src_path, session_id, out_dir):
    # 模型优先级: state.vscdb 真实模型 > transcript(通常不记) > audit 档位别名
    cwd = _read_cwd_from_jsonl(src_path)
    model = ((_qoder_state_model(cwd, session_id) if cwd else None)
             or _last_model(src_path) or _qoder_audit_model(session_id))
    dst = Path(out_dir) / _zip_name("qoder", model, session_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    zf, tmp = _open_zip_atomic(dst)
    try:
        zf.write(_os_path(src_path), arcname=src_path.name)
        _commit_zip(zf, tmp, dst)
    except Exception:
        _abort_zip(zf, tmp)
        raise
    return dst.resolve(), 1


# ---------------- qoderwork / Qoder CLI (claude 风格: 主 jsonl + 同名状态目录) ----------------
# Qoder(~/.qoder)、qoderwork(~/.qoderwork)、Qoder CLI 是三个独立产品:
#   Qoder(IDE):  ~/.qoder/projects/<enc>/transcript/{sid}.jsonl                  → 见上 qoder_*
#   Qoder CLI:   ~/.qoder/projects/<enc>/{sid}.jsonl(顶层) + 同名 {sid}/ 状态目录  → qodercli_*
#   qoderwork:   ~/.qoderwork/projects/<enc>/{sid}.jsonl     + 同名 {sid}/ 状态目录  → qoderwork_*
# Qoder CLI 与 Qoder 共用 ~/.qoder/projects 根,靠布局区分(顶层 jsonl vs transcript/ 子目录)。
# (~/.qoder-cli 只是 CLI 的 ai-stats 代码统计,非会话,不在此。)

def _pack_main_plus_sibling(src_path, session_id, out_dir, prefix, product_root,
                            request_records=None):
    """主 {sid}.jsonl(子 agent 以 isSidechain 内联其中)
    + 同名运行时状态目录 {sid}/(state.json / compression-v2/...)
    + 段日志 {product_root}/logs/sessions/<enc>/{sid}/segments/*(执行轨迹, 归到 {sid}/logs/)
    + (可选)request_records → 最外层 request-ids.jsonl

    <enc> 为项目编码目录名(= src_path.parent.name),projects 与 logs/sessions 同编码。"""
    dst = Path(out_dir) / _zip_name(prefix, _last_model(src_path), session_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    sibling_dir = src_path.parent / session_id
    enc = src_path.parent.name
    logs_dir = product_root / "logs" / "sessions" / enc / session_id

    n = 0
    zf, tmp = _open_zip_atomic(dst)
    try:
        zf.write(_os_path(src_path), arcname=src_path.name)
        n += 1
        n += _add_dir_to_zip(zf, sibling_dir, session_id)
        n += _add_dir_to_zip(zf, logs_dir, f"{session_id}/logs")
        n += _zip_write_jsonl(zf, "request-ids.jsonl", request_records)
        _commit_zip(zf, tmp, dst)
    except Exception:
        _abort_zip(zf, tmp)
        raise
    return dst.resolve(), n


def qodercli_available():
    return (HOME / ".qoder" / "projects").exists()


def qodercli_list(cwd):
    # 顶层 *.jsonl = Qoder CLI 会话;transcript/*.jsonl 是 Qoder(IDE),不在此匹配。
    return _list_jsonl_projects(HOME / ".qoder" / "projects", cwd, "*.jsonl")


def qodercli_pack(src_path, session_id, out_dir):
    # 文件名前缀与工具键一致,均为 qoder-cli
    # assistant 的 message.id 形如 chatcmpl-<uuid>,<uuid> 即百炼 request-id(旧版无此字段则跳过)
    return _pack_main_plus_sibling(
        src_path, session_id, out_dir, "qoder-cli", HOME / ".qoder",
        request_records=_assistant_request_ids(src_path, "id"))


def qoderwork_available():
    return (HOME / ".qoderwork" / "projects").exists()


def qoderwork_list(cwd):
    return _list_jsonl_projects(HOME / ".qoderwork" / "projects", cwd, "*.jsonl")


def qoderwork_pack(src_path, session_id, out_dir):
    # qoderwork assistant 的 message.id 形如 chatcmpl-<uuid>,<uuid> 即百炼 request-id
    return _pack_main_plus_sibling(
        src_path, session_id, out_dir, "qoderwork", HOME / ".qoderwork",
        request_records=_assistant_request_ids(src_path, "id"))


# ---------------- Codex ----------------

def _codex_home():
    """Codex 数据根:CODEX_HOME 优先,否则 ~/.codex。
    Windows 上 home 即 %USERPROFILE%,与官方默认 %USERPROFILE%\\.codex 一致
    (Codex 在 Windows 用的是 home/.codex,不是 %APPDATA%)。"""
    env = os.environ.get("CODEX_HOME")
    return Path(env) if env else HOME / ".codex"


CODEX_DB = _codex_home() / "state_5.sqlite"


# threads.source 语义: 'cli'/'exec'=Codex CLI, 'vscode'=Codex App(IDE),
# 以 '{' 开头的 JSON 串=spawn 出来的 subagent(通过 thread_spawn_edges 递归带出,不作顶层)。
CODEX_CLI_SOURCES = ("cli", "exec")
CODEX_APP_SOURCES = ("vscode",)


def _codex_list(cwd, sources):
    """按 cwd + source 取该项目会话。cwd 先走 SQL 精确相等(命中即走索引、零额外开销);
    未命中再回扫同 source 全部行、用 _same_path 规范化比对——Windows 上 threads.cwd
    的盘符大小写与分隔符形态可能与本进程 os.getcwd() 不同,裸相等会整体漏匹配。"""
    if not CODEX_DB.exists():
        return []
    conn = sqlite3.connect(_sqlite_ro_uri(CODEX_DB), uri=True)
    try:
        ph = ",".join("?" * len(sources))
        rows = conn.execute(
            "SELECT id, rollout_path, updated_at FROM threads "
            f"WHERE archived = 0 AND cwd = ? AND source IN ({ph}) "
            "ORDER BY updated_at DESC",
            (cwd, *sources)
        ).fetchall()
        if not rows:
            rows = [(sid, path, upd) for sid, path, upd, c in conn.execute(
                "SELECT id, rollout_path, updated_at, cwd FROM threads "
                f"WHERE archived = 0 AND source IN ({ph}) "
                "ORDER BY updated_at DESC", tuple(sources)
            ).fetchall() if _same_path(c, cwd)]
    finally:
        conn.close()
    out = []
    for sid, path, updated_at in rows:
        p = Path(_os_path(path)) if path else None
        if p and p.exists():
            out.append((sid, p, _safe_float(updated_at)))
    return out


def codexcli_available():
    return CODEX_DB.exists()


def codexapp_available():
    return CODEX_DB.exists()


def codexcli_list(cwd):
    return _codex_list(cwd, CODEX_CLI_SOURCES)


def codexapp_list(cwd):
    return _codex_list(cwd, CODEX_APP_SOURCES)


def codexcli_pack(src_path, session_id, out_dir):
    return _codex_pack(src_path, session_id, out_dir, "codex-cli")


def codexapp_pack(src_path, session_id, out_dir):
    return _codex_pack(src_path, session_id, out_dir, "codex-app")


def _codex_pack(src_path, session_id, out_dir, prefix):
    """主 rollout jsonl + 递归 spawn 的全部子 agent rollout(各为独立文件)。
    prefix 区分 codex-cli / codex-app,二者子 agent 收集逻辑一致。"""
    dst = Path(out_dir) / _zip_name(prefix, _last_model(src_path), session_id)
    dst.parent.mkdir(parents=True, exist_ok=True)

    n = 0
    zf, tmp = _open_zip_atomic(dst)
    try:
        zf.write(_os_path(src_path), arcname=src_path.name)
        n += 1
        # 递归 thread_spawn_edges 收集全部后代子 agent 的 rollout
        if CODEX_DB.exists():
            conn = sqlite3.connect(_sqlite_ro_uri(CODEX_DB), uri=True)
            try:
                cur = conn.execute(
                    "WITH RECURSIVE d(id) AS ("
                    "  SELECT child_thread_id FROM thread_spawn_edges WHERE parent_thread_id = ?"
                    "  UNION ALL"
                    "  SELECT e.child_thread_id FROM thread_spawn_edges e JOIN d ON e.parent_thread_id = d.id"
                    ") SELECT d.id, t.rollout_path FROM d LEFT JOIN threads t ON t.id = d.id",
                    (session_id,)
                )
                for _cid, cpath in cur.fetchall():
                    if cpath:
                        p = Path(cpath)
                        if Path(_os_path(p)).is_file():
                            zf.write(_os_path(p), arcname=f"{session_id}/subagents/{p.name}")
                            n += 1
            except sqlite3.Error:
                # thread_spawn_edges 不存在(旧版本)等：只导主 rollout，不致命
                pass
            finally:
                conn.close()
        _commit_zip(zf, tmp, dst)
    except Exception:
        _abort_zip(zf, tmp)
        raise
    return dst.resolve(), n


# ---------------- OpenCode ----------------

def _opencode_db_candidates():
    """OpenCode 数据库候选位置(按优先级)。OpenCode 走 XDG 风格路径且**不分平台**,
    macOS 也用 ~/.local/share/opencode(不是 ~/Library/Application Support);
    Windows 官方 troubleshooting 指向 %USERPROFILE%\\.local\\share\\opencode,
    但部分版本/桌面端落在 %LOCALAPPDATA%\\opencode,故 Windows 两处都探。
    OPENCODE_DB 可直接指定库文件,OPENCODE_DATA_DIR / XDG_DATA_HOME 指定数据根。"""
    dirs = []
    data_dir = os.environ.get("OPENCODE_DATA_DIR")
    if data_dir:
        dirs.append(Path(data_dir))
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        dirs.append(Path(xdg) / "opencode")
    dirs.append(HOME / ".local" / "share" / "opencode")
    if IS_WINDOWS:
        local = os.environ.get("LOCALAPPDATA")
        dirs.append((Path(local) if local else HOME / "AppData" / "Local") / "opencode")
    out = []
    db = os.environ.get("OPENCODE_DB")
    if db:
        out.append(Path(db))
    out += [d / "opencode.db" for d in dirs]
    return out


def _resolve_opencode_db():
    """取首个真实存在的候选库;都不存在时返回默认位置(供 available() 判否与报错展示)。"""
    cands = _opencode_db_candidates()
    for p in cands:
        try:
            if p.is_file():
                return p
        except OSError:
            continue
    return HOME / ".local" / "share" / "opencode" / "opencode.db"


OPENCODE_DB = _resolve_opencode_db()


def opencode_available():
    return OPENCODE_DB.exists()


def _opencode_conn():
    return sqlite3.connect(_sqlite_ro_uri(OPENCODE_DB), uri=True)


def opencode_list(cwd):
    """directory 列同 Codex 的 cwd:先 SQL 精确相等,未命中再回扫按 _same_path 规范化比对
    (Windows 盘符大小写/分隔符形态差异)。"""
    if not OPENCODE_DB.exists():
        return []
    conn = _opencode_conn()
    try:
        rows = conn.execute(
            "SELECT id, time_updated FROM session "
            "WHERE time_archived IS NULL AND directory = ? "
            "ORDER BY time_updated DESC",
            (cwd,)
        ).fetchall()
        if not rows:
            rows = [(sid, ts) for sid, ts, d in conn.execute(
                "SELECT id, time_updated, directory FROM session "
                "WHERE time_archived IS NULL ORDER BY time_updated DESC"
            ).fetchall() if _same_path(d, cwd)]
    finally:
        conn.close()
    return [(sid, OPENCODE_DB, _safe_float(ts) / 1000) for sid, ts in rows]


def _opencode_last_model(conn, ids):
    """从 message.data 取最后一个模型标识:data.model.modelID(嵌套)或 data.modelID(扁平);无则 None。
    (OpenCode 会话存 SQLite,模型记在 assistant 消息的 data JSON 里,非独立列;中途切换以最终为准。)"""
    ph = ",".join("?" * len(ids))
    try:
        cur = conn.execute(
            f"SELECT data FROM message WHERE session_id IN ({ph}) ORDER BY rowid", ids)
    except sqlite3.Error:
        return None
    last = None
    for (data,) in cur.fetchall():
        if not isinstance(data, str):
            continue
        try:
            d = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(d, dict):
            continue
        m = d.get("model")
        if isinstance(m, dict) and isinstance(m.get("modelID"), str) and m["modelID"]:
            last = m["modelID"]
        elif isinstance(d.get("modelID"), str) and d["modelID"]:
            last = d["modelID"]
    return last


def opencode_pack(_db_path, session_id, out_dir):
    """从 session/message/part 还原 jsonl；按 parent_id 递归包含全部子会话(subagent)。"""
    buf = io.StringIO()
    n = 0
    model = None
    conn = _opencode_conn()
    try:
        cur = conn.execute(
            "WITH RECURSIVE tree(id) AS ("
            "  SELECT id FROM session WHERE id = ?"
            "  UNION ALL"
            "  SELECT s.id FROM session s JOIN tree t ON s.parent_id = t.id"
            ") SELECT id FROM tree",
            (session_id,)
        )
        ids = [r[0] for r in cur.fetchall()]
        if not ids:
            ids = [session_id]
        ph = ",".join("?" * len(ids))
        model = _opencode_last_model(conn, ids)

        # session 行
        cur = conn.execute(f"SELECT * FROM session WHERE id IN ({ph})", ids)
        cols = [d[0] for d in cur.description]
        for row in cur.fetchall():
            d = dict(zip(cols, row))
            d["_table"] = "session"
            _maybe_parse_json_field(d, "data")
            buf.write(json.dumps(d, ensure_ascii=False, default=str) + "\n")
            n += 1

        # message + 其 part
        cur = conn.execute(
            f"SELECT * FROM message WHERE session_id IN ({ph}) ORDER BY rowid", ids)
        cols = [d[0] for d in cur.description]
        for row in cur.fetchall():
            d = dict(zip(cols, row))
            d["_table"] = "message"
            _maybe_parse_json_field(d, "data")
            buf.write(json.dumps(d, ensure_ascii=False, default=str) + "\n")
            n += 1
            pcur = conn.execute(
                "SELECT * FROM part WHERE message_id = ? ORDER BY rowid",
                (d.get("id"),))
            pcols = [pd[0] for pd in pcur.description]
            for prow in pcur.fetchall():
                pd = dict(zip(pcols, prow))
                pd["_table"] = "part"
                _maybe_parse_json_field(pd, "data")
                buf.write(json.dumps(pd, ensure_ascii=False, default=str) + "\n")
                n += 1
    finally:
        conn.close()

    dst = Path(out_dir) / _zip_name("opencode", model, session_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    zf, tmp = _open_zip_atomic(dst)
    try:
        zf.writestr(f"{session_id}.jsonl", buf.getvalue())
        _commit_zip(zf, tmp, dst)
    except Exception:
        _abort_zip(zf, tmp)
        raise
    return dst.resolve(), 1


# ---------------- oh-my-pi (~/.omp/agent/sessions) ----------------

def _omp_root():
    return HOME / ".omp" / "agent" / "sessions"


def omp_available():
    return _omp_root().exists()


def omp_list(cwd):
    """~/.omp/agent/sessions/<enc>/<timestamp>_<sid>.jsonl；session 行带 cwd，
    sessionId = 文件名末段(时间戳后)。按 enc 目录用文件内 cwd 精确匹配。"""
    root = _omp_root()
    if not root.exists():
        return []
    out = []
    for enc in Path(_os_path(root)).iterdir():
        if not enc.is_dir():
            continue
        files = sorted(enc.glob("*.jsonl"),
                       key=lambda p: p.stat().st_mtime, reverse=True)
        probe_cwd = None
        for probe in files:
            probe_cwd = _read_cwd_from_jsonl(probe)
            if probe_cwd is not None:
                break
        if not _same_path(probe_cwd, cwd):
            continue
        for f in files:
            if "_" not in f.stem:   # 只认 <timestamp>_<sid> 主会话文件
                continue
            out.append((f.stem.split("_")[-1], f, f.stat().st_mtime))
    out.sort(key=lambda t: t[2], reverse=True)
    return out


def omp_pack(src_path, session_id, out_dir):
    """主会话 jsonl(omp 单文件自包含，子 agent 内联其中)
    + 最外层 request-ids.jsonl:assistant 的 message.responseId(chatcmpl-<uuid>)剥前缀"""
    dst = Path(out_dir) / _zip_name("oh-my-pi", _last_model(src_path), session_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    zf, tmp = _open_zip_atomic(dst)
    try:
        zf.write(_os_path(src_path), arcname=f"{session_id}.jsonl")
        n += 1
        n += _zip_write_jsonl(zf, "request-ids.jsonl",
                              _assistant_request_ids(src_path, "responseId"))
        _commit_zip(zf, tmp, dst)
    except Exception:
        _abort_zip(zf, tmp)
        raise
    return dst.resolve(), n


# ---------------- Kimi Code (~/.kimi-code) ----------------
# 布局: ~/.kimi-code/sessions/<ws>/session_<uuid>/{state.json, agents/*/wire.jsonl, logs/}
# state.json 记可靠 cwd 与 updatedAt(ms);wire.jsonl 为逐行事件流(顶层时间字段 time,
# 首行 metadata 用 created_at),不记录 claude 风格 model/message 字段。
# 注意: user-history/<md5(cwd)>.jsonl 是项目级聚合(该项目所有会话的输入历史,
# 无时间戳/会话归属字段),无法按当前会话过滤,故不纳入导出,避免带出其它会话内容。

def _kimi_root():
    return HOME / ".kimi-code"


def kimi_available():
    return (_kimi_root() / "sessions").is_dir()


def _kimi_state(session_dir):
    """会话目录内 state.json(cwd/updatedAt 等元数据);缺失/坏返 None"""
    sj = Path(_os_path(Path(session_dir) / "state.json"))
    if not sj.is_file():
        return None
    try:
        d = json.loads(sj.read_text(encoding="utf-8", errors="ignore"))
    except (OSError, json.JSONDecodeError):
        return None
    return d if isinstance(d, dict) else None


def kimi_list(cwd):
    """遍历 sessions/<ws>/session_*/,用 state.json 的真实 cwd 精确匹配(不依赖 <ws> 目录名)。
    sid 取会话目录名(session_<uuid>),按 updatedAt 降序。"""
    root = _kimi_root() / "sessions"
    if not root.is_dir():
        return []
    out = []
    for ws in Path(_os_path(root)).iterdir():
        if not ws.is_dir():
            continue
        for sd in ws.iterdir():
            if not sd.is_dir():
                continue
            st = _kimi_state(sd)
            if not st or not _same_path(st.get("cwd"), cwd):
                continue
            wire = sd / "agents" / "main" / "wire.jsonl"
            if not wire.is_file():
                continue
            upd = _safe_float(st.get("updatedAt")) / 1000 or wire.stat().st_mtime
            out.append((sd.name, wire, upd))
    out.sort(key=lambda t: t[2], reverse=True)
    return out


def _kimi_last_model(src_path):
    """Kimi 的 wire.jsonl 无 claude 风格 model 字段;模型记在 profile.bind 事件的
    modelAlias(如 tokenhub/mdataplus)。取最后一次声明,中途切换以最终为准;无则 None。"""
    last = None
    try:
        with open(_os_path(src_path), encoding="utf-8", errors="ignore") as f:
            for line in f:
                if '"profile.bind"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                m = d.get("modelAlias") if isinstance(d, dict) else None
                if isinstance(m, str) and m:
                    last = m
    except OSError:
        return None
    return last


def _kimi_request_ids(session_dir):
    """requestId 提取:各 agents/*/wire.jsonl 的 loop 事件里 event.messageId 形如
    chatcmpl-<uuid>,剥前缀即大模型接口 requestId。按 requestId 去重、时间升序。
    wire 顶层时间字段 time 为 epoch 毫秒,统一转 ISO8601 与其它产品对齐。"""
    from datetime import datetime, timezone
    out, seen = [], set()
    for wire in sorted(Path(_os_path(session_dir)).glob("agents/*/wire.jsonl")):
        try:
            with open(_os_path(wire), encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "chatcmpl-" not in line:
                        continue
                    try:
                        d = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    ev = d.get("event") if isinstance(d, dict) else None
                    ev = ev if isinstance(ev, dict) else {}
                    rid = _strip_chatcmpl(ev.get("messageId"))
                    if not rid or rid in seen:
                        continue
                    seen.add(rid)
                    ts = d.get("time") if isinstance(d, dict) else None
                    iso = None
                    if isinstance(ts, (int, float)) and ts > 0:
                        iso = datetime.fromtimestamp(ts / 1000, tz=timezone.utc) \
                                  .isoformat().replace("+00:00", "Z")
                    out.append({"timestamp": iso, "request_id": rid})
        except OSError:
            continue
    return sorted(out, key=lambda r: r.get("timestamp") or "")


def kimi_pack(src_path, session_id, out_dir):
    """仅当前会话目录(state.json + 全部 agents/*/wire.jsonl + logs/)
    + 最外层 request-ids.jsonl。user-history/ 是项目级跨会话聚合,不收。"""
    session_dir = src_path.parents[2]   # .../session_*/agents/main/wire.jsonl → 会话目录
    dst = Path(out_dir) / _zip_name("kimi-code", _kimi_last_model(src_path), session_id)
    dst.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    zf, tmp = _open_zip_atomic(dst)
    try:
        n += _add_dir_to_zip(zf, session_dir, session_id)
        n += _zip_write_jsonl(zf, "request-ids.jsonl",
                              _kimi_request_ids(session_dir))
        _commit_zip(zf, tmp, dst)
    except Exception:
        _abort_zip(zf, tmp)
        raise
    return dst.resolve(), n


# ---------------- 注册 ----------------

PARSERS = {
    "claude-code": (claudecode_available, claudecode_list, claudecode_pack),
    "qwen-code":   (qwen_available,       qwen_list,       qwen_pack),
    "qoder":       (qoder_available,      qoder_list,      qoder_pack),
    "qoder-cli":   (qodercli_available,   qodercli_list,   qodercli_pack),
    "qoderwork":   (qoderwork_available,  qoderwork_list,  qoderwork_pack),
    "codex-cli":   (codexcli_available,   codexcli_list,   codexcli_pack),
    "codex-app":   (codexapp_available,   codexapp_list,   codexapp_pack),
    "opencode":    (opencode_available,   opencode_list,   opencode_pack),
    "oh-my-pi":    (omp_available,        omp_list,        omp_pack),
    "kimi-code":   (kimi_available,       kimi_list,       kimi_pack),
}
PRIORITY = ["qoder-cli", "qoder", "qoderwork", "qwen-code", "oh-my-pi",
            "kimi-code", "codex-cli", "codex-app", "opencode", "claude-code"]

# 客户端专属安装根 → 该客户端会话工具。用于在多个工具共享同一 cwd 时,
# 依脚本自身安装位置(__file__)优先归属当前客户端。共享的 ~/.claude/skills
# 被多个客户端扫描、无法区分,故不在此表;此时退回 PRIORITY + cwd。
_CLIENT_ROOTS = [
    (".qoderwork", ["qoderwork"]),
    (".qoder",     ["qoder-cli", "qoder"]),
    (".codex",     ["codex-cli", "codex-app"]),
    (".qwen",      ["qwen-code"]),
    ("opencode",   ["opencode"]),   # ~/.config/opencode
    (".omp",       ["oh-my-pi"]),
    (".kimi-code", ["kimi-code"]),
]


# macOS 由 OS 注入的“启动 app bundle id” → 客户端。shell env 共享伪造不了(非继承链能改的普通 env),
# 且 com.qoder.work / com.qoder.ide 能精确区分 qoderwork/qoder(env 标志做不到)。
# 注意:在独立终端跑 CLI 时此值是终端的 bundle id(如 com.apple.Terminal),不代表 agent,
# 故优先级低于进程祖先链,且在 env 内排在“会话 id”类变量之后。
_BUNDLE_ID_CLIENTS = [
    ("com.qoder.work",                 ["qoderwork"]),
    ("com.qoder.ide",                  ["qoder-cli", "qoder"]),
    ("com.openai.codex",               ["codex-cli", "codex-app"]),
    ("com.anthropic.claudefordesktop", ["claude-code"]),
]


def _client_from_env():
    """据客户端注入的运行时环境变量判定当前客户端(最后兜底信号)。
    信号从专属到通用:
      1) “会话 id”类产品专属变量(不可能被其它产品误设);
      2) macOS 的 __CFBundleIdentifier(OS 注入的启动 app id,精确且难伪造)。
    Windows 没有等价的“启动 app 标识”环境变量(信号 2 天然为空),识别改由更靠前的
    进程祖先链承担(见 _client_from_process,Windows 分支基于 toolhelp 快照 + 命令行)。
    不用 CLAUDECODE / AI_AGENT / QODER_AGENT 等“标志”类变量:
      - CLAUDECODE/AI_AGENT 被兼容 claude skill 的工具(oh-my-pi)共享;
      - QODER_AGENT/QODER_IDE 无法区分 Qoder 与 QoderWork(两者共享同一 agent SDK)。"""
    # Codex 专属(thread/session id,仅 Codex 注入)
    if os.environ.get("CODEX_THREAD_ID") or os.environ.get("CODEX_SESSION_ID"):
        return ["codex-cli", "codex-app"]
    # Claude Code 专属(会话 id,仅 Claude Code 注入)
    if os.environ.get("CLAUDE_CODE_SESSION_ID"):
        return ["claude-code"]
    # macOS: OS 注入的启动 app bundle id(GUI-agent-app 精确区分,不依赖 ps)
    bid = os.environ.get("__CFBundleIdentifier")
    if bid:
        for key, tools in _BUNDLE_ID_CLIENTS:
            if bid == key or bid.startswith(key + "."):
                return tools
    return []


_WIN_PROC_TABLE = None


def _win_process_table():
    """Windows 全进程表快照 {pid: (ppid, exeName)}。
    Windows 没有 ps,这是 `ps -o ppid=,comm=` 的等价替代:CreateToolhelp32Snapshot 纯 ctypes
    调用,不起子进程、无解释器启动开销,一次拿到全表。进程表在单次导出内不变,故全局缓存一次。
    非 Windows / API 失败(权限等)返 {},调用方自然降级到其它信号。"""
    global _WIN_PROC_TABLE
    if _WIN_PROC_TABLE is not None:
        return _WIN_PROC_TABLE
    _WIN_PROC_TABLE = {}
    if not IS_WINDOWS:
        return _WIN_PROC_TABLE
    try:
        import ctypes
        from ctypes import wintypes

        class _PE32(ctypes.Structure):
            _fields_ = [
                ("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD),
                ("th32DefaultHeapID", ctypes.c_void_p),
                ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD),
                ("pcPriClassBase", ctypes.c_long), ("dwFlags", wintypes.DWORD),
                ("szExeFile", ctypes.c_char * 260),
            ]

        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        # 必须显式声明 restype:HANDLE 在 64 位下是 8 字节,默认 c_int 会截断句柄
        k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        k32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        k32.Process32First.restype = wintypes.BOOL
        k32.Process32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PE32)]
        k32.Process32Next.restype = wintypes.BOOL
        k32.Process32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PE32)]
        k32.CloseHandle.argtypes = [wintypes.HANDLE]

        snap = k32.CreateToolhelp32Snapshot(0x00000002, 0)   # TH32CS_SNAPPROCESS
        if not snap or snap == ctypes.c_void_p(-1).value:
            return _WIN_PROC_TABLE
        try:
            e = _PE32()
            e.dwSize = ctypes.sizeof(_PE32)
            ok = k32.Process32First(snap, ctypes.byref(e))
            while ok:
                _WIN_PROC_TABLE[int(e.th32ProcessID)] = (
                    int(e.th32ParentProcessID),
                    e.szExeFile.decode("mbcs", errors="ignore"),
                )
                e = _PE32()
                e.dwSize = ctypes.sizeof(_PE32)
                ok = k32.Process32Next(snap, ctypes.byref(e))
        finally:
            k32.CloseHandle(snap)
    except Exception:
        # ctypes 不可用 / 结构体布局异常 / 权限不足:视作拿不到进程信息
        _WIN_PROC_TABLE = {}
    return _WIN_PROC_TABLE


def _win_ancestor_chain():
    """Windows: 自身及各级祖先的 [(pid, exeName)](自身在前)。
    ppid 在 Windows 会被复用(父进程退出后 pid 可能指向无关新进程),故遇到已访问过的 pid
    或 pid<=0 即停止,避免成环;上溯层数与 POSIX 分支同为 20。"""
    table = _win_process_table()
    out, seen, pid = [], set(), os.getpid()
    for _ in range(20):
        ent = table.get(pid)
        if not ent:
            break
        out.append((pid, ent[1]))
        seen.add(pid)
        pid = ent[0]
        if pid <= 0 or pid in seen:
            break
    return out


def _self_path_fragments():
    """本脚本自身路径的各种书写形态(原样/resolve/posix 分隔符)+ skill 目录。
    用于从命令行文本里剔除自身路径:本脚本常安装在 ~/.claude/skills/export-session/ 下,
    启动它的命令行里含 'claude' 字样,若不剔除会让 _CLIENT_PROC_MARKERS 误判客户端。"""
    me, skill_dir = Path(__file__), Path(__file__).parents[1]
    frags = set()
    for p in (me, me.resolve(), skill_dir, skill_dir.resolve()):
        frags.add(str(p).lower())
        frags.add(p.as_posix().lower())
    env_dir = os.environ.get("CLAUDE_SKILL_DIR")
    if env_dir:
        frags.add(env_dir.lower())
        frags.add(env_dir.replace("\\", "/").lower())
    return {f for f in frags if f}


def _win_ancestor_cmdlines():
    """Windows: 祖先链各进程的完整命令行(小写,已剔除本脚本自身路径)。
    npm/node 安装的 CLI(qwen-code / kimi-code / oh-my-pi / npm 版 claude-code)进程名
    一律是 node.exe,exe 名区分不出客户端,只有命令行里的入口脚本路径能区分。
    Win32_Process.CommandLine 只能经 WMI 取(toolhelp 不提供),PowerShell 启动有开销,
    故仅在 exe 名匹配失败时才调用,且只查祖先链这几个 pid。取不到返 []。"""
    if not IS_WINDOWS:
        return []
    import subprocess
    pids = [pid for pid, _ in _win_ancestor_chain()]
    if not pids:
        return []
    flt = " or ".join(f"ProcessId={p}" for p in pids)
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command",
             f"Get-CimInstance Win32_Process -Filter '{flt}' | "
             "ForEach-Object { $_.CommandLine }"],
            capture_output=True, text=True, timeout=15,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except (OSError, subprocess.SubprocessError):
        return []
    frags = _self_path_fragments()
    out = []
    for line in (r.stdout or "").splitlines():
        low = line.strip().lower()
        if not low:
            continue
        for f in frags:
            low = low.replace(f, " ")
        out.append(low)
    return out


def _proc_ancestry():
    """上溯进程祖先链,返回每个祖先的可执行名/路径。
    skill 经软链共享安装(__file__ 落 ~/.claude 无法区分)、且客户端不注入专属环境变量时,
    进程树是唯一可靠的当前客户端信号。
    POSIX 用 ps;Windows 无 ps,走 toolhelp 快照(见 _win_process_table)。
    两者都拿不到时返 [],不影响其它信号。"""
    if IS_WINDOWS:
        return [name for _, name in _win_ancestor_chain()]
    import subprocess
    out, pid = [], os.getpid()
    for _ in range(20):
        if pid <= 1:
            break
        try:
            r = subprocess.run(["ps", "-o", "ppid=,comm=", "-p", str(pid)],
                               capture_output=True, text=True, timeout=2)
        except (OSError, subprocess.SubprocessError):
            break
        line = (r.stdout or "").strip()
        if not line:
            break
        parts = line.split(None, 1)
        if len(parts) < 2:
            break
        out.append(parts[1])
        try:
            nxt = int(parts[0])
        except ValueError:
            break
        if nxt == pid:
            break
        pid = nxt
    return out


# 进程可执行名/路径 → 客户端会话工具(有序)。同一进程可能对应多个共享存储的工具
# (Qoder 应用既跑 IDE 会话也可跑 CLI、Codex 应用同含 app/cli),进程名无法区分,
# 故需列出全部候选,交由 detect_tool 按'当前活跃'择一。与 _CLIENT_ROOTS 对齐。
# qoderwork 含 'qoder' 子串,必须排在 qoder 前。
_CLIENT_PROC_MARKERS = [
    (["qoderwork"],              ("qoderwork",)),
    (["qoder-cli", "qoder"],     (".qoder-cli", "qoder")),
    (["codex-cli", "codex-app"], ("codex",)),
    (["qwen-code"],              ("qwen",)),
    (["kimi-code"],              ("kimi",)),
    (["oh-my-pi"],               ("oh-my-pi", "omp")),
    (["claude-code"],            ("claude",)),
    (["opencode"],               ("opencode",)),
]


def _match_proc_marker(text):
    """一段进程可执行名/路径/命令行文本命中哪个客户端;不命中返 None。
    basename 同时按 '/' 和 '\\' 切(Windows 是反斜杠,且 exe 名带 .exe 后缀,
    故除精确等值外仍保留子串匹配:'claude' in 'claude.exe')。"""
    low = text.lower()
    base = low.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    for tools, markers in _CLIENT_PROC_MARKERS:
        if any(mk == base or mk in low for mk in markers):
            return list(tools)
    return None


def _client_from_process():
    """据进程祖先链的可执行名判定当前客户端 → 对应会话工具(可多个);识别不到返 []。
    claude 系分支(qoder CLI / qoderwork / claude-code)的 jsonl 结构相同、无法内容区分,
    但进程可执行名不同(qoder / qoderwork / claude)。同一应用内 IDE/CLI 不可区分时返回全部候选。
    Windows 上 npm/node 安装的 CLI 进程名全是 node.exe,exe 名无从区分,故再退一步查
    祖先链命令行里的入口脚本路径(仅此时才付 WMI 查询开销,见 _win_ancestor_cmdlines)。"""
    for comm in _proc_ancestry():
        tools = _match_proc_marker(comm)
        if tools:
            return tools
    for cmdline in _win_ancestor_cmdlines():
        tools = _match_proc_marker(cmdline)
        if tools:
            return tools
    return []


def _client_bias():
    """识别当前客户端 → 该客户端对应的会话工具(有序);识别不到返回 []。
    信号按可靠性从高到低:
      1) 安装位置:脚本 __file__ / 客户端注入的 $CLAUDE_SKILL_DIR 落在某客户端专属根;
         未解析路径与 resolve() 结果都看,兼容 `skills link` 软链安装。这是物理事实,最稳。
      2) 客户端运行时环境特征(见 _client_from_env)。
    共享的 ~/.claude/skills 路径无法区分客户端,故此时只能靠 (2)。"""
    # 按"路径段"比较:不受平台分隔符差异影响(Windows 是 '\\'),且天然精确
    # (.qoderwork 不会被 .qoder 误命中)
    seg_sets = [set(Path(__file__).parts), set(Path(__file__).resolve().parts)]
    skill_dir = os.environ.get("CLAUDE_SKILL_DIR")
    if skill_dir:
        seg_sets.append(set(Path(skill_dir).parts))
    for marker, tools in _CLIENT_ROOTS:
        if any(marker in segs for segs in seg_sets):
            return tools
    # 安装路径无法区分(skill 软链到 ~/.claude/skills 被多客户端共享)时,
    # 用进程祖先链这一运行时物理事实识别;再退回环境变量。
    proc = _client_from_process()
    if proc:
        return proc
    return _client_from_env()


def _ordered(bias):
    return bias + [t for t in PRIORITY if t not in bias]


# ---- 多因子锁定"当前会话"(仅在同 cwd 出现多个候选会话/工具时启用;单候选走快路径,零额外开销) ----
# 因子按可靠性从高到低:
#   1) 客户端注入的"当前会话 id"环境变量(精确):Claude 的 CLAUDE_CODE_SESSION_ID / CLAUDE_SESSION_ID、
#      Codex 的 CODEX_THREAD_ID / CODEX_SESSION_ID;取不到即回退到下一因子。
#   2) 运行时文件记录的属主 pid 命中本进程祖先链——该工具进程亲自拉起了本次导出,必是当前会话
#      (Qwen 的 <sid>.runtime.json 记 pid;其余工具运行时文件无 pid)。
#   3) 会话内容末条 timestamp 最新(当前会话此刻正被写入),并以 (mtime, sid) 做确定性兜底。
_SESSION_ID_ENV = {
    "claude-code": ("CLAUDE_CODE_SESSION_ID", "CLAUDE_SESSION_ID"),
    "codex-cli":   ("CODEX_THREAD_ID", "CODEX_SESSION_ID"),
    "codex-app":   ("CODEX_THREAD_ID", "CODEX_SESSION_ID"),
}


def _env_session_id(tool_name):
    """客户端注入的当前会话 id(逐个候选环境变量取首个非空);无则 None。"""
    for k in _SESSION_ID_ENV.get(tool_name, ()):
        v = os.environ.get(k)
        if v and v.strip():
            return v.strip()
    return None


def _ancestor_pids():
    """自身 + 全部祖先进程 pid 集合;取不到进程信息时至少返回自身 pid。
    Windows 走 toolhelp 快照(无 ps),POSIX 走 ps。"""
    if IS_WINDOWS:
        return {pid for pid, _ in _win_ancestor_chain()} or {os.getpid()}
    import subprocess
    pids, pid = {os.getpid()}, os.getpid()
    for _ in range(20):
        if pid <= 1:
            break
        try:
            r = subprocess.run(["ps", "-o", "ppid=", "-p", str(pid)],
                               capture_output=True, text=True, timeout=2)
        except (OSError, subprocess.SubprocessError):
            break
        line = (r.stdout or "").strip()
        if not line:
            break
        try:
            ppid = int(line.split()[0])
        except (ValueError, IndexError):
            break
        if ppid == pid or ppid in pids:
            break
        pids.add(ppid)
        pid = ppid
    return pids


def _session_owner_pid(tool_name, src_path):
    """会话属主进程 pid(部分工具在运行时文件里记录);无则 None。
    目前:Qwen 同目录 <sid>.runtime.json 的 pid。"""
    if tool_name == "qwen-code":
        rt = Path(_os_path(Path(src_path).parent / (Path(src_path).stem + ".runtime.json")))
        if rt.is_file():
            try:
                data = json.loads(rt.read_text(encoding="utf-8", errors="ignore"))
                return int(data.get("pid"))
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                return None
    return None


def _owner_pid_current(tool_name, items):
    """多候选里,若恰有一个会话的属主 pid 命中本进程祖先链→即当前会话(精确);
    无 pid 信息 / 0 或 >1 命中→返 None,交由上层其它因子兜底。"""
    owners = [(it, _session_owner_pid(tool_name, it[1])) for it in items]
    if not any(pid for _, pid in owners):
        return None
    anc = _ancestor_pids()
    hits = [it for it, pid in owners if pid and pid in anc]
    return hits[0] if len(hits) == 1 else None


def _my_ttys():
    """本进程及祖先进程的控制终端名(如 ttys032;去 /dev/ 前缀)。
    agent 在某终端(tty)里跑 CLI 并 spawn 本导出脚本时二者共享控制终端,
    故 tty 可把'当前终端'关联到 agent 写在磁盘上的 per-tty 会话记录。ps 不可用返空集。
    Windows 没有控制终端(tty)概念、oh-my-pi 也不会写 per-tty 记录,直接返空集降级:
    调用方(_omp_current)得 None 后自然回落到内容时间戳等其余因子。"""
    if IS_WINDOWS:
        return set()
    import subprocess
    names = set()
    for pid in _ancestor_pids():
        try:
            r = subprocess.run(["ps", "-o", "tty=", "-p", str(pid)],
                               capture_output=True, text=True, timeout=2)
        except (OSError, subprocess.SubprocessError):
            break
        t = (r.stdout or "").strip()
        if t and t not in ("?", "??"):
            names.add(t.rsplit("/", 1)[-1])
    return names


def _omp_tty_session(cwd):
    """oh-my-pi 会话文件不含属主 pid,改用'本终端 tty'关联当前会话:
    ~/.omp/agent/terminal-sessions/<tty> 内容 第1行=cwd 第2行=当前会话 jsonl 路径。
    仅当记录的 cwd 与目标 cwd 一致时返回该会话路径(精确);否则 None。
    与 skill 安装位置无关,是共享安装位置下识别 oh-my-pi 的关键信号。"""
    root = HOME / ".omp" / "agent" / "terminal-sessions"
    if not root.is_dir():
        return None
    for tty in _my_ttys():
        f = Path(_os_path(root / tty))
        try:
            if not f.is_file():
                continue
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        if len(lines) >= 2 and _same_path(lines[0].strip(), cwd):
            return _norm_path(lines[1].strip())
    return None


def _omp_current(items, cwd):
    """omp 多候选里,本终端 tty 记录指向的会话即当前会话(精确);无匹配返 None。"""
    sess = _omp_tty_session(cwd)
    if not sess:
        return None
    for it in items:
        if _same_path(str(it[1]), sess):
            return it
    return None


def _most_active_tool(matches, cwd):
    """多个工具争同一 cwd 时按精确信号择一:环境变量精确命中 > 属主 pid 命中祖先链
    > oh-my-pi 的 tty 会话记录命中 > 按 PRIORITY 顺序取首个(即 qoder-cli 最优先)。
    matches=[(tool_name, items)],已按 PRIORITY/bias 排序。
    兜底不看时间戳:同一 cwd 下 claude-code 会话可能碰巧更新而误赢 qoder-cli。"""
    for name, items in matches:
        sid = _env_session_id(name)
        if sid and any(it[0] == sid for it in items):
            return name, items
    for name, items in matches:
        if _owner_pid_current(name, items) is not None:
            return name, items
    for name, items in matches:
        if name == "oh-my-pi" and _omp_current(items, cwd) is not None:
            return name, items
    # 无精确信号 → 按 PRIORITY 顺序取首个(qoder-cli 永远最优先)
    return matches[0]


def detect_tool(cwd):
    """自动定位当前会话所属工具。
    - 识别到当前客户端(_client_bias 非空)→ 仅在其工具内找,不回退别家(避免误导出同目录别家旧会话);
      同源多工具(如 qoder / qoder-cli 共用 ~/.qoder)争同一 cwd 时,按'当前活跃'择一而非盲目按序。
    - 识别不到 → 该 cwd 只有 1 个工具有会话则直接用;2+ 个同样按'当前活跃'择一。
    '当前活跃'见 _most_active_tool(环境变量 / 属主 pid / 内容时间戳多因子)。"""
    def _collect(names):
        out = []
        for name in names:
            avail, list_fn, _ = PARSERS[name]
            try:
                if avail():
                    items = list_fn(cwd)
                    if items:
                        out.append((name, items))
            except (sqlite3.Error, OSError):
                # 单个工具探测出错(如 db 不可读)不能拖垮整体识别,跳过该工具
                continue
        return out

    bias = _client_bias()
    matches = _collect(bias if bias else PRIORITY)
    if not matches:
        return None, []
    return matches[0] if len(matches) == 1 else _most_active_tool(matches, cwd)


def _choose_session(tool_name, items, cwd):
    """同工具多会话里选当前会话(多因子;仅多候选时才计算,单候选直接返回):
    1) 客户端注入的当前会话 id 环境变量(精确,见 _SESSION_ID_ENV);
    2) 运行时属主 pid 命中本进程祖先链(精确,仅 Qwen 有此信息);
    3) oh-my-pi 的本终端 tty 会话记录(精确,omp 无属主 pid,见 _omp_tty_session);
    4) 内容时间戳最新者(免疫文件 mtime 扰动),以 (mtime, sid) 做确定性兜底。
    仍选不准的极端并发场景,应由调用方用 --session 精确指定。"""
    if len(items) == 1:
        return items[0]
    env_sid = _env_session_id(tool_name)
    if env_sid:
        for it in items:
            if it[0] == env_sid:
                return it
    owned = _owner_pid_current(tool_name, items)
    if owned is not None:
        return owned
    if tool_name == "qoder":
        active = _qoder_active_session(cwd)
        if active:
            for it in items:
                if it[0] == active:
                    return it
    if tool_name == "oh-my-pi":
        omp = _omp_current(items, cwd)
        if omp is not None:
            return omp
    return max(items, key=lambda it: (_session_recency(it[1], it[2]), it[2], it[0]))


# jsonl 类工具的存储根 + 会话文件 glob(用于 --session 跨项目定位)
_SESSION_GLOBS = [
    ("qoder-cli",   HOME / ".qoder" / "projects",    "*.jsonl"),
    ("qoder",       HOME / ".qoder" / "projects",    "transcript/*.jsonl"),
    ("qoderwork",   HOME / ".qoderwork" / "projects", "*.jsonl"),
    ("qwen-code",   HOME / ".qwen" / "projects",     "chats/*.jsonl"),
    ("claude-code", HOME / ".claude" / "projects",   "*.jsonl"),
]


def _find_session_by_location(sid):
    """跨所有工具、所有项目,按 session id 定位文件物理位置 → 确定所属工具。
    位置即事实:文件在谁的目录结构里就是谁的产品,不依赖优先级/cwd/环境变量。
    找到返回 (tool_name, (sid, path, mtime));找不到返 (None, None)。"""
    # 1) jsonl 类: 按文件名匹配(sid 即 stem 或 stem 尾部)
    for tool, root, glob in _SESSION_GLOBS:
        if not root.is_dir():
            continue
        for f in Path(_os_path(root)).glob("*/" + glob):
            if f.stem == sid or f.stem.endswith("_" + sid):
                return tool, (sid, f, f.stat().st_mtime)
    # 2) oh-my-pi: <ts>_<sid>.jsonl
    omp_root = HOME / ".omp" / "agent" / "sessions"
    if omp_root.is_dir():
        for f in Path(_os_path(omp_root)).glob("*/*.jsonl"):
            if f.stem.endswith("_" + sid):
                return "oh-my-pi", (sid, f, f.stat().st_mtime)
    # 2b) Kimi Code: 会话目录名 session_<uuid>(用户可能只给 uuid 后缀)
    kimi_root = _kimi_root() / "sessions"
    if kimi_root.is_dir():
        for sd in Path(_os_path(kimi_root)).glob("*/session_*"):
            if not (sd.name == sid or sd.name.endswith("_" + sid)):
                continue
            wire = sd / "agents" / "main" / "wire.jsonl"
            if not wire.is_file():
                continue
            st = _kimi_state(sd)
            mt = _safe_float(st.get("updatedAt")) / 1000 if st else 0.0
            return "kimi-code", (sd.name, wire, mt or wire.stat().st_mtime)
    # 3) Codex: DB 查 id → rollout_path
    if CODEX_DB.exists():
        try:
            conn = sqlite3.connect(_sqlite_ro_uri(CODEX_DB), uri=True)
            row = conn.execute(
                "SELECT rollout_path, source FROM threads WHERE id = ?", (sid,)
            ).fetchone()
            conn.close()
            p = Path(_os_path(row[0])) if row and row[0] else None
            if p and p.is_file():
                tool = "codex-app" if row[1] == "vscode" else "codex-cli"
                return tool, (sid, p, p.stat().st_mtime)
        except sqlite3.Error:
            pass
    # 4) OpenCode: DB 查 id → 确认存在
    if OPENCODE_DB.exists():
        try:
            conn = _opencode_conn()
            row = conn.execute(
                "SELECT id FROM session WHERE id = ?", (sid,)
            ).fetchone()
            conn.close()
            if row:
                return "opencode", (sid, OPENCODE_DB, 0.0)
        except sqlite3.Error:
            pass
    return None, None


def find_session_in_cwd(cwd, sid):
    """按 session id 查找会话,通过文件物理位置确定所属工具(位置即事实,不靠优先级猜)。
    1) 先在 cwd 范围内全量搜索(所有工具平等,不按 bias 排序);
    2) cwd 内未命中 → 扩大到全量项目按文件位置定位(跨 cwd)。
    命中返回 (tool_name, item);未命中返 (None, None)。"""
    # 1) cwd 内: 全量工具平等搜索
    for name in PARSERS:
        avail, list_fn, _ = PARSERS[name]
        try:
            if not avail():
                continue
            for item in list_fn(cwd):
                if item[0] == sid:
                    return name, item
        except (sqlite3.Error, OSError):
            continue
    # 2) 扩大: 按文件物理位置定位(忽略 cwd)
    return _find_session_by_location(sid)


def _session_contains_text(src_path, text, max_bytes=512 * 1024):
    """在 session 文件尾部 max_bytes 内搜索 text;命中 True。
    当前对话内容一定在文件末尾(正在被写入),尾部窗口即可。"""
    if not isinstance(src_path, Path):
        return False
    fp = Path(_os_path(src_path))
    if not fp.is_file():
        return False
    try:
        size = fp.stat().st_size
        with open(fp, "rb") as f:
            if size > max_bytes:
                f.seek(size - max_bytes)
            data = f.read()
    except OSError:
        return False
    return text in data.decode("utf-8", errors="ignore")


def _verify_or_relocate(cwd, verify_text, current_tool, current_sid):
    """内容匹配兜底:当前选择未命中 verify_text → 跨工具/跨会话搜索包含该内容的 session。
    找到返回 (tool_name, item);全部未命中返 None。"""
    candidates = []
    for name in PARSERS:
        avail, list_fn, _ = PARSERS[name]
        try:
            if not avail():
                continue
            for item in list_fn(cwd):
                if item[0] == current_sid:
                    continue
                candidates.append((name, item))
        except (sqlite3.Error, OSError):
            continue
    candidates.sort(key=lambda ni: _session_recency(ni[1][1], ni[1][2]), reverse=True)
    for name, item in candidates:
        if _session_contains_text(item[1], verify_text):
            return name, item
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Pack current AI Agent session (jsonl + subagents + tool-results) into a zip in project root"
    )
    parser.add_argument("--project", default=os.getcwd())
    parser.add_argument("--output", default=".session-export")
    parser.add_argument("--session", default=None,
                        help="精确指定 sessionId，仅在当前项目范围内查找")
    parser.add_argument("--tool", default=None, choices=list(PARSERS.keys()),
                        help="显式指定产品，跳过自动识别(当调用方确知自身产品时用)")
    parser.add_argument("--verify", default=None,
                        help="本轮对话中的一段独特文本,用于内容匹配二次确认选中的 session 是否正确")
    args = parser.parse_args()

    cwd = os.path.abspath(args.project)
    out_dir = (Path(args.output) if os.path.isabs(args.output)
               else Path(cwd) / args.output)

    if out_dir.exists() and not out_dir.is_dir():
        print(f"error: --output {out_dir} exists but is not a directory",
              file=sys.stderr)
        sys.exit(5)

    try:
        if args.session is not None:
            if not args.session.strip():
                print("error: --session 不能为空", file=sys.stderr)
                sys.exit(2)
            tool_name, item = find_session_in_cwd(cwd, args.session)
            if not tool_name:
                installed = [n for n in PRIORITY if PARSERS[n][0]()]
                if not installed:
                    print("error: no supported tool installed", file=sys.stderr)
                    sys.exit(4)
                print(f"error: session {args.session} not found in {cwd} (checked {installed})",
                      file=sys.stderr)
                sys.exit(3)
            items = [item]
        elif args.tool is not None:
            # 显式指定产品:跳过自动识别,直接在该产品内取当前(最近活跃)会话。
            avail, list_fn, _ = PARSERS[args.tool]
            if not avail():
                print(f"error: tool {args.tool} not installed", file=sys.stderr)
                sys.exit(4)
            items = list_fn(cwd)
            if not items:
                print(f"error: no {args.tool} session found for {cwd}",
                      file=sys.stderr)
                sys.exit(3)
            tool_name = args.tool
            items = [_choose_session(tool_name, items, cwd)]
        else:
            tool_name, items = detect_tool(cwd)
            if not tool_name:
                installed = [n for n in PRIORITY if PARSERS[n][0]()]
                if not installed:
                    print("error: no supported tool installed", file=sys.stderr)
                    sys.exit(4)
                print(f"error: no session found for {cwd} (checked {installed})",
                      file=sys.stderr)
                sys.exit(3)
            # 同工具多会话里选当前会话(Claude 用会话环境变量精确锁定,否则内容时间戳最新)
            items = [_choose_session(tool_name, items, cwd)]

        # --verify 内容匹配二次确认:模型传入本轮对话独特文本,验证选中的 session 确实包含它
        if args.verify:
            sid, src, _ = items[0]
            if not _session_contains_text(src, args.verify):
                found = _verify_or_relocate(cwd, args.verify, tool_name, sid)
                if found:
                    tool_name, item = found
                    items = [item]
                    print(f"verify: relocated to [{tool_name}] {item[0][:12]}...",
                          file=sys.stderr)
                else:
                    print("verify: warning - text not found in any session, "
                          "proceeding with best match", file=sys.stderr)

        _, _, pack_fn = PARSERS[tool_name]
        total_entries = 0
        for sid, src, _ in items:
            out_path, n = pack_fn(src, sid, out_dir)
            print(str(out_path))
            total_entries += n

        print(f"exported {len(items)} session(s) [{tool_name}], "
              f"{total_entries} file(s)/record(s) inside zip", file=sys.stderr)
        sys.exit(0)

    except sqlite3.Error as e:
        print(f"error: sqlite: {e}", file=sys.stderr)
        sys.exit(5)
    except OSError as e:
        print(f"error: io: {e}", file=sys.stderr)
        sys.exit(5)
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(5)


if __name__ == "__main__":
    main()
