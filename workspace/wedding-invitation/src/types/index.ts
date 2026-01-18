// 카카오 SDK 타입 정의
declare global {
  interface Window {
    Kakao: {
      init: (key: string) => void;
      isInitialized: () => boolean;
      Share: {
        sendDefault: (options: KakaoShareOptions) => void;
      };
    };
  }
}

interface KakaoShareOptions {
  objectType: 'feed';
  content: {
    title: string;
    description: string;
    imageUrl: string;
    link: {
      mobileWebUrl: string;
      webUrl: string;
    };
  };
  buttons?: Array<{
    title: string;
    link: {
      mobileWebUrl: string;
      webUrl: string;
    };
  }>;
}

// 갤러리 이미지 타입
export interface GalleryImage {
  src: string;
  alt: string;
}

// 계좌 정보 타입
export interface AccountInfo {
  bank: string;
  number: string;
  holder: string;
}

// 셔틀버스 정보 타입
export interface ShuttleRoute {
  name: string;
  departure: string;
  times: string[];
  duration: string;
}

// 섹션 애니메이션 프롭스
export interface SectionProps {
  children: React.ReactNode;
  className?: string;
  id?: string;
}

export {};
