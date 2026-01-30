# Troubleshooting Guide Template

## Structure

```markdown
# [서비스/기능명] Troubleshooting Guide

| 속성 | 값 |
|------|-----|
| 🏷️ 태그 | Troubleshooting, Debug |
| 👤 담당자 | @name |
| 📅 상태 | 작성중 / 배포됨 |
| 📆 최종수정 | YYYY-MM-DD |

## Quick Reference

| 증상 | 가능한 원인 | 바로가기 |
|------|------------|----------|
| 앱이 시작되지 않음 | 환경변수 누락 | [#startup-error](#startup-error) |
| API 응답 없음 | 네트워크/타임아웃 | [#api-timeout](#api-timeout) |
| 로그인 실패 | 토큰 만료 | [#auth-error](#auth-error) |

## Common Issues

### 🚨 Startup Error {#startup-error}

**증상**
- 앱 실행 시 즉시 종료
- "Configuration error" 메시지 출력
- 화이트 스크린 후 크래시

**원인**
환경변수가 설정되지 않았거나 잘못된 값이 입력됨

**진단**
```bash
# 환경변수 확인
echo $API_KEY
cat .env
```

**해결**
1. `.env` 파일 존재 여부 확인
2. 필수 환경변수 설정:
   ```bash
   # .env
   API_KEY=your_api_key
   DATABASE_URL=postgres://...
   ```
3. 앱 재시작

✅ 해결 확인: 앱이 정상적으로 시작되고 로그에 "Server started" 출력

▶️ 관련 로그 예시
   ```
   [ERROR] ConfigurationException: API_KEY is not defined
   at Config.validate (config.js:42)
   at App.init (app.js:15)
   ```

💡 개발 환경에서는 `.env.development`가 우선 적용됩니다.

---

### ⚠️ API Timeout {#api-timeout}

**증상**
- API 호출 후 응답 없음
- 30초 후 타임아웃 에러
- "Connection timed out" 메시지

**원인**
1. 네트워크 연결 문제
2. 서버 과부하
3. 방화벽 차단

**진단**
```bash
# 연결 테스트
curl -v https://api.example.com/health

# DNS 확인
nslookup api.example.com

# 포트 확인
telnet api.example.com 443
```

**해결**

| 원인 | 해결 방법 |
|------|----------|
| 네트워크 | VPN 연결 확인, 프록시 설정 확인 |
| 서버 과부하 | 잠시 후 재시도, 관리자 문의 |
| 방화벽 | IT팀에 포트 오픈 요청 |

✅ 해결 확인: `curl` 명령어로 200 응답 수신

---

### 🔐 Auth Error {#auth-error}

**증상**
- 로그인 후 즉시 로그아웃
- "401 Unauthorized" 에러
- "Token expired" 메시지

**원인**
- 토큰 만료
- 토큰 형식 오류
- 서버 시간 불일치

**진단**
```bash
# 토큰 디코딩 (JWT)
echo $TOKEN | cut -d'.' -f2 | base64 -d
```

**해결**
1. 토큰 재발급:
   ```bash
   curl -X POST https://api.example.com/auth/refresh \
     -H "Authorization: Bearer $REFRESH_TOKEN"
   ```
2. 시간 동기화:
   ```bash
   sudo ntpdate -s time.google.com
   ```

⚠️ Refresh Token도 만료된 경우 재로그인 필요

---

## Error Code Reference

| 코드 | 메시지 | 원인 | 해결 |
|------|--------|------|------|
| E001 | Config not found | 설정 파일 누락 | `.env` 파일 생성 |
| E002 | DB connection failed | DB 연결 실패 | 연결 문자열 확인 |
| E003 | Invalid token | 토큰 검증 실패 | 토큰 재발급 |

## Escalation Guide

문제가 해결되지 않을 경우:

1. **Level 1**: 본 문서로 자가 해결 시도
2. **Level 2**: 팀 Slack 채널 `#tech-support`
3. **Level 3**: 담당자 직접 멘션 @oncall
4. **Level 4**: 긴급 연락처 (장애 상황)

🚨 프로덕션 장애는 Level 3부터 시작하십시오.

## Logs & Debugging

### 로그 위치

| 환경 | 위치 |
|------|------|
| Local | `./logs/app.log` |
| Docker | `docker logs <container>` |
| Cloud | Cloud Logging 콘솔 |

### 디버그 모드 활성화

```bash
# 환경변수로 설정
DEBUG=true npm start

# 또는 플래그로
flutter run --debug
```

---
📝 **유지보수 노트**
- 새로운 에러 패턴 발견 시 추가
- 에러 코드 변경 시 업데이트
- 분기별 검토 권장
```

## Key Elements

1. **Quick Reference 테이블**: 증상으로 빠르게 찾기
2. **일관된 구조**: 증상 → 원인 → 진단 → 해결 → 확인
3. **진단 명령어**: 복사 가능한 코드 블록
4. **해결 확인**: 정상 상태 정의
5. **에스컬레이션**: 자가 해결 불가 시 경로
6. **에러 코드 테이블**: 코드별 빠른 참조
