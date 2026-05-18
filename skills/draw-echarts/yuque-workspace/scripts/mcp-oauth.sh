#!/usr/bin/env bash
# ============================================================
#  语雀 MCP · Shell OAuth 客户端
#  纯 curl 实现 OAuth2.0 + PKCE + MCP Streamable HTTP
#  Token 统一存储到 credentials.json 的 mcp_tokens 字段
# ============================================================
set -euo pipefail

# ---------- 配置 ----------
MCP_BASE="https://mcp.alibaba-inc.com"
MCP_ENDPOINT="${MCP_BASE}/yuque/mcp"
CALLBACK_PORT=9876
CALLBACK_URI="http://127.0.0.1:${CALLBACK_PORT}/callback"

# ---------- 凭证文件路径 (悟空平台用 workspace，其他用 home) ----------
if [[ "$(pwd)" == *"/.real/"* ]]; then
  CRED_DIR="$(pwd)/.yoho-yuque"
else
  CRED_DIR="${HOME}/.yoho-yuque"
fi
CREDENTIALS="${CRED_DIR}/credentials.json"
SESSION_FILE="${CRED_DIR}/mcp-session"

# ---------- 颜色 ----------
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
log()  { echo -e "${GREEN}[✓]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
info() { echo -e "${CYAN}[→]${NC} $*"; }

# ============================================================
#  凭证读写 — 统一操作 credentials.json
# ============================================================
ensure_cred_file() {
  if [[ ! -f "$CREDENTIALS" ]] || [[ ! -s "$CREDENTIALS" ]] || ! CRED_PATH="$CREDENTIALS" python3 -c "import json,os; json.load(open(os.environ['CRED_PATH']))" 2>/dev/null; then
    info "初始化凭证文件: ${CREDENTIALS}"
    mkdir -p "$(dirname "$CREDENTIALS")"
    CRED_PATH="$CREDENTIALS" python3 -c "
import json, os
p = os.environ['CRED_PATH']
json.dump({'api_base':'https://yuque-api.antfin-inc.com','tokens':{},'mcp_tokens':{},'default_group':''}, open(p,'w'), indent=2)
"
    chmod 600 "$CREDENTIALS"
  fi
}

read_mcp_token() {
  ensure_cred_file
  CRED_PATH="$CREDENTIALS" python3 -c "
import json, os, sys
cred = json.load(open(os.environ['CRED_PATH']))
at = cred.get('mcp_tokens', {}).get('access_token', '')
if not at:
    sys.exit(1)
print(at)
" 2>/dev/null
}

save_mcp_tokens() {
  local oauth_resp="$1"
  ensure_cred_file
  CRED_PATH="$CREDENTIALS" CLIENT_ID_VAL="${CLIENT_ID:-}" CLIENT_SECRET_VAL="${CLIENT_SECRET:-}" \
    python3 -c "
import json, time, os, sys
resp = json.loads(sys.stdin.read())
p = os.environ['CRED_PATH']
cred = json.load(open(p))
expires_in = resp.get('expires_in', 3600)
cred['mcp_tokens'] = {
    'access_token': resp['access_token'],
    'refresh_token': resp.get('refresh_token', ''),
    'expires_at': int(time.time()) + expires_in,
    'client_id': os.environ['CLIENT_ID_VAL'],
    'client_secret': os.environ['CLIENT_SECRET_VAL']
}
json.dump(cred, open(p, 'w'), indent=2, ensure_ascii=False)
print(resp['access_token'])
" <<< "$oauth_resp"
  chmod 600 "$CREDENTIALS"
  log "MCP token 已保存到 ${CREDENTIALS}" >&2
}

load_mcp_client_info() {
  ensure_cred_file
  eval "$(CRED_PATH="$CREDENTIALS" python3 -c "
import json, os
cred = json.load(open(os.environ['CRED_PATH']))
mt = cred.get('mcp_tokens', {})
print(f'CLIENT_ID={repr(mt.get(\"client_id\", \"\"))}')
print(f'CLIENT_SECRET={repr(mt.get(\"client_secret\", \"\"))}')
print(f'REFRESH_TOKEN={repr(mt.get(\"refresh_token\", \"\"))}')
")"
}

# ============================================================
#  动态客户端注册
# ============================================================
register_client() {
  info "动态注册 OAuth 客户端..."
  local resp
  resp=$(curl -sf -X POST "${MCP_BASE}/oauth/register" \
    -H "Content-Type: application/json" \
    -d '{
      "client_name":"yuque-mcp-cli",
      "redirect_uris":["'"${CALLBACK_URI}"'"],
      "grant_types":["authorization_code","refresh_token"],
      "response_types":["code"],
      "token_endpoint_auth_method":"none"
    }')
  eval "$(echo "$resp" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'CLIENT_ID={d[\"client_id\"]!r}')
print(f'CLIENT_SECRET={d[\"client_secret\"]!r}')
")"
  log "client_id: ${CLIENT_ID}"
}

# ============================================================
#  PKCE 生成
# ============================================================
generate_pkce() {
  eval "$(python3 -c "
import secrets,hashlib,base64
v=secrets.token_urlsafe(32)
c=base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).rstrip(b'=').decode()
print(f'CODE_VERIFIER={v!r}')
print(f'CODE_CHALLENGE={c!r}')
")"
}

# ============================================================
#  本地回调服务器 (单次)
# ============================================================
start_callback_server() {
  AUTH_CODE_FILE=$(mktemp /tmp/.mcp-auth-code.XXXXXX)
  chmod 600 "$AUTH_CODE_FILE"
  info "启动回调服务器 (port ${CALLBACK_PORT})..."
  AUTH_CODE_FILE="$AUTH_CODE_FILE" python3 -c "
import http.server,urllib.parse,threading,os
code_file = os.environ['AUTH_CODE_FILE']
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/callback'):
            qs=urllib.parse.urlparse(self.path).query
            p=dict(urllib.parse.parse_qsl(qs))
            with open(code_file,'w') as f: f.write(p.get('code',''))
            self.send_response(200)
            self.send_header('Content-Type','text/html;charset=utf-8')
            self.end_headers()
            self.wfile.write(b'''<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>\xe8\xaf\xad\xe9\x9b\x80 MCP \xe6\x8e\x88\xe6\x9d\x83</title>
<style>body{font-family:-apple-system,system-ui,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#f9fafb}
.card{text-align:center;padding:32px 48px;border-radius:12px;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.08)}
h1{font-size:18px;font-weight:600;color:#16a34a;margin:0 0 6px}p{font-size:13px;color:#9ca3af;margin:0}</style></head>
<body><div class=\"card\"><h1>\xe2\x9c\x85 \xe6\x8e\x88\xe6\x9d\x83\xe6\x88\x90\xe5\x8a\x9f</h1><p>\xe5\x8f\xaf\xe4\xbb\xa5\xe5\x85\xb3\xe9\x97\xad\xe6\xad\xa4\xe9\xa1\xb5\xe9\x9d\xa2\xe4\xba\x86</p></div></body></html>''')
            threading.Thread(target=self.server.shutdown).start()
        else: self.send_response(404); self.end_headers()
    def log_message(self,*a): pass
s=http.server.HTTPServer(('127.0.0.1',int(os.environ.get('CALLBACK_PORT','9876'))),H)
s.serve_forever()
" &
  CALLBACK_PID=$!
  sleep 0.5
}

# ============================================================
#  浏览器授权
# ============================================================
open_browser() {
  local encoded_uri
  encoded_uri=$(CALLBACK_URI_VAL="$CALLBACK_URI" python3 -c "import urllib.parse,os; print(urllib.parse.quote(os.environ['CALLBACK_URI_VAL']))")
  local encoded_resource
  encoded_resource=$(MCP_ENDPOINT_VAL="$MCP_ENDPOINT" python3 -c "import urllib.parse,os; print(urllib.parse.quote(os.environ['MCP_ENDPOINT_VAL']))")
  local auth_url="${MCP_BASE}/oauth/authorize?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${encoded_uri}&code_challenge=${CODE_CHALLENGE}&code_challenge_method=S256&state=yuque-mcp&resource=${encoded_resource}"

  info "打开浏览器进行授权..."
  open "$auth_url" 2>/dev/null || xdg-open "$auth_url" 2>/dev/null || warn "请手动打开:\n$auth_url"
  info "等待授权回调..."
  wait $CALLBACK_PID 2>/dev/null || true
}

# ============================================================
#  授权码换 Token → 写入 credentials.json
# ============================================================
exchange_token() {
  local code
  code=$(cat "$AUTH_CODE_FILE"); rm -f "$AUTH_CODE_FILE"
  [[ -z "$code" ]] && { echo "未获取到授权码" >&2; exit 1; }

  info "用授权码换取 access_token..."
  local resp
  resp=$(curl -sf -X POST "${MCP_BASE}/oauth/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=authorization_code&code=${code}&redirect_uri=${CALLBACK_URI}&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&code_verifier=${CODE_VERIFIER}")

  ACCESS_TOKEN=$(save_mcp_tokens "$resp")
}

# ============================================================
#  MCP 会话管理
# ============================================================
mcp_session_init() {
  info "MCP 握手 (initialize)..."
  local resp_headers
  resp_headers=$(mktemp /tmp/.mcp-resp-headers.XXXXXX)

  curl -sf -D "$resp_headers" -X POST "$MCP_ENDPOINT" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"yuque-mcp-cli","version":"1.0"}}}' \
    > /dev/null

  SESSION_ID=$(grep -i 'mcp-session-id' "$resp_headers" | awk '{print $2}' | tr -d '\r')
  rm -f "$resp_headers"

  if [[ -z "$SESSION_ID" ]]; then
    warn "未获取到 session-id"
    return 0
  fi

  curl -sf -X POST "$MCP_ENDPOINT" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Mcp-Session-Id: ${SESSION_ID}" \
    -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
    > /dev/null

  echo "$SESSION_ID" > "$SESSION_FILE"
  log "session: ${SESSION_ID}"
}

# ============================================================
#  MCP 调用 (带 session)
# ============================================================
REQUEST_ID=10
mcp_call() {
  local method="$1"; shift
  local params="${1:-{}}"
  REQUEST_ID=$((REQUEST_ID + 1))

  local session_header=""
  if [[ -f "$SESSION_FILE" ]]; then
    session_header="-H Mcp-Session-Id:$(cat "$SESSION_FILE")"
  fi

  curl -sf -X POST "$MCP_ENDPOINT" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    ${session_header} \
    -d "{\"jsonrpc\":\"2.0\",\"id\":${REQUEST_ID},\"method\":\"${method}\",\"params\":${params}}" \
    | python3 -m json.tool
}

# ============================================================
#  刷新 Token → 写入 credentials.json
# ============================================================
refresh_token() {
  load_mcp_client_info
  [[ -z "$REFRESH_TOKEN" ]] && { echo "无 refresh_token" >&2; return 1; }

  info "刷新 access_token..."
  local resp
  resp=$(curl -sf -X POST "${MCP_BASE}/oauth/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=refresh_token&refresh_token=${REFRESH_TOKEN}&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}")

  ACCESS_TOKEN=$(save_mcp_tokens "$resp")
  log "token 已刷新"
}

# ============================================================
#  三步流程: ensure_token → mcp_session_init → mcp_call
# ============================================================

# 第一步: 有 token 就用，没有就 OAuth 拿一个
ensure_token() {
  ACCESS_TOKEN=$(read_mcp_token) && return 0

  # 区分: 文件权限错误 vs 真的没 token
  if [[ ! -r "$CREDENTIALS" ]] && [[ -e "$CREDENTIALS" ]]; then
    echo "凭证文件无读取权限: ${CREDENTIALS}" >&2; exit 1
  fi

  info "无 MCP token，发起 OAuth 授权..."
  register_client
  generate_pkce
  start_callback_server
  open_browser
  exchange_token
}

# 第二步: 建立 MCP 会话 (mcp_session_init 已在上方定义)

# 第三步: 发起 MCP 请求 (mcp_call 已在上方定义)

# 串联三步
mcp_ready() {
  ensure_token
  mcp_session_init
}

# ============================================================
#  主流程
# ============================================================
main() {
  cat <<'BANNER'

  ╔══════════════════════════════════╗
  ║  语雀 MCP · Shell OAuth 客户端   ║
  ╚══════════════════════════════════╝

BANNER
  mcp_ready
  log "就绪"
}

# ============================================================
#  入口
# ============================================================
show_help() {
  cat <<EOF
用: $0 <command> [args]

命令:
  auth                       OAuth 授权 (首次使用)
  session                    建立 MCP 会话 (已有 token 时)
  tools                      列出可用工具
  call <method> [params]     调用 MCP 方法
  whoami                     查看当前语雀用户
  doc <slug>                 获取文档 (如 group/book/doc)
  toc <slug>                 获取知识库目录 (如 group/book)
  refresh                    刷新 MCP OAuth token

示例:
  $0 auth
  $0 whoami
  $0 doc aone/platform/overview
  $0 toc aone/platform
  $0 call tools/list '{}'
EOF
}

case "${1:-help}" in
  auth)
    main ;;
  session)
    mcp_ready ;;
  tools)
    mcp_ready; mcp_call "tools/list" '{}' ;;
  call)
    mcp_ready; mcp_call "$2" "${3:-{}}" ;;
  whoami)
    mcp_ready
    mcp_call "tools/call" '{"name":"yuque_whoami","arguments":{}}' ;;
  doc)
    mcp_ready
    mcp_call "tools/call" "{\"name\":\"yuque_get_doc_detail\",\"arguments\":{\"url_or_slug\":\"${2:?需要 slug}\"}}" ;;
  toc)
    mcp_ready
    mcp_call "tools/call" "{\"name\":\"yuque_get_repo_toc\",\"arguments\":{\"url_or_slug\":\"${2:?需要 slug}\"}}" ;;
  refresh)
    refresh_token ;;
  help|*)
    show_help ;;
esac
