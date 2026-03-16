# Runbook: OpenClaw Obsidian/Korail 운영 명령 모음

## 1) Cron 등록 예시

### Daily Capture (00:30 UTC 기준 예시)
```bash
openclaw cron add \
  --name "obsidian-daily-capture" \
  --cron "30 0 * * *" \
  --session isolated \
  --message "Generate daily Obsidian note: summary/decisions/tasks/mentions into 01-daily/YYYY-MM-DD.md and update 00-inbox/inbox.md" \
  --no-deliver
```

### CEO Morning Brief (07:00)
```bash
openclaw cron add \
  --name "ceo-morning-brief" \
  --cron "0 7 * * *" \
  --session isolated \
  --message "Create CEO brief in 05-reports/ceo-brief/YYYY-MM-DD.md with: yesterday wins, risks, top3 priorities." \
  --announce \
  --channel discord \
  --to "channel:1472227926295445525"
```

### Weekly Review (월요일 08:00)
```bash
openclaw cron add \
  --name "weekly-review" \
  --cron "0 8 * * 1" \
  --session isolated \
  --message "Create weekly report in 05-reports/weekly/YYYY-Www.md with KPI summary and next-week actions." \
  --announce \
  --channel discord \
  --to "channel:1472227926295445525"
```

## 2) 코레일 승인형 워크플로우 메시지 템플릿

### 후보 발견 알림
```text
[Korail Candidate]
서울 -> 부산 | 2026-02-28 07:32 KTX
일반석 1석 발견
명령: approve / skip / halt
```

### 예약 성공 알림
```text
[Korail Booked]
KTX 07:32 서울 -> 부산
예약 성공 ✅
PNR: xxxx
```

### 예약 실패 알림
```text
[Korail Failed]
사유: 좌석 소진
다음 재시도: 90초 후
연속 실패 카운트: 2/10
```

## 3) 운영 점검

```bash
openclaw cron list
openclaw cron runs --id <job-id>
openclaw sessions --active 120
```

## 4) 안전 규칙
- 승인형에서 충분히 검증 전까지 완전자동 예약 금지
- 연속 실패 임계치 도달 시 자동 halt
- 민감정보는 채널에 평문 노출 금지
