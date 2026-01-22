# Wedding Invitation (웨딩 청첩장)

모바일 최적화된 웨딩 청첩장 스태틱 사이트입니다.

## Features

### 필수 섹션
- **메인 커버 (Hero)**: 신랑/신부 이름, 결혼식 날짜, 배경 이미지
- **인사말**: 양가 부모님 성함, 결혼 인사 메시지, 연락처
- **갤러리**: 웨딩 사진 슬라이더 + 라이트박스
- **예식 정보**: 날짜, 시간, 장소, 달력, D-Day 카운트다운
- **오시는 길**: 지도 (카카오맵/네이버/티맵), 교통 안내, 셔틀버스
- **계좌 정보**: 신랑측/신부측 계좌번호 (접기 기능, 복사)
- **카카오톡 공유**: OG 메타태그 기반 썸네일

### 선택 섹션
- **영상**: YouTube 임베드
- **배경음악**: 자동재생 BGM + 컨트롤 버튼
- **RSVP**: Google Forms 연동 참석 의사 확인
- **방명록**: Giscus (GitHub Discussions) 기반
- **모바일 저장**: 연락처 저장 (vCard), 일정 저장 (ICS)

## Tech Stack

| Category | Technology |
|----------|------------|
| Framework | Next.js 15+ (App Router, Static Export) |
| Styling | Tailwind CSS v4 |
| Animation | Framer Motion |
| Carousel | Embla Carousel |
| Icons | Lucide React |
| Toast | Sonner |

## Getting Started

### 1. 의존성 설치

```bash
npm install
# 또는
npm install --cache=/tmp/npm-cache  # npm 캐시 문제 시
```

### 2. 개발 서버 실행

```bash
npm run dev
```

[http://localhost:3000](http://localhost:3000) 에서 확인

### 3. 정보 수정

`src/lib/constants.ts` 파일에서 결혼식 정보를 수정하세요:

```typescript
export const WEDDING_INFO = {
  groom: {
    name: '김민준',
    // ...
  },
  bride: {
    name: '이서연',
    // ...
  },
  date: '2025-05-17T14:00:00+09:00',
  venue: {
    name: '더채플앳청담',
    // ...
  },
  // ...
};
```

### 4. 이미지 추가

```
public/
├── images/
│   ├── hero-bg.jpg          # 메인 배경 이미지 (1080x1920 권장)
│   ├── og-image.jpg         # 카카오톡 공유 이미지 (800x400)
│   └── gallery/
│       ├── 1.jpg            # 갤러리 이미지들
│       ├── 2.jpg
│       └── ...
├── music/
│   └── bgm.mp3              # 배경음악 (선택)
└── favicon.ico
```

### 5. 빌드 및 배포

```bash
# 빌드
npm run build

# 빌드 결과물 확인
npx serve out
```

## Deployment

### Vercel (권장)

1. [Vercel](https://vercel.com)에 GitHub 저장소 연결
2. Framework Preset: Next.js 자동 감지
3. Deploy!

### GitHub Pages

1. `next.config.ts`에서 `basePath` 주석 해제:
   ```typescript
   basePath: '/your-repo-name',
   ```

2. GitHub Actions 또는 수동 배포

## Customization

### 색상 테마

`src/app/globals.css`에서 CSS 변수 수정:

```css
:root {
  --color-primary: #8B7355;    /* 메인 색상 */
  --color-secondary: #F5F0EB;  /* 보조 색상 */
  --color-accent: #C9A961;     /* 강조 색상 */
}
```

### 카카오톡 공유

카카오 공유 기능 활성화:

1. [Kakao Developers](https://developers.kakao.com)에서 앱 생성
2. JavaScript 키 발급
3. `src/components/sections/Share.tsx`에서 초기화:
   ```typescript
   window.Kakao.init('YOUR_KAKAO_APP_KEY');
   ```

### 방명록 (Giscus)

1. [giscus.app](https://giscus.app)에서 설정 생성
2. `src/lib/constants.ts`에서 설정 업데이트:
   ```typescript
   guestbook: {
     repo: 'your-username/your-repo',
     repoId: 'your-repo-id',
     category: 'Announcements',
     categoryId: 'your-category-id',
   },
   ```

### RSVP (Google Forms)

1. Google Forms에서 참석 의사 폼 생성
2. `src/lib/constants.ts`에서 URL 업데이트:
   ```typescript
   rsvp: {
     formUrl: 'https://forms.gle/your-form-id',
   },
   ```

## Project Structure

```
src/
├── app/
│   ├── layout.tsx          # Root Layout (메타태그, 폰트)
│   ├── page.tsx            # 메인 페이지
│   └── globals.css         # 글로벌 스타일
├── components/
│   ├── sections/           # 페이지 섹션 컴포넌트
│   ├── ui/                 # UI 컴포넌트 (Button, Modal)
│   └── common/             # 공통 컴포넌트 (Section, Divider)
├── hooks/                  # Custom Hooks
├── lib/
│   ├── constants.ts        # 결혼식 정보 상수
│   └── utils.ts            # 유틸리티 함수
└── types/                  # TypeScript 타입
```

## License

MIT License
