# Clinic Consult 실행 가이드

외국인 환자 피부과 예약 대행 시스템 운영 매뉴얼

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [설치 및 환경설정](#2-설치-및-환경설정)
3. [실행 방법](#3-실행-방법)
4. [웹 대시보드 사용법](#4-웹-대시보드-사용법)
5. [예약 상태 흐름](#5-예약-상태-흐름)
6. [보안 참고사항](#6-보안-참고사항)
7. [트러블슈팅](#7-트러블슈팅)

---

## 1. 프로젝트 개요

### 시스템 목적

Clinic Consult는 일본인 등 외국인 환자의 한국 피부과 시술 예약을 자동으로 대행하는 봇 시스템이다. 운영자가 웹 대시보드에서 예약 요청을 생성하면, 시스템이 카카오톡/LINE 채널을 통해 해당 클리닉에 자동으로 연락하고 LLM(대규모 언어 모델)을 활용하여 한국어로 예약 협상을 진행한다.

### 주요 기능

- **카카오톡 자동 예약**: Android 에뮬레이터(LDPlayer)와 uiautomator2를 통해 카카오톡 채널 채팅을 자동화한다.
- **LLM 기반 대화 협상**: Claude(Anthropic), GPT-4o(OpenAI) 등 복수의 LLM 프로바이더를 지원하며, 폴백(fallback) 체인으로 안정성을 확보한다.
- **웹 대시보드**: FastAPI 기반 웹 인터페이스에서 예약 생성, 모니터링, 수동 개입, CSV 내보내기를 수행한다.
- **클리닉 자동 검색**: hospitals.db에서 클리닉 이름으로 자동완성 검색하고 카카오톡 채널 URL을 자동 연결한다.
- **상태 머신 관리**: 예약 생성부터 확정/거절까지 10단계 상태를 체계적으로 관리한다.

### 기술 스택

| 구성 요소 | 기술 |
|-----------|------|
| 런타임 | Python 3.13+ |
| 패키지 관리 | uv |
| 웹 프레임워크 | FastAPI + Uvicorn |
| 데이터베이스 | SQLite (WAL 모드) |
| LLM 프로바이더 | Anthropic Claude, OpenAI GPT-4o |
| 안드로이드 자동화 | uiautomator2 |
| 설정 관리 | pydantic-settings + YAML |
| 템플릿 엔진 | Jinja2 |

---

## 2. 설치 및 환경설정

### 사전 요구사항

- Python 3.13 이상
- uv 패키지 매니저 (pip install uv 또는 brew install uv)
- 카카오톡 자동화를 사용하는 경우: LDPlayer Android 에뮬레이터 + ADB

### 프로젝트 설치

프로젝트 디렉토리로 이동한 후 uv를 사용하여 의존성을 설치한다.

```bash
cd tools/clinic-consult
uv sync
```

개발 의존성(pytest, ruff, mypy)을 포함하여 설치하려면 다음과 같이 실행한다.

```bash
uv sync --dev
```

### 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 환경변수를 설정한다.

```dotenv
# 웹 대시보드 인증 (필수)
RESERVE_USER=admin
RESERVE_PASS=안전한_비밀번호를_설정하세요

# LLM API 키 (최소 하나 이상 필수)
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
```

**환경변수 설명:**

| 변수명 | 필수 여부 | 설명 |
|--------|----------|------|
| `RESERVE_USER` | 선택 | 웹 대시보드 로그인 사용자명. 기본값: `admin` |
| `RESERVE_PASS` | **필수** | 웹 대시보드 로그인 비밀번호. 미설정 시 로그인 불가 |
| `ANTHROPIC_API_KEY` | 조건부 | Claude LLM 사용 시 필수 |
| `OPENAI_API_KEY` | 조건부 | OpenAI GPT-4o 사용 시 필수 |

LLM API 키는 최소 하나 이상 설정해야 한다. 기본 프로바이더는 Claude이며, `config.yaml`의 `llm.default_provider` 항목으로 변경할 수 있다.

### config.yaml 설정 가이드

`config.yaml` 파일은 비밀이 아닌 운영 설정값을 관리한다. 설정 우선순위는 다음과 같다(높은 쪽이 우선).

1. 환경변수
2. `.env` 파일
3. `config.yaml`
4. 코드 내 기본값

주요 설정 항목은 다음과 같다.

**에뮬레이터 설정 (emulator)**

```yaml
emulator:
  ldplayer_path: "C:/LDPlayer/LDPlayer9"  # LDPlayer 설치 경로
  instance_name: "LDPlayer"                # 에뮬레이터 인스턴스 이름
  serial: "127.0.0.1:5555"                 # ADB 연결 시리얼
  kakao_package: "com.kakao.talk"          # 카카오톡 패키지명
```

**LLM 설정 (llm)**

```yaml
llm:
  default_provider: "claude"                    # 기본 LLM: claude, openai, ollama
  claude_model: "claude-sonnet-4-20250514"      # Claude 모델
  openai_model: "gpt-4o"                        # OpenAI 모델
  max_tokens: 500                               # 최대 토큰 수
  temperature: 0.7                              # 생성 온도
```

**예약 설정 (reservation)**

```yaml
reservation:
  hospitals_db: "../../data/clinic-results/hospitals.db"  # 클리닉 DB 경로
  export_dir: "data/exports"                               # CSV 내보내기 디렉토리
  max_turns: 15                                            # 최대 대화 턴 수
  greeting_timeout_hours: 2                                # 인사 후 응답 대기 시간(시)
  negotiation_timeout_hours: 1                             # 협상 중 응답 대기 시간(시)
  followup_after_hours: 4                                  # 팔로업 메시지 발송 대기(시)
  agency_name: "Global Skin Care Concierge"                # 에이전시 이름
```

**스케줄링 설정 (scheduling)**

```yaml
scheduling:
  active_start_hour: 9    # 운영 시작 시각 (KST)
  active_end_hour: 22     # 운영 종료 시각 (KST)
  weekend_enabled: false  # 주말 운영 여부
```

**속도 제한 설정 (rate_limit)**

```yaml
rate_limit:
  max_responses_per_hour: 30    # 시간당 최대 응답 수
  max_responses_per_day: 200    # 일일 최대 응답 수
  min_interval_seconds: 10      # 응답 최소 간격(초)
  cooldown_after_errors: 60     # 오류 후 대기 시간(초)
```

**데이터베이스 설정 (database)**

```yaml
database:
  path: "data/consult.db"  # SQLite DB 파일 경로
```

**웹 설정 (web)**

```yaml
web:
  host: "127.0.0.1"  # 바인드 호스트
  port: 8000          # 바인드 포트
```

---

## 3. 실행 방법

### 웹 대시보드 실행

웹 대시보드를 기본 설정(127.0.0.1:8000)으로 시작한다.

```bash
uv run python -m src.reserve
```

호스트와 포트를 지정하여 시작할 수도 있다.

```bash
uv run python -m src.reserve --host 0.0.0.0 --port 8080
```

시작 후 브라우저에서 `http://127.0.0.1:8000` 으로 접속한다. HTTP Basic Auth 인증 창이 표시되며, 환경변수에 설정한 `RESERVE_USER`와 `RESERVE_PASS` 값을 입력한다.

### 백그라운드 워커 실행

워커 모드는 활성 상태의 예약을 30초 간격으로 폴링하면서 자동으로 처리한다.

```bash
uv run python -m src.reserve --worker
```

카카오톡 실제 전송 없이 워커 로직만 테스트하려면 `--dry-run` 플래그를 추가한다.

```bash
uv run python -m src.reserve --worker --dry-run
```

워커를 중지하려면 `Ctrl+C`를 누른다. SIGINT/SIGTERM 신호를 받으면 현재 처리 사이클을 완료한 후 안전하게 종료한다.

### 단일 예약 처리

특정 예약 건을 지정하여 단독으로 처리한다.

```bash
uv run python -m src.reserve --process REQ-20260220-001
```

실제 카카오톡 전송 없이 예약 정보만 확인하려면 다음과 같이 실행한다.

```bash
uv run python -m src.reserve --process REQ-20260220-001 --dry-run
```

### 테스트 실행

전체 테스트 스위트를 실행한다.

```bash
uv run pytest tests/
```

커버리지 보고서와 함께 실행한다.

```bash
uv run pytest tests/ --cov=src --cov-report=term-missing
```

특정 테스트 파일만 실행한다.

```bash
uv run pytest tests/test_worker.py -v
```

### CLI 옵션 요약

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--host` | 웹 서버 바인드 호스트 | `127.0.0.1` |
| `--port` | 웹 서버 바인드 포트 | `8000` |
| `--worker` | 백그라운드 워커 모드로 실행 | 비활성 |
| `--process REQ-ID` | 특정 예약 건 단독 처리 | - |
| `--dry-run` | 카카오톡 실제 전송 건너뛰기 | 비활성 |

---

## 4. 웹 대시보드 사용법

### 로그인

웹 대시보드는 HTTP Basic Auth로 보호된다. 브라우저 접속 시 인증 팝업이 표시되며, 환경변수 `RESERVE_USER`(기본값: admin)와 `RESERVE_PASS`를 입력한다.

`RESERVE_PASS`가 설정되지 않은 경우 401 Unauthorized 오류가 반환되며 로그인할 수 없다.

### 메인 대시보드 (/)

메인 대시보드에서 확인할 수 있는 정보는 다음과 같다.

- **통계 요약**: 전체 예약 수, 진행 중(active), 확정(confirmed), 거절(declined), 일시 정지(paused) 건수
- **예약 목록**: 최신순으로 정렬된 예약 목록
- **상태 필터**: URL 파라미터 `?status=negotiating`과 같이 특정 상태로 필터링 가능
- **일시 정지 알림**: `paused_for_human` 상태의 건이 있으면 건수를 별도로 표시

### 예약 생성 (/create)

새 예약을 생성하는 절차는 다음과 같다.

1. 메인 대시보드에서 예약 생성 버튼을 클릭한다.
2. **클리닉 이름**: 클리닉 이름을 입력하면 hospitals.db에서 자동완성 검색 결과가 표시된다. 선택하면 카카오톡 채널 URL이 자동으로 연결된다.
3. **시술명**: 예약할 시술 이름을 입력한다 (예: "레이저 토닝", "보톡스").
4. **희망 날짜**: 쉼표로 구분하여 입력한다 (예: "2026-03-01, 2026-03-02").
5. **희망 시간대**: "오전", "오후", "any" 중 선택한다.
6. **환자 정보**: 이름, 국적(기본값: JP), 나이, 성별, 연락처를 입력한다.
7. **메모**: 특이사항이 있으면 추가한다.
8. 제출 버튼을 클릭하면 `REQ-날짜-시분초` 형식의 요청 ID가 자동 생성되고 상세 페이지로 이동한다.

클리닉 자동완성 검색은 `/api/clinics/search?q=검색어` API를 내부적으로 호출하며, 최대 10건의 결과를 반환한다.

### 예약 상세 (/reservations/{id})

예약 상세 페이지에서 확인 및 조작할 수 있는 기능은 다음과 같다.

- **예약 정보**: 클리닉명, 시술명, 환자 정보, 희망 날짜/시간, 현재 상태
- **대화 로그**: 시스템이 보낸 메시지(outgoing)와 클리닉에서 받은 메시지(incoming)의 전체 이력
- **수동 메시지 전송**: `paused_for_human` 상태일 때, 담당자가 직접 메시지를 작성하여 대화를 재개할 수 있다. 메시지 전송 후 상태가 `negotiating`으로 전환된다.
- **예약 완료**: `confirmed` 상태에서 완료 처리 버튼을 클릭하면 `completed`로 전환되고 CSV로 내보내기된다.
- **예약 취소**: 진행 중인 예약을 취소하면 `failed` 상태로 전환되며 "Cancelled by staff" 사유가 기록된다.

### CSV 내보내기 (/export/csv)

모든 예약 데이터를 CSV 파일로 다운로드한다. 메인 대시보드 또는 다음 URL에서 직접 다운로드할 수 있다.

```
GET /export/csv
```

내보내기 파일은 `data/exports/` 디렉토리에도 저장된다. 예약이 `confirmed` 또는 `completed` 상태로 전환될 때 자동으로 개별 내보내기가 수행된다.

### API 엔드포인트

프로그래밍 방식으로 데이터에 접근할 수 있는 REST API도 제공한다.

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/clinics/search?q=검색어` | 클리닉 자동완성 검색 |
| GET | `/api/reservations` | 전체 예약 목록 (JSON) |
| GET | `/api/reservations?status=negotiating` | 상태별 예약 필터 |
| GET | `/api/docs` | FastAPI 자동 생성 Swagger 문서 |

모든 API 엔드포인트는 HTTP Basic Auth 인증이 필요하다.

---

## 5. 예약 상태 흐름

### 상태 목록

| 상태 | 표시명 | 설명 |
|------|--------|------|
| `created` | Created | 예약 요청이 생성됨. 워커가 처리 대기 중 |
| `contacting` | Contacting | 클리닉 카카오톡 채널 URL을 확인하고 채팅 준비 중 |
| `greeting_sent` | Sent | 초기 인사 메시지를 전송함. 클리닉 응답 대기 중 |
| `negotiating` | Negotiating | 클리닉과 대화 진행 중. LLM이 자동 응답 생성 |
| `paused_for_human` | Paused | 사람 개입 필요. 담당자가 직접 대응해야 함 |
| `confirmed` | Confirmed | 예약 확정. 날짜, 시간, 가격 등 세부 정보 확정 |
| `declined` | Declined | 클리닉이 예약을 거절함 |
| `completed` | Completed | 예약이 최종 완료 처리됨 |
| `timed_out` | Timed Out | 클리닉 무응답으로 타임아웃 |
| `failed` | Failed | 처리 중 오류 발생 또는 담당자가 취소 |

### 상태 전이 규칙

아래 다이어그램은 허용된 상태 전이를 나타낸다.

```
created -----> contacting -----> greeting_sent -----> negotiating
  |                |                   |                  |
  |                |                   |                  +---> confirmed ---> completed
  |                |                   |                  |
  |                |                   |                  +---> declined
  |                |                   |                  |
  |                |                   +---> timed_out    +---> paused_for_human
  |                |                   |                           |
  |                |                   +---> paused_for_human      +---> negotiating
  |                |                                               +---> confirmed
  v                v                                               +---> declined
failed          failed                                             +---> failed
```

상태 전이 규칙의 상세 내용은 다음과 같다.

| 현재 상태 | 전이 가능 상태 |
|-----------|---------------|
| `created` | `contacting`, `failed` |
| `contacting` | `greeting_sent`, `failed` |
| `greeting_sent` | `negotiating`, `paused_for_human`, `timed_out`, `failed` |
| `negotiating` | `confirmed`, `declined`, `paused_for_human`, `timed_out`, `failed` |
| `paused_for_human` | `negotiating`, `confirmed`, `declined`, `failed` |
| `confirmed` | `completed`, `failed` |
| `declined` | (종료 상태 - 전이 불가) |
| `completed` | (종료 상태 - 전이 불가) |
| `timed_out` | `contacting`, `failed` |
| `failed` | (종료 상태 - 전이 불가) |

### paused_for_human 전환 조건

시스템이 자동으로 `paused_for_human` 상태로 전환하는 경우는 다음과 같다.

- **최대 턴 수 초과**: 대화가 15턴(기본값)을 초과하면 자동 일시 정지된다. `config.yaml`의 `reservation.max_turns`에서 조정할 수 있다.
- **LLM 응답 파싱 실패**: LLM이 구조화된 JSON 응답을 생성하지 못하면 안전을 위해 사람에게 위임한다.
- **LLM 판단에 의한 위임**: LLM이 대화 내용을 분석하여 사람의 개입이 필요하다고 판단한 경우 (예: 복잡한 가격 협상, 특수 요구사항).

`paused_for_human` 상태에서 재개하려면 웹 대시보드의 예약 상세 페이지에서 수동 메시지를 작성하여 전송한다. 전송 후 상태가 `negotiating`으로 복귀한다.

### 타임아웃 처리

- **인사 후 무응답**: `greeting_sent` 상태에서 `greeting_timeout_hours`(기본값: 2시간) 동안 클리닉 응답이 없으면 팔로업 메시지를 자동 전송한다.
- **최대 팔로업 횟수**: 기본 2회까지 팔로업을 시도한다. 그 이후에도 무응답이면 `timed_out` 상태로 전환한다.
- **타임아웃 후 재시도**: `timed_out` 상태에서 `contacting`으로 재전환하여 다시 시도할 수 있다.

---

## 6. 보안 참고사항

### 인증 보안

- **RESERVE_PASS 필수 설정**: `RESERVE_PASS` 환경변수가 설정되지 않으면 웹 대시보드에 접근할 수 없다. 이는 의도적인 설계로, 비밀번호 없이 운영하는 것을 방지한다.
- **비밀번호 비교**: `secrets.compare_digest()`를 사용하여 타이밍 공격(timing attack)에 안전한 비교를 수행한다.
- **강력한 비밀번호 사용**: 충분히 긴 무작위 문자열을 비밀번호로 사용할 것을 권장한다.

### CSRF 보호

- 모든 POST 요청(예약 생성, 재개, 취소, 완료)에 CSRF 토큰 검증이 자동으로 적용된다.
- CSRF 토큰은 사용자 세션별로 생성되며, `secrets.token_hex(32)`로 64자리 16진수 토큰을 생성한다.
- 토큰이 일치하지 않으면 HTTP 403 Forbidden 응답을 반환한다.

### API 키 관리

- API 키는 반드시 환경변수 또는 `.env` 파일에만 저장한다. `config.yaml`에는 API 키를 포함하지 않는다.
- `.env` 파일을 `.gitignore`에 추가하여 버전 관리 시스템에 커밋되지 않도록 한다.
- 프로덕션 환경에서는 환경변수를 통해 직접 주입하는 것을 권장한다.

### 데이터베이스 보안

- 모든 SQL 쿼리는 파라미터화된 쿼리(parameterised queries)를 사용하여 SQL 인젝션을 방지한다.
- 업데이트 가능한 컬럼명은 화이트리스트로 관리되며, 허용되지 않은 컬럼명이 전달되면 `ValueError`가 발생한다.
- 상태 전이는 유효한 전이 규칙 테이블에 의해 검증되며, 잘못된 상태 전이 시도는 거부된다.

### 네트워크 보안

- 웹 서버의 기본 바인드 주소는 `127.0.0.1`(로컬호스트)이다. 외부 접근이 필요한 경우에만 `--host 0.0.0.0`으로 변경한다.
- 외부에 노출할 경우 반드시 HTTPS 역방향 프록시(nginx, Caddy 등)를 앞단에 배치할 것을 권장한다.

---

## 7. 트러블슈팅

### 웹 대시보드 접속 불가

**증상**: 브라우저에서 인증 후 401 Unauthorized 오류가 반환된다.

**원인**: `RESERVE_PASS` 환경변수가 설정되지 않았다.

**해결**:
1. `.env` 파일에 `RESERVE_PASS=비밀번호`를 추가한다.
2. 또는 쉘에서 `export RESERVE_PASS=비밀번호`를 실행한 후 서버를 재시작한다.

---

### LLM 응답 생성 실패

**증상**: 예약이 `failed` 상태로 전환되며 오류 메시지에 API 관련 내용이 표시된다.

**원인**: LLM API 키가 올바르지 않거나 만료되었다.

**해결**:
1. `.env` 파일에서 `ANTHROPIC_API_KEY` 또는 `OPENAI_API_KEY` 값을 확인한다.
2. 해당 API 서비스의 대시보드에서 키 상태를 확인한다.
3. 폴백 프로바이더가 설정되어 있는지 확인한다. 기본 폴백 순서는 Claude -> OpenAI -> Ollama이다.

---

### 에뮬레이터 연결 실패

**증상**: 워커 시작 시 "Could not connect to emulator" 경고가 표시되고 dry-run 모드로 전환된다.

**원인**: LDPlayer 에뮬레이터가 실행 중이지 않거나 ADB 연결이 안 된다.

**해결**:
1. LDPlayer가 실행 중인지 확인한다.
2. 터미널에서 `adb devices`를 실행하여 장치 목록에 에뮬레이터가 표시되는지 확인한다.
3. `config.yaml`의 `emulator.serial` 값이 실제 에뮬레이터의 시리얼과 일치하는지 확인한다.
4. ADB 연결이 끊어진 경우 `adb connect 127.0.0.1:5555`를 실행한다.

---

### 클리닉 검색 결과 없음

**증상**: 예약 생성 시 클리닉 이름 자동완성이 작동하지 않는다.

**원인**: hospitals.db 파일이 지정된 경로에 존재하지 않는다.

**해결**:
1. `config.yaml`의 `reservation.hospitals_db` 경로가 올바른지 확인한다. 기본 경로는 `../../data/clinic-results/hospitals.db`이다.
2. 해당 경로에 데이터베이스 파일이 존재하는지 확인한다.
3. 클리닉 데이터가 수집(크롤링)되어 있는지 확인한다.

---

### 예약이 timed_out 상태로 전환됨

**증상**: 클리닉에 메시지를 보냈으나 타임아웃 처리되었다.

**원인**: 설정된 대기 시간 내에 클리닉 응답이 감지되지 않았다.

**해결**:
1. `config.yaml`의 `reservation.greeting_timeout_hours` 값을 늘려본다 (기본값: 2시간).
2. 클리닉의 운영 시간을 고려하여 `scheduling.active_start_hour`와 `active_end_hour`를 조정한다.
3. `timed_out` 상태의 예약은 워커가 자동으로 `contacting`으로 재전환하여 재시도할 수 있다.

---

### 데이터베이스 초기화

**증상**: 데이터베이스 관련 오류가 발생하거나 테이블이 없다는 메시지가 표시된다.

**원인**: SQLite 데이터베이스 파일이 손상되었거나 처음 실행이다.

**해결**:
1. 시스템은 시작 시 `init_db()`를 호출하여 테이블을 자동 생성한다. 일반적으로 별도 초기화가 필요하지 않다.
2. 데이터베이스 파일이 손상된 경우 `data/consult.db` 파일을 삭제하고 서버를 재시작하면 새로 생성된다. 기존 데이터는 유실되므로 주의한다.

---

### 포트 충돌

**증상**: 서버 시작 시 "Address already in use" 오류가 발생한다.

**원인**: 지정된 포트(기본값: 8000)를 다른 프로세스가 사용 중이다.

**해결**:
1. 다른 포트를 지정하여 시작한다: `uv run python -m src.reserve --port 8080`
2. 또는 해당 포트를 사용 중인 프로세스를 확인하고 종료한다: `lsof -i :8000`

---

### 로그 확인

시스템은 structlog를 사용하여 구조화된 로그를 출력한다. 로그 파일은 `logs/` 디렉토리에 저장되며, `config.yaml`의 `logging` 섹션에서 로그 레벨과 파일 크기를 조정할 수 있다.

```yaml
logging:
  level: "DEBUG"        # DEBUG로 변경하면 상세 로그 출력
  log_dir: "logs"
  max_bytes: 10485760   # 10MB
  backup_count: 5       # 최대 백업 파일 수
```

---

*이 문서는 clinic-consult v0.1.0 기준으로 작성되었다.*
