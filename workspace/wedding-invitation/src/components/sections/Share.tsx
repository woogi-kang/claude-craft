'use client';

import { motion } from 'framer-motion';
import { Share2, Calendar, User, Link2, MessageCircle } from 'lucide-react';
import { toast } from 'sonner';
import { Section, SectionTitle } from '@/components/common/Section';
import { Button } from '@/components/ui/Button';
import { WEDDING_INFO } from '@/lib/constants';
import { saveToCalendar, saveContact, copyToClipboard, shareUrl } from '@/lib/utils';

export function Share() {
  const { groom, bride, date, dateDisplay, venue } = WEDDING_INFO;

  const handleSaveCalendar = () => {
    const startDate = new Date(date);
    const endDate = new Date(startDate.getTime() + 2 * 60 * 60 * 1000); // 2시간 후

    saveToCalendar(
      `${groom.name} ♥ ${bride.name} 결혼식`,
      `${venue.name} ${venue.hall}에서 결혼식이 있습니다.`,
      venue.roadAddress,
      startDate,
      endDate
    );

    toast.success('캘린더에 저장되었습니다');
  };

  const handleSaveGroomContact = () => {
    saveContact(
      `${groom.name} (신랑)`,
      groom.phone,
      `${dateDisplay.year}년 ${dateDisplay.month}월 ${dateDisplay.day}일 결혼`
    );
    toast.success('연락처가 저장되었습니다');
  };

  const handleSaveBrideContact = () => {
    saveContact(
      `${bride.name} (신부)`,
      bride.phone,
      `${dateDisplay.year}년 ${dateDisplay.month}월 ${dateDisplay.day}일 결혼`
    );
    toast.success('연락처가 저장되었습니다');
  };

  const handleCopyLink = async () => {
    const success = await copyToClipboard(window.location.href);
    if (success) {
      toast.success('링크가 복사되었습니다');
    } else {
      toast.error('복사에 실패했습니다');
    }
  };

  const handleShare = async () => {
    await shareUrl();
    toast.success('공유 창이 열렸습니다');
  };

  const handleKakaoShare = () => {
    // 카카오 SDK가 로드되지 않았을 경우 대비
    if (typeof window !== 'undefined' && window.Kakao) {
      if (!window.Kakao.isInitialized()) {
        // 카카오 앱 키로 초기화 필요
        // window.Kakao.init('YOUR_KAKAO_APP_KEY');
      }

      window.Kakao.Share.sendDefault({
        objectType: 'feed',
        content: {
          title: `${groom.name} ♥ ${bride.name} 결혼합니다`,
          description: `${dateDisplay.year}년 ${dateDisplay.month}월 ${dateDisplay.day}일 ${dateDisplay.dayOfWeek} ${dateDisplay.time}\n${venue.name} ${venue.hall}`,
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
    } else {
      toast.info('카카오 공유를 사용하려면 카카오 SDK 설정이 필요합니다');
    }
  };

  return (
    <Section id="share" background="white">
      <SectionTitle title="공유하기" subtitle="SHARE" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="space-y-4"
      >
        {/* Calendar Save */}
        <div className="rounded-xl bg-[var(--color-secondary)] p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white">
                <Calendar className="h-5 w-5 text-[var(--color-primary)]" />
              </div>
              <div>
                <p className="font-medium">캘린더에 저장</p>
                <p className="text-xs text-[var(--color-text-light)]">
                  결혼식 일정을 저장해요
                </p>
              </div>
            </div>
            <Button variant="ghost" size="sm" onClick={handleSaveCalendar}>
              저장
            </Button>
          </div>
        </div>

        {/* Contact Save */}
        <div className="rounded-xl bg-[var(--color-secondary)] p-4">
          <div className="mb-3 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white">
              <User className="h-5 w-5 text-[var(--color-primary)]" />
            </div>
            <div>
              <p className="font-medium">연락처 저장</p>
              <p className="text-xs text-[var(--color-text-light)]">
                연락처를 저장해요
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={handleSaveGroomContact}
              className="flex-1"
            >
              신랑 {groom.name}
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={handleSaveBrideContact}
              className="flex-1"
            >
              신부 {bride.name}
            </Button>
          </div>
        </div>

        {/* Share Buttons */}
        <div className="grid grid-cols-3 gap-3">
          {/* Kakao */}
          <button
            onClick={handleKakaoShare}
            className="flex flex-col items-center gap-2 rounded-xl bg-[#FEE500] p-4 transition-transform hover:scale-105"
          >
            <MessageCircle className="h-6 w-6 text-[#3C1E1E]" />
            <span className="text-xs font-medium text-[#3C1E1E]">카카오톡</span>
          </button>

          {/* Link Copy */}
          <button
            onClick={handleCopyLink}
            className="flex flex-col items-center gap-2 rounded-xl bg-[var(--color-secondary)] p-4 transition-transform hover:scale-105"
          >
            <Link2 className="h-6 w-6 text-[var(--color-primary)]" />
            <span className="text-xs font-medium">링크 복사</span>
          </button>

          {/* Native Share */}
          <button
            onClick={handleShare}
            className="flex flex-col items-center gap-2 rounded-xl bg-[var(--color-secondary)] p-4 transition-transform hover:scale-105"
          >
            <Share2 className="h-6 w-6 text-[var(--color-primary)]" />
            <span className="text-xs font-medium">공유하기</span>
          </button>
        </div>
      </motion.div>
    </Section>
  );
}
