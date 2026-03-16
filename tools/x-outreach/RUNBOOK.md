# X-Outreach 운영 런북

X (Twitter) 자동 아웃리치 파이프라인 운영 가이드. 일본인 대상 한국 피부과 전문가 계정 운영.

---

## 사전 요구사항

| 항목 | 버전 | 비고 |
|------|------|------|
| Python | 3.13+ | |
| uv | 최신 | 패키지 관리 |
| PostgreSQL | 14+ | 메인 데이터베이스 |
| Playwright | Chromium | 브라우저 자동화 |
| Codex CLI | 최신 | LLM 콘텐츠 생성 (기본) |
| Gemini CLI | 최신 | LLM 폴백 |

---

## 설정

### 환경변수

```bash
cp .env.example .env
# 필수:
# MASTER_A_USERNAME / MASTER_A_PASSWORD  (p01_price - みく)
# MASTER_B_USERNAME / MASTER_B_PASSWORD  (p02_beginner - あや)
# MASTER_C_USERNAME / MASTER_C_PASSWORD  (p03_procedure - りこ)
# MASTER_D_USERNAME / MASTER_D_PASSWORD  (p04_risk - なつみ)
# MASTER_E_USERNAME / MASTER_E_PASSWORD  (p05_lifestyle - ゆい)
# DATABASE_URL=postgresql://localhost:5432/outreach
# GEMINI_API_KEY=...  (SDK 사용 시만 필요, CLI는 불필요)
```

### 페르소나별 설정

`personas/` 디렉토리에 5개 페르소나 정의:

| 계정 | 페르소나 | 전문 분야 | 파일 |
|------|----------|-----------|------|
| master_a | みく | 가격 분석 | `p01_price.md` |
| master_b | あや | 초보자 가이드 | `p02_beginner_guide.md` |
| master_c | りこ | 시술 설명 | `p03_procedure_explainer.md` |
| master_d | なつみ | 리스크/애프터케어 | `p04_risk_care.md` |
| master_e | ゆい | 라이프스타일 | `p05_lifestyle.md` |

### 의존성 설치

```bash
cd tools/x-outreach
uv sync --all-extras
uv run playwright install chromium
```

### 데이터베이스 초기화

```bash
# PostgreSQL DB 생성
createdb outreach

# 마이그레이션 (SQLite에서 전환한 경우)
uv run python scripts/migrate_sqlite_to_pg.py
```

---

## 서비스 시작

### 단일 실행 (테스트용)

```bash
# 드라이런 (실제 게시 없음)
uv run python -m src run --account-id master_b --dry-run

# 실제 파이프라인 실행
uv run python -m src run --account-id master_b
```

### 데몬 모드 (프로덕션)

```bash
# 백그라운드 스케줄러 (2-3시간 간격 자동 실행)
uv run python -m src daemon --account-id master_b

# 전체 페르소나 데몬 (각각 별도 터미널/프로세스)
for id in master_a master_b master_c master_d master_e; do
  uv run python -m src daemon --account-id $id &
done
```

### 프로필 설정 (최초 1회)

```bash
uv run python scripts/setup_profiles.py --account master_b
```

---

## 모니터링

### 파이프라인 상태 확인

```bash
uv run python -m src status
```

### 로그 확인

```bash
# 최근 로그
tail -100 logs/x-outreach.log

# 에러만 필터
grep ERROR logs/x-outreach.log | tail -20

# 특정 페르소나 로그
grep "master_b" logs/x-outreach.log | tail -30
```

### 데이터베이스 조회

```bash
# 오늘 활동 요약
psql outreach -c "
  SELECT account_id, action_type, COUNT(*)
  FROM actions
  WHERE created_at >= CURRENT_DATE
  GROUP BY account_id, action_type
  ORDER BY account_id;
"

# 일일 한도 소진 현황
psql outreach -c "
  SELECT account_id,
    SUM(CASE WHEN action_type='reply' THEN 1 ELSE 0 END) as replies,
    SUM(CASE WHEN action_type='dm' THEN 1 ELSE 0 END) as dms,
    SUM(CASE WHEN action_type='post' THEN 1 ELSE 0 END) as posts
  FROM actions
  WHERE created_at >= CURRENT_DATE
  GROUP BY account_id;
"
```

---

## 긴급 정지

### 즉시 전체 정지

```bash
# 모든 데몬 프로세스 종료
pkill -f "python -m src daemon"

# 확인
ps aux | grep "python -m src" | grep -v grep
```

### 특정 계정만 정지

```bash
# 프로세스 찾기
ps aux | grep "master_b" | grep -v grep

# 해당 PID 종료
kill <PID>
```

### 계정 쿨다운 (DB 레벨)

```bash
# 특정 계정 일시 정지 (쿨다운 시간 강제 설정)
psql outreach -c "
  UPDATE account_pool
  SET cooldown_until = NOW() + INTERVAL '24 hours'
  WHERE account_id = 'master_b';
"
```

---

## 세션 복구

브라우저 세션이 만료된 경우:

```bash
# 1. 해당 계정 데몬 정지
pkill -f "daemon --account-id master_b"

# 2. 기존 세션 데이터 삭제
rm -rf data/sessions/master_b/

# 3. headful 모드로 수동 로그인 (config.yaml: headless: false)
uv run python -m src run --account-id master_b --dry-run
# → 브라우저에서 수동 로그인 → 쿠키 자동 저장

# 4. 데몬 재시작
uv run python -m src daemon --account-id master_b
```

---

## 일반적인 문제 해결

### Playwright 브라우저 오류

```bash
# Chromium 재설치
uv run playwright install chromium --force

# 브라우저 프로세스 정리
pkill -f chromium
```

### PostgreSQL 연결 오류

```bash
# 서비스 상태 확인
pg_isready -h localhost -p 5432

# 커넥션 풀 확인
psql outreach -c "SELECT count(*) FROM pg_stat_activity WHERE datname='outreach';"
```

### 레이트 리밋 도달

`config.yaml` 기준 일일 한도:

| 행동 | 일일 한도 | 간격 |
|------|-----------|------|
| 리플라이 | 20 | 15-20분 |
| DM | 15 | 20-40분 |
| 포스팅 | 3 | 3시간+ |
| 팔로우 | 5 | — |
| 좋아요 | 8 | — |

한도 도달 시 다음 날까지 자동 대기합니다. 강제 리셋 필요 시:

```bash
psql outreach -c "
  DELETE FROM rate_limits
  WHERE account_id = 'master_b' AND date = CURRENT_DATE;
"
```

### LLM 응답 품질 이슈

콘텐츠 생성은 2단계로 동작:
1. **Expert phase**: 한국 피부과 전문 프롬프트 (정확한 정보)
2. **Persona phase**: Codex CLI → Gemini CLI 폴백 (페르소나 톤 적용)

```bash
# Codex CLI 상태 확인
codex --version

# Gemini CLI 폴백 확인
gemini --version
```

---

## 활성 시간대

| 설정 | 값 (JST) |
|------|----------|
| 검색/리플라이/DM | 09:00-22:00 |
| 데몬 활성 | 08:00-23:00 |
| 데몬 간격 | 2-3시간 |
| 주말 | config에 따름 |
