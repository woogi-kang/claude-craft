# Clinic Consult 운영 런북

외국인 환자 한국 피부과 예약 자동화 시스템의 운영 가이드.

---

## 사전 요구사항

| 항목 | 버전 | 비고 |
|------|------|------|
| Python | 3.13+ | |
| uv | 최신 | 패키지 관리 |
| SQLite | 기본 내장 | WAL 모드 사용 |
| LDPlayer | 9.x | Android 에뮬레이터 |
| Anthropic API 키 | — | `.env`에 설정 |
| OpenAI API 키 | — | 폴백용 (선택) |

---

## 설정

### 환경변수

```bash
cp .env.example .env
# 필수 키 설정:
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...  (폴백용)
```

### 설정 파일

`config.yaml`에서 주요 파라미터를 조정:

```yaml
# 에뮬레이터 연결
emulator:
  serial: "127.0.0.1:5555"

# LLM 설정 (Claude → OpenAI → Ollama 폴백)
llm:
  default_provider: "claude"
  claude_model: "claude-sonnet-4-20250514"

# 데이터베이스
database:
  path: "data/consult.db"

# 예약 시스템
reservation:
  hospitals_db: "../../data/clinic-results/hospitals.db"
```

### 의존성 설치

```bash
cd tools/clinic-consult
uv sync --all-extras
```

---

## 서비스 시작

### 인바운드 봇 (카카오톡 모니터링)

```bash
uv run python -m src
```

### 아웃바운드 예약 시스템 (웹 대시보드)

```bash
uv run python src/reserve.py
# 대시보드: http://127.0.0.1:8000
```

### 에뮬레이터 연결 확인

```bash
# LDPlayer가 실행 중인지 확인
adb devices
# 예상 출력: 127.0.0.1:5555  device
```

---

## 헬스 체크

```bash
# 프로세스 확인
ps aux | grep "python -m src"

# 로그 확인 (최근)
tail -50 logs/clinic-consult.log

# DB 상태 확인
sqlite3 data/consult.db "SELECT COUNT(*) FROM reservations WHERE status='active';"

# 에뮬레이터 연결 상태
adb -s 127.0.0.1:5555 shell getprop ro.build.version.sdk

# 웹 대시보드 응답 확인
curl -s http://127.0.0.1:8000/health
```

---

## 일반적인 문제 해결

### 에뮬레이터 연결 실패

```bash
# ADB 서버 재시작
adb kill-server && adb start-server

# LDPlayer 포트 확인
adb connect 127.0.0.1:5555
```

### LLM API 오류

```bash
# API 키 유효성 확인
python -c "import anthropic; c=anthropic.Anthropic(); print(c.models.list())"

# 폴백 체인 확인: Claude → OpenAI → Ollama
# Ollama 로컬 서버 상태
curl http://localhost:11434/api/tags
```

### 카카오톡 UI 요소 인식 실패

```bash
# 현재 화면 덤프
uv run python -c "import uiautomator2 as u2; d=u2.connect('127.0.0.1:5555'); print(d.dump_hierarchy())"

# selectors.py에서 KAKAO/LINE 셀렉터 확인
```

### 예약 상태 이상

```bash
# 특정 예약 상태 확인
sqlite3 data/consult.db "SELECT id, status, updated_at FROM reservations ORDER BY updated_at DESC LIMIT 10;"

# stuck 상태 예약 리셋 (주의: 수동 확인 후 실행)
sqlite3 data/consult.db "UPDATE reservations SET status='pending' WHERE status='greeting' AND updated_at < datetime('now', '-2 hours');"
```

---

## 데이터베이스 백업/복원

### 백업

```bash
# SQLite 온라인 백업 (서비스 중단 불필요)
sqlite3 data/consult.db ".backup data/backups/consult-$(date +%Y%m%d-%H%M%S).db"

# 또는 파일 복사 (WAL 포함)
cp data/consult.db data/consult.db-wal data/backups/
```

### 복원

```bash
# 서비스 중지 후 복원
pkill -f "python -m src"
cp data/backups/consult-YYYYMMDD-HHMMSS.db data/consult.db
# 서비스 재시작
uv run python -m src
```

### 데이터 내보내기

```bash
# CSV 내보내기 (웹 대시보드에서도 가능)
sqlite3 -header -csv data/consult.db "SELECT * FROM reservations;" > data/exports/reservations.csv
```

---

## 레이트 리밋 참고

`config.yaml` 기준:

| 항목 | 제한 |
|------|------|
| 시간당 응답 | 30 |
| 일일 응답 | 200 |
| 최소 응답 간격 | 10초 |
| 활성 시간대 | 09:00-22:00 KST |
| 주말 | 비활성 |
