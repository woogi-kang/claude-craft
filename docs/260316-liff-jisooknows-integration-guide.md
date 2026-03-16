# LIFF x jisooknows 통합 가이드

> LINE Front-end Framework 전체 문서 분석 + jisooknows 적용 전략
> 작성일: 2026-03-16

---

## 목차

1. [LIFF 개요](#1-liff-개요)
2. [채널 & 앱 등록](#2-채널--앱-등록)
3. [SDK 설치 & 초기화](#3-sdk-설치--초기화)
4. [인증 플로우 (LIFF + Firebase Auth 브릿지)](#4-인증-플로우)
5. [전체 API 레퍼런스](#5-전체-api-레퍼런스)
6. [Server API & 토큰 검증](#6-server-api--토큰-검증)
7. [브라우저 환경별 차이점](#7-브라우저-환경별-차이점)
8. [보안 가이드라인](#8-보안-가이드라인)
9. [Pluggable SDK & 번들 최적화](#9-pluggable-sdk--번들-최적화)
10. [LIFF CLI 개발 워크플로우](#10-liff-cli-개발-워크플로우)
11. [LIFF Plugin 시스템](#11-liff-plugin-시스템)
12. [jisooknows 호환성 매트릭스](#12-jisooknows-호환성-매트릭스)
13. [jisooknows 기능별 LIFF API 매핑](#13-jisooknows-기능별-liff-api-매핑)
14. [제한사항 & 주의사항 총정리](#14-제한사항--주의사항-총정리)
15. [LINE MINI App 마이그레이션 로드맵](#15-line-mini-app-마이그레이션-로드맵)
16. [실행 계획](#16-실행-계획)

---

## 1. LIFF 개요

LIFF(LINE Front-end Framework)는 LY Corporation이 제공하는 LINE 내 웹앱 플랫폼입니다.
LIFF 앱은 LINE 메신저 안에서 동작하며 LINE 사용자 데이터에 접근하고 메시지를 전송할 수 있습니다.

### 동작 환경

| 환경 | 엔진 | 비고 |
|------|------|------|
| iOS LIFF 브라우저 | WKWebView | 최신 OS 권장 |
| Android LIFF 브라우저 | Android WebView (Chromium) | 최신 OS 권장 |
| 외부 브라우저 | Edge, Chrome, Firefox, Safari | 최신 버전 |

### 화면 크기 옵션

| 사이즈 | 설명 | jisooknows 권장 |
|--------|------|:---:|
| **Full** | 전체 화면 | **O (권장)** |
| Tall | 화면 대부분 | |
| Compact | 화면 하단 일부 | |

---

## 2. 채널 & 앱 등록

### 2.1 채널 생성 절차

1. [LINE Developers Console](https://developers.line.biz/console/) 로그인
2. Provider 생성 (예: "jisooknows")
3. 채널 유형 선택

| 채널 유형 | 용도 | 비고 |
|-----------|------|------|
| **LINE Login** | 표준 LIFF 앱 | 기본 선택 |
| **LINE MINI App** | LINE MINI App 기반 LIFF | 향후 통합 대비 권장 |

**필수 규칙:**
- 채널 이름에 "LINE" 또는 유사 문자열 사용 금지
- App type = "Web app" 선택
- **한번 생성된 채널은 다른 Provider로 이동 불가**
- LINE Login 채널과 Messaging API 채널은 **반드시 같은 Provider** 하에 생성

### 2.2 LIFF 앱 등록

LINE Developers Console → LINE Login 채널 → **LIFF** 탭 → **Add**

**jisooknows 권장 설정:**

```json
{
  "view": {
    "type": "full",
    "url": "https://jisooknows.com/liff",
    "moduleMode": false
  },
  "description": "jisooknows AI Beauty Consultation",
  "features": {
    "qrCode": true
  },
  "permanentLinkPattern": "concat",
  "scope": ["openid", "email", "profile", "chat_message.write"],
  "botPrompt": "aggressive"
}
```

| 설정 | 값 | 이유 |
|------|-----|------|
| 사이즈 | **Full** | 상담 UI에 충분한 화면 공간, 최소화/scanCodeV2 지원 조건 |
| Endpoint URL | `https://jisooknows.com/liff` | HTTPS 필수 (Cloud Run 자동 충족) |
| Scope - openid | **필수** | Firebase Auth 연동용 ID Token |
| Scope - profile | **필수** | 사용자 이름/프로필 사진 |
| Scope - email | 선택 | 예약 확인 등 (별도 OpenID Connect 권한 신청 필요) |
| Scope - chat_message.write | 상황별 | 상담 결과 채팅 전송 (단, 브라우저 최소화 기능과 충돌) |
| 친구 추가 | **aggressive** | 일본 관광객에게 공식계정 친구 추가 적극 유도 |
| Module Mode | false | 액션 버튼 유지 (공유/새로고침 등) |

**등록 완료 시 자동 생성:**
- LIFF ID: `1234567890-AbcdEfgh`
- LIFF URL: `https://liff.line.me/1234567890-AbcdEfgh`

**제한:** 채널당 최대 30개 LIFF 앱

---

## 3. SDK 설치 & 초기화

### 3.1 설치

```bash
npm install @line/liff@2.27.3
```

> webpack v5 호환 = v2.16.1+, Pluggable SDK = v2.22.0+, Next.js 16과 완벽 호환

### 3.2 초기화

```typescript
// src/lib/liff.ts
'use client';

import liff from '@line/liff';

export async function initLiff() {
  await liff.init({
    liffId: process.env.NEXT_PUBLIC_LIFF_ID!,
    withLoginOnExternalBrowser: true  // 외부 브라우저 자동 로그인
  });
}
```

**초기화 규칙:**
- 페이지가 열릴 때마다 반드시 실행
- Endpoint URL 또는 하위 경로에서만 실행
- **Promise resolve 전에 URL 변경 금지** (`location`, `pushState`, `replaceState`, 301/302)
- v2.11.0+: resolve 시 URL에서 credential 정보 자동 제거

**초기화 전 사용 가능한 메서드:**
`liff.ready`, `liff.getOS()`, `liff.getAppLanguage()`, `liff.getVersion()`, `liff.isInClient()`, `liff.closeWindow()` (v2.4.0+), `liff.use()`

**외부 브라우저 주의:** `liff.init()`을 2번 호출해야 합니다:
1. SDK 로드 후 초기 호출
2. `liff.login()` 리다이렉트 완료 후 재호출

### 3.3 window.liff 금지

> `window.liff`를 직접 선언하거나 수정하면 LINE 앱 오동작 발생

---

## 4. 인증 플로우

### 4.1 LIFF + Firebase Auth 브릿지 아키텍처

```
[사용자] → LIFF URL 접근
         → liff.init() 자동 로그인 (LIFF 브라우저)
         → liff.getIDToken() → Raw JWT 획득
         → POST /api/auth/line (서버로 JWT 전송)

[서버 - Next.js API Route]
         → POST https://api.line.me/oauth2/v2.1/verify (LINE에서 검증)
         → userId(sub), name, picture, email 추출
         → Firebase Admin: createCustomToken(lineUserId)
         → PostgreSQL 사용자 레코드 upsert

[클라이언트]
         → signInWithCustomToken(auth, firebaseToken)
         → Firebase Auth 세션 활성화
         → Redis 세션 캐시
```

### 4.2 구현 예시

**클라이언트:**
```typescript
// LIFF 환경 감지 후 인증 분기
if (liff.isInClient()) {
  // LIFF 브라우저: 자동 로그인됨
  const idToken = liff.getIDToken();
  const res = await fetch('/api/auth/line', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ idToken })
  });
  const { firebaseToken } = await res.json();
  await signInWithCustomToken(auth, firebaseToken);
} else {
  // 외부 브라우저: 기존 Firebase Auth 플로우 유지
  // (Kakao, LINE Login, etc.)
}
```

**서버:**
```typescript
// /api/auth/line (Next.js API Route)
export async function POST(req: Request) {
  const { idToken } = await req.json();

  // LINE ID Token 검증
  const lineRes = await fetch('https://api.line.me/oauth2/v2.1/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      id_token: idToken,
      client_id: process.env.LINE_CHANNEL_ID!
    })
  });
  const profile = await lineRes.json();
  // profile: { sub, name, picture, email, iss, aud, exp, iat }

  // Firebase Custom Token 생성
  const firebaseToken = await admin.auth()
    .createCustomToken(`line:${profile.sub}`, {
      provider: 'line',
      displayName: profile.name,
      photoURL: profile.picture
    });

  return Response.json({ firebaseToken });
}
```

### 4.3 토큰 관리

| 토큰 | 메서드 | 용도 | 수명 |
|------|--------|------|------|
| Access Token | `liff.getAccessToken()` | API 호출 인증 | 12시간 (앱 닫으면 revoke 가능) |
| ID Token (JWT) | `liff.getIDToken()` | **서버 전송용** | openid scope 필요 |
| Decoded ID Token | `liff.getDecodedIDToken()` | **클라이언트 표시 전용** | 서버 전송 금지 |

### 4.4 Permission 관리

```typescript
// 부여된 모든 scope 조회
const scopes = await liff.permission.getGrantedAll();
// ["profile", "chat_message.write", "openid", "email"]

// 특정 permission 상태
const result = await liff.permission.query("email");
// { state: "granted" | "prompt" | "unavailable" }

// LINE MINI App 전용: 전체 permission 요청
await liff.permission.requestAll();
```

---

## 5. 전체 API 레퍼런스

### 5.1 환경 감지

| API | 반환 | init 전 | 설명 |
|-----|------|:---:|------|
| `liff.getOS()` | `"ios"` / `"android"` / `"web"` | O | OS 감지 |
| `liff.getAppLanguage()` | RFC 5646 코드 | O | LINE 앱 언어 (v2.24.0+) |
| `liff.getVersion()` | string | O | SDK 버전 |
| `liff.getLineVersion()` | string / null | - | LINE 버전 (외부에서 null) |
| `liff.isInClient()` | boolean | O | LIFF 브라우저 여부 |
| `liff.isLoggedIn()` | boolean | - | 로그인 상태 |
| `liff.isApiAvailable(name)` | boolean | - | API 사용 가능 여부 |

### 5.2 인증

| API | 설명 | 조건 |
|-----|------|------|
| `liff.login(config?)` | 외부 브라우저 로그인 | LIFF 브라우저에서 사용 불가 (자동) |
| `liff.logout()` | 로그아웃 | 페이지 리로드 필요 |
| `liff.getAccessToken()` | Access Token | |
| `liff.getIDToken()` | Raw JWT | openid scope |
| `liff.getDecodedIDToken()` | 디코딩된 프로필 | openid scope, 서버 전송 금지 |

### 5.3 프로필

```typescript
// 사용자 프로필
const profile = await liff.getProfile();
// { userId, displayName, pictureUrl?, statusMessage? }

// 프로필 이미지 크기
// 원본: pictureUrl
// 200x200: pictureUrl + "/large"
// 51x51: pictureUrl + "/small"

// 공식계정 친구 상태
const { friendFlag } = await liff.getFriendship();
```

### 5.4 Context

```typescript
const ctx = liff.getContext();
// {
//   type: "utou" | "group" | "room" | "external" | "none",
//   userId, liffId, viewType, endpointUrl, accessTokenHash,
//   availability: { shareTargetPicker, multipleLiffTransition, ... },
//   scope: ["openid", "profile", ...],
//   menuColorSetting: { ... }
// }
```

### 5.5 메시징

**liff.sendMessages() - 채팅방 메시지 전송**

```typescript
await liff.sendMessages([
  { type: "text", text: "상담 결과입니다" },
  {
    type: "flex",
    altText: "AI 뷰티 상담 결과",
    contents: { /* Flex Message */ }
  }
]);
// 최대 5개, chat_message.write scope, LIFF 브라우저 전용
```

지원 타입: text, image, video, audio, location, template (URI actions만), flex (URI actions만)

**liff.shareTargetPicker() - 친구/그룹 선택 공유**

```typescript
if (liff.isApiAvailable("shareTargetPicker")) {
  const result = await liff.shareTargetPicker(
    [{ type: "flex", altText: "상담 결과", contents: { /* ... */ } }],
    { isMultiple: true }
  );
  if (result) { /* 성공 */ } else { /* 취소 */ }
}
// 로그인 필수, Console에서 활성화 필요
```

### 5.6 윈도우 & 네비게이션

```typescript
liff.openWindow({ url: "https://...", external: false });
liff.closeWindow();  // 외부 브라우저에서 보장 안됨

// Permanent Link
const link = await liff.permanentLink.createUrlBy(
  "https://jisooknows.com/liff/result/123"
);
// → https://liff.line.me/{liffId}/result/123
```

### 5.7 QR 코드

```typescript
const { value } = await liff.scanCodeV2();
// iOS 14.3+, Full 모드, Console에서 "Scan QR" 활성화 필요
```

### 5.8 에러 코드

| 코드 | 설명 |
|------|------|
| `INIT_FAILED` | SDK 초기화 실패 |
| `INVALID_CONFIG` | liffId 없음 / URL 불일치 |
| `INVALID_ARGUMENT` | 잘못된 인자 |
| `UNAUTHORIZED` | 미인가/토큰 없음 |
| `FORBIDDEN` | 권한 없음/미지원 환경 |
| `INVALID_ID_TOKEN` | ID 토큰 검증 실패 |
| `429` | Rate limit 초과 |
| `EXCEPTION_IN_SUBWINDOW` | 서브윈도우 문제 (10분+ 유휴) |

### 5.9 Deprecated 메서드

| Deprecated | 대체 |
|------------|------|
| `liff.scanCode()` | `liff.scanCodeV2()` |
| `liff.getLanguage()` | `liff.getAppLanguage()` |
| `liff.permanentLink.createUrl()` | `liff.permanentLink.createUrlBy()` |
| `line://app/{liffId}` | `https://liff.line.me/{liffId}` |

---

## 6. Server API & 토큰 검증

### 6.1 LIFF Server API

Base URL: `https://api.line.me/liff/v1`
인증: Channel Access Token (Bearer)

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| POST | `/apps` | LIFF 앱 추가 (채널당 최대 30개) |
| GET | `/apps` | 전체 LIFF 앱 조회 |
| PUT | `/apps/{liffId}` | LIFF 앱 수정 |
| DELETE | `/apps/{liffId}` | LIFF 앱 삭제 |

### 6.2 LINE Login API (토큰 검증)

**ID Token 검증 (핵심):**
```
POST https://api.line.me/oauth2/v2.1/verify
Content-Type: application/x-www-form-urlencoded
Body: id_token={jwt}&client_id={channelId}

Response: { sub, name, picture, email, iss, aud, exp, iat, amr }
```

**Access Token 검증:**
```
GET https://api.line.me/oauth2/v2.1/verify?access_token={token}
Response: { scope, client_id, expires_in }
```

**서버 측 프로필 조회:**
```
GET https://api.line.me/v2/profile
Authorization: Bearer {access_token}
Response: { userId, displayName, pictureUrl, statusMessage }
```

**토큰 갱신:**
```
POST https://api.line.me/oauth2/v2.1/token
Body: grant_type=refresh_token&refresh_token={token}&client_id={id}&client_secret={secret}
// Access Token: 30일, Refresh Token: 90일 (갱신해도 연장 안됨)
```

**토큰 폐기:**
```
POST https://api.line.me/oauth2/v2.1/revoke
Body: access_token={token}&client_id={id}&client_secret={secret}
```

**우정 상태 (서버 측):**
```
GET https://api.line.me/friendship/v1/status
Authorization: Bearer {access_token}
Response: { friendFlag: boolean }
```

---

## 7. 브라우저 환경별 차이점

### 7.1 LIFF 브라우저 vs LINE 인앱 브라우저

| 기능 | LIFF 브라우저 | 인앱 브라우저 |
|------|:---:|:---:|
| 화면 크기 지정 | O | X |
| 액션 버튼 / 멀티탭 뷰 | O | X |
| sendMessages / shareTargetPicker | O | X |
| LIFF → LIFF 전환 | O | X |
| 외부 사이트 이동 팝업 | O | X |

### 7.2 LIFF 브라우저 vs 외부 브라우저 - API 가용성

| API | LIFF | 외부 |
|-----|:---:|:---:|
| `liff.login()` | X (자동) | O |
| `liff.sendMessages()` | O | **X** |
| `liff.closeWindow()` | O | 보장 안됨 |
| `liff.getLineVersion()` | 반환 | null |
| `liff.isInClient()` | true | false |

### 7.3 LIFF 브라우저에서 미지원 웹 기술

| 웹 기술 | jisooknows 영향 |
|---------|----------------|
| `theme-color` 메타 태그 | 낮음 |
| `download` 속성 | 없음 |
| Add to Home Screen (A2HS) | 중간 - PWA 불가 |
| **Service Workers** | **높음 - 오프라인 캐싱 불가** |

### 7.4 WebView 웹 API 호환성

| API | iOS WKWebView | Android WebView | 외부 브라우저 |
|-----|:---:|:---:|:---:|
| **EventSource (SSE)** | O (iOS 4.0+) | O (4.4+) | O |
| **fetch + ReadableStream** | 부분적 (BYOB/pipeTo 제한) | O (145+) | O |
| **WebSocket** | O | O | O |
| localStorage / sessionStorage | O | O | O |
| Cookie | O (ITP 제한 가능) | O (SameSite 정책) | O |

---

## 8. 보안 가이드라인

### 8.1 필수 (MUST)

- `liff.getDecodedIDToken()` / `liff.getProfile()` 결과를 **서버에 전송하지 않음**
- Raw JWT(`liff.getIDToken()`)만 서버로 보내 서버 측에서 LINE API로 검증
- 모든 URL은 HTTPS (Cloud Run 기본 충족)
- `liff.init()` resolve 전에 URL 조작하지 않음
- Primary Redirect URL(access_token 포함)을 GA 등 외부 로깅 도구에 전송 금지
- 사용자 동의 없이 쿠키/localStorage로 추적하지 않음
- 카메라/마이크 접근은 반드시 사용자 액션에 의해 트리거

### 8.2 금지 (MUST NOT)

- `window.liff` 직접 선언/수정
- `liff.*` 접두어로 시작하는 쿼리 파라미터 사용 (SDK 예약)
- LIFF URL fragment(#) 기반 라우팅
- 부하 테스트에서 LIFF 스킴 대량 접근
- Service Worker에 의존하는 오프라인 기능 설계

### 8.3 SPA 지원

> Next.js App Router는 History API 기반 = LIFF 호환
> Hash-based 라우팅은 LIFF와 호환성 제한

### 8.4 디바이스 기능 접근

카메라, 마이크, 위치 정보는 **반드시 사용자 버튼 클릭 등 액션**에 의해 트리거

### 8.5 Rate Limit

- LINE Login API의 rate limit 임계값은 비공개
- 초과 시 `429 Too Many Requests` 반환
- 대량 LIFF API 요청 부하 테스트 금지

---

## 9. Pluggable SDK & 번들 최적화

### 9.1 Pluggable SDK (약 34% 번들 절감)

npm 전용, v2.22.0+, `liff.use()`는 반드시 `liff.init()` 전에 실행

**jisooknows 권장 설정:**

```typescript
// src/lib/liff.ts
'use client';

import liff from "@line/liff/core";
import GetOS from "@line/liff/get-os";
import GetAppLanguage from "@line/liff/get-app-language";
import GetContext from "@line/liff/get-context";
import IsInClient from "@line/liff/is-in-client";
import IsLoggedIn from "@line/liff/is-logged-in";
import Login from "@line/liff/login";
import GetProfile from "@line/liff/get-profile";
import SendMessages from "@line/liff/send-messages";
import CloseWindow from "@line/liff/close-window";
import Permission from "@line/liff/permission";
import I18n from "@line/liff/i18n";

liff.use(new GetOS());
liff.use(new GetAppLanguage());
liff.use(new GetContext());
liff.use(new IsInClient());
liff.use(new IsLoggedIn());
liff.use(new Login());
liff.use(new GetProfile());
liff.use(new SendMessages());
liff.use(new CloseWindow());
liff.use(new Permission());
liff.use(new I18n());

// 제외: scanCodeV2, openWindow, logout, permanentLink

export default liff;
```

### 9.2 전체 모듈 목록

| 모듈 | 임포트 경로 | jisooknows 필요 |
|------|------------|:---:|
| `liff.getOS()` | `@line/liff/get-os` | O |
| `liff.getAppLanguage()` | `@line/liff/get-app-language` | O |
| `liff.getContext()` | `@line/liff/get-context` | O |
| `liff.isInClient()` | `@line/liff/is-in-client` | O |
| `liff.isLoggedIn()` | `@line/liff/is-logged-in` | O |
| `liff.login()` | `@line/liff/login` | O |
| `liff.logout()` | `@line/liff/logout` | X |
| `liff.getProfile()` | `@line/liff/get-profile` | O |
| `liff.sendMessages()` | `@line/liff/send-messages` | O |
| `liff.scanCodeV2()` | `@line/liff/scan-code-v2` | X |
| `liff.openWindow()` | `@line/liff/open-window` | X |
| `liff.closeWindow()` | `@line/liff/close-window` | O |
| Permission APIs | `@line/liff/permission` | O |
| Permanent Link | `@line/liff/permanent-link` | X |
| i18n APIs | `@line/liff/i18n` | O |

### 9.3 Dynamic Import (초기 로드 최적화)

```typescript
// components/LiffProvider.tsx
'use client';
import { useEffect, useState } from 'react';

export function LiffProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    (async () => {
      const liff = (await import('@/lib/liff')).default;
      await liff.init({ liffId: process.env.NEXT_PUBLIC_LIFF_ID! });
      setReady(true);
    })();
  }, []);

  if (!ready) return <LoadingSkeleton />;
  return <>{children}</>;
}
```

### 9.4 Next.js 빌드 최적화

```javascript
// next.config.ts
{
  experimental: {
    optimizePackageImports: ['@line/liff'],
  }
}
```

---

## 10. LIFF CLI 개발 워크플로우

### 10.1 설치 & 설정

```bash
npm install -g @line/liff-cli@0.4.1

# 채널 등록
liff-cli channel add <CHANNEL_ID>
liff-cli channel use <CHANNEL_ID>

# SSL 인증서 (최초 1회)
brew install mkcert
mkcert -install
mkcert localhost
```

### 10.2 로컬 개발 서버

```bash
# 터미널 1: Next.js
npm run dev  # http://localhost:3000

# 터미널 2: LIFF 프록시
liff-cli serve --liff-id <LIFF_ID> \
  --url http://localhost:3000/ \
  --proxy-type local-proxy

# 디버깅 (Chrome DevTools)
liff-cli serve --liff-id <LIFF_ID> \
  --url http://localhost:3000/ --inspect

# 실제 기기 테스트 (ngrok)
NGROK_AUTHTOKEN=<TOKEN> liff-cli serve \
  --liff-id <LIFF_ID> --url http://localhost:3000/ \
  --proxy-type ngrok
```

**아키텍처:**
```
[LINE App] → [LIFF Proxy :9000] → [Next.js Dev :3000] → [Cloud Run API]
```

**경고:** 배포된 앱에서 `liff-cli serve` 실행 금지 (Endpoint URL 덮어쓰기)

### 10.3 LIFF 앱 관리 (CLI)

```bash
liff-cli app create --channel-id <ID> --name "jisooknows" \
  --endpoint-url https://jisooknows.com --view-type full
liff-cli app update --liff-id <ID> --name "Updated"
liff-cli app list --channel-id <ID>
liff-cli app delete --liff-id <ID>
```

---

## 11. LIFF Plugin 시스템

### 11.1 구조

LIFF SDK v2.19.0+, 두 가지 필수 요소: `name` + `install()` 메서드

```typescript
class BeautyConsultPlugin {
  name = "beautyConsult";

  install(context: any, option: any) {
    return {
      startSession: () => { /* 상담 세션 시작 */ },
      shareResult: (resultId: string) => { /* 결과 공유 */ }
    };
  }
}

// 사용
liff.use(new BeautyConsultPlugin());
liff.$beautyConsult.startSession();
```

### 11.2 Hook 시스템

| LIFF API | Hook | 타입 | 시점 |
|----------|------|------|------|
| `liff.init()` | `before` | async | init() 호출 직후 |
| `liff.init()` | `after` | async | successCallback 전 |

커스텀 훅: `@liff/hooks` 패키지의 `SyncHook` / `AsyncHook`

### 11.3 공식 플러그인

- **LIFF Inspector**: 별도 기기에서 Chrome DevTools 디버깅
- **LIFF Mock**: 테스트용 모의 모드 (LIFF 서버 없이 단위/부하 테스트)

---

## 12. jisooknows 호환성 매트릭스

### 12.1 핵심 기능 호환성

| 기능 | LIFF (iOS) | LIFF (Android) | 외부 브라우저 | 위험도 |
|------|:---:|:---:|:---:|:---:|
| **SSE 스트리밍 채팅** | O | O | O | **낮음** |
| **fetch + ReadableStream** | 부분적 | O | O | **중간** |
| **WebSocket** | O | O | O | 낮음 |
| **Firebase Auth** | O | O | O | 중간 |
| **localStorage 세션** | O | O | O | 중간 |
| **Next.js App Router** | O | O | O | 낮음 |
| **Service Workers** | **X** | **X** | O | 높음 |
| **PWA 홈화면 추가** | **X** | **X** | O | 높음 |
| **liff.sendMessages()** | O | O | **X** | - |
| **liff.closeWindow()** | O | O | 보장 안됨 | 낮음 |

### 12.2 스트리밍 채팅 위험 평가

jisooknows의 Gemini API SSE 스트리밍은 **전체 위험도: 낮음~중간**

**권장 폴백 전략:**
```
1순위: fetch() + ReadableStream (기본 getReader().read() 패턴)
  ↓ 실패 시
2순위: EventSource (네이티브 SSE, iOS 4.0+/Android 4.4+ 지원)
  ↓ 실패 시
3순위: 폴링 (setInterval + fetch)
```

### 12.3 CSP 헤더 추가 필요

```typescript
// next.config.ts - CSP에 LIFF SDK CDN 허용 추가
// script-src: 'static.line-scdn.net' 추가
// connect-src: 'api.line.me' 추가
```

### 12.4 Android Edge-to-Edge (2026.03.09~)

하단 콘텐츠가 네비게이션 바와 겹칠 수 있음:

```css
.bottom-fixed-button {
  padding-bottom: env(safe-area-inset-bottom, 16px);
}
```

---

## 13. jisooknows 기능별 LIFF API 매핑

| jisooknows 기능 | LIFF Client API | Server API | Scope |
|----------------|-----------------|------------|-------|
| **LINE 로그인** | `init()`, `login()`, `isLoggedIn()` | - | - |
| **Firebase Auth 브릿지** | `getIDToken()` | `POST /oauth2/v2.1/verify` | openid |
| **프로필 표시** | `getProfile()`, `getDecodedIDToken()` | `GET /v2/profile` | profile, openid |
| **이메일 수집** | `getDecodedIDToken().email` | ID Token claim | openid, email |
| **상담 결과 → 채팅** | `sendMessages()` (Flex) | - | chat_message.write |
| **상담 결과 공유** | `shareTargetPicker()` (Flex) | - | 로그인 |
| **공식계정 친구 상태** | `getFriendship()` | `GET /friendship/v1/status` | profile |
| **환경별 UI 분기** | `isInClient()`, `getOS()`, `getContext()` | - | - |
| **다국어 감지** | `getAppLanguage()` | - | - |
| **딥링크** | `permanentLink.createUrlBy()` | - | - |
| **LIFF 앱 관리** | - | `GET/POST/PUT/DELETE /liff/v1/apps` | Channel Token |

### 상담 결과 Flex Message 예시

```typescript
const consultationResult = {
  type: "flex",
  altText: "AI ビューティー相談結果",
  contents: {
    type: "bubble",
    hero: {
      type: "image",
      url: clinicImageUrl,
      size: "full",
      aspectRatio: "20:13"
    },
    body: {
      type: "box",
      layout: "vertical",
      contents: [
        { type: "text", text: "相談結果", weight: "bold", size: "xl" },
        { type: "text", text: summary, wrap: true, size: "sm" }
      ]
    },
    footer: {
      type: "box",
      layout: "vertical",
      contents: [{
        type: "button",
        action: {
          type: "uri",
          label: "詳細を見る",
          uri: `https://liff.line.me/${liffId}/result/${resultId}`
        }
      }, {
        type: "button",
        action: {
          type: "uri",
          label: "私も相談する",
          uri: `https://liff.line.me/${liffId}`
        }
      }]
    }
  }
};
```

---

## 14. 제한사항 & 주의사항 총정리

### 기술적 제한

| 제한 | 영향 | 대응 |
|------|------|------|
| Service Workers 미지원 | 오프라인 캐싱 불가 | 온라인 전용 서비스로 설계 |
| sendMessages() 외부 브라우저 불가 | 채팅 메시지 전송 제한 | `isInClient()` 분기 + shareTargetPicker 폴백 |
| sendMessages() 리로드 후 불가 | 최근 서비스에서 재로드 시 | UX 안내 메시지 표시 |
| 화면 크기 런타임 변경 불가 | Full/Tall/Compact 고정 | Full로 등록 |
| URL 계층 상위 이동 보장 안됨 | Endpoint URL 상위 경로 | 하위 경로만 사용 |
| OpenChat 미지원 | 프로필 조회 불가 | OpenChat 미사용 |
| 채널당 LIFF 앱 30개 제한 | | 충분 |
| URL fragment(#) 사용 불가 | 엔드포인트 URL | Next.js App Router = 문제 없음 |

### 플랫폼별 주의

| 항목 | 내용 |
|------|------|
| Android Edge-to-Edge (2026.03.09~) | 하단 UI safe-area-inset-bottom 적용 필수 |
| iOS WKWebView ITP | 서드파티 쿠키 제한 가능 |
| Android SameSite 정책 | 쿠키 SameSite 속성 주의 |
| webpack v5 호환 | LIFF SDK v2.16.1+ 필수 (Next.js 16) |
| 외부 사이트 이동 경고 | "외부 페이지입니다" 팝업 표시 |

### 세션 관리

| 상황 | 동작 |
|------|------|
| LIFF 앱 닫기 (LINE v15.12.0+, 최근 사용 조건 충족) | 12시간 세션 유지 |
| LIFF 앱 닫기 (조건 미충족) | 즉시 종료, 토큰 만료 |
| LIFF 앱 닫기 (LINE v15.12.0 미만) | 항상 즉시 종료 |
| 최근 사용 서비스 재진입 | 12시간 이내 + 상위 10개 = resume, 그 외 = reload |

---

## 15. LINE MINI App 마이그레이션 로드맵

### 현재 상황

- LINE 공식: **LIFF와 LINE MINI App은 단일 브랜드로 통합 예정**
- 신규 앱은 LINE MINI App 권장
- LIFF v2 = Active 상태, v3 출시일 미정
- LINE MINI App 지역: **일본, 대만, 태국** (jisooknows 타겟 = 일본)

### LIFF vs LINE MINI App

| 항목 | LIFF | LINE MINI App |
|------|------|---------------|
| 채널당 앱 수 | 복수 | **단일** |
| 서비스 메시지 | 불가 | **가능** |
| 인앱 결제 | 불가 | **가능** (일본, 2026.02~) |
| 검색 노출 | 불가 | **가능** (인증 후) |
| 홈화면 추가 | 불가 | **가능** (인증 후) |
| 검증 배지 | 없음 | 있음 (인증 후) |
| 지역 제한 | 없음 | 일본/대만/태국 |
| 기술 기반 | LIFF SDK | LIFF SDK (동일) |

### 마이그레이션 타임라인

| Phase | 시기 | 작업 |
|-------|------|------|
| **Phase 1** | 즉시 | LIFF 앱으로 개발 시작, Pluggable SDK 적용 |
| **Phase 2** | MVP 완성 후 | LINE MINI App 채널 생성, 검증 심사 제출 |
| **Phase 3** | 심사 통과 후 | 홈화면 추가, LINE 검색 노출, 인앱 결제 연동 |
| **Phase 4** | LIFF v3 발표 시 | 공식 마이그레이션 가이드 따라 전환 |

**jisooknows 권장:** 일본 타겟이므로 **처음부터 LINE MINI App 채널로 시작**하는 것이 가장 효율적.
코드는 동일(LIFF SDK), 추가 작업 = 채널 구성 + 개인정보처리방침 URL + 검증 심사

---

## 16. 실행 계획

### Phase 1: 기반 구축 (1주)

- [ ] LINE Developers Console에 Provider "jisooknows" 생성
- [ ] LINE Login 채널 (또는 LINE MINI App 채널) 생성
- [ ] Messaging API 채널 생성 (같은 Provider)
- [ ] LIFF 앱 등록 (Full, openid+profile+chat_message.write)
- [ ] `npm install @line/liff@2.27.3`
- [ ] Pluggable SDK 설정 (`src/lib/liff.ts`)
- [ ] `next.config.ts` CSP에 `static.line-scdn.net`, `api.line.me` 추가

### Phase 2: 인증 통합 (1주)

- [ ] LIFF + Firebase Auth 브릿지 API Route 구현 (`/api/auth/line`)
- [ ] LINE ID Token 서버 검증 로직
- [ ] `liff.isInClient()` 환경 감지 → 인증 플로우 분기
- [ ] PostgreSQL 사용자 테이블에 `line_user_id` 컬럼 추가
- [ ] 기존 Firebase Auth 플로우와 병행 동작 확인

### Phase 3: LIFF 기능 통합 (1주)

- [ ] `liff.getProfile()` → 프로필 표시 연동
- [ ] `liff.getAppLanguage()` → 자동 언어 감지 활용
- [ ] `liff.sendMessages()` → 상담 결과 Flex Message 전송
- [ ] `liff.shareTargetPicker()` → 상담 결과 공유 기능
- [ ] `liff.getFriendship()` → 공식계정 친구 추가 유도 UI

### Phase 4: 테스트 & 최적화 (1주)

- [ ] LIFF CLI 로컬 개발 환경 구축
- [ ] iOS/Android LIFF 브라우저 SSE 스트리밍 테스트
- [ ] Android Edge-to-Edge safe-area 대응
- [ ] 외부 브라우저 폴백 테스트
- [ ] Bundle size 최적화 확인
- [ ] OGP 메타 태그 설정 (공유 시 미리보기 카드)

### Phase 5: LINE MINI App 마이그레이션 (MVP 후)

- [ ] LINE MINI App 채널 전환
- [ ] 개인정보처리방침 URL 등록
- [ ] 검증 심사 제출
- [ ] 서비스 메시지 API 연동 (예약 알림)
- [ ] LINE 검색 노출 / 홈화면 추가 활성화

---

## 참고 문서

- [LIFF Overview](https://developers.line.biz/en/docs/liff/overview/)
- [Developing a LIFF App](https://developers.line.biz/en/docs/liff/developing-liff-apps/)
- [LIFF v2 API Reference](https://developers.line.biz/en/reference/liff/)
- [LIFF Server API Reference](https://developers.line.biz/en/reference/liff-server/)
- [Development Guidelines](https://developers.line.biz/en/docs/liff/development-guidelines/)
- [Using User Profile](https://developers.line.biz/en/docs/liff/using-user-profile/)
- [LIFF vs In-App Browser](https://developers.line.biz/en/docs/liff/differences-between-liff-browser-and-line-in-app-browser/)
- [LIFF vs External Browser](https://developers.line.biz/en/docs/liff/differences-between-liff-browser-and-external-browser/)
- [Pluggable SDK](https://developers.line.biz/en/docs/liff/pluggable-sdk/)
- [LIFF Plugin](https://developers.line.biz/en/docs/liff/liff-plugin/)
- [LIFF CLI](https://developers.line.biz/en/docs/liff/liff-cli/)
- [Versioning Policy](https://developers.line.biz/en/docs/liff/versioning-policy/)
- [Release Notes](https://developers.line.biz/en/docs/liff/release-notes/)
- [Registering LIFF Apps](https://developers.line.biz/en/docs/liff/registering-liff-apps/)
- [Opening a LIFF App](https://developers.line.biz/en/docs/liff/opening-liff-app/)
- [Minimizing LIFF Browser](https://developers.line.biz/en/docs/liff/minimizing-liff-browser/)
