// 결혼식 정보 상수
// 이 파일의 값들을 수정하여 청첩장 내용을 변경하세요

export const WEDDING_INFO = {
  // 신랑 정보
  groom: {
    name: '김민준',
    englishName: 'Minjun',
    father: '김철수',
    mother: '박영희',
    fatherDeceased: false,
    motherDeceased: false,
    phone: '010-1234-5678',
    account: {
      bank: '신한은행',
      number: '110-123-456789',
      holder: '김민준',
    },
    fatherAccount: {
      bank: '국민은행',
      number: '123-456-789012',
      holder: '김철수',
    },
    motherAccount: {
      bank: '우리은행',
      number: '1002-123-456789',
      holder: '박영희',
    },
  },

  // 신부 정보
  bride: {
    name: '이서연',
    englishName: 'Seoyeon',
    father: '이영수',
    mother: '최미경',
    fatherDeceased: false,
    motherDeceased: false,
    phone: '010-9876-5432',
    account: {
      bank: '카카오뱅크',
      number: '3333-12-3456789',
      holder: '이서연',
    },
    fatherAccount: {
      bank: '하나은행',
      number: '123-456789-12345',
      holder: '이영수',
    },
    motherAccount: {
      bank: '농협',
      number: '123-4567-8901-23',
      holder: '최미경',
    },
  },

  // 결혼식 날짜/시간
  date: '2025-05-17T14:00:00+09:00',
  dateDisplay: {
    year: 2025,
    month: 5,
    day: 17,
    dayOfWeek: '토요일',
    time: '오후 2시',
    timeDetail: '14:00',
  },

  // 예식장 정보
  venue: {
    name: '더채플앳청담',
    hall: '5층 그랜드홀',
    address: '서울특별시 강남구 청담동 123-45',
    roadAddress: '서울특별시 강남구 도산대로 123',
    tel: '02-1234-5678',
    coordinates: {
      lat: 37.5234,
      lng: 127.0456,
    },
    parking: '건물 내 지하주차장 이용 가능 (2시간 무료)',
    subway: '압구정로데오역 5번 출구에서 도보 5분',
    bus: '청담사거리 정류장 하차 (340, 143, 463)',
  },

  // 셔틀버스 정보
  shuttle: {
    available: true,
    routes: [
      {
        name: '강남역 출발',
        departure: '강남역 11번 출구 앞',
        times: ['12:30', '13:00', '13:30'],
        duration: '약 20분 소요',
      },
      {
        name: '잠실역 출발',
        departure: '잠실역 8번 출구 앞',
        times: ['12:30', '13:00'],
        duration: '약 25분 소요',
      },
    ],
  },

  // 인사말
  greeting: {
    title: '결혼합니다',
    message: `서로 다른 두 사람이 만나
하나의 사랑을 이루게 되었습니다.

소중한 분들을 모시고
사랑의 약속을 하려 합니다.

부디 오셔서 축복해 주시면
더없는 기쁨으로 간직하겠습니다.`,
  },

  // 갤러리 이미지
  gallery: {
    images: [
      { src: '/images/gallery/1.jpg', alt: '웨딩 사진 1' },
      { src: '/images/gallery/2.jpg', alt: '웨딩 사진 2' },
      { src: '/images/gallery/3.jpg', alt: '웨딩 사진 3' },
      { src: '/images/gallery/4.jpg', alt: '웨딩 사진 4' },
      { src: '/images/gallery/5.jpg', alt: '웨딩 사진 5' },
      { src: '/images/gallery/6.jpg', alt: '웨딩 사진 6' },
    ],
  },

  // 영상 URL (YouTube)
  video: {
    enabled: true,
    youtubeId: 'dQw4w9WgXcQ', // YouTube 영상 ID로 교체
    title: '우리의 이야기',
  },

  // 배경음악
  music: {
    enabled: true,
    src: '/music/bgm.mp3',
    title: 'Beautiful in White',
    artist: 'Shane Filan',
  },

  // RSVP Google Forms URL
  rsvp: {
    enabled: true,
    formUrl: 'https://forms.gle/your-form-id',
  },

  // 방명록 (Giscus 설정)
  guestbook: {
    enabled: true,
    // Giscus 설정 - https://giscus.app 에서 생성
    repo: 'your-username/your-repo',
    repoId: 'your-repo-id',
    category: 'Announcements',
    categoryId: 'your-category-id',
  },
};

// OG 메타데이터
export const OG_METADATA = {
  title: `${WEDDING_INFO.groom.name} ♥ ${WEDDING_INFO.bride.name} 결혼합니다`,
  description: `${WEDDING_INFO.dateDisplay.year}년 ${WEDDING_INFO.dateDisplay.month}월 ${WEDDING_INFO.dateDisplay.day}일 ${WEDDING_INFO.dateDisplay.dayOfWeek} ${WEDDING_INFO.dateDisplay.time}`,
  image: '/images/og-image.jpg',
  url: 'https://your-wedding-invitation.vercel.app',
};

// 디자인 테마
export const THEME = {
  colors: {
    primary: '#8B7355', // 따뜻한 브라운
    secondary: '#F5F0EB', // 아이보리
    accent: '#C9A961', // 골드
    text: '#2C3E50', // 다크 네이비
    textLight: '#7F8C8D', // 그레이
    background: '#FFFCF9', // 웜 화이트
    white: '#FFFFFF',
  },
  fonts: {
    title: 'var(--font-serif)',
    body: 'var(--font-sans)',
  },
};
