# Obsidian + NAS + Claude Code 전체 셋업 체크리스트

> Synology NAS 기반 부부 공용 Obsidian 환경 구축

## Overview

| 구성 | 설명 |
|------|------|
| **Personal Vault (woogi)** | 개발 노트, Daily, 기획 문서 |
| **Personal Vault (wife)** | PRD, 화면설계서, 업무, 일기 |
| **Family Vault** | 공유 Todo, 가계부, 여행 계획 |

---

## Phase 1: NAS 기본 설정

- [ ] **1.1 Docker 설치 확인**
  - Synology DSM > 패키지센터 > Docker/Container Manager 설치

- [ ] **1.2 Vault 폴더 생성**
  ```
  /volume1/obsidian/
  ├── woogi/
  ├── wife/
  └── family/
  ```

- [ ] **1.3 NAS 사용자 권한 설정**
  - woogi 계정: woogi/, family/ 접근
  - wife 계정: wife/, family/ 접근

---

## Phase 2: CouchDB 설치 (LiveSync용)

- [ ] **2.1 CouchDB Docker 컨테이너 생성**

  `docker-compose.yml`:
  ```yaml
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

- [ ] **2.2 CouchDB 초기 설정**
  - admin 계정 생성
  - CORS 설정 활성화

- [ ] **2.3 데이터베이스 생성**
  ```bash
  # 각 Vault용 데이터베이스 생성
  curl -X PUT http://admin:<PASSWORD>@localhost:5984/obsidian-woogi
  curl -X PUT http://admin:<PASSWORD>@localhost:5984/obsidian-wife
  curl -X PUT http://admin:<PASSWORD>@localhost:5984/obsidian-family
  ```

- [ ] **2.4 데이터베이스 권한 설정**
  - 각 DB별 접근 권한 설정

---

## Phase 3: HTTPS 리버스 프록시 (모바일용)

- [ ] **3.1 도메인/DDNS 설정**
  - Synology DDNS 또는 자체 도메인

- [ ] **3.2 SSL 인증서 발급**
  - Let's Encrypt 자동 갱신 설정

- [ ] **3.3 리버스 프록시 설정**
  - DSM > 제어판 > 응용 프로그램 포털 > 역방향 프록시
  - Source: `https://vault.your-domain.com:6984`
  - Destination: `http://localhost:5984`

- [ ] **3.4 방화벽 포트 개방**
  - 포트 6984 (HTTPS CouchDB)

---

## Phase 4: PC Obsidian 설정 (woogi)

- [ ] **4.1 Obsidian 설치**
  - https://obsidian.md

- [ ] **4.2 Personal Vault 생성**
  - 로컬 폴더 생성 후 LiveSync로 동기화

- [ ] **4.3 Family Vault 생성**
  - 별도 Vault로 열기

- [ ] **4.4 필수 플러그인 설치**
  - [ ] Obsidian LiveSync
  - [ ] Dataview
  - [ ] Templater
  - [ ] Calendar
  - [ ] Periodic Notes
  - [ ] obsidian-claude-code-mcp

- [ ] **4.5 LiveSync 설정**
  - Personal Vault → `obsidian-woogi` DB 연결
  - Family Vault → `obsidian-family` DB 연결

- [ ] **4.6 MCP 플러그인 설정**
  - Personal Vault: Port 22360
  - Family Vault: Port 22361

- [ ] **4.7 폴더 구조 생성**
  - 개발자용 구조 적용 (참고: `obsidian-vault-architect` 스킬)

- [ ] **4.8 템플릿 설정**
  - Templater 템플릿 폴더 지정: `90-Meta/Templates/`
  - 기본 템플릿 복사

---

## Phase 5: PC Obsidian 설정 (wife)

- [ ] **5.1 Obsidian 설치**

- [ ] **5.2 Personal Vault 생성**

- [ ] **5.3 Family Vault 생성**

- [ ] **5.4 필수 플러그인 설치**
  - (woogi와 동일)

- [ ] **5.5 LiveSync 설정**
  - Personal Vault → `obsidian-wife` DB 연결
  - Family Vault → `obsidian-family` DB 연결

- [ ] **5.6 MCP 플러그인 설정**
  - Personal Vault: Port 22360
  - Family Vault: Port 22361

- [ ] **5.7 폴더 구조 생성**
  - 기획자용 구조 적용 (참고: `obsidian-vault-architect` 스킬)

- [ ] **5.8 템플릿 설정**
  - PRD, 화면설계서, User Story, Use Case 템플릿

---

## Phase 6: 모바일 설정

- [ ] **6.1 Obsidian 모바일 앱 설치**
  - iOS App Store / Android Play Store

- [ ] **6.2 LiveSync 플러그인 설치**
  - Community Plugins에서 설치

- [ ] **6.3 HTTPS 연결 설정**
  - URI: `https://vault.your-domain.com:6984`
  - 각자 DB 연결

- [ ] **6.4 동기화 테스트**
  - PC에서 작성 → 모바일에서 확인
  - 모바일에서 작성 → PC에서 확인

---

## Phase 7: Claude Code 연동

- [ ] **7.1 `.mcp.json` 설정 추가**
  ```json
  {
    "mcpServers": {
      "obsidian-personal": {
        "command": "npx",
        "args": ["mcp-remote", "http://localhost:22360/sse"],
        "$comment": "개인 Obsidian Vault"
      },
      "obsidian-family": {
        "command": "npx",
        "args": ["mcp-remote", "http://localhost:22361/sse"],
        "$comment": "공유 Obsidian Vault"
      }
    }
  }
  ```

- [ ] **7.2 권한 설정 (`.claude/settings.json`)**
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

- [ ] **7.3 연동 테스트**
  - "내 Obsidian에서 오늘 Daily 노트 만들어줘"
  - "Family Vault에 이번 주 할일 추가해줘"

---

## Phase 8: 검증 & 마무리

- [ ] **8.1 동기화 테스트**
  - [ ] woogi PC ↔ NAS (CouchDB)
  - [ ] wife PC ↔ NAS (CouchDB)
  - [ ] woogi Mobile ↔ NAS
  - [ ] wife Mobile ↔ NAS
  - [ ] Family Vault 공유 확인 (동시 편집 주의)

- [ ] **8.2 백업 설정**
  - Synology Hyper Backup 스케줄 설정
  - 매일 자동 백업

- [ ] **8.3 문서화**
  - 설정 정보 기록 (비밀번호는 별도 보관)
  - 트러블슈팅 노트 작성

---

## 포트 정리

| 서비스 | 포트 | 용도 |
|--------|------|------|
| CouchDB (내부) | 5984 | 내부 동기화 |
| CouchDB (HTTPS) | 6984 | 외부/모바일 동기화 |
| MCP Personal | 22360 | Claude Code 연결 |
| MCP Family | 22361 | Claude Code 연결 |

---

## 관련 문서

- [Obsidian MCP 설정 가이드](./obsidian-mcp-setup.md)
- [obsidian-core 스킬](./.claude/skills/obsidian-core/SKILL.md)
- [obsidian-vault-architect 스킬](./.claude/skills/obsidian-vault-architect/SKILL.md)

---

## 참고 자료

- [obsidian-claude-code-mcp (GitHub)](https://github.com/iansinnott/obsidian-claude-code-mcp)
- [Obsidian LiveSync (GitHub)](https://github.com/vrtmrz/obsidian-livesync)
- [CouchDB on Synology (Gist)](https://gist.github.com/gabeosx/93b9b099dec830706bab3ee2513eba8a)

---

**Created**: 2026-01-30
**Version**: 1.0.0
