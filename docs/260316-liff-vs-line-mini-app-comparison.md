# LIFF vs LINE MINI App 비교 분석

> jisooknows 프로젝트 관점에서의 의사결정 가이드
> 작성일: 2026-03-16

---

## 한눈에 보는 비교

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| **본질** | LINE 내 웹앱 프레임워크 | LIFF 기반의 검증된 서비스 플랫폼 |
| **기술 기반** | LIFF SDK | LIFF SDK (동일) |
| **코드 변경** | - | 거의 없음 (동일 SDK) |
| **심사** | 없음 | 1~2주 (Verified 기준) |
| **비용** | 무료 | 무료 (심사/인프라 비용 별도) |

---

## 1. 채널 & 설정

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| 채널 유형 | LINE Login 채널 | LINE MINI App 전용 채널 |
| 내부 채널 구조 | 1개 | **3개** (Developing / Review / Published) |
| 채널당 앱 수 | **최대 30개** | **1개만** |
| 리전 제한 | 없음 | **일본, 대만, 태국만** |
| Module Mode | O (액션 버튼 숨김 가능) | **X (액션 버튼 항상 표시)** |
| Endpoint URL | 1개 | **3개** (채널별 별도) |
| Channel Access Token | 1개 | **3개** (채널별 별도) |

### jisooknows 영향
- **LIFF**: 단일 Cloud Run 배포로 충분
- **MINI App**: dev / review / prod 3개 환경 배포 필요 → Cloud Run 서비스 3개 또는 환경변수 분기

---

## 2. 인증 & 동의

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| 로그인 방식 | LINE Login (자동/수동) | LINE Login (자동/수동) - 동일 |
| 동의 화면 | 매번 전체 scope 표시 | **채널 동의 간소화** (최초 1회 후 생략) |
| 간소화 대상 | - | openid 자동, 나머지는 실행 시 요청 |
| 일본 적용 | - | 2026.01.08부터 **자동 적용** |
| `permission.requestAll()` | 사용 불가 | **사용 가능** (MINI App 전용) |

### jisooknows 영향
- **LIFF**: 매번 동의 화면 → 일본 관광객 이탈 가능성
- **MINI App**: 한번 동의하면 다른 MINI App에서도 생략 → **온보딩 마찰 대폭 감소**

---

## 3. 검색 & 발견

| 항목 | LIFF | LINE MINI App (Verified) |
|------|------|--------------------------|
| LINE 검색 노출 | **X** | **O** |
| 홈 탭 "서비스" 노출 | X | **최대 8개** (최근 사용) |
| 검증 배지 | X | **O** |
| Custom Path | X | **O** (`miniapp.line.me/jisooknows`) |
| 홈 화면 바로가기 추가 | X | **O** (`liff.createShortcutOnHomeScreen()`) |
| 즐겨찾기 | X | **O** (일본, LINE 15.18.0+) |
| 외부 브라우저 접근 | LIFF URL로 가능 | **O** (2025.10~ 랜딩 페이지 제공) |
| QR 코드 접근 | O | O |

### jisooknows 영향
- **LIFF**: LINE 채팅/URL 공유로만 유입 → 자체 마케팅 필수
- **MINI App**: LINE 검색에서 "韓国 皮膚科"로 발견 가능 + 홈 화면 추가로 재방문율 증가

---

## 4. 메시징 & 알림

| 항목 | LIFF | LINE MINI App (Verified) |
|------|------|--------------------------|
| `liff.sendMessages()` | O (LIFF 브라우저, chat_message.write) | O (동일) |
| `liff.shareTargetPicker()` | O | O |
| **서비스 메시지** | **X** | **O** (사용자 행동 기반, 최대 5개/행동) |
| 서비스 메시지 템플릿 | - | 채널당 최대 20개, 6개 언어 |
| Push Message | Messaging API 별도 연동 | Messaging API 별도 연동 |

### 서비스 메시지 상세 (MINI App 전용)

```
사용자 행동 → 서비스 메시지 발송 (최대 5개)
예) 예약 완료 → 예약 확인 메시지
    결제 완료 → 결제 확인 메시지
    상담 완료 → 결과 요약 메시지
```

**제한:** 광고/프로모션/할인 정보 발송 금지. 능동적 리마인더(예: "내일 예약 있음")는 서비스 메시지 불가 → Messaging API 필요.

### jisooknows 영향
- **LIFF**: 알림 기능 없음, Official Account Push Message만 가능
- **MINI App**: 예약 확인, 결제 확인, 상담 결과를 서비스 메시지로 자동 발송 → **사용자 경험 대폭 향상**

---

## 5. 결제

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| 외부 결제 연동 | O (Stripe, PayPay 등) | O (동일) |
| LINE Pay | 일본 종료 (2025.04.30) | 일본 종료 |
| 인앱 결제 (IAP) | **X** | **O** (일본, Verified, 디지털 콘텐츠만) |
| LIFF SDK 요구 | - | v2.26.0+ (IAP 사용 시) |

### jisooknows 영향
- 피부과 예약 보증금 = 물리적 서비스 → 인앱 결제 대상 아님
- 두 방식 모두 **Stripe Japan** 등 외부 결제 연동이 현실적
- 결제 자체에는 차이 없음, 단 MINI App은 결제 완료 후 **서비스 메시지 발송 가능**

---

## 6. 프로필 & 편의 기능

| 항목 | LIFF | LINE MINI App (Verified) |
|------|------|--------------------------|
| `liff.getProfile()` | O | O |
| `liff.getFriendship()` | O | O |
| **Quick-fill (프로필 자동입력)** | **X** | **O** (이름, 전화, 이메일, 주소 등 15개 필드) |
| Quick-fill 언어 | - | **일본어만** |
| Quick-fill 요구 | - | Verified + LIFF SDK v2.19.0+ + 사전 신청 |

### jisooknows 영향
- **LIFF**: 예약 시 사용자가 직접 정보 입력
- **MINI App**: Quick-fill로 이름/전화번호/이메일 **자동완성** → 예약 전환율 향상, 일본어 전용이라 일본인 타겟에 최적

---

## 7. UI & 디자인

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| 화면 크기 | Full / Tall / Compact 선택 가능 | Full / Tall / Compact 선택 가능 |
| 액션 버튼 | Module Mode로 **숨기기 가능** | **항상 표시** (숨기기 불가) |
| 커스텀 액션 버튼 | X | **O** (Verified) |
| 멀티탭 뷰 | O | O |
| 로딩 아이콘 | 자유 | **가이드라인 준수 필수** |
| Safe Area | 자유 | **가이드라인 준수 필수** (가로 모드 포함) |
| 아이콘 규격 | 채널 아이콘만 | **130x130px 배경, 54~76px 로고, PNG/JPEG** |

### jisooknows 영향
- **LIFF**: UI 자유도 높음, Module Mode로 풀스크린 경험 가능
- **MINI App**: 액션 버튼 상단 고정 → 상담 채팅 UI 설계 시 고려 필요, 아이콘/로딩 디자인 별도 제작 필요

---

## 8. 개발 & 배포

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| SDK | `@line/liff` | `@line/liff` (동일) |
| Pluggable SDK | O (v2.22.0+) | O (동일) |
| LIFF CLI | O | O |
| 배포 | 자체 서버에 배포 후 URL 등록 | 자체 서버에 배포 후 URL 등록 (동일) |
| **환경 수** | **1개** | **3개** (dev/review/prod) |
| 심사 | **없음** | **1~2주** (Verified) |
| 재심사 | 없음 | 설정 변경 시마다 재심사 |
| 자동 배포 | 즉시 | 승인 후 30일 내 수동 또는 31일째 자동 |

### 재심사 필요 항목 (MINI App)
- 채널 아이콘/이름/설명
- Endpoint URL
- Scope 변경
- 개인정보처리방침/이용약관 URL
- 서비스 메시지 템플릿
- 인앱 결제 설정

### jisooknows 영향
- **LIFF**: 즉시 배포, 빠른 이터레이션 → MVP에 적합
- **MINI App**: 심사 대기 + 3환경 관리 → 초기 셋업 복잡하지만 장기적 이점

---

## 9. 심사 & 정책

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| 심사 여부 | **없음** | **필수** (Verified) |
| 심사 기간 | - | 1~2주 (보장 안됨) |
| 거절 시 | - | 사유 설명 의무 없음, 재제출 가능 |
| 정책 준수 | LIFF 가이드라인 | **LINE MINI App Policy 전체** |
| 금지 업종 | 명시적 제한 없음 | 의약품, 도박, 성인, 종교, 정치 등 |
| 콘텐츠 기준 | 자유 | **전 연령대 적합** 필수 |
| 개인정보처리방침 | 권장 | **필수** (URL 등록) |
| 이용약관 | 권장 | **필수** (URL 등록) |
| 브랜드 가이드 | 없음 | **네이밍 20자, 아이콘 규격** 등 |
| 사전 통보 없는 삭제 | - | **가능** (정책 위반 시) |

### jisooknows 헬스케어 관련 주의

MINI App 정책에서 "미승인 의약품/의료기기"는 금지 업종:
- **허용**: "AI 뷰티 상담", "피부 타입 분석", "스킨케어 추천", "피부과 안내"
- **금지**: "여드름 치료", "피부질환 진단", "의학적 처방"
- 서비스 설명에서 **의료 행위 표현 완전 배제** 필수

---

## 10. 크로스보더 (한국 → 일본)

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| 운영 주체 제한 | 없음 | **일본 법인번호 또는 개인사업자** 필요 |
| 데이터 보호 | LIFF 가이드라인 | **APPI (일본 개인정보보호법)** 준수 필수 |
| 국외 데이터 이전 | 자유 (가이드라인 준수) | **사전 고지 필수** (보호 조치 + 수신국 정보) |
| 언어 요구 | 없음 | 개인정보처리방침/이용약관 **일본어 필수** |

### jisooknows 영향
- **LIFF**: 한국 법인으로 바로 운영 가능
- **MINI App**: **일본 현지 법인 또는 파트너사 필요** → 사업 구조 사전 준비 필수

---

## 11. 성능 기준

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| 로딩 시간 | 제한 없음 (권장만) | **1초 이내 권장, 3초 이내 필수** |
| Lighthouse 점수 | 제한 없음 | **50점 이상 권장** |
| PC 접근 시 | 자유 | **QR 코드로 모바일 전환 표시 권장** |
| 톱 페이지 | 자유 | **리다이렉트 금지, 텍스트만/오류 화면 불가** |

### jisooknows 영향
- **LIFF**: 성능 제약 없음
- **MINI App**: Cold Start 최적화 필수 → Cloud Run `min-instances=1` + Next.js ISR/SSG 활용

---

## 12. 기능 비교 총괄표

| 기능 | LIFF | MINI App (Unverified) | MINI App (Verified) |
|------|:---:|:---:|:---:|
| LINE 내 실행 | O | O | O |
| 외부 브라우저 실행 | O | O | O |
| LINE Login | O | O | O |
| sendMessages | O | O | O |
| shareTargetPicker | O | O | O |
| 채널 동의 간소화 | X | X | **O** |
| 서비스 메시지 | X | X | **O** |
| LINE 검색 노출 | X | X | **O** |
| 검증 배지 | X | X | **O** |
| 홈 화면 추가 | X | X | **O** |
| 즐겨찾기 | X | X | **O** |
| Custom Path | X | X | **O** |
| Quick-fill | X | X | **O** |
| 인앱 결제 | X | X | **O** |
| 커스텀 액션 버튼 | X | O | O |
| Official Account 연동 | O | O | O |
| Module Mode (버튼 숨김) | **O** | X | X |
| 채널당 복수 앱 | **O (30개)** | X | X |
| 심사 없음 | **O** | O | X |

---

## 13. 개발 공수 비교

### LIFF로 진행 시

| 작업 | 예상 공수 |
|------|-----------|
| LIFF SDK 통합 + 초기화 | 0.5일 |
| 인증 브릿지 (LIFF → Firebase Auth) | 1일 |
| 프로필/환경 감지 연동 | 0.5일 |
| sendMessages / shareTargetPicker | 1일 |
| 테스트 & 디버깅 | 1일 |
| **합계** | **~4일** |

### LINE MINI App으로 진행 시

| 작업 | 예상 공수 |
|------|-----------|
| LIFF SDK 통합 + 초기화 | 0.5일 |
| 인증 브릿지 (LIFF → Firebase Auth) | 1일 |
| 프로필/환경 감지 연동 | 0.5일 |
| sendMessages / shareTargetPicker | 1일 |
| 3환경 배포 구성 (dev/review/prod) | 1일 |
| 서비스 메시지 API 연동 + 템플릿 | 2일 |
| 아이콘/로딩 디자인 제작 | 1일 |
| 개인정보처리방침/이용약관 일본어 작성 | 1~2일 |
| 심사 제출 준비 (테스트 시나리오 등) | 1일 |
| 심사 대기 | 1~2주 |
| Quick-fill 연동 (Verified 후) | 0.5일 |
| 홈 화면 추가 연동 | 0.5일 |
| **합계** | **~10일 + 심사 1~2주** |

### 추가 비용 (MINI App)
- 일본 법인/파트너사 확보 (필수)
- 일본어 개인정보처리방침/이용약관 법률 검토
- 아이콘/디자인 에셋 제작

---

## 14. 의사결정 매트릭스

### LIFF를 선택해야 할 때

- MVP를 빠르게 출시하고 싶을 때
- 일본 법인/파트너사가 아직 없을 때
- 심사 없이 즉시 배포하고 이터레이션하고 싶을 때
- Module Mode로 풀스크린 몰입 경험이 중요할 때
- 여러 LIFF 앱을 하나의 채널에서 운영하고 싶을 때

### LINE MINI App을 선택해야 할 때

- 일본 시장에서 **본격적으로** 서비스할 때
- LINE 검색 노출 + 홈 화면 추가가 중요할 때 (= 유기적 유입)
- 서비스 메시지로 예약/결제 확인 알림이 필요할 때
- Quick-fill로 예약 전환율을 높이고 싶을 때
- 브랜드 신뢰도(검증 배지)가 중요할 때
- 장기적으로 LINE 생태계에 깊이 통합하고 싶을 때

---

## 15. jisooknows 권장 전략

### 권장: 2단계 접근

```
Phase 1 (지금)          Phase 2 (일본 법인 확보 후)
──────────────          ─────────────────────────
LIFF로 MVP 출시    →    LINE MINI App으로 전환
- 4일 개발               - 코드 변경 거의 없음
- 즉시 배포               - 추가 기능 연동 (~6일)
- 빠른 검증               - 심사 1~2주
                          - 서비스 메시지 활성화
                          - LINE 검색 노출
                          - Quick-fill
                          - 홈 화면 추가
```

### 이유

1. **코드는 동일** — LIFF SDK 기반이므로 LIFF → MINI App 전환 시 코드 변경 거의 없음
2. **일본 법인 이슈** — MINI App Verified는 일본 법인번호 필요, 아직 없다면 LIFF로 먼저 시작
3. **빠른 시장 검증** — LIFF로 MVP를 먼저 출시하여 일본 관광객 반응 확인
4. **점진적 업그레이드** — 반응이 좋으면 일본 법인 설립 후 MINI App으로 전환하여 서비스 메시지, 검색 노출 등 활성화

### 만약 일본 법인이 이미 있다면

→ **처음부터 LINE MINI App (Verified)으로 시작** 권장
- 코드는 동일하되, 처음부터 3환경 배포 + 심사를 거치면 됨
- 이미 있는 Next.js 앱에 LIFF SDK만 추가
- 서비스 메시지, Quick-fill, 검색 노출 등 처음부터 활용 가능

---

## 16. 전환 시 코드 변경사항

LIFF → LINE MINI App 전환 시 **실제로 바뀌는 것**:

| 항목 | 변경 내용 | 코드 수정 |
|------|-----------|:---------:|
| LIFF ID | 새 MINI App 채널의 LIFF ID로 교체 | 환경변수만 |
| Endpoint URL | 3개 환경별 URL 설정 | 환경변수만 |
| Channel Access Token | 3개 환경별 토큰 | 환경변수만 |
| 서비스 메시지 API | 신규 추가 | **추가 개발** |
| Quick-fill | 신규 추가 | **추가 개발** |
| 홈 화면 추가 | `liff.createShortcutOnHomeScreen()` 호출 | **추가 개발** |
| `permission.requestAll()` | 간소화 동의 활용 | **소규모 수정** |
| 아이콘/디자인 | MINI App 가이드라인 에셋 | 디자인만 |
| 정책 문서 | 개인정보처리방침/이용약관 | 문서만 |
| 배포 파이프라인 | 3환경 CI/CD | 인프라만 |

**핵심: LIFF SDK 코드 자체는 변경 없음. 환경변수 교체 + 추가 기능 연동이 전부.**

---

## 참고

- [LIFF 통합 가이드](./260316-liff-jisooknows-integration-guide.md) — LIFF 전체 문서 분석
- [LINE MINI App 문서](./260316-line-mini-app-jisooknows-documentation.md) — MINI App 전체 문서 분석
- [LIFF Overview](https://developers.line.biz/en/docs/liff/overview/)
- [LINE MINI App Introduction](https://developers.line.biz/en/docs/line-mini-app/discover/introduction/)
