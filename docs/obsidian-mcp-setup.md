# Obsidian + Claude Code MCP 설정 가이드

> Synology NAS 기반 하이브리드 Vault 구성 (개인 2개 + 공유 1개)

## 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────┐
│                        Synology NAS                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Docker: CouchDB (LiveSync)                               │   │
│  │  ├── db: obsidian-woogi    (개인)                         │   │
│  │  ├── db: obsidian-wife     (개인)                         │   │
│  │  └── db: obsidian-family   (공유)                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Vault Storage: /volume1/obsidian/                        │   │
│  │  ├── woogi/    (백업)                                     │   │
│  │  ├── wife/     (백업)                                     │   │
│  │  └── family/   (공유)                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Reverse Proxy: https://vault.your-domain.com:6984        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
              │ LiveSync              │ LiveSync
              ▼                       ▼
┌─────────────────────┐      ┌─────────────────────┐
│  woogi PC           │      │  wife PC            │
│  ├── Obsidian       │      │  ├── Obsidian       │
│  │   ├── 개인 Vault │      │  │   ├── 개인 Vault │
│  │   └── 공유 Vault │      │  │   └── 공유 Vault │
│  └── Claude Code    │      │  └── Claude Code    │
└─────────────────────┘      └─────────────────────┘
```

---

## 1. 포트 할당

| 서비스 | 포트 | 용도 |
|--------|------|------|
| CouchDB | 5984 | 내부 LiveSync |
| CouchDB HTTPS | 6984 | 모바일/외부 LiveSync |
| MCP 개인 Vault | 22360 | Claude Code 연결 |
| MCP 공유 Vault | 22361 | Claude Code 연결 |

---

## 2. NAS 설정 (사전 준비)

### 2.1 CouchDB Docker 설치

```yaml
# docker-compose.yml
version: "3"
services:
  couchdb:
    image: couchdb:latest
    container_name: obsidian-couchdb
    environment:
      - COUCHDB_USER=admin
      - COUCHDB_PASSWORD=<SECURE_PASSWORD>
    volumes:
      - /volume1/docker/couchdb/data:/opt/couchdb/data
      - /volume1/docker/couchdb/local.ini:/opt/couchdb/etc/local.d/local.ini
    ports:
      - "5984:5984"
    restart: unless-stopped
```

### 2.2 CouchDB 데이터베이스 생성

```bash
# 각 Vault용 데이터베이스 생성
curl -X PUT http://admin:<PASSWORD>@localhost:5984/obsidian-woogi
curl -X PUT http://admin:<PASSWORD>@localhost:5984/obsidian-wife
curl -X PUT http://admin:<PASSWORD>@localhost:5984/obsidian-family
```

### 2.3 리버스 프록시 (모바일용)

Synology DSM > Application Portal에서 HTTPS 리버스 프록시 설정:
- Source: `https://vault.your-domain.com:6984`
- Destination: `http://localhost:5984`

---

## 3. PC Obsidian 설정

### 3.1 플러그인 설치

Community Plugins에서 설치:
1. **Obsidian LiveSync** - 동기화용
2. **obsidian-claude-code-mcp** - Claude Code 연동용

### 3.2 LiveSync 설정

Settings > Obsidian LiveSync > Setup:
- URI: `http://<NAS_IP>:5984` (내부) 또는 `https://vault.your-domain.com:6984` (외부)
- Username: `admin`
- Password: `<CouchDB 비밀번호>`
- Database: `obsidian-woogi` (본인 개인) 또는 `obsidian-family` (공유)

### 3.3 MCP 플러그인 설정

Settings > obsidian-claude-code-mcp:

**개인 Vault:**
- Port: `22360` (기본값)
- Enable WebSocket: ✅
- Enable SSE: ✅

**공유 Vault (별도 창에서 열 때):**
- Port: `22361` (충돌 방지)
- Enable WebSocket: ✅
- Enable SSE: ✅

---

## 4. Claude Code MCP 설정

### 4.1 프로젝트 레벨 설정 (`.mcp.json`)

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "obsidian-personal": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:22360/sse"],
      "description": "개인 Obsidian Vault MCP 연결"
    },
    "obsidian-family": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:22361/sse"],
      "description": "공유 Obsidian Vault MCP 연결"
    }
  }
}
```

### 4.2 사용자 레벨 설정 (`~/.claude/settings.json`)

전역 설정이 필요한 경우:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:22360/sse"]
    }
  }
}
```

### 4.3 권한 설정 (`.claude/settings.json`)

MCP 도구 사용 허용:

```json
{
  "permissions": {
    "allow": [
      "mcp__obsidian-personal__*",
      "mcp__obsidian-family__*"
    ]
  }
}
```

---

## 5. 사용 가능한 MCP 도구

obsidian-claude-code-mcp 플러그인 설치 후 사용 가능:

| 도구 | 설명 |
|------|------|
| `list_files` | Vault 내 파일 목록 조회 |
| `read_file` | 노트 내용 읽기 |
| `write_file` | 노트 생성/수정 |
| `search` | Vault 내 검색 |
| `get_tags` | 태그 목록 조회 |
| `get_backlinks` | 백링크 조회 |

---

## 6. 사용 시나리오

### 6.1 Claude Code에서 개인 노트 검색

```
"내 Obsidian에서 Flutter 관련 노트 찾아줘"
→ obsidian-personal MCP의 search 도구 사용
```

### 6.2 공유 Vault에 가계부 작성

```
"이번 달 가계부 정리해서 공유 노트에 저장해줘"
→ obsidian-family MCP의 write_file 도구 사용
```

### 6.3 개발 노트 자동 정리

```
"오늘 작업한 내용을 개발일지로 정리해서 내 Obsidian에 저장해줘"
→ obsidian-personal MCP의 write_file 도구 사용
```

---

## 7. 문제 해결

### 7.1 MCP 연결 실패

```bash
# Obsidian 플러그인 상태 확인
# Settings > obsidian-claude-code-mcp > Status

# 포트 충돌 확인
lsof -i :22360
lsof -i :22361
```

### 7.2 LiveSync 동기화 안됨

1. CouchDB 컨테이너 상태 확인
2. 네트워크 연결 확인
3. 데이터베이스 권한 확인

### 7.3 모바일에서 연결 안됨

1. HTTPS 리버스 프록시 설정 확인
2. 방화벽 포트 열림 확인 (6984)
3. SSL 인증서 유효성 확인

---

## 8. 보안 권장사항

1. **CouchDB 비밀번호**: 강력한 비밀번호 사용
2. **HTTPS 필수**: 외부 접속 시 반드시 HTTPS 사용
3. **방화벽**: 필요한 포트만 개방
4. **VPN 권장**: 외부에서 접속 시 Synology VPN 사용 권장

---

## 9. 참고 자료

- [obsidian-claude-code-mcp (GitHub)](https://github.com/iansinnott/obsidian-claude-code-mcp)
- [Obsidian LiveSync (GitHub)](https://github.com/vrtmrz/obsidian-livesync)
- [CouchDB on Synology (Gist)](https://gist.github.com/gabeosx/93b9b099dec830706bab3ee2513eba8a)

---

**Last Updated**: 2026-01-30
**Version**: 1.0.0
