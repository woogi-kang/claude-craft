import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// 날짜 포맷팅
export function formatDate(date: Date | string): string {
  const d = new Date(date);
  return `${d.getFullYear()}년 ${d.getMonth() + 1}월 ${d.getDate()}일`;
}

// D-Day 계산
export function calculateDday(targetDate: Date | string): number {
  const target = new Date(targetDate);
  const today = new Date();

  // 시간을 0으로 설정하여 날짜만 비교
  target.setHours(0, 0, 0, 0);
  today.setHours(0, 0, 0, 0);

  const diff = target.getTime() - today.getTime();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

// 클립보드 복사
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      document.execCommand('copy');
      return true;
    } catch {
      return false;
    } finally {
      textArea.remove();
    }
  }
}

// 전화 연결
export function callPhone(phoneNumber: string): void {
  window.location.href = `tel:${phoneNumber.replace(/-/g, '')}`;
}

// 문자 보내기
export function sendSms(phoneNumber: string): void {
  window.location.href = `sms:${phoneNumber.replace(/-/g, '')}`;
}

// 카카오톡 공유
export function shareKakao(): void {
  if (typeof window !== 'undefined' && window.Kakao) {
    window.Kakao.Share.sendDefault({
      objectType: 'feed',
      content: {
        title: '결혼식에 초대합니다',
        description: '소중한 분들을 모시고 사랑의 약속을 하려 합니다.',
        imageUrl: `${window.location.origin}/images/og-image.jpg`,
        link: {
          mobileWebUrl: window.location.href,
          webUrl: window.location.href,
        },
      },
      buttons: [
        {
          title: '청첩장 보기',
          link: {
            mobileWebUrl: window.location.href,
            webUrl: window.location.href,
          },
        },
      ],
    });
  }
}

// URL 공유
export async function shareUrl(): Promise<boolean> {
  if (navigator.share) {
    try {
      await navigator.share({
        title: '결혼식에 초대합니다',
        text: '소중한 분들을 모시고 사랑의 약속을 하려 합니다.',
        url: window.location.href,
      });
      return true;
    } catch {
      return false;
    }
  }
  return copyToClipboard(window.location.href);
}

// 캘린더 저장 (ICS 형식)
export function saveToCalendar(
  title: string,
  description: string,
  location: string,
  startDate: Date,
  endDate: Date
): void {
  const formatICSDate = (date: Date): string => {
    return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
  };

  const icsContent = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Wedding Invitation//EN
BEGIN:VEVENT
DTSTART:${formatICSDate(startDate)}
DTEND:${formatICSDate(endDate)}
SUMMARY:${title}
DESCRIPTION:${description}
LOCATION:${location}
END:VEVENT
END:VCALENDAR`;

  const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'wedding.ics';
  link.click();
  URL.revokeObjectURL(link.href);
}

// 연락처 저장 (vCard 형식)
export function saveContact(
  name: string,
  phone: string,
  note: string
): void {
  const vCardContent = `BEGIN:VCARD
VERSION:3.0
FN:${name}
TEL;TYPE=CELL:${phone}
NOTE:${note}
END:VCARD`;

  const blob = new Blob([vCardContent], { type: 'text/vcard;charset=utf-8' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${name}.vcf`;
  link.click();
  URL.revokeObjectURL(link.href);
}
