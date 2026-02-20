# X Outreach Pipeline

X(Twitter) 자동 아웃리치 파이프라인 -- **@ask.nandemo** 계정을 통해 한국 피부과 의료관광 정보를 일본 사용자에게 제공하는 시스템.

일본어 트윗을 자동 수집하고, AI로 의도를 분류한 뒤, Playwright 브라우저 자동화를 통해 맞춤형 일본어 답글과 DM을 발송합니다. X API는 사용하지 않으며, 모든 상호작용은 브라우저 자동화로 처리됩니다.

**비즈니스:** 한국 피부과 의료관광 인바운드 리드 생성

---

## 목차

- [아키텍처 개요](#아키텍처-개요)
- [파이프라인 단계](#파이프라인-단계)
- [디렉토리 구조](#디렉토리-구조)
- [사전 요구사항](#사전-요구사항)
- [설치](#설치)
- [설정](#설정)
- [사용법](#사용법)
- [데이터베이스 스키마](#데이터베이스-스키마)
- [계정 구조](#계정-구조)
- [AI 분류 시스템](#ai-분류-시스템)
- [지식 베이스](#지식-베이스)
- [브라우저 자동화](#브라우저-자동화)
- [데몬 모드](#데몬-모드)
- [안전 시스템](#안전-시스템)
- [보안](#보안)
- [테스트](#테스트)
- [문제 해결](#문제-해결)
- [의존성](#의존성)

---

## 아키텍처 개요

```
                          +-------------------+
                          |   config.yaml     |
                          |   .env (시크릿)    |
                          +--------+----------+
                                   |
                                   v
+----------+    +----------+    +----------+    +----------+    +----------+
|  검색     |--->|  수집     |--->|  분석     |--->|  답글     |--->|   DM    |
| (burner)  |    | (필터링)  |    |  (AI)    |    |(nandemo) |    |(nandemo) |
+----------+    +----------+    +----------+    +----------+    +----------+
     |               |               |               |               |
     v               v               v               v               v
 Playwright     PostgreSQL      Gemini API      Playwright       Playwright
  (크롤링)       (저장)         (분류)           (게시)           (발송)
     |               |               |               |               |
     +-------+-------+-------+-------+-------+-------+-------+------+
             |                        |                       |
             v                        v                       v
        outreach_shared          structlog              긴급 정지
        (브라우저 스텔스,         (구조화 로깅)          시스템
         인간 시뮬레이션,
         DB, 레이트 리미터)
```

파이프라인은 5단계 순차 프로세스로 실행됩니다. 각 단계는 공유 PostgreSQL 데이터베이스에 읽기/쓰기합니다. 1단계와 4-5단계는 X 웹 인터페이스에 대한 Playwright 브라우저 자동화를 사용합니다.

---

## 파이프라인 단계

### 1단계: 검색 (Search)

Playwright 브라우저 자동화로 일본어 피부과 키워드에 매칭되는 트윗을 크롤링합니다. **버너 계정**을 사용합니다.

- 설정된 각 키워드에 대해 `x.com/search`로 이동
- `data-testid` CSS 셀렉터를 사용하여 DOM에서 트윗 데이터 추출
- 검색 간 인간과 유사한 스크롤 및 지연 적용
- 키워드 결과 간 트윗 ID 기반 중복 제거
- 키워드 예시: `韓国皮膚科`, `ピコレーザー`, `韓国美容`, `韓国クリニック` 등 15개

### 2단계: 수집 (Collect)

원시 트윗을 필터링하고 적격한 것만 PostgreSQL에 `collected` 상태로 저장합니다.

다음 조건에 해당하면 거부됩니다:
- 팔로워 10,000명 초과 계정
- 프로필 사진 없음 (설정 가능)
- 바이오 없음 (설정 가능)
- 클리닉 마케팅 계정 (바이오에 URL + 클리닉 키워드 동시 포함)
- 24시간 이상 경과 (설정 가능)
- 데이터베이스에 이미 존재 (중복)

### 3단계: 분석 (Analyze)

2단계 분류 시스템:

1. **키워드 프리필터** (빠름, 코드 레벨, LLM 호출 없음) -- 일본어 키워드를 5개 의도 카테고리에 매칭. 제외 키워드(스팸, 봇, 광고)에 매칭되는 트윗은 즉시 거부.
2. **Gemini LLM 분류** -- 트윗 내용, 작성자 메타데이터, 인게이지먼트 지표를 Gemini 2.0 Flash에 JSON 모드로 전송. `intent_type`, `confidence`, `llm_decision`, `rationale` 반환.

신뢰도 임계값(기본 0.7) 미만 분류는 자동 거부됩니다.

### 4단계: 답글 (Reply)

Playwright를 통해 승인된 트윗에 맞춤형 일본어 답글을 생성하고 게시합니다.

- **@ask.nandemo** 계정 사용
- Gemini가 시술 지식 컨텍스트를 기반으로 콘텐츠 생성
- 일일 답글 제한 적용 (기본 50건)
- 조용한 시간: 23:00-08:00 JST 동안 답글 없음
- 제한 신호 감지 시 긴급 정지

### 5단계: DM

Playwright를 통해 고의도 사용자에게 맞춤형 일본어 DM을 발송합니다.

- DM 간 최소 간격 (기본 25분)
- 일일 DM 제한 (기본 20건)
- DM 고유성 검사 (이전 DM과 30자 이상 차이 필요)
- 생성된 DM에서 모든 URL 자동 제거
- 제한 신호 감지 시 긴급 정지

---

## 디렉토리 구조

```
tools/x-outreach/
    .env.example              # 시크릿 템플릿
    config.yaml               # 비밀이 아닌 기본값 (키워드, 임계값, 지연)
    pyproject.toml            # 프로젝트 메타데이터 및 의존성
    src/
        __init__.py
        __main__.py           # python -m src 진입점
        main.py               # CLI 진입점 + PipelineRunner 오케스트레이터
        config.py             # pydantic-settings 설정 시스템
        daemon.py             # 2-4시간 변동 주기 24시간 데몬
        ai/
            classifier.py     # 5카테고리 트윗 분류기 (키워드 + Gemini)
            content_gen.py    # Gemini 기반 답글/DM 콘텐츠 생성
            keywords.py       # 일본어 포함/제외 키워드 프리필터
            prompts.py        # 시스템/사용자 프롬프트 템플릿
        browser/
            session.py        # 영구 브라우저 세션 관리자
        cli/
            blocklist.py      # 사용자 차단 목록 관리
            report.py         # 주간 리포트 생성
            setup.py          # 최초 설정 검증
            status.py         # 파이프라인 상태 표시
        db/
            models.py         # 공유 라이브러리에서 DDL 재수출
            repository.py     # 비동기 PostgresRepository의 동기 래퍼
        knowledge/
            templates.py      # 카테고리별 응답 메시지 템플릿
            treatments.py     # 한국 피부과 시술 지식 베이스
        pipeline/
            analyze.py        # 분류 파이프라인 단계
            collect.py        # 중복 제거 및 필터링을 통한 트윗 수집
            dm.py             # Playwright를 통한 DM 발송
            dm_track.py       # DM 응답 추적
            halt.py           # 긴급 정지 시스템
            reply.py          # Playwright를 통한 답글 발송
            search.py         # Playwright 기반 X 검색
            track.py          # 액션 추적 및 통계
            warmup.py         # 신규 계정 점진적 볼륨 증가
        platform/
            login.py          # X 로그인 헬퍼
            selectors.py      # X DOM 셀렉터/상수
    scripts/
        migrate_sqlite_to_pg.py  # SQLite -> PostgreSQL 일회성 마이그레이션
        setup.sh                 # 개발 환경 설정
        status.py               # 빠른 상태 확인 스크립트
    launchd/
        com.asknandemo.xoutreach.plist  # macOS launchd 데몬 설정
    tests/
        conftest.py           # 공유 픽스처
        test_analyze.py       # 분류 파이프라인 테스트
        test_classifier.py    # TweetClassifier 및 키워드 프리필터 테스트
        test_collect.py       # 트윗 필터링/저장 테스트
        test_config.py        # 설정 로딩/검증 테스트
        test_content_gen.py   # 답글/DM 콘텐츠 생성 테스트
        test_db.py            # 리포지토리 및 DB 연산 테스트
        test_keywords.py      # 일본어 키워드 매칭 테스트
        test_m4.py            # 다단계 파이프라인 통합 테스트
        test_pipeline.py      # 전체 파이프라인 오케스트레이션 테스트
        test_search.py        # Playwright 검색 파이프라인 테스트
        test_templates.py     # 템플릿 선택/로테이션 테스트
        (총 244개 테스트)

tools/_shared/                # 크로스 플랫폼 공유 라이브러리 (outreach_shared)
    outreach_shared/
        ai/llm_client.py     # LLM Protocol + GeminiClient + ClaudeClient
        account/pool.py       # 계정 로테이션, 성숙도 라이프사이클
        account/health.py     # 에스컬레이션 프로토콜
        browser/human_sim.py  # 인간과 유사한 타이핑, 스크롤, 일시정지
        browser/stealth.py    # playwright-stealth 브라우저 실행
        daemon/loop.py        # 시그널 핸들링을 포함한 비동기 데몬 루프
        db/models.py          # 통합 PostgreSQL DDL (posts, accounts, outreach)
        db/postgres.py        # 비동기 PostgresRepository (asyncpg, CRUD, 커넥션 풀링)
        utils/logger.py       # 구조화 로깅 (structlog)
        utils/rate_limiter.py # 토큰 버킷 레이트 리미터
        utils/time_utils.py   # 타임존 헬퍼
```

---

## 사전 요구사항

- **Python** >= 3.13
- **PostgreSQL** >= 14 (실행 중이고 접근 가능해야 함)
- **Node.js** (Playwright 브라우저 다운로드에 필요)
- **uv** 패키지 매니저 (권장) 또는 pip
- **Gemini API 키** (Google AI Studio에서 발급)

---

## 설치

### 빠른 설정 (uv)

```bash
cd tools/x-outreach

# 가상 환경 생성 및 모든 의존성 설치
uv sync --all-extras

# Playwright Chromium 브라우저 설치
uv run playwright install chromium
```

### 수동 설정

```bash
cd tools/x-outreach

# 가상 환경 생성
python3.13 -m venv .venv
source .venv/bin/activate

# 프로젝트 및 개발 의존성 설치
pip install -e ".[dev]"

# 공유 라이브러리 설치 (editable)
pip install -e ../_shared

# Playwright 브라우저 설치
python -m playwright install chromium
```

### 데이터베이스 설정

PostgreSQL 데이터베이스를 생성합니다:

```bash
createdb outreach
```

스키마는 최초 실행 시 `Repository.init_db()`를 통해 자동 생성됩니다.

### 환경 변수

예제 파일을 복사하고 자격 증명을 입력합니다:

```bash
cp .env.example .env
```

`.env` 파일을 편집합니다:

```
# 버너 계정 자격 증명 (크롤링 전용)
BURNER_X_USERNAME=your_burner_username
BURNER_X_PASSWORD=your_burner_password

# @ask.nandemo 자격 증명 (답글 및 DM 발송용)
NANDEMO_X_USERNAME=your_nandemo_username
NANDEMO_X_PASSWORD=your_nandemo_password

# Gemini API 키 (Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key

# PostgreSQL 연결 문자열
DATABASE_URL=postgresql://user:pass@localhost:5432/outreach
```

### 설정 검증

```bash
uv run python -m src setup
```

자격 증명, 데이터베이스 연결, 브라우저 가용성을 확인하는 시작 검사를 실행합니다.

---

## 설정

설정은 다음 우선순위(높은 순)로 계층적으로 해석됩니다:

1. **환경 변수** (셸 레벨)
2. **`.env` 파일** (시크릿 전용)
3. **`config.yaml`** (비밀이 아닌 기본값)
4. **필드 기본값** (Pydantic 모델)

### config.yaml

모든 비밀이 아닌 설정은 `config.yaml`에 있습니다:

```yaml
search:
  keywords:                   # 일본어 검색 키워드 (리스트)
    - "韓国皮膚科"             # 한국 피부과
    - "韓国美容"               # 한국 미용
    - "韓国美容皮膚科"          # 한국 미용 피부과
    - "レーザー治療"            # 레이저 치료
    - "ピコレーザー"            # 피코레이저
    - "韓国クリニック"          # 한국 클리닉
    - "韓国整形"               # 한국 성형
    - "美容皮膚科 韓国"         # 미용 피부과 한국
    - "韓国 シミ取り"           # 한국 기미 제거
    - "韓国 ニキビ跡"           # 한국 여드름 자국
    - "韓国 毛穴"              # 한국 모공
    - "フラクショナルレーザー"    # 프락셔널 레이저
    - "韓国 ボトックス"         # 한국 보톡스
    - "韓国 ヒアルロン酸"       # 한국 히알루론산
    - "韓国 美肌"              # 한국 미피부
  max_post_age_hours: 24      # 수집할 트윗의 최대 경과 시간

collect:
  max_follower_count: 10000   # 팔로워 수 상한선
  require_profile_pic: true   # 프로필 사진 필수 여부
  require_bio: true           # 바이오 필수 여부

classification:
  confidence_threshold: 0.7   # LLM 분류 신뢰도 임계값
  categories:                 # 5개 의도 카테고리
    - hospital
    - price
    - procedure
    - complaint
    - review

reply:
  enabled: true               # 답글 기능 활성화
  daily_limit: 50             # 일일 답글 제한

dm:
  enabled: true               # DM 기능 활성화
  daily_limit: 20             # 일일 DM 제한
  min_interval_minutes: 25    # DM 간 최소 간격 (분)

browser:
  headless: true              # 헤드리스 브라우저 모드
  viewport_width: 1280
  viewport_height: 720

delays:
  search_min_seconds: 30      # 검색 간 최소 지연
  search_max_seconds: 300     # 검색 간 최대 지연
  action_min_seconds: 5       # 액션 간 최소 지연
  action_max_seconds: 30      # 액션 간 최대 지연

daemon:
  min_interval_hours: 2.0     # 주기 간 최소 간격 (시간)
  max_interval_hours: 4.0     # 주기 간 최대 간격 (시간)
  active_start_hour: 8        # 활성 시작 시간 (JST)
  active_end_hour: 23         # 활성 종료 시간 (JST)

logging:
  level: "INFO"
  log_dir: "logs"
  max_bytes: 10485760         # 10MB
  backup_count: 5

database:
  url: "postgresql://localhost:5432/outreach"
  min_pool_size: 2
  max_pool_size: 10

account_pool:
  cooldown_minutes_crawl: 30      # 크롤링 계정 쿨다운 (분)
  cooldown_minutes_outreach: 60   # 아웃리치 계정 쿨다운 (분)

llm:
  provider: gemini
  model: gemini-2.0-flash
```

### .env (시크릿 전용)

| 변수 | 필수 | 설명 |
|------|------|------|
| `BURNER_X_USERNAME` | 필수 | 크롤링용 버너 계정 사용자명 |
| `BURNER_X_PASSWORD` | 필수 | 버너 계정 비밀번호 |
| `NANDEMO_X_USERNAME` | DM 활성화 시 | @ask.nandemo 사용자명 |
| `NANDEMO_X_PASSWORD` | DM 활성화 시 | @ask.nandemo 비밀번호 |
| `GEMINI_API_KEY` | 필수 | Google Gemini API 키 |
| `DATABASE_URL` | 필수 | PostgreSQL 연결 문자열 |

---

## 사용법

모든 명령은 `python -m src` (또는 `uv run python -m src`)로 실행합니다.

### 파이프라인 1회 실행

```bash
# 전체 파이프라인: 검색 -> 수집 -> 분석 -> 답글 -> DM
uv run python -m src run

# 드라이런: 브라우저 검색 건너뛰고 이미 수집된 트윗만 분석
uv run python -m src run --dry-run
```

### 데몬 시작 (24시간 운영)

```bash
uv run python -m src daemon
```

데몬은 2-4시간 변동 간격으로 파이프라인을 반복 실행하며, 활성 시간(08:00-23:00 JST) 동안만 작동합니다. SIGTERM/SIGINT 시그널을 처리하여 정상 종료합니다.

### 파이프라인 상태 확인

```bash
uv run python -m src status
```

현재 통계를 표시합니다: 수집된 트윗, 분석 완료, 답글 발송, DM 발송, 오류 수.

### 설정 검사

```bash
uv run python -m src setup
```

모든 사전 요구사항을 검증합니다: 환경 변수, 데이터베이스 연결, Playwright 브라우저, Gemini API 접근.

### 긴급 정지

```bash
# 정지 상태 확인
uv run python -m src halt

# 정지 해제 (다음 주기는 50% 볼륨으로 실행)
uv run python -m src halt resume
```

### 차단 목록 관리

```bash
# 차단된 사용자 목록 조회
uv run python -m src blocklist list

# 사용자 차단
uv run python -m src blocklist add @username

# 사용자 차단 해제
uv run python -m src blocklist remove @username
```

### 주간 리포트

```bash
uv run python -m src report
```

지난 1주일의 파이프라인 활동 요약을 생성합니다.

---

## 데이터베이스 스키마

파이프라인은 공유 라이브러리(`outreach_shared.db.models`)에 정의된 3개의 핵심 테이블과 함께 PostgreSQL을 사용합니다.

### posts 테이블

분류 결과와 함께 크롤링된 모든 트윗을 저장합니다.

```sql
CREATE TABLE IF NOT EXISTS posts (
    id              SERIAL PRIMARY KEY,
    post_id         TEXT UNIQUE NOT NULL,       -- 트윗 고유 ID
    platform        TEXT NOT NULL,              -- 'x'
    user_id         TEXT NOT NULL,              -- 작성자 사용자명
    username        TEXT,                       -- 표시 이름
    contents        TEXT NOT NULL,              -- 트윗 본문
    intent_type     TEXT,                       -- hospital/price/procedure/complaint/review
    keyword_intent  TEXT,                       -- 키워드 프리필터에서 결정된 카테고리
    llm_decision    BOOLEAN DEFAULT NULL,       -- true = 아웃리치 권장
    llm_rationale   TEXT,                       -- LLM 판단 근거
    likes_count     INTEGER DEFAULT 0,
    comments_count  INTEGER DEFAULT 0,
    retweets_count  INTEGER DEFAULT 0,
    post_url        TEXT,                       -- 트윗 URL
    author_bio      TEXT,                       -- 작성자 바이오
    author_followers INTEGER DEFAULT 0,         -- 팔로워 수
    search_keyword  TEXT,                       -- 검색에 사용된 키워드
    status          TEXT NOT NULL DEFAULT 'collected',
    crawled_at      TIMESTAMPTZ DEFAULT NOW(),
    post_created_at TIMESTAMPTZ,               -- 트윗 작성 시각
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

**상태 라이프사이클:** `collected` -> `analyzed` -> `replied` -> `dm_sent`

### accounts 테이블

성숙도 라이프사이클을 추적하는 계정 풀입니다.

```sql
CREATE TABLE IF NOT EXISTS accounts (
    account_id      TEXT PRIMARY KEY,           -- 계정 고유 ID
    platform        TEXT NOT NULL,              -- 'x'
    account_type    TEXT NOT NULL,              -- 'burner' 또는 'outreach'
    username        TEXT,
    proxy_ip        TEXT,                       -- 프록시 IP (향후 일본 프록시 대비)
    status          TEXT NOT NULL DEFAULT 'nurturing',
    maturity        TEXT NOT NULL DEFAULT 'new',
    daily_comment_count INTEGER DEFAULT 0,      -- 일일 댓글 카운터
    daily_dm_count  INTEGER DEFAULT 0,          -- 일일 DM 카운터
    daily_search_count INTEGER DEFAULT 0,       -- 일일 검색 카운터
    last_warning_at TIMESTAMPTZ,               -- 마지막 경고 시각
    last_used_at    TIMESTAMPTZ,               -- 마지막 사용 시각
    session_data_dir TEXT,                      -- 세션 데이터 저장 경로
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    banned_at       TIMESTAMPTZ                -- 차단 시각
);
```

**성숙도 라이프사이클:** `new` -> `nurturing` -> `active` -> `suspended` -> `banned`

### outreach 테이블

발송된 모든 액션(답글, DM)을 추적 및 중복 방지를 위해 기록합니다.

```sql
CREATE TABLE IF NOT EXISTS outreach (
    id              SERIAL PRIMARY KEY,
    post_id         TEXT REFERENCES posts(post_id),     -- 대상 트윗
    user_id         TEXT NOT NULL,                      -- 대상 사용자
    account_id      TEXT REFERENCES accounts(account_id), -- 사용된 계정
    platform        TEXT NOT NULL,                      -- 'x'
    outreach_type   TEXT NOT NULL,                      -- 'reply' 또는 'dm'
    message         TEXT NOT NULL,                      -- 발송된 콘텐츠
    status          TEXT NOT NULL DEFAULT 'pending',    -- pending/sent/failed
    error_message   TEXT,                               -- 실패 시 오류 메시지
    replied         BOOLEAN DEFAULT FALSE,              -- 사용자가 DM에 응답했는지 여부
    scheduled_at    TIMESTAMPTZ,                        -- 예약 발송 시각
    sent_at         TIMESTAMPTZ,                        -- 실제 발송 시각
    replied_at      TIMESTAMPTZ,                        -- 응답 감지 시각
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### 인덱스

```sql
CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
CREATE INDEX IF NOT EXISTS idx_posts_platform ON posts(platform);
CREATE INDEX IF NOT EXISTS idx_posts_post_id ON posts(post_id);
CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_crawled_at ON posts(crawled_at);
CREATE INDEX IF NOT EXISTS idx_outreach_status ON outreach(status);
CREATE INDEX IF NOT EXISTS idx_outreach_post_id ON outreach(post_id);
CREATE INDEX IF NOT EXISTS idx_outreach_account_id ON outreach(account_id);
CREATE INDEX IF NOT EXISTS idx_outreach_platform ON outreach(platform);
CREATE INDEX IF NOT EXISTS idx_accounts_platform ON accounts(platform);
CREATE INDEX IF NOT EXISTS idx_accounts_status ON accounts(status);
CREATE INDEX IF NOT EXISTS idx_accounts_maturity ON accounts(maturity);
```

---

## 계정 구조

파이프라인은 역할이 분리된 2개의 X 계정을 사용합니다:

| 계정 | 역할 | 사용 단계 |
|------|------|-----------|
| 버너 계정 | 크롤링 및 검색 전용 | 1단계 (검색) |
| @ask.nandemo | 답글 및 DM 발송 | 4-5단계 (답글, DM) |

이 분리는 공격적인 검색 패턴으로 인한 @ask.nandemo 계정의 레이트 리미팅 또는 정지 위험을 방지합니다.

### 성숙도 라이프사이클

계정은 다음 단계를 거칩니다:

- **new** -- 새로 생성, 아직 사용되지 않음
- **nurturing** -- 자연스러운 활동으로 워밍업 중
- **active** -- 아웃리치에 완전히 운영 가능
- **suspended** -- X에 의해 일시적으로 제한됨
- **banned** -- 영구적으로 제한됨

계정은 쿨다운 기간과 함께 LRU(Least Recently Used) 방식으로 로테이션됩니다:
- 크롤링 쿨다운: 30분 (설정 가능)
- 아웃리치 쿨다운: 60분 (설정 가능)

---

## AI 분류 시스템

### 2단계 분류

**1단계: 일본어 키워드 프리필터** (`src/ai/keywords.py`)

큐레이션된 일본어 키워드 목록에 대해 트윗 내용을 매칭하는 빠른 코드 레벨 필터입니다. 이 단계에서는 LLM을 호출하지 않습니다.

- **제외 키워드**: 트윗을 즉시 거부 (스팸, 봇, 광고, 암호화폐, 마케팅 계정 등)
- **카테고리 키워드**: 트윗을 5개 의도 카테고리 중 하나로 라우팅
- 첫 매칭 우선; 카테고리 우선순위: hospital > price > procedure > complaint > review

**2단계: Gemini LLM 분류** (`src/ai/classifier.py`)

키워드 필터링을 통과한 트윗은 Gemini 2.0 Flash로 심층 분류됩니다:

- **입력:** 프롬프트 인젝션 방어를 위해 `<tweet>` XML 구분자로 감싼 트윗 내용, 작성자 사용자명, 바이오, 팔로워/팔로잉 수, 인게이지먼트 지표
- **출력:** `intent_type`, `confidence` (0.0-1.0), `llm_decision` (boolean), `rationale`를 포함한 JSON
- **신뢰도 임계값:** 0.7 (미만은 자동 거부)

### 5개 의도 카테고리

| 카테고리 | 설명 | 신호 예시 |
|----------|------|-----------|
| `hospital` | 특정 클리닉을 찾거나 묻는 경우 | 클리닉 추천, 비교, 첫 방문 |
| `price` | 시술 비용을 논의하거나 비교하는 경우 | 가격 공유, 예산 질문, 가성비 비교 |
| `procedure` | 특정 시술을 논의하는 경우 | 시술 경험, 비포/애프터, 시술 문의 |
| `complaint` | 부정적 경험이나 우려를 표현하는 경우 | 시술 실패, 업셀링 불만, 사후 관리 문제 |
| `review` | 일반적인 리뷰나 경험 보고서를 공유하는 경우 | 여행 리포트, 클리닉 리뷰, 추천 글 |

### 인게이지먼트 결정 (`llm_decision`)

LLM은 도움이 될 수 있는 정보가 있는 진정한 개인에게만 `llm_decision=true`를 설정합니다. 다음은 거부됩니다:

- 클리닉 공식/마케팅 계정
- 봇 또는 스팸 게시물
- 팔로워 10,000명 초과 인플루언서 (상업 계정)
- 일본인으로 가장한 한국 계정의 스텔스 마케팅
- 진정한 필요나 질문이 없는 콘텐츠

---

## 지식 베이스

### 시술 지식 (`src/knowledge/treatments.py`)

일본어 피부과 용어를 한국어 등가물에 매핑하는 인메모리 지식 베이스로, 시작 시 공유 JSON 데이터셋에서 로드됩니다.

30개 이상의 시술을 다룹니다:
- 보톡스, 필러, 히알루론산 주사
- 피코레이저, 프락셔널 레이저, 레이저 토닝
- 포텐자, 더마펜, 리쥬란, 물광주사
- HIFU, 슈링크, 울쎄라
- 실리프팅, 지방분해 주사

피부 고민(기미, 모공, 주름, 처짐, 여드름 자국)도 추천 시술에 매핑합니다.

### 메시지 템플릿 (`src/knowledge/templates.py`)

의도 카테고리별로 정리된 답글 및 DM 템플릿입니다. `TemplateSelector` 클래스는 동일한 메시지를 반복 전송하지 않도록 LRU 로테이션을 사용합니다.

모든 템플릿은 @ask.nandemo의 목소리에 맞는 자연스러운 일본어입니다:
- 캐주얼 일본어 (보통체 기반, 가끔 데스마스체로 완화)
- 따뜻하지만 과하지 않은 톤
- 데이터 기반: 가능할 때 구체적인 숫자 포함
- 클리닉 마케팅 계정처럼 들리지 않음

---

## 브라우저 자동화

모든 X 상호작용은 Chromium과 함께 **Playwright**를 사용합니다. X API(v1, v2, Tweepy)는 사용하지 않습니다.

### 스텔스

- `playwright-stealth` 패치를 적용하여 봇 탐지 회피
- 쿠키 저장소를 통한 영구 세션으로 재실행 간 유지
- 세션 저장 위치: `data/sessions/{account_name}/`

### 인간 시뮬레이션 (`outreach_shared.browser.human_sim`)

- **타이핑:** 문자별 랜덤 지연 (자연스러운 타이핑 속도 시뮬레이션)
- **마우스 이동:** 액션 간 랜덤 커서 이동
- **스크롤:** 가변 속도의 인간과 유사한 스크롤 패턴
- **일시정지:** 모든 액션 간 랜덤 지연 (최소/최대 설정 가능)

### DOM 셀렉터 (`src/platform/selectors.py`)

모든 CSS 셀렉터는 단일 파일에 집중되어 있습니다. X가 DOM 구조를 변경할 때 하나의 파일만 업데이트하면 됩니다. 셀렉터는 주로 비교적 안정적인 `data-testid` 속성을 사용합니다.

---

## 데몬 모드

데몬은 내장된 안전 메커니즘과 함께 파이프라인을 지속적으로 실행합니다.

### 타이밍

- **주기 간격:** 2-4시간 랜덤 (고정 간격이 아닌 변동 간격)
- **활성 시간:** 08:00-23:00 JST만 (야간에는 실행하지 않음)
- **타임존:** 모든 시간 계산은 Asia/Tokyo (JST) 사용

### 시그널 핸들링

- **SIGTERM / SIGINT:** 현재 주기 완료 후 정상 종료
- 공유 `DaemonLoop` 클래스가 관리

### macOS launchd

macOS 백그라운드 서비스로 데몬을 실행하기 위한 `launchd` plist가 `launchd/com.asknandemo.xoutreach.plist`에 포함되어 있습니다.

---

## 안전 시스템

### 긴급 정지 (`src/pipeline/halt.py`)

파이프라인은 계정 제한 신호를 모니터링하고 감지 시 자동으로 정지합니다:

- **HTTP 403** + 제한 문구 ("suspended", "restricted", "locked")
- **HTTP 429** + 레이트 리밋 메시지
- **Playwright 차단 페이지** ("account suspended", "verify your identity" 등)

정지 시:
- `data/.halt` 경로에 `.halt` 센티넬 파일이 생성됨
- 수동 해제까지 모든 예약된 실행이 건너뛰어짐
- 정지 사유, 소스, 타임스탬프가 로깅됨

`python -m src halt resume`으로 해제합니다. 해제 후 첫 주기는 안전 조치로 **50% 볼륨**으로 실행됩니다.

### 워밍업 모드 (`src/pipeline/warmup.py`)

파이프라인 운영 첫 **14일** 동안:
- 일일 답글 및 DM 제한이 절반으로 감소
- 설정된 키워드의 절반만 검색
- 시작 날짜는 설정 저장소에 영구 보존

### 레이트 리미팅

- **일일 상한:** 답글 50건, DM 20건 (설정 가능, 워밍업 중 절반)
- **최소 DM 간격:** DM 간 25분
- **검색 지연:** 키워드 검색 간 30-300초
- **액션 지연:** 브라우저 액션 간 5-30초
- **조용한 시간:** 23:00-08:00 JST 동안 아웃리치 없음

### 보존 모드

긴급 정지 해제 후, 파이프라인은 다음 주기를 **50% 볼륨**으로 실행한 후 정상 운영으로 복귀합니다.

---

## 보안

### SQL 인젝션 방지

동적 UPDATE 쿼리는 컬럼 이름 허용 목록을 사용합니다. `update_post_status`, `update_account`, `update_outreach_status` 등의 메서드에서 사전 승인된 컬럼 이름만 키워드 인수로 허용됩니다.

```python
_POSTS_ALLOWED_COLUMNS = frozenset({
    "status", "intent_type", "keyword_intent", "llm_decision",
    "llm_rationale", "post_url", "author_bio", "author_followers",
    "likes_count", "comments_count", "retweets_count",
    "search_keyword", "post_created_at",
})
```

허용 목록에 없는 컬럼이 전달되면 `ValueError`가 발생합니다.

### 프롬프트 인젝션 방어

사용자 생성 콘텐츠(트윗 텍스트)는 LLM에 전달될 때 항상 `<tweet>` XML 구분자로 감싸집니다:

```
<tweet>
{tweet_content}
</tweet>
```

이로써 신뢰할 수 없는 사용자 콘텐츠와 프롬프트의 시스템 지시문이 분리됩니다.

### 로그 보안

- **오류 메시지:** 로그에서 200자로 잘림
- **트윗 내용:** 로그 항목에서 50자로 잘림
- **데이터베이스 URL:** 자격 증명 없이 로깅
- **시크릿 없음:** API 키, 비밀번호가 로그 출력에 나타나지 않음

### URL 제거

모든 URL은 안전 조치로 생성된 DM 콘텐츠에서 제거됩니다. 정규식 `https?://\S+`가 발송 전 모든 DM에 적용됩니다.

### 자격 증명 격리

시크릿은 `.env`에만 저장됩니다 (gitignore 처리). `config.yaml` 파일에는 민감하지 않은 기본값만 포함됩니다.

---

## 테스트

테스트 스위트는 11개 테스트 파일에 걸쳐 **244개 테스트**를 포함합니다.

### 테스트 실행

```bash
# 전체 테스트 실행
uv run pytest tests/

# 커버리지 포함 실행
uv run pytest tests/ --cov=src --cov-report=term-missing

# 특정 테스트 파일 실행
uv run pytest tests/test_classifier.py

# 특정 테스트 실행
uv run pytest tests/test_classifier.py::TestTweetClassifier::test_classify_hospital
```

### 린팅

```bash
# 코드 스타일 검사
uv run ruff check src/

# 스타일 이슈 자동 수정
uv run ruff check src/ --fix

# 타입 검사
uv run mypy src/
```

### 테스트 아키텍처

- 모든 테스트는 **목(mock) 기반 테스트**를 사용 -- 실제 DB 연결, API 호출, 브라우저 세션 없음
- `conftest.py`가 목 리포지토리, 분류기, 설정을 위한 공유 픽스처 제공
- `pytest-asyncio`를 `asyncio_mode = "auto"`로 사용하여 비동기 테스트 함수 지원
- `ruff`는 Python 3.13 대상, 100자 라인 길이로 설정

### 테스트 파일

| 파일 | 유형 | 커버리지 영역 |
|------|------|---------------|
| `test_pipeline.py` | 통합 | 전체 파이프라인 오케스트레이션 |
| `test_m4.py` | 통합 | 다단계 파이프라인 시나리오 |
| `test_analyze.py` | 단위 | 분류 파이프라인 단계 |
| `test_classifier.py` | 단위 | TweetClassifier 및 키워드 프리필터 |
| `test_content_gen.py` | 단위 | 답글 및 DM 콘텐츠 생성 |
| `test_collect.py` | 단위 | 트윗 필터링 및 저장 |
| `test_config.py` | 단위 | 설정 로딩 및 검증 |
| `test_db.py` | 단위 | 리포지토리 및 DB 연산 |
| `test_keywords.py` | 단위 | 일본어 키워드 매칭 |
| `test_templates.py` | 단위 | 템플릿 선택 및 로테이션 |
| `test_search.py` | 단위 | Playwright 검색 파이프라인 |

---

## 문제 해결

### "GEMINI_API_KEY is not set"

파이프라인이 Gemini API 키를 찾을 수 없습니다. `.env` 파일이 존재하고 유효한 `GEMINI_API_KEY`를 포함하는지 확인하세요. `python -m src setup`으로 검증하세요.

### "Failed to login to burner account"

X가 추가 인증(CAPTCHA, 이메일/전화 확인 등)을 요청하고 있을 수 있습니다:

1. 브라우저를 수동으로 열고 버너 계정에 로그인
2. 인증 챌린지를 완료
3. 세션 캐시 삭제: `rm -rf data/sessions/burner/`
4. 파이프라인 재시도

### "session_expired_relogin" 로그

저장된 브라우저 세션이 만료되었습니다. 파이프라인이 자동으로 재로그인을 시도합니다. 반복 실패 시:

1. 세션 삭제: `rm -rf data/sessions/{account_name}/`
2. `config.yaml`에서 `browser.headless: false`로 일시 변경
3. 파이프라인 실행 후 인터랙티브 챌린지 완료
4. 헤드리스 모드 재활성화

### 파이프라인이 예기치 않게 정지됨

정지 상태와 사유를 확인합니다:

```bash
uv run python -m src halt
```

제한 신호에 의해 트리거되었지만 계정이 정상인 경우 해제합니다:

```bash
uv run python -m src halt resume
```

### "classification_low_confidence"가 빈번하게 나타남

Gemini 모델이 많은 트윗에 대해 불확실합니다. 가능한 원인:

- `config.yaml`의 키워드가 너무 광범위하여 관련 없는 콘텐츠를 끌어옴
- 신뢰도 임계값(0.7)이 사용 사례에 너무 높을 수 있음
- `config.yaml`에서 `classification.confidence_threshold` 조정

### 데이터베이스 연결 오류

PostgreSQL이 실행 중이고 연결 문자열이 올바른지 확인합니다:

```bash
psql $DATABASE_URL -c "SELECT 1"
```

스키마가 없는 경우 파이프라인 시작 시 자동 생성됩니다. 강제 재초기화:

```python
from src.db.repository import Repository
repo = Repository("postgresql://user:pass@localhost:5432/outreach")
repo.init_db()
```

### Playwright 브라우저를 찾을 수 없음

필요한 브라우저를 설치합니다:

```bash
uv run playwright install chromium
```

### "event loop is closed" 테스트 실패

`pytest-asyncio >= 0.24`를 사용하고 `pyproject.toml`에 `asyncio_mode = "auto"`가 설정되어 있는지 확인하세요.

### 데몬 모드에서 높은 메모리 사용량

데몬은 각 주기마다 새 Playwright 브라우저 컨텍스트를 생성하고 이후 닫습니다. 시간이 지남에 따라 메모리가 증가하면:

1. 로그에서 유출된 브라우저 컨텍스트 확인
2. 데몬을 주기적으로 재시작 (macOS에서는 launchd plist가 처리)
3. `python -m src status`로 모니터링

---

## 의존성

### 런타임

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `outreach-shared` | local | 공유 라이브러리 (DB, 브라우저, AI, 유틸리티) |
| `playwright` | >= 1.49 | 브라우저 자동화 |
| `playwright-stealth` | >= 1.0.6 | 봇 탐지 회피 |
| `pydantic` | >= 2.9 | 데이터 검증 |
| `pydantic-settings` | >= 2.7 | 설정 관리 |
| `structlog` | >= 24.4 | 구조화 로깅 |
| `pyyaml` | >= 6.0 | YAML 설정 파싱 |
| `python-dotenv` | >= 1.0 | .env 파일 로딩 |

### 공유 라이브러리 (outreach_shared)

| 패키지 | 용도 |
|--------|------|
| `asyncpg` | 커넥션 풀링을 지원하는 비동기 PostgreSQL 드라이버 |
| `google-genai` | Gemini API 클라이언트 |

### 개발

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `pytest` | >= 8.0 | 테스트 프레임워크 |
| `pytest-asyncio` | >= 0.24 | 비동기 테스트 지원 |
| `pytest-cov` | >= 5.0 | 커버리지 리포팅 |
| `ruff` | >= 0.9 | 린팅 및 포매팅 |
| `mypy` | >= 1.14 | 정적 타입 검사 |
