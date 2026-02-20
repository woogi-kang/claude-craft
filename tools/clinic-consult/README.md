# Clinic Consult

외국인 환자를 위한 한국 피부과 예약 자동화 시스템

---

## 개요

Clinic Consult는 일본인 등 외국인 환자의 한국 피부과 시술 예약을 자동으로 대행하는 봇 시스템이다. Android 에뮬레이터(LDPlayer)와 uiautomator2를 활용하여 카카오톡/LINE 채널 채팅을 자동화하고, LLM(Claude, GPT-4o)을 이용해 한국어로 예약 협상을 수행한다.

### 주요 기능

- **멀티 메신저 지원**: 카카오톡과 LINE을 플랫폼 추상화 레이어를 통해 통합 지원
- **인바운드 봇**: 카카오톡 채팅방에서 수신 메시지를 모니터링하고 자동 응답 생성
- **아웃바운드 예약 시스템**: 웹 대시보드에서 예약 요청을 생성하면 자동으로 클리닉에 연락
- **LLM 기반 대화 엔진**: Claude -> OpenAI -> Ollama 폴백 체인으로 안정적인 응답 생성
- **10단계 상태 머신**: 예약 생성부터 확정/거절까지 체계적인 상태 관리
- **웹 대시보드**: FastAPI 기반 관리 인터페이스 (예약 생성, 모니터링, 수동 개입, CSV 내보내기)

---

## 기술 스택

| 구성 요소 | 기술 |
|-----------|------|
| 런타임 | Python 3.13+ |
| 패키지 관리 | uv |
| 웹 프레임워크 | FastAPI + Uvicorn |
| 데이터베이스 | SQLite (WAL 모드) |
| LLM 프로바이더 | Anthropic Claude, OpenAI GPT-4o, Ollama |
| Android 자동화 | uiautomator2 |
| 설정 관리 | pydantic-settings + YAML |
| 템플릿 엔진 | Jinja2 |
| 로깅 | structlog |

---

## 프로젝트 구조

```
clinic-consult/
├── src/
│   ├── main.py                 # 인바운드 봇 진입점 (파이프라인 오케스트레이터)
│   ├── reserve.py              # 아웃바운드 예약 시스템 진입점
│   ├── config.py               # pydantic-settings 설정 시스템
│   │
│   ├── messenger/              # 메신저 플랫폼 추상화 레이어
│   │   ├── __init__.py         #   normalize_platform() 플랫폼명 정규화
│   │   ├── selectors.py        #   MessengerSelectors 데이터클래스 (KAKAO, LINE)
│   │   └── deep_link.py        #   딥링크 URL 빌더 및 검증
│   │
│   ├── device/                 # Android UI 자동화 (uiautomator2)
│   │   ├── navigator.py        #   화면 탐색 (포그라운드, 채팅방 진입/이탈)
│   │   ├── reader.py           #   채팅방 메시지 읽기
│   │   ├── sender.py           #   메시지 전송 (Human-like 타이핑 딜레이)
│   │   ├── monitor.py          #   채팅 목록 모니터링 (새 메시지 감지)
│   │   └── selectors.py        #   (deprecated) 레거시 셀렉터
│   │
│   ├── ai/                     # LLM 통합
│   │   ├── router.py           #   멀티 프로바이더 라우터 (폴백 체인)
│   │   ├── classifier.py       #   메시지 의도 분류기
│   │   ├── prompts.py          #   시스템 프롬프트 템플릿
│   │   └── providers/          #   LLM 프로바이더 구현
│   │       ├── base.py         #     추상 기본 클래스
│   │       ├── claude.py       #     Anthropic Claude
│   │       ├── openai_provider.py  # OpenAI GPT-4o
│   │       └── ollama.py       #     로컬 Ollama
│   │
│   ├── pipeline/               # 인바운드 메시지 처리 파이프라인
│   │   ├── receive.py          #   메시지 수신 단계
│   │   ├── classify.py         #   메시지 분류 단계
│   │   ├── respond.py          #   응답 생성 단계
│   │   ├── send.py             #   메시지 발송 단계
│   │   └── track.py            #   대화 추적 단계
│   │
│   ├── outbound/               # 아웃바운드 예약 시스템
│   │   ├── worker.py           #   백그라운드 폴링 워커
│   │   ├── conversation.py     #   LLM 기반 대화 상태 머신
│   │   ├── contact.py          #   ADB 딥링크로 채팅방 열기
│   │   └── prompts.py          #   예약 협상 프롬프트
│   │
│   ├── reservation/            # 예약 데이터 관리
│   │   ├── repository.py       #   SQLite CRUD + 상태 전이 검증
│   │   ├── models.py           #   상태 머신 정의 (VALID_TRANSITIONS)
│   │   └── exporter.py         #   CSV 내보내기
│   │
│   ├── clinic/                 # 클리닉 데이터베이스
│   │   ├── lookup.py           #   hospitals.db 검색 (이름, ID, 플랫폼)
│   │   └── models.py           #   ClinicInfo, DoctorInfo 데이터클래스
│   │
│   ├── web/                    # 웹 대시보드
│   │   ├── app.py              #   FastAPI 라우트 (인증, CSRF, API)
│   │   └── templates/          #   Jinja2 HTML 템플릿
│   │
│   ├── knowledge/              # 지식 베이스
│   │   ├── templates.py        #   응답 템플릿 관리
│   │   └── faq_matcher.py      #   FAQ 매칭 (jamo 한글 분해)
│   │
│   ├── emulator/               # Android 에뮬레이터 관리
│   │   ├── ldplayer.py         #   LDPlayer 프로세스 제어
│   │   ├── device.py           #   uiautomator2 장치 연결
│   │   └── human_sim.py        #   인간 행동 시뮬레이션
│   │
│   ├── db/                     # 인바운드 봇 데이터베이스
│   │   ├── repository.py       #   대화 기록 SQLite 저장
│   │   └── models.py           #   DB 모델 정의
│   │
│   └── utils/                  # 유틸리티
│       ├── logger.py           #   structlog 기반 구조화 로깅
│       ├── rate_limiter.py     #   요청 속도 제한
│       ├── korean_text.py      #   한국어 텍스트 처리 (jamo)
│       └── time_utils.py       #   운영 시간 판별
│
├── tests/                      # 테스트 (pytest, 355+ 테스트)
├── data/                       # 런타임 데이터 (SQLite DB, 내보내기)
├── docs/                       # 문서
│   └── GUIDE-KO.md             #   운영 매뉴얼 (상세)
├── config.yaml                 # 운영 설정 (비밀 제외)
├── pyproject.toml              # 프로젝트 메타데이터 및 의존성
└── uv.lock                     # 의존성 잠금 파일
```

---

## 아키텍처

### 시스템 구성도

```
┌──────────────────────────────────────────────────────────────────┐
│                        Clinic Consult                             │
│                                                                  │
│  ┌──────────────┐     ┌──────────────────┐     ┌──────────────┐ │
│  │  인바운드 봇  │     │   아웃바운드 예약  │     │  웹 대시보드  │ │
│  │  (main.py)   │     │  (reserve.py)    │     │  (web/app.py) │ │
│  └──────┬───────┘     └────────┬─────────┘     └──────┬───────┘ │
│         │                      │                       │         │
│  ┌──────▼───────┐     ┌────────▼─────────┐            │         │
│  │   Pipeline   │     │     Worker       │            │         │
│  │  receive ->  │     │   상태 머신      │            │         │
│  │  classify -> │     │  created ->      │            │         │
│  │  respond ->  │     │  contacting ->   │            │         │
│  │  send ->     │     │  greeting_sent ->│            │         │
│  │  track       │     │  negotiating     │            │         │
│  └──────┬───────┘     └────────┬─────────┘            │         │
│         │                      │                       │         │
│  ┌──────▼──────────────────────▼───────────────────────▼───────┐ │
│  │                    공유 인프라                                │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐ │ │
│  │  │ AI 엔진  │ │ Messenger│ │ Clinic DB│ │  Reservation   │ │ │
│  │  │ Claude/  │ │ 추상화   │ │ hospitals│ │  Repository    │ │ │
│  │  │ OpenAI/  │ │ KakaoTalk│ │ .db      │ │  SQLite        │ │ │
│  │  │ Ollama   │ │ / LINE   │ │          │ │                │ │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Android 에뮬레이터 (LDPlayer)                   │ │
│  │  Navigator / Reader / Sender / Monitor (uiautomator2)       │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 두 가지 동작 모드

**1. 인바운드 봇 (`python -m src.main`)**

카카오톡 채팅방에서 수신 메시지를 폴링하고 자동으로 응답하는 모드이다. 5단계 파이프라인(수신 -> 분류 -> 응답 생성 -> 전송 -> 추적)으로 구성된다. FAQ 매칭을 우선 시도하고, 매칭 실패 시 LLM으로 응답을 생성한다.

**2. 아웃바운드 예약 (`python -m src.reserve`)**

웹 대시보드에서 예약 요청을 생성하면 백그라운드 워커가 자동으로 클리닉에 연락하는 모드이다. 딥링크로 메신저 채팅방을 열고, LLM이 한국어로 예약 협상을 진행한다.

### 메신저 플랫폼 추상화

모든 UI 자동화 모듈(Navigator, Reader, Sender, Monitor)은 `MessengerSelectors` 데이터클래스를 통해 플랫폼별 Android UI 셀렉터를 주입받는다.

```python
# 플랫폼 선택
from src.messenger.selectors import get_selectors, KAKAO, LINE

selectors = get_selectors("kakao")  # 또는 "line"
navigator = Navigator(device, selectors=selectors)
reader = MessageReader(device, selectors=selectors)
sender = MessageSender(device, selectors=selectors)
```

현재 지원 플랫폼:
- **카카오톡** (`com.kakao.talk`): 기본 플랫폼
- **LINE** (`jp.naver.line.android`): 일본 시장 대상

### LLM 폴백 체인

LLMRouter는 여러 프로바이더를 체인으로 연결하여 안정성을 확보한다.

```
Claude (기본) -> OpenAI GPT-4o (폴백 1) -> Ollama (폴백 2)
```

각 프로바이더가 실패하면 자동으로 다음 프로바이더를 시도한다.

### 예약 상태 머신

```
created -> contacting -> greeting_sent -> negotiating -> confirmed -> completed
                              |               |
                              +-> timed_out    +-> declined
                              |               |
                              +-> paused       +-> paused_for_human -> negotiating
                                  _for_human
```

| 상태 | 설명 |
|------|------|
| `created` | 예약 요청 생성됨. 워커 처리 대기 |
| `contacting` | 클리닉 채널 URL 확인 및 채팅 준비 |
| `greeting_sent` | 인사 메시지 전송. 응답 대기 |
| `negotiating` | LLM이 클리닉과 예약 협상 진행 |
| `paused_for_human` | 사람 개입 필요 (최대 턴 초과, 복잡한 요청) |
| `confirmed` | 예약 확정 |
| `declined` | 클리닉 거절 |
| `completed` | 최종 완료 처리 |
| `timed_out` | 클리닉 무응답 타임아웃 |
| `failed` | 오류 발생 또는 취소 |

---

## 설치

### 사전 요구사항

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) 패키지 매니저
- (선택) LDPlayer Android 에뮬레이터 + ADB (메신저 자동화 사용 시)

### 의존성 설치

```bash
cd tools/clinic-consult
uv sync        # 프로덕션 의존성
uv sync --dev  # 개발 의존성 포함 (pytest, ruff, mypy)
```

### 환경변수 설정

`.env` 파일을 프로젝트 루트에 생성한다.

```dotenv
# 웹 대시보드 인증 (필수)
RESERVE_USER=admin
RESERVE_PASS=안전한_비밀번호

# LLM API 키 (최소 하나 필수)
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx

# 기본 메신저 플랫폼 (선택, 기본값: kakao)
MESSENGER_PLATFORM=kakao
```

### 설정 파일

`config.yaml`에서 비밀이 아닌 운영 설정을 관리한다. 설정 우선순위: 환경변수 > `.env` > `config.yaml` > 코드 기본값

상세 설정 항목은 [운영 가이드](docs/GUIDE-KO.md)를 참고한다.

---

## 실행

### 웹 대시보드

```bash
uv run python -m src.reserve                        # 기본 (127.0.0.1:8000)
uv run python -m src.reserve --host 0.0.0.0 --port 8080  # 호스트/포트 지정
```

브라우저에서 `http://127.0.0.1:8000`에 접속한다. HTTP Basic Auth로 인증한다.

### 백그라운드 워커

```bash
uv run python -m src.reserve --worker              # 워커 모드 (30초 폴링)
uv run python -m src.reserve --worker --dry-run     # 드라이런 (메신저 전송 안 함)
```

### 메신저 플랫폼 지정

```bash
uv run python -m src.reserve --platform line        # LINE 플랫폼 사용
uv run python -m src.reserve --platform kakao       # 카카오톡 (기본값)
```

### 단일 예약 처리

```bash
uv run python -m src.reserve --process REQ-20260220-001
uv run python -m src.reserve --process REQ-20260220-001 --dry-run
```

### 인바운드 봇

```bash
uv run python -m src.main
```

---

## 웹 대시보드

### 주요 페이지

| 경로 | 설명 |
|------|------|
| `/` | 메인 대시보드 - 예약 목록, 통계 요약, 상태 필터 |
| `/create` | 예약 생성 폼 - 클리닉 자동완성 검색 |
| `/reservations/{id}` | 예약 상세 - 대화 로그, 수동 개입, 완료/취소 |
| `/export/csv` | 전체 예약 CSV 다운로드 |

### API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/clinics/search?q=검색어` | 클리닉 자동완성 (최대 10건) |
| GET | `/api/reservations` | 예약 목록 JSON |
| GET | `/api/reservations?status=negotiating` | 상태별 필터 |
| GET | `/api/docs` | Swagger API 문서 |

모든 엔드포인트는 HTTP Basic Auth 인증이 필요하다.

---

## 테스트

```bash
uv run pytest tests/                                # 전체 테스트 (355+)
uv run pytest tests/ --cov=src --cov-report=term-missing  # 커버리지 포함
uv run pytest tests/test_messenger.py -v             # 특정 파일
```

### 테스트 파일 목록

| 파일 | 테스트 영역 |
|------|------------|
| `test_messenger.py` | 메신저 추상화 (딥링크, 셀렉터, URL 검증, 스푸핑 방지) |
| `test_clinic_lookup.py` | 클리닉 DB 검색 (이름, ID, 플랫폼, 의사 정보) |
| `test_clinic_models.py` | ClinicInfo/DoctorInfo 데이터클래스 |
| `test_reservation_repository.py` | 예약 CRUD, 상태 전이, SQL 인젝션 방어 |
| `test_reservation_migrations.py` | DB 스키마 마이그레이션 |
| `test_reservation_exporter.py` | CSV 내보내기 |
| `test_outbound_worker.py` | 백그라운드 워커 상태 처리 |
| `test_outbound_conversation.py` | LLM 대화 상태 머신 |
| `test_outbound_prompts.py` | 예약 협상 프롬프트 |
| `test_web_auth.py` | 웹 인증, CSRF 보호 |
| `test_pipeline_stages.py` | 인바운드 파이프라인 단계 |
| `test_router.py` | LLM 라우터 폴백 체인 |
| `test_classifier.py` | 메시지 의도 분류 |
| `test_config.py` | 설정 시스템 |
| `test_monitor.py` | 채팅 목록 모니터링 |
| `test_db.py` | 인바운드 DB 저장소 |
| `test_rate_limiter.py` | 속도 제한 |
| `test_faq_matcher.py` | FAQ 매칭 (jamo 한글 분해) |
| `test_template.py` | 응답 템플릿 |
| `test_human_sim.py` | 인간 행동 시뮬레이션 |
| `test_korean_text.py` | 한국어 텍스트 처리 |

---

## 보안

### 인증

- 웹 대시보드는 HTTP Basic Auth로 보호된다
- `RESERVE_PASS` 미설정 시 접근 불가 (의도적 설계)
- `secrets.compare_digest()`로 타이밍 공격 방지

### CSRF 보호

- 모든 POST 요청에 CSRF 토큰 검증 적용
- `secrets.token_hex(32)` 기반 64자리 토큰

### 데이터베이스 보안

- 파라미터화된 쿼리로 SQL 인젝션 방지
- 업데이트 가능 컬럼 화이트리스트 검증
- 상태 전이 규칙 테이블로 무효 전이 거부

### URL 검증

- `urlparse()` 기반 도메인 검증으로 스푸핑 공격 방지
- 채널 URL 플랫폼별 허용 도메인 화이트리스트

### 네트워크

- 기본 바인드: `127.0.0.1` (로컬 전용)
- 외부 노출 시 HTTPS 역방향 프록시 권장

---

## 개발

### 코드 품질

```bash
uv run ruff check src/ tests/    # 린트
uv run ruff format src/ tests/   # 포맷팅
uv run mypy src/                 # 타입 체크
```

### 새 메신저 플랫폼 추가

1. `src/messenger/selectors.py`에 `MessengerSelectors` 인스턴스 추가
2. `get_selectors()`에 분기 추가
3. `src/messenger/deep_link.py`에 URL 빌더/검증 로직 추가
4. `normalize_platform()`에 별칭 등록 (필요 시)

---

## 문서

| 문서 | 설명 |
|------|------|
| [운영 가이드](docs/GUIDE-KO.md) | 상세 설치, 설정, 실행, 트러블슈팅 매뉴얼 |

---

## 라이선스

이 프로젝트는 비공개 소프트웨어이다.
