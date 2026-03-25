# API Backend Eval Preset

API 백엔드 구현의 품질을 평가하는 루브릭.
`eval-harness` 스킬 및 `live-qa-agent`에서 `eval_type: api` 시 사용.

## 평가 축 (가중치)

### Correctness (40%)

모든 엔드포인트가 스펙대로 작동하는가?

| 점수 | 기준 |
|------|------|
| 9-10 | 모든 엔드포인트 스펙 준수, 에지 케이스 처리, 정확한 상태 코드 |
| 7-8 | 주요 엔드포인트 정상, 사소한 응답 형식 불일치 |
| 5-6 | 핵심 기능 작동하나 일부 엔드포인트 미완성 |
| 3-4 | 여러 엔드포인트 오동작, DB 상태 불일치 |
| 1-2 | 서버 시작 안 됨 또는 대부분 엔드포인트 실패 |

**체크리스트**:
- [ ] 정상 요청 → 올바른 응답 본문 + 상태 코드
- [ ] 잘못된 입력 → 422 Validation Error (Pydantic)
- [ ] 존재하지 않는 리소스 → 404
- [ ] DB 상태가 요청 후 올바르게 변경되는가
- [ ] 페이지네이션이 올바르게 작동하는가

### Robustness (25%)

비정상 상황에서 안전하게 처리하는가?

| 점수 | 기준 |
|------|------|
| 9-10 | 멱등성, 동시성, 대용량 모두 처리 |
| 7-8 | 대부분의 비정상 케이스 처리, 사소한 누락 |
| 5-6 | 기본적 에러 핸들링은 있으나 에지 케이스 미처리 |
| 3-4 | 예외 발생 시 500 에러, 스택 트레이스 노출 |
| 1-2 | 비정상 입력에 서버 크래시 |

**체크리스트**:
- [ ] 중복 생성 요청 → 멱등성 보장 또는 409 Conflict
- [ ] 빈 문자열, null, 초과 길이 입력 처리
- [ ] 동시 요청 시 레이스 컨디션 없음
- [ ] 타임아웃 설정 (외부 API 호출)
- [ ] 500 에러 시 스택 트레이스가 클라이언트에 노출되지 않음

### Security (20%)

인증/인가가 올바르게 적용되는가?

| 점수 | 기준 |
|------|------|
| 9-10 | 완전한 인증/인가, OWASP Top 10 방어, 민감 정보 보호 |
| 7-8 | 인증/인가 올바름, 사소한 보안 개선 여지 |
| 5-6 | 기본 인증은 있으나 인가 세분화 부족 |
| 3-4 | 인증 우회 가능, SQL 인젝션 등 취약점 |
| 1-2 | 인증 없음 또는 하드코딩된 시크릿 |

**체크리스트**:
- [ ] 인증 없는 접근 → 401 Unauthorized
- [ ] 권한 없는 리소스 접근 → 403 Forbidden
- [ ] SQL 인젝션 시도 → 차단 (ORM 사용)
- [ ] 민감 정보(비밀번호, 토큰) → 응답에서 제외
- [ ] CORS 설정이 적절한가
- [ ] Rate limiting이 적용되어 있는가 (API 키 기반)

### Performance (15%)

응답 시간과 리소스 사용이 적절한가?

| 점수 | 기준 |
|------|------|
| 9-10 | P95 < 200ms, 최적화된 쿼리, 캐싱 적용 |
| 7-8 | P95 < 500ms, 대부분 효율적 쿼리 |
| 5-6 | P95 < 1000ms, 일부 비효율 쿼리 |
| 3-4 | P95 > 1000ms, N+1 쿼리 발견 |
| 1-2 | 타임아웃 빈발, 메모리 누수 |

**체크리스트**:
- [ ] N+1 쿼리 없음 (joinedload/selectinload 사용)
- [ ] 풀 테이블 스캔 없음 (인덱스 적용)
- [ ] 불필요한 데이터 로딩 없음 (필요한 필드만 선택)
- [ ] 리스트 조회에 페이지네이션 적용

## 합격 기준

```
가중 평균 = (Correctness × 0.40) + (Robustness × 0.25) + (Security × 0.20) + (Performance × 0.15)

PASS: 가중 평균 ≥ 7.0
FAIL: Correctness에서 critical 항목 FAIL
FAIL: Security 이슈 발견 (심각도 무관)
FAIL: 서버 시작 불가
```

## 검증 방법

### API 직접 호출
```bash
# Playwright evaluate 또는 curl/httpie
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password"}'

# 상태 코드 확인
# 응답 본문 검증
# 헤더 검증 (Content-Type, CORS 등)
```

### DB 상태 검증
```bash
# SQLite
sqlite3 app.db "SELECT * FROM users WHERE email='test@test.com'"

# PostgreSQL
psql -c "SELECT * FROM users WHERE email='test@test.com'"
```

## 출력 형식

```markdown
## API Backend Evaluation

| Axis | Score | Weight | Weighted |
|------|-------|--------|----------|
| Correctness | 8 | 40% | 3.20 |
| Robustness | 7 | 25% | 1.75 |
| Security | 9 | 20% | 1.80 |
| Performance | 7 | 15% | 1.05 |
| **Total** | | | **7.80** |

**Result**: PASS

### Endpoint Results
| Method | Path | Status | Details |
|--------|------|--------|---------|
| POST | /auth/login | PASS | 200 OK, JWT 반환 |
| POST | /auth/login | PASS | 401, 잘못된 비밀번호 |
| GET | /auth/me | PASS | 200 OK, 사용자 정보 |
| GET | /auth/me | PASS | 401, 토큰 없음 |
```
