# LINE MINI App 완전 문서 - jisooknows AI 뷰티 상담 챗봇

> **작성일**: 2026-03-16
> **대상 서비스**: jisooknows (Next.js 16, GCP Cloud Run, Firebase Auth, 일본인 관광객 대상 한국 피부과 상담)
> **공식 문서 기반**: LINE Developers 공식 문서 전체 페이지 분석 완료
> **LINE MINI App Policy 최종 개정일**: 2026년 2월 19일

---

## 목차

1. [LINE MINI App 개요](#1-line-mini-app-개요)
2. [LIFF vs LINE MINI App 핵심 차이점](#2-liff-vs-line-mini-app-핵심-차이점)
3. [기술 사양](#3-기술-사양)
4. [채널 생성 및 구성](#4-채널-생성-및-구성)
5. [3개 내부 채널 아키텍처](#5-3개-내부-채널-아키텍처)
6. [개발 개요 및 절차](#6-개발-개요-및-절차)
7. [콘솔 설정 상세](#7-콘솔-설정-상세)
8. [인증 플로우 및 Channel Consent Simplification](#8-인증-플로우-및-channel-consent-simplification)
9. [UI 컴포넌트 구조](#9-ui-컴포넌트-구조)
10. [빌트인 기능](#10-빌트인-기능)
11. [커스텀 기능](#11-커스텀-기능)
12. [서비스 메시지](#12-서비스-메시지)
13. [결제 처리](#13-결제-처리)
14. [퍼머넌트 링크](#14-퍼머넌트-링크)
15. [홈 화면 추가](#15-홈-화면-추가)
16. [커스텀 경로](#16-커스텀-경로)
17. [외부 브라우저 지원](#17-외부-브라우저-지원)
18. [Common Profile Quick-fill](#18-common-profile-quick-fill)
19. [디자인 가이드라인](#19-디자인-가이드라인)
20. [성능 가이드라인](#20-성능-가이드라인)
21. [개발 가이드라인 (필수 준수)](#21-개발-가이드라인-필수-준수)
22. [심사 제출 프로세스](#22-심사-제출-프로세스)
23. [LINE MINI App 정책 (금지사항)](#23-line-mini-app-정책-금지사항)
24. [서비스 운영](#24-서비스-운영)
25. [업데이트 후 재심사](#25-업데이트-후-재심사)
26. [광고 게재](#26-광고-게재)
27. [인앱 결제 (일본 전용)](#27-인앱-결제-일본-전용)
28. [LINE Official Account 연동](#28-line-official-account-연동)
29. [웹앱을 MINI App으로 전환하기](#29-웹앱을-mini-app으로-전환하기)
30. [jisooknows 적용 시 핵심 고려사항](#30-jisooknows-적용-시-핵심-고려사항)

---

## 1. LINE MINI App 개요

LINE MINI App은 **LINE 앱 내에서 실행되는 웹 애플리케이션**이다. 사용자는 별도의 네이티브 앱 설치 없이 LINE을 통해 서비스에 접근할 수 있다.

### 핵심 특성
- **HTML5 기반**: 거의 모든 HTML5 사양을 사용 가능
- **LIFF 기반 구현**: LINE Front-end Framework(LIFF)를 사용하여 개발
- **별도 앱 설치 불필요**: LINE 앱 내에서 바로 동작
- **LINE 로그인 통합**: LINE 계정을 통한 자동 로그인
- **서비스 메시지**: LINE 채팅방으로 사용자에게 알림 전송 가능

### 사용자 접근 경로

**LINE 외부에서 접근:**
- 퍼머넌트 링크
- QR 코드
- 홈 화면 바로가기

**LINE 내부에서 접근:**
- LINE Official Account (리치 메뉴, 리치 메시지)
- 홈 탭 (서비스 섹션 - 최근 사용한 앱 8개 표시)
- 검색 기능
- 메시지 공유

### 2단계 분류 체계

| 구분 | 미인증 MINI App | 인증 MINI App |
|------|----------------|---------------|
| 상태 | 인증 심사 미통과 | 인증 심사 통과 |
| 배지 | 없음 | 인증 배지 표시 |
| 서비스 메시지 | 불가 | 가능 |
| 커스텀 경로 | 불가 | 가능 |
| 홈 화면 바로가기 | 불가 | 가능 |
| Quick-fill | 불가 | 가능 |
| 결제 시스템 | 가능 | 가능 |
| 커스텀 액션 버튼 | 가능 | 가능 |
| Official Account 친구 추가 유도 | 가능 | 가능 |

---

## 2. LIFF vs LINE MINI App 핵심 차이점

### 기능적 차이

| 항목 | 일반 LIFF 앱 | LINE MINI App |
|------|-------------|---------------|
| Module 모드 | 사용 가능 | **사용 불가** |
| 같은 채널에 여러 LIFF 앱 | 가능 | **불가** (채널당 1개) |
| 서비스 메시지 | 없음 | 인증 앱에서 사용 가능 |
| Channel Consent 간소화 | 없음 | 일본 리전에서 자동 적용 |
| 인증 심사 | 없음 | LY Corporation 심사 필요 |
| 인증 배지 | 없음 | 인증 앱에 표시 |
| 홈 화면 추가 | 없음 | 인증 앱에서 가능 |
| 커스텀 경로 URL | 없음 | 인증 앱에서 가능 |
| Quick-fill 자동 입력 | 없음 | 인증 앱에서 가능 |
| 헤더 표시 | LIFF 기본 헤더 | LINE MINI App 전용 헤더 |
| URL 도메인 | liff.line.me | **miniapp.line.me** |

### 아키텍처적 차이
- LINE MINI App 채널 생성 시 **3개의 내부 채널이 자동 생성** (Developing, Review, Published)
- 일반 LIFF는 이런 구조 없음
- LINE MINI App은 LIFF SDK v2.1 이상 필수
- Module 모드(액션 버튼 숨기기) 설정 불가
- 채널당 추가 LIFF 앱 생성 불가

> **중요**: LINE은 향후 LIFF와 LINE MINI App 간 통합 계획이 있으므로, 신규 개발 시 LINE MINI App으로 만드는 것을 권장한다.

---

## 3. 기술 사양

### 개발 기반
- **LIFF(LINE Front-end Framework)** 기반 개발
- **최소 LIFF SDK 버전**: v2.1 (v2.1.x 시리즈의 모든 LIFF API 접근 가능)
- Channel Consent Simplification 사용 시: **v2.13.x 이상** 필수
- Quick-fill 사용 시: **v2.19.0 이상** 필수
- 인앱 결제 사용 시: **v2.26.0 이상** 필수

### HTML5 지원
- 거의 모든 HTML5 사양 사용 가능
- **Geolocation API**: 위치 기반 서비스 가능
- **Map API**: Google Maps API 호환
- **미디어 요소**: 표준 HTML5 미디어/이미지 포맷
- 호환성 확인: caniuse.com 참고

### 플랫폼 지원
- LIFF의 "권장 운영 환경"과 동일
- iOS / Android LINE 앱 내부
- **2025년 10월부터**: 외부 브라우저에서도 접근 가능
- 버전은 사전 고지 없이 변경될 수 있음

### 지원 리전
채널 생성 시 선택 가능한 리전:
- **일본** (Japan)
- **태국** (Thailand)
- **대만** (Taiwan)

> **리전별 별도 채널 필요**: 각 리전마다 별도의 채널을 생성해야 한다.

---

## 4. 채널 생성 및 구성

### 전제 조건
- LINE Developers Console 계정
- LINE MINI App Policy의 "허용된 고객" 자격
- 비즈니스 ID (LINE Developers Console 접근용)

### 채널 생성 필수 필드

| 필드 | 설명 | 주의사항 |
|------|------|---------|
| Channel Type | "LINE MINI App" 선택 | 필수 |
| Region | Japan, Thailand, Taiwan 중 선택 | **생성 후 변경 불가** (리전별 별도 채널) |
| Channel Name | 서비스명 | "LINE" 또는 유사 문자열 포함 불가, **20자 제한** |
| Channel Description | 서비스 설명 | 개발사와 서비스 제공사가 다르면 반드시 명시 |
| Email Address | 채널 업데이트 수신 | 필수 |
| Privacy Policy URL | 개인정보처리방침 | 인증 제공자 필수; 기타는 생성 후 설정 |

### 필수 동의 약관
- LINE Developers Agreement
- LINE MINI App Platform Agreement
- LINE MINI App Policy
- (태국의 경우) LY Corporation Privacy Policy

### 핵심 제약사항

> **경고**: "채널을 생성하면 다른 Provider로 이동할 수 없다." 서로 다른 Provider에서는 사용자에게 다른 ID가 부여되므로, Provider 간 사용자 식별이 불가능하다.

### 채널 이름 규칙 (정책 기반)
- 기존 네이티브 앱이나 웹사이트가 있으면 해당 이름과 일치시킬 것
- 회사명/브랜드명/서비스명이 다르면 사용자에게 가장 친숙한 이름 사용
- 여러 앱의 경우 매장별 등 구분되는 이름 사용
- 서비스를 식별하는 고유명사 사용 (단순한 보통명사 "대기", "주문" 금지)
- "LINE"을 LY Corporation 연관으로 오해되도록 사용 금지
- **20자 제한** (초과 시 "..."으로 표시)

---

## 5. 3개 내부 채널 아키텍처

LINE MINI App 채널 생성 시 자동으로 3개의 내부 채널이 생성된다:

### 5.1 Developing Channel (개발 채널)
- **용도**: 개발 및 테스트 환경
- **상태**: 항상 "Developing"
- **관리자 접근**: 권한 부여된 관리자만
- **사용자 접근**: 권한 부여된 테스터만
- **설정 확인**: LINE MINI App 채널 설정 화면에서

### 5.2 Review Channel (심사 채널)
- **용도**: LY Corporation 인증 심사용
- **상태**: 항상 "Developing"
- **관리자 접근**: 관리자 + LY Corporation 심사자
- **사용자 접근**: LY Corporation 심사자만

### 5.3 Published Channel (출시 채널)
- **용도**: 실제 사용자에게 공개되는 서비스
- **상태**: 항상 "Published"
- **관리자 접근**: 관리자 ("Published Data" 버튼으로 확인)
- **사용자 접근**: 일반 사용자
- **채널 상태 변경 불가**

### 각 채널별 필수 구성
- 각 내부 채널마다 **고유한 LIFF ID** 존재
- 각 채널마다 **별도의 Endpoint URL** 배포 필요
- 각 채널마다 **별도의 Channel Access Token** 발행 필요

### 설정 반영 방식

**미인증 MINI App의 경우:**
- Developing 채널 변경 시 Published 채널에 **자동 반영**
- 단, 서비스 메시지 템플릿과 Channel Consent Simplification은 인증 승인 필요

**인증 MINI App의 경우:**
- Developing 변경은 Developing 채널에만 영향
- Review 채널: 심사 시작 시 설정 복사
- Published 채널: 출시 시 설정 복사

### 헤더 서브텍스트 표시 차이
- Developing/Review: 항상 도메인 표시
- Published 미인증: 도메인 표시
- Published 인증: **앱 이름 + 인증 배지** 표시

---

## 6. 개발 개요 및 절차

### 개발 전 필수 확인 사항
1. **사양 확인**: 기술 능력 및 제약
2. **디자인 가이드라인**: 아이콘 사양, 가로 모드 안전 영역, 로딩 아이콘
3. **성능 요구사항**: 최적화 기준
4. **제출 요구사항**: 심사 및 정책 준수

### 개발 6단계 절차

#### 1단계: LINE MINI App 채널 생성
- LINE Developers Console 접속
- Channels > Create a new channel > LINE MINI App 선택
- 필수 필드 입력 및 약관 동의

#### 2단계: LIFF SDK 로드
CDN 방식:
```html
<script charset="utf-8" src="https://static.line-scdn.net/liff/edge/2/sdk.js"></script>
```
또는 npm 패키지 설치

#### 3단계: LIFF 앱 초기화
```javascript
liff.init({ liffId: "123456-abcdefg" })
  .then(() => { /* LIFF API 사용 */ })
  .catch((err) => { console.log(err.code, err.message); });
```

#### 4단계: 필수 기능 구현
- LIFF API 활용 (사용자 프로필, 인증 토큰 등)
- 서비스 메시지 구현 (서버 사이드)
- HTML5 기능 활용

#### 5단계: Endpoint URL 설정
- 웹앱 URL을 LINE MINI App 채널 설정에 등록
- 각 내부 채널마다 별도 URL 필요

#### 6단계: 심사 요청
- 미인증 또는 인증 MINI App으로 출시
- 인증 상태는 LY Corporation 심사 필요

### Basic Authentication (출시 전 접근 제한)
- **사용 가능 조건**: "Not yet reviewed" 또는 "Reviewing" 상태 앱
- **범위**: LIFF 브라우저에서만 동작
- **설정**: Web app settings에서 Basic Auth 자격 증명 포함 Endpoint URL 설정
- **제한**: LIFF-to-LIFF 전환 시 사용 불가
- **Digest 인증 미지원**

> **경고**: "Basic authentication은 단순한 접근 제한용 인증 방식이다. 개발자는 보안 요구사항을 자체적으로 평가하고 판단해야 한다."

### Channel Access Token
- **Stateless channel access token 사용 권장** (Long-lived 토큰 미지원)
- 각 내부 채널별로 별도 토큰 발행
- Channel ID와 Channel Secret은 "Channel basic settings" 탭에서 확인
- **Developing 채널 토큰을 Review/Published 서비스 메시지에 사용 금지**

---

## 7. 콘솔 설정 상세

### Provider 설정
- **Provider 이름**: 인증 화면 및 채널 동의 화면에 표시

### Basic Settings 탭

**Channel Icon:**
- 액션 버튼, 멀티탭 뷰, 인증 화면, 동의 화면, 서비스 메시지 푸터, 바로가기 추가 화면에 표시
- 사양: 130x130px 배경, 54~90px 로고 (권장 54~76px)
- 포맷: PNG 또는 JPEG만 허용

**Channel Name:**
- 모든 UI 터치포인트에 표시
- **영문으로 입력 필수**; 다른 언어는 로컬라이제이션으로 설정
- "LIFF app name으로 자동 복사됨"

**Channel Description:**
- 인증 및 동의 화면에 표시
- **영문으로 입력 필수**; 로컬라이제이션으로 다국어 지원
- 외주 개발 시 반드시 명시: 서비스 회사명, 개발 회사명, 실제 데이터 수신 주체

**Privacy Policy URL:**
- 채널 동의 화면에 표시

**Localization (다국어 지원):**
- 사용자의 LINE 언어 설정에 따라 표시
- 로컬라이제이션 미설정 시 영문 기본 표시

> **중요**: "서비스를 제공하는 국가의 주요 언어로 반드시 로컬라이제이션하라."

### Web App Settings 탭
- **Endpoint URL**: 바로가기 추가 화면 및 액션 버튼에 표시
- LIFF 앱 추가 불가 (기본 LINE MINI App만)
- 스코프, 친구 추가 옵션을 LIFF 앱별로 설정 불가
- Module 모드 설정 불가

### 사용자 대면 화면별 표시 정보

| 화면 | 표시 정보 |
|------|----------|
| 액션 버튼 | 앱 이름, 아이콘 |
| 멀티탭 뷰 | 이름, 아이콘 |
| 인증 화면 | 아이콘, 이름, Provider 이름, 설명 |
| 채널 동의 화면 | 아이콘, 이름, Provider 이름, 설명, 개인정보처리방침 URL, 인증 배지(인증 앱) |
| 서비스 메시지 | 푸터에 이름, 아이콘 |
| 바로가기 추가 화면 | 이름, 아이콘, Endpoint URL |

---

## 8. 인증 플로우 및 Channel Consent Simplification

### Channel Consent Simplification이란?
사용자가 **한 번만 동의**하면 다른 LINE MINI App에 처음 접근할 때 채널 동의 화면이 **생략**되는 기능이다. `openid` 스코프(사용자 ID 조회)만 간소화 대상이며, 추가 스코프는 별도 인증 화면이 필요하다.

### 설정 요건
- **서비스 리전**: "Japan"으로 설정된 경우에만 사용 가능
- **채널 상태**: "Not yet reviewed"
- **2026년 1월 8일 이후 생성된 채널**: 자동 활성화
- **이전 생성 채널**: Web app settings 탭에서 수동 토글

### 동작 조건
- 인증 MINI App 상태
- **LIFF SDK v2.13.x 이상**
- LIFF-to-LIFF 전환으로 열린 경우 동작하지 않음

### 2단계 인증 플로우 (활성화 시)

**1단계: 간소화 동의 화면**
- `openid` 스코프에 대한 권한 요청
- "동의" 탭: 모든 MINI App에 대해 동의 부여
- "지금은 안함" 선택: 24시간 동안 건너뛰고, 이후 개별 채널 동의 화면으로 복귀

**2단계: 추가 스코프 인증 화면**
- `liff.getProfile()`, `liff.sendMessages()` 등 실행 시 표시
- `profile`, `chat_message.write` 등 추가 스코프 권한 요청

### 스코프-메서드 매핑

| 스코프 | 관련 메서드 |
|--------|-----------|
| `email` | `getIDToken()`, `getDecodedIDToken()` |
| `profile` | `getProfile()`, `getFriendship()` |
| `chat_message.write` | `sendMessages()` |

### 권한 조회 및 요청 API
- `liff.permission.query()`: 권한 상태 확인
- `liff.permission.requestAll()`: 앱 시작이 아닌 최적 시점에 인증 화면 트리거

### 친구 추가 옵션 주의사항
스코프에 `openid`만 지정하면 인증/동의 화면이 표시되지 않아 친구 추가 유도가 불가능하다. 추가 스코프를 포함하여 화면이 표시되도록 권장.

### 비활성화 시 동작
전통적인 채널 동의 화면이 표시되며, 요청된 모든 권한이 첫 접근 시 나열된다.

---

## 9. UI 컴포넌트 구조

LINE MINI App 페이지는 **(A) 헤더**와 **(B) 바디**로 구성된다.

### 헤더 컴포넌트 (플랫폼 네이티브, LINE이 자동 생성)

| 요소 | 설명 |
|------|------|
| 서비스 이름 | 페이지의 `<title>` 요소에서 가져옴. 폰트 커스터마이즈 불가 |
| 서브텍스트 | 미인증: 도메인 표시 / 인증: MINI App 이름 + 인증 배지 |
| 액션 버튼 | LINE 15.12.0+: 멀티탭 뷰 / 이전 버전: 옵션 표시 |
| 닫기/최소화 버튼 | iOS <14.15.1, Android <15.0.0: 닫기 / 이후 버전: 미인증=닫기, 인증=최소화 |
| 뒤로 가기 버튼 | 이전 페이지로 이동 |
| 로딩 바 | 페이지 로드 진행 상황 표시 |

### 바디 섹션
- WebView 기술 사용
- HTML5 및 LIFF로 서비스 개발

---

## 10. 빌트인 기능

### 10.1 액션 버튼
- 모든 페이지의 공통 헤더에 기본 표시
- **숨길 수 없음** (Module 모드 설정 불가)
- LINE 15.12.0+: 멀티탭 뷰 표시
- 이전 버전: 옵션 표시

### 10.2 멀티탭 뷰
액션 버튼 탭 시 표시되는 기능 목록:

| 기능 | 상세 | 요구사항 |
|------|------|---------|
| 새로고침 | 현재 페이지 리로드 | - |
| 공유 | LIFF URL/퍼머넌트 링크를 LINE 메시지로 배포 | - |
| 홈에 추가 | 디바이스 홈 화면 바로가기 생성 | 인증 MINI App + LINE 14.3.0+ |
| 즐겨찾기 | MINI App 즐겨찾기 추가 | 인증 + **일본 리전** + LINE 15.18.0+ |
| 브라우저 최소화 | LIFF 브라우저 축소 | 인증 MINI App만 |
| 권한 설정 | 카메라/마이크 접근 관리 | LINE 14.6.0+ |
| 서비스 정보 | Provider 페이지 열기 | 인증 MINI App만 |
| 신고 | 문의 양식 외부 실행 | **일본 리전** + LINE 15.6.0+ |

### 10.3 최근 사용 서비스
- 최대 50개의 이전 접근 MINI App/LIFF 앱 표시
- 최근 사용 순으로 정렬
- 빠른 재접근 가능

---

## 11. 커스텀 기능

### 기능 가용성 매트릭스

| 기능 | 미인증 | 인증 |
|------|--------|------|
| 서비스 메시지 | ❌ | ✅ |
| 커스텀 경로 | ❌ | ✅ |
| 홈 화면 바로가기 | ❌ | ✅ |
| Official Account 친구 추가 유도 | ✅ | ✅ |
| 결제 시스템 | ✅ | ✅ |
| 커스텀 액션 버튼 | ✅ | ✅ |
| Common Profile Quick-fill | ❌ | ✅ |

### 커스텀 액션 버튼 구현
- 헤더의 빌트인 액션 버튼 대신 바디에 커스텀 버튼 배치
- Share Target Picker를 통해 친구/그룹 선택 UI 표시
- **Flex Message Bubble 컨테이너만 사용** (Carousel 불가)

**커스텀 공유 메시지 구조:**
- (A) 이미지 - 선택사항 (높이 <= 너비 x 2)
- (B) 제목 - 필수 (최대 2줄)
- (C) 부제목 - 선택사항 (최대 2줄)
- (D) 상세 - 선택사항 (최대 10항목 / 이미지 목록 타입은 5항목)
- (E) 버튼 - 필수 (최대 3개, 첫 번째는 primary 스타일)
- (F) 푸터 - 필수 (앱 아이콘, 이름, 네비게이션 버튼)

> 부제목 또는 상세 섹션 중 하나는 반드시 포함해야 한다.

### URL 형식 변경 (2023.12.13 이후)
- 이전: `https://liff.line.me/{liffId}`
- 이후: `https://miniapp.line.me/{liffId}`
- 이전 URL도 여전히 동작하지만 업데이트 권장

---

## 12. 서비스 메시지

### 개요
사용자가 LINE MINI App 내에서 수행한 액션에 대한 확인/응답으로 알림을 전송하는 기능.

### 접근 요건
- **인증 MINI App만** 사용 가능 (미인증은 개발 채널에서만 테스트)
- Admin 또는 Tester 권한 필요 (개발 중)

### 허용 사용 사례
- 레스토랑/숙소 예약 확인
- 티켓/상품 구매 확인
- 체크인 완료 알림
- 주문 배송 알림
- 구매한 티켓의 이벤트 리마인더

### 금지 사항
> **"광고 및 이벤트 알림(할인, 쇼핑 리워드, 신제품, 할인 쿠폰, 프로모션 포함)은 전송 불가"**

### 리전별 표시 위치

| 리전 | 채팅방 이름 |
|------|-----------|
| 일본 | LINEミニアプリ お知らせ |
| 태국 | LINE MINI App Notice |
| 대만 | LINE MINI App 通知 |

### 메시지 템플릿
- 카테고리별 정리 (매장 예약, 대기열 관리, 배송 알림 등)
- **6개 언어 지원**: 일본어, 영어, 중국어 번체, 태국어, 인도네시아어, 한국어
- 채널당 **최대 20개 템플릿**

### 메시지 구조
- **(A) 제목 섹션**: 제목 + 부제목
- **(B) 상세 섹션**: "detailed" (복수 키) 또는 "simple" (단일 키) 레이아웃
- **(C) 버튼**: 템플릿별 수량 상이; URL 필수; 첫 번째 버튼 필수
- **(D) 푸터**: 채널 아이콘 + 이름; 탭 시 앱 최상위 페이지 실행

### 글자 수 제한

| 섹션 | 권장 | Soft Limit | Hard Limit |
|------|------|-----------|-----------|
| Detailed | 10 | 36 | 50 |
| Simple | 32 | 100 | 150 |

- Hard Limit 초과 시 **메시지 전송 실패**
- **grapheme cluster 단위** 측정 (UTF-16 code unit 아님)

### 토큰 아키텍처 (3종 필요)

1. **Channel Access Token**: Stateless 토큰 권장 (Long-lived 미지원)
2. **LIFF Access Token**: `liff.getAccessToken()`로 획득
3. **Service Notification Token**: Channel + LIFF 토큰으로 발행; **발행 후 1년 만료**

### 최초 메시지 전송 플로우
1. 앱에서 `liff.getAccessToken()` 호출
2. LIFF 토큰을 서버로 전송
3. Channel Access Token 획득
4. `/notifier/token` 엔드포인트로 Service Notification Token 발행
5. `/notifier/send?target=service` 엔드포인트로 메시지 전송 (템플릿명 + 파라미터)

### 후속 메시지 전송
- 이전 응답의 Service Notification Token 사용
- 원래 Channel/LIFF 토큰으로 재발행하지 말 것
- 각 응답에 업데이트된 토큰 포함

### 메시지 쿼터
- 사용자 액션당 **최대 5개 서비스 메시지** (1년 토큰 유효 기간 내)

### 템플릿 심사 상태
- **DEVELOPING**: 심사 중; 개발 채널에서만 사용 가능
- **PUBLISHING**: 심사 통과; 프로덕션 사용 가능

> **경고**: 선언된 용도와 다르게 사용하면 기능이 정지될 수 있다.

---

## 13. 결제 처리

### 지원 결제 방식

| 방식 | 상세 |
|------|------|
| LINE Pay | 주요 권장 방식 |
| 인앱 결제 | 일본 전용 |
| 기타 결제 수단 | 신용카드 등 커스텀 구현 |

### LINE Pay

**Merchant Account 필요**: [LINE Pay 공식 웹사이트](https://pay.line.me/portal/global/main)에서 신청

**결제 플로우 (3단계):**
1. 사용자가 MINI App 내에서 거래 시작
2. LINE Pay에서 결제 상세 확인 및 인증
3. 주문 확인 페이지 표시

**테스트**: [LINE Pay Sandbox](https://developers-pay.line.me/sandbox) 사용

> **중요 (일본)**: "일본에서의 LINE Pay 서비스는 2025년 4월 30일에 종료되었다." 대만과 태국은 정상 운영 중.

### 기타 결제 방식
- 일반 웹페이지와 동일하게 구현
- 단, 외부 도메인/앱에서 거래 완료 후 **반드시 LINE MINI App 페이지로 리다이렉트** 설계 필요

> **jisooknows 참고**: 일본에서 LINE Pay가 종료되었으므로, 신용카드 결제 또는 인앱 결제를 활용해야 한다.

---

## 14. 퍼머넌트 링크

### 생성 공식
```
퍼머넌트 링크 = LIFF URL + (LINE MINI App URL - Endpoint URL)
```

### 예시

| 구성요소 | 값 |
|---------|---|
| LIFF URL | `https://miniapp.line.me/123456-abcedfg` |
| 웹앱 페이지 URL | `https://example.com/shop?search=shoes#item10` |
| Endpoint URL | `https://example.com` |
| **퍼머넌트 링크** | `https://miniapp.line.me/123456-abcedfg/shop?search=shoes#item10` |

### URL 컴포넌트 지원
- Raw 경로, 쿼리 파라미터, 해시 프래그먼트 모두 사용 가능

### 자동 생성
- 헤더 액션 버튼으로 공유 시 LINE 앱이 **자동으로 퍼머넌트 링크 생성**
- 다른 시나리오에서는 개발자가 수동 구성

### 도메인명 차이
- LINE 13.20 이상: `https://miniapp.line.me/{liffId}`
- 이전 버전: `https://liff.line.me/{liffId}`
- 이전 URL로 접근해도 LINE MINI App이 열림

### LINE 미설치 사용자
- 브라우저에서 LINE MINI App 접근 안내 페이지 표시
- "웹 브라우저에서 열기" 옵션으로 LIFF Endpoint URL 페이지 표시

---

## 15. 홈 화면 추가

### 요건
- **인증 MINI App만** 사용 가능
- 미인증은 개발 채널에서만 테스트

### iOS 플랫폼 호환성

| 브라우저 | iOS 버전 | 동작 여부 |
|---------|---------|----------|
| Safari | 모든 버전 | 동작 |
| Chrome | 16.4 이상 | 동작 |
| 기타 브라우저 | 16.4 이상 | 보장 안됨 |
| Safari 제외 | 16.4 미만 | 동작 안함 |

### Android
- 일반적으로 동작
- 일부 기기에서 LINE 앱 아이콘 변경 시 기존 바로가기가 삭제될 수 있음

### 사용자 활성화 방법
1. **액션 버튼 경로**: 멀티탭 뷰 > "홈에 추가"
2. **프로그래밍 경로**: `liff.createShortcutOnHomeScreen()` 메서드

### 권장 사용 사례
- 멤버십 카드
- 모바일 주문

---

## 16. 커스텀 경로

### 개요
인증 MINI App이 LIFF ID 대신 브랜드 URL을 사용할 수 있는 기능.

**예시**: `https://miniapp.line.me/cony_coffee` (LIFF ID URL도 계속 동작)

### 신청 프로세스

**일본의 경우:**
- Yahoo 양식으로 신청
- 심사 기간: **1~2주**
- 복수 앱 일괄 신청 가능

**대만/태국의 경우:**
- 담당 영업 담당자에게 연락

### 문자열 요구사항
- **길이**: 4~29자
- **허용 문자**: 반각 영숫자(`a-z`, `0-9`) 및 밑줄(`_`)
- **제한**: 밑줄로 끝날 수 없음, 숫자만으로 구성 불가, 공백 불가
- **브랜딩**: 브랜드/서비스를 식별하는 고유명사 포함 필수
- **제외**: LY Corporation 서비스 중복, 기존 문자열(경쟁사 포함) 중복, 부적절한 문자열

### 핵심 참고사항
- MINI App 심사 완료 전에 신청 가능하나, **심사 통과 후에만 활성화**
- **설정 후 변경 불가** (영구적)
- LINE Developers Console에 커스텀 URL이 표시되지 않음
- LIFF ID URL은 백업 접근 방식으로 계속 동작

---

## 17. 외부 브라우저 지원

### 개요
2025년 10월부터 LINE MINI App을 외부 브라우저에서 사용 가능.

### 로그인 처리

**자동 로그인:**
```javascript
liff.init({
  liffId: "123456-abcdefg",
  withLoginOnExternalBrowser: true
});
```

**수동 로그인:**
```javascript
if (!liff.isLoggedIn()) {
  liff.login();
}
```

### 외부 브라우저에서 사용 불가 기능
- `liff.sendMessages()`
- `liff.openWindow()`
- `liff.closeWindow()`
- `liff.scanCode()` (deprecated)
- `liff.iap.*` (인앱 결제 기능)

> 이러한 기능이 필요한 경우, LINE 앱에서 MINI App을 열도록 안내하는 메시지를 표시해야 한다.

### 로그인 없이 사용 가능한 API
- `liff.id`
- `liff.init()`
- `liff.getOS()`
- `liff.isInClient()`
- `liff.isLoggedIn()`
- `liff.permanentLink.createUrlBy()`

### 환경 감지
- `liff.getContext()`: 실행 컨텍스트 확인
- `liff.isInClient()`: LINE 내부/외부 판별

### 정책 요구사항
> **"Endpoint URL은 웹 브라우저(Safari, Chrome 등)에서 접근 가능해야 한다."**

---

## 18. Common Profile Quick-fill

### 개요
사용자가 "자동 입력" 버튼 한 번 탭으로 프로필 정보를 자동 채우는 기능. Account Center에 설정된 Common Profile 데이터를 활용한다.

### 접근 요건
- 인증 MINI App 채널
- 신청서 제출 및 승인
- LINE Developers Console에서 스코프 지정
- **LIFF SDK v2.19.0 이상** + Quick-fill 플러그인

### 언어 지원
- **현재 일본어만 지원**: LINE 앱 언어 설정과 무관하게 일본어로 표시

### 구현 방식

**CDN 방식:**
```html
<script src="CDN_URL"></script>
<!-- window.liffCommonProfile 사용 -->
```

**NPM 방식:**
```bash
npm install @line/liff-common-profile-plugin
```
```javascript
import LiffCommonProfilePlugin from '@line/liff-common-profile-plugin';
liff.use(new LiffCommonProfilePlugin());
```

### 핵심 API (3개)
- `liff.$commonProfile.get()`: 사용자 프로필 데이터 조회
- `liff.$commonProfile.getDummy()`: 테스트 데이터 조회 (`caseId` 파라미터, 10개 테스트 케이스)
- `liff.$commonProfile.fill()`: 폼 필드에 프로필 데이터 자동 입력

### 요청 가능한 프로필 데이터 (15개 항목)
성(family name), 이름(given name), 성 요미가나(phonetic family name), 이름 요미가나(phonetic given name), 성별(숫자 enum), 생년월일(일/월/년), 전화번호, 이메일 주소, 우편번호, 주소 4단계(level 1~4)

### 운영 제약
- **iOS 및 Android LINE에서만 동작**
- Node.js v18.15.0+ 필요 (npm 설치 시)
- LIFF 앱은 정확한 Endpoint URL 또는 하위 디렉토리 경로에서만 동작
- 글자 수 제한: 반각 문자열 100~200자, 일본어 텍스트 50~69자

### 데이터 처리 옵션 (기본값 true)
- `excludeEmojis`: 이름 필드에서 이모지 제거
- `excludeNonJp`: 12자리 초과 전화번호 거부
- `digitsOnly`: 숫자만 포함된 우편번호만 허용

### Quick-fill 디자인 규정

**허용된 4가지 화면 전환 패턴:**
1. 등록 화면에서 즉시 모달 표시
2. 입력 필드 클릭 시 모달 활성화
3. 자동 입력 버튼 탭 후에만 모달 표시
4. 채널 동의 후 바로 등록 화면 + 모달 표시

**금지된 3가지 화면 전환 패턴:**
1. 폼이 없는 화면에서 모달 표시
2. 폼에 존재하지 않는 데이터 요청
3. 자동 입력 후 폼 완성 없이 바로 다음 화면 이동

**자동 입력 버튼 규칙:**
- 수정/편집/애니메이션/효과 추가 금지
- 좌측 또는 중앙 정렬
- 모든 측면에 10px 여백
- 줌/회전/장식/3D/그림자/테두리 금지
- 커스텀 대체 버튼 금지
- 버튼 아래 텍스트 배치 금지
- LINE CDN URL에서 직접 로드 (로컬 다운로드 금지)

**버튼 타입 및 사양:**
- Type A/B/C: 264px x 73px (각 4가지 색상)
- Type D: 288px x 66px (4가지 색상)
- **이미지가 지정 크기의 2배**: 원본 크기로 표시하지 않도록 주의

---

## 19. 디자인 가이드라인

### 19.1 아이콘 사양

**배경 영역**: 정확히 130x130px

**로고 크기**: 최소 54x54px, 최대 90x90px, **권장 54~76px**

**파일 포맷**: PNG 및 JPEG만 허용

**금지 요소**: 공식 LINE MINI App 로고 포함 불가

**디자인 원칙**: 독립적인 아이콘 또는 워드마크로 기능해야 함

**외곽선/테두리 색상:**

| 배경색 | 외곽선 색상 | 불투명도 |
|--------|-----------|---------|
| 흰색 (#FFFFFF) | 검정 (#000000) | 12% |
| 검정/다크 (#000000/#181818) | 흰색 (#FFFFFF) | 8% |
| 기타 색상 | 검정 (#000000) | 8% |

**표시 위치**: 채널 동의 화면, 홈 탭, LINE 메시지, 서비스 메시지

**업로드**: LINE Developers Console > Basic settings > Channel icon에서 업로드. 시스템이 자동 크롭 및 배경 투명화 처리.

### 19.2 안전 영역

**일반 모드 (세로):**
- 하단 패딩: **34px**

**가로 모드:**
- 좌측 패딩: **44px**
- 우측 패딩: **44px**
- 하단 패딩: **21px**

**구현**: CSS padding 속성으로 메인 컨테이너에 적용

> "노치가 있는 기기에서도 LINE MINI App의 모든 부분이 보이도록 CSS를 사용하여 안전 영역 내에 포함시키는 것을 권장한다."

### 19.3 로딩 아이콘
- **크기**: 30x30px
- **정렬**: 컨테이너 내 중앙 정렬
- **포맷**: SVG (라이트/다크 모드 각각 제공)
- LINE이 제공하는 스피너 파일 사용 권장

---

## 20. 성능 가이드라인

### 공식 권장 성능 지표
**Lighthouse Performance 점수 50 이상** 권장 (LY Corporation 기준)

### 측정 도구
- **Lighthouse** (주 권장)
- **PageSpeed Insights**

### 측정 시 필수 조건

1. **LINE Login 실행 제외**: "LINE Login이 동시 실행되면 LINE Login 페이지의 성능이 측정되어 LINE MINI App 성능을 측정할 수 없다."

2. **프로덕션 환경에서 측정**: "반드시 프로덕션 환경(실제 환경)에서 측정하라. 네트워크 환경이 성능 점수에 영향을 줄 수 있다."

### 정책 권장 로딩 시간
> "첫 페이지를 3초 이내에 표시하라; 1초를 권장한다."

---

## 21. 개발 가이드라인 (필수 준수)

### 21.1 대량 요청 금지
- LIFF 스킴이나 LIFF API/Service Message API에 로드 테스트 목적의 대량 요청 금지
- `https://miniapp.line.me/{liffId}` 과도한 접근 금지
- 별도 테스트 환경 구축 필수
- 요율 제한 위반 시 `429 Too Many Requests` 응답

### 21.2 로그 저장 (필수)

**Service Message API 요청 시 최소 저장 필수 데이터:**
- API 요청 타임스탬프
- 요청 메서드 타입
- 전체 API 엔드포인트 URL
- LINE Platform 반환 상태 코드

**선택적 강화 로깅:**
- 요청 본문
- 응답 본문 (Service Notification Token 제외)

> **"문의에도 불구하고 Service Message API 요청 로그를 제공하지 않는다. 로그는 개발자가 직접 저장해야 한다."**

### 21.3 사용자 해제 시 Deauthorize
- 사용자 탈퇴 또는 앱-LINE 연동 해제 시 deauthorization 엔드포인트 사용 필수
- 약관/등록 화면에서 해제 결과를 명확히 안내
- 예시 문구: "탈퇴 시 서비스와 LINE 앱 간 연동이 해제됩니다"

### 21.4 기반 규칙
모든 LINE MINI App 개발은 **LIFF app development guidelines** 및 이용약관/정책을 준수해야 한다.

---

## 22. 심사 제출 프로세스

### 제출 전 체크리스트
- [ ] 디자인 가이드라인 준수 (아이콘, 안전 영역, 로딩 아이콘)
- [ ] 커스텀 액션 버튼 구현 확인
- [ ] 성능 가이드라인 준수 (Lighthouse 50+)
- [ ] LINE MINI App Policy 준수
- [ ] Provider 이름과 서비스 제공자 일치
- [ ] 채널 설명 최신화
- [ ] 개인정보처리방침 회사 일치
- [ ] Published 및 Review 채널 간 LIFF URL 일관성

### 리전별 제한

| 리전 | 제한사항 |
|------|---------|
| 일본 | 인증 심사 제한 없음 |
| 대만 | **인증 Provider만** 심사 신청 가능 |
| 태국 | **인증 Provider만** 심사 신청 가능 |

### 심사 기간
- **표준 소요 기간**: 약 **1~2주**
- 반려 시 추가 기간 소요 가능
- 완료 날짜 보장 불가; 충분한 버퍼 확보 필요

### 복수 앱 제출 전략
> "먼저 하나의 LINE MINI App에 대해 심사를 요청하라. 승인 후 일괄 심사를 요청하라."

### 제출 프로세스

**LINE Developers Console > Review request 탭에서 제출:**
- 필수 정보 필드
- Basic Authentication 자격 증명 (접근 제한 시)
- 거래 서비스의 테스트 시나리오 (예약, 결제, 주문)
- 심사 참고 자료

**취소**: 심사 시작 전에만 "Cancel review request" 버튼으로 가능

### 채널 설명 요구사항
- **나쁜 예**: 일반적인 서비스명
- **좋은 예**: "이것은 모바일 주문 서비스입니다... 사전에 주문하고 결제할 수 있습니다."

### 인앱 결제 통합 시
- 제출 전 사전 승인 필요
- 승인 후 "Apply to publish in-app purchase" 토글
- **제한**: IAP 심사 중 인증 심사 불가; 인증 심사 중 IAP 신청 불가

### 승인 후 워크플로우

**최초 제출의 경우:**
- 상태 자동 변경: "Approved" → "Reflected"
- **Search enable** 버튼으로 검색 노출 활성화
- **자동 활성화**: 수동 활성화 미완료 시 31일차 오전 9시 JST에 자동 활성화
- 검색 활성화 후 설정 변경을 위해 상태가 "Not yet reviewed"로 복귀

**기존 출시 앱의 경우:**
- 승인 후 수동 **Publish changes** 버튼 클릭 필요
- 30일 이내 수동 활성화; 31일차 오전 9시 JST 자동 활성화
- 승인 및 버튼 활성화 후에만 변경 적용

### 인증 Provider 상태
- "Japan" 리전 설정 앱이 승인되면 **자동으로 "certified provider"** 획득

> **참고**: 예정 시간에도 불구하고 상태 변경에 **1~2시간 지연**이 발생할 수 있다.

---

## 23. LINE MINI App 정책 (금지사항)

> **최종 개정: 2026년 2월 19일**

### 허용된 고객

**미인증 MINI App:**
- 법인번호가 있는 조직 (일본) 또는 TAX ID (대만/태국)
- 개인사업자 (일본)
- 개인 (일본, 대만, 태국)

**인증 MINI App:**
- 법인번호가 있는 조직 (일본) 또는 TAX ID (대만/태국)
- 개인사업자 (일본)
- **개인은 인증 MINI App 불가**

### LINE MINI App 사용 금지 업종
- 종교 단체
- 성인 바/나이트클럽/호스트클럽/스낵바/걸스바/보이스바
- 도박, 슬롯머신
- 소개팅/매칭/만남 주선 (회사 승인 없는 한)
- 대출 업체 (회사 승인 없는 한)
- 모금/기부/크라우드펀딩 (회사 승인 없는 한)
- 다단계 마케팅
- 담배/전자담배
- 무기/독극물
- 미승인 의약품/의료기기 해외 구매
- **임상 시험**
- 투자 컨설팅/자기개발 세미나
- 사설 탐정
- 정치
- 동물/곤충 판매 (회사 승인 없는 한)

### 금지 콘텐츠 및 행위
- 법률/판결/행정조치 위반 콘텐츠
- 불법 행위 조장
- 지적재산권 침해
- 명예훼손/도덕 위반
- 반사회적 메시지
- 개인정보 무단 수집/공개
- 폭력/성적 표현
- 차별적 콘텐츠
- 포르노/음란
- 특정 종교/사상 관련
- 도박 조장
- 비과학적/미신적 콘텐츠
- 네트워크 마케팅/피라미드 스킴
- 서비스 운영 방해
- Apple/Google 정책 위반

### 위반 시 제재
- LINE MINI App 삭제
- 서비스 정지
- 서비스 계약 해지
- 특정 기능 정지
- 인증 취소

> **"LY Corporation은 이유를 제공할 의무가 없다."**

### 운영 관련 정책 요점

**서비스 메시지 제한**: 광고 금지, 사용자 액션에 대한 확인/응답만 허용

**외부 유도 제한**: 메인 기능은 MINI App 내에서만 제공. 다음의 경우만 외부 리다이렉트 허용:
- 거래/인증
- 네이티브 앱 결제
- 개인정보처리방침/약관/회사 웹사이트
- 매장 위치 확인용 지도 앱

**콘텐츠 안전**: 모든 연령(어린이~노인)에게 안전하고 적절해야 함

**별도 채널 사용자 데이터 저장**: 채널 동의 화면 권한 범위 내에서 사용자 데이터 활용. 소셜 미디어 계정 로그인은 서비스 계정이 LINE 계정과 연동된 경우에만 허용.

**TOP 페이지**: 사용자를 혼란시키는 내용 금지. 텍스트만 또는 에러 화면처럼 보이면 안 됨. 리다이렉트 설정 금지 (로딩 속도 저하).

**회사 정보**: 개발사와 서비스 제공사가 다르면 채널 동의 화면과 개인정보처리방침 페이지에서 사용자에게 고지.

**개인정보처리방침 필수 기재 사항:**
- 사용자 동의 하에 제3자에 대한 개인정보 제공
- 개인정보를 공유하는 제3자 이름
- 제3자와 공유하는 정보
- 개인정보 제공 시점

### 퍼포먼스 권장사항
- 첫 페이지 **3초 이내** 표시 (1초 권장)
- 약속한 모든 기능 구현
- 서비스 제공자 이름 표시
- 고객 지원 연락처 표시

---

## 24. 서비스 운영

### 공유 시 퍼머넌트 링크 사용
외부 채널(웹, 이메일, SNS, 리치 메시지, 리치 메뉴, 커스텀 액션 버튼)에서 공유 시 퍼머넌트 링크 사용 권장.

### 서비스 메시지 제한 (재강조)
- 사용자 액션에 대한 확인/응답만 허용
- 사용자 액션당 **최대 5개 메시지**
- "사용 시나리오에 따라 변경될 수 있음"
- 채널당 **최대 20개 템플릿**

### 위반 결과
- 부적절한 서비스 메시지 전송 시 **API 접근 일시 금지**
- "약관을 반복 위반하면 LINE에서 LINE MINI App이 삭제될 수 있다."

### 일본 채널 자동 설정
- **Channel Consent Simplification** 자동 활성화

---

## 25. 업데이트 후 재심사

### 재심사가 필요한 변경사항

**Basic Settings:**
- Channel icon, Channel name, Channel description
- Email address, Privacy policy URL, Terms of use URL
- Localization (다국어 지원)
- Linked LINE Official Account

**Web App Settings:**
- shareTargetPicker, Channel consent simplification
- **Endpoint URL for Published**
- Scopes, Add friend option

**비즈니스/연락처 정보:**
- 서비스 회사 상세, 개발 회사 정보
- 연락처 정보, 서비스 메시지 템플릿 (모든 정보)

**인앱 결제:**
- "Apply to use in-app purchase" 탭 업데이트

> **Consent Simplification 참고**: "2026년 1월 8일 이전에 생성된 일본 LINE MINI App 채널에서만 업데이트 가능"

### 재심사 불필요한 경우
- LINE Developers Console 설정 변경이 아닌 경우
- 유지보수를 위한 임시 Endpoint URL 교체 — "변경 후 즉시 페이지가 전환된다."

---

## 26. 광고 게재

### 승인된 광고 네트워크
**Yahoo! JAPAN Ads만** 허용 (다른 광고 네트워크 불가)

### 요건
- 인증/미인증 MINI App 모두 가능
- **일본에서 제공되는 서비스만**
- 일본어만 지원

### 3단계 절차
1. 광고 게재 관련 문서 검토
2. **Yahoo! JAPAN Ads Network Partner** 등록
3. Yahoo! JAPAN Ads 사이트 심사 제출

### 광고 게재 불가 서비스
종교, 성인, 소개팅, 도박/파칭코, 다단계, 탐정, 담배, 무기/독극물, 정치, 미승인 의약품, 대출업, 정보상품/자기개발, 모금/기부, 임상시험 관련

---

## 27. 인앱 결제 (일본 전용)

### 개요
LINE MINI App 내에서 디지털 콘텐츠를 구매할 수 있는 시스템. App Store/Google Play 결제 시스템 활용. 현재 **소모성 디지털 콘텐츠만** 대상.

### 자격 요건
- 서비스 리전 및 회사/소유자 국가 모두 **"Japan"** 설정
- 인증 MINI App (미인증은 Development/Review 채널에서만)
- **LIFF SDK v2.26.0 이상**
- LIFF 브라우저 내에서만 동작
- 사용자: 일본 전화번호가 등록된 LINE 계정
- 사용자 LINE 버전: **15.6.0 이상**

### 가격 설정
- 일본 엔화로 사전 정의
- `liff.iap.getPlatformProducts()`로 각 앱 스토어 리전에 맞는 현지 가격 표시

### 구현 플로우 (5단계)
1. LINE Developers Console > In-app purchase 탭에서 신청
2. 승인 후 webhook URL 및 테스트 결제 사용자 등록
3. Development 채널에서 기능 통합 및 테스트 결제
4. 인증 심사 신청 ("Release in-app purchase feature" 토글 활성화)
5. 인증 MINI App과 함께 인앱 결제 기능 출시

### 환불 정책
> "LY Corporation은 인앱 결제로 완료된 결제 취소를 지원하지 않는다." 사용자는 App Store/Google Play에 직접 환불 요청해야 한다.

---

## 28. LINE Official Account 연동

### 통합 방식
1. **리치 메시지**: 시각적 메시지로 MINI App 가치 전달
2. **리치 메뉴**: 채팅에서 LIFF URL/퍼머넌트 링크로 직접 접근
3. **친구 추가 옵션**: 인증/동의 화면에서 Official Account 친구 추가 유도

### 친구 추가 옵션 요건 (모두 충족 필요)
- LINE Official Account가 Messaging API 사용 중
- Messaging API 채널과 MINI App 채널이 **같은 Provider** 소속
- MINI App 채널에 Admin 역할 + Official Account에 Administrator 역할

### 설정 절차
1. LINE Developers Console 접속
2. MINI App 채널 > Basic settings 탭
3. "Linked LINE Official Account" > Edit
4. Official Account 선택 > Update
5. Web app settings 탭
6. "Add friend option" > Edit
7. **On (normal)** 선택 > Update

### 인증 Provider 기본 설정
> "LINE MINI App 채널이 인증 Provider에 속하면, 인증 화면과 채널 동의 화면의 친구 추가 옵션이 기본으로 활성화된다."

---

## 29. 웹앱을 MINI App으로 전환하기

### 필수 조건
- HTML, CSS, JavaScript, 웹 개발/배포 지식
- 기능 중인 웹 서버
- Business ID (LINE Developers Console 접근용)

> "운영 중인 웹앱 개발 시 사용한 지식과 기술을 그대로 사용할 수 있다."

### 6단계 전환 절차

1. **LINE MINI App 채널 생성** → LIFF ID 획득
2. **LIFF SDK 로드** (CDN 또는 npm)
3. **LIFF 앱 초기화** (`liff.init()`)
4. **필수 기능 구현** (LIFF API, 서비스 메시지, HTML5)
5. **Endpoint URL 설정** (웹앱 URL을 MINI App 채널에 등록)
6. **심사 요청** (미인증 또는 인증)

### 핵심 기술 차이점
- LIFF SDK 로드 및 초기화 필수
- 채널 기반 배포 (직접 웹 접근 대신 LINE 플랫폼 인프라)
- 서비스 메시지 (LINE 에코시스템 내 푸시 알림)
- ID Token 인증 (LINE 엔드포인트 대한 서버 사이드 검증)

---

## 30. jisooknows 적용 시 핵심 고려사항

### 30.1 리전 및 채널 설정

**필수 선택: Japan 리전**
- jisooknows는 일본인 관광객 대상이므로 Japan 리전으로 채널 생성
- Channel Consent Simplification 자동 활성화 혜택
- 즐겨찾기 기능 사용 가능 (일본 리전 + LINE 15.18.0+)
- 신고 기능 사용 가능 (일본 리전 + LINE 15.6.0+)

**로컬라이제이션 필수:**
- 기본 입력은 영문이지만, **일본어 로컬라이제이션 필수** 설정
- 한국어도 추가 로컬라이제이션 고려 (한국 피부과 서비스이므로)

### 30.2 인증 구조 (Firebase Auth + LINE Login)

**현재**: Firebase Auth 사용
**필요**: LIFF SDK 통합으로 LINE Login 자동 처리

**권장 구현:**
```javascript
// Next.js 16에서 LIFF 초기화
liff.init({ liffId: LIFF_ID })
  .then(() => {
    if (liff.isLoggedIn()) {
      const idToken = liff.getIDToken();
      // 서버로 전송하여 Firebase Custom Token으로 변환
    }
  });
```

- LINE ID Token을 서버에서 검증 후 Firebase Custom Auth Token 발급
- 기존 Firebase Auth 사용자 데이터와 LINE 사용자 매핑

### 30.3 결제 관련

> **경고**: 일본에서 LINE Pay가 2025년 4월 30일에 종료되었다.

**대안:**
1. 신용카드 결제 (일반 웹 결제와 동일하게 구현)
2. 인앱 결제 (디지털 콘텐츠만, LIFF SDK v2.26.0+)
3. 기타 결제 수단 (외부 도메인 결제 후 MINI App으로 리다이렉트)

### 30.4 서비스 메시지 활용

jisooknows에 적합한 서비스 메시지 사용 사례:
- **예약 확인**: 피부과 상담 예약 확인
- **예약 리마인더**: 상담 일정 리마인더
- **상담 결과**: AI 뷰티 상담 결과 전달

**금지**: 프로모션, 할인, 새 서비스 알림 등은 서비스 메시지로 전송 불가

### 30.5 Quick-fill 활용

- 현재 **일본어만 지원**이므로 일본인 사용자에게 최적
- 성명, 전화번호, 이메일, 주소 자동 입력으로 예약 폼 편의성 향상
- **LIFF SDK v2.19.0 이상** 필요
- 인증 MINI App 상태 필요

### 30.6 외부 브라우저 대응

- 2025년 10월부터 외부 브라우저 지원
- LINE 미설치 사용자도 접근 가능 → 마케팅 범위 확대
- 단, 일부 기능 제한 (`sendMessages`, `scanCode`, `iap` 등)
- `liff.isInClient()`로 환경 감지 후 적절한 UI 표시

### 30.7 퍼포먼스 요구사항

- Lighthouse Performance **50 이상** (공식 기준)
- 첫 페이지 **3초 이내** (1초 권장)
- Next.js 16의 SSR/ISR 활용하여 성능 최적화
- GCP Cloud Run의 콜드 스타트 최소화 필요

### 30.8 안전 영역 CSS

```css
/* 세로 모드 */
.app-container {
  padding-bottom: 34px;
}

/* 가로 모드 */
@media (orientation: landscape) {
  .app-container {
    padding-left: 44px;
    padding-right: 44px;
    padding-bottom: 21px;
  }
}
```

### 30.9 심사 제출 전 체크리스트 (jisooknows 특화)

- [ ] Japan 리전 채널 생성 완료
- [ ] 일본어 로컬라이제이션 설정 완료
- [ ] 아이콘 사양 준수 (130x130px, PNG/JPEG)
- [ ] 안전 영역 CSS 적용 (세로 34px, 가로 44/44/21px)
- [ ] 로딩 아이콘 구현 (30x30px SVG)
- [ ] 커스텀 액션 버튼 구현 (Flex Message Bubble)
- [ ] Lighthouse 성능 50+ 달성
- [ ] 첫 페이지 3초 이내 로드
- [ ] 개인정보처리방침 URL 설정 (일본어 + 영어)
- [ ] 채널 설명 구체적 작성
- [ ] 서비스 메시지 템플릿 구성 (예약 확인, 리마인더 등)
- [ ] Basic Auth 설정 (심사 전 접근 제한)
- [ ] Developing/Review/Published 각 채널 Endpoint URL 배포
- [ ] deauthorize 엔드포인트 구현
- [ ] 서비스 메시지 API 요청 로그 저장 구현
- [ ] LINE MINI App Policy 금지 업종/콘텐츠 해당 없음 확인
- [ ] 외부 브라우저 접근 대응
- [ ] `<title>` 요소 적절히 설정 (헤더 서비스 이름으로 표시됨)

### 30.10 일본 시장 특화 정보

1. **인증 Provider 자동 획득**: Japan 리전에서 심사 통과 시 자동으로 certified provider
2. **Channel Consent Simplification**: 일본에서만 사용 가능, 2026년 1월 8일 이후 생성 채널은 자동 활성화
3. **Quick-fill**: 일본어만 지원 → 일본인 사용자에게 최적
4. **인앱 결제**: 일본에서만 사용 가능
5. **광고 게재**: 일본에서만 가능 (Yahoo! JAPAN Ads)
6. **즐겨찾기 기능**: 일본 리전 + LINE 15.18.0+ 필요
7. **LINE Pay 종료**: 2025년 4월 30일에 일본 서비스 종료
8. **홈 탭 표시**: 리전에 따라 정책이 다름
9. **심사 기간**: 약 1~2주
10. **자동 검색 활성화**: 수동 미활성화 시 31일차 오전 9시 JST에 자동 활성화

---

## 부록: 전체 LINE MINI App 문서 사이드바 구조

### API Reference
- LINE MINI App API Reference

### Development Guidelines
- LINE MINI App development guidelines

### Quickstart
- Get started with LINE MINI App

### Discover LINE MINI App
- Introducing LINE MINI App
- LINE Developers Console Guide for LINE MINI App
- Specifications
- Built-in features
- Custom Features
- LINE MINI App UI components

### Design LINE MINI App
- Icon specifications and guidelines
- Safe area of LINE MINI App
- Loading icon

### Develop LINE MINI App
- Getting started with development
- Authorization flow
- Implementing custom action buttons
- Sending service messages
- Configuring Custom Path
- Handling payments
- Creating permanent links
- Add to home screen
- Managing settings on Developers Console
- Open in external browser
- Implementing web apps as MINI Apps
- Performance guidelines

### Common Profile Quick-fill
- Overview of Quick-fill
- Quick-fill design regulations

### In-app Purchase
- In-app purchase overview
- Development guidelines
- Apply to use in-app purchase
- Set up in-app purchase
- Integrate the feature

### Submit LINE MINI App
- Submitting LINE MINI App
- LINE MINI App policy

### Service LINE MINI App
- Running your service
- Place ads in MINI Apps
- Re-review after updating
- Use LINE Official Account

### Tools
- LINE MINI App Playground (https://miniapp.line.me/lineminiapp_playground)

---

## 부록: 주요 URL 참조

| 리소스 | URL |
|--------|-----|
| LINE MINI App 문서 메인 | https://developers.line.biz/en/docs/line-mini-app/ |
| LINE Developers Console | https://developers.line.biz/console/ |
| LINE MINI App Policy | https://terms2.line.me/LINE_MINI_App?lang=en |
| LINE MINI App Playground | https://miniapp.line.me/lineminiapp_playground |
| LINE Pay 개발자 | https://developers-pay.line.me/online |
| LINE Pay Sandbox | https://developers-pay.line.me/sandbox |
| LIFF SDK CDN | https://static.line-scdn.net/liff/edge/2/sdk.js |
