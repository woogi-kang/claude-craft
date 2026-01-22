'use client';

import { motion } from 'framer-motion';
import { Calendar, Clock, MapPin } from 'lucide-react';
import { Section, SectionTitle, HorizontalDivider } from '@/components/common/Section';
import { WEDDING_INFO } from '@/lib/constants';
import { useCountdown } from '@/hooks/useCountdown';

export function WeddingInfo() {
  const { date, dateDisplay, venue } = WEDDING_INFO;
  const countdown = useCountdown(date);

  // 달력 데이터 생성
  const generateCalendar = () => {
    const year = dateDisplay.year;
    const month = dateDisplay.month - 1; // 0-indexed
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    const days = [];
    // 빈 칸 추가
    for (let i = 0; i < firstDay; i++) {
      days.push(null);
    }
    // 날짜 추가
    for (let i = 1; i <= lastDate; i++) {
      days.push(i);
    }
    return days;
  };

  const calendarDays = generateCalendar();
  const weekDays = ['일', '월', '화', '수', '목', '금', '토'];

  return (
    <Section id="info" background="white">
      <SectionTitle title="예식 안내" subtitle="WEDDING DAY" />

      {/* Date & Time */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="mb-8 text-center"
      >
        <div className="mb-2 flex items-center justify-center gap-3">
          <Calendar className="h-5 w-5 text-[var(--color-primary)]" />
          <span className="font-serif text-lg">
            {dateDisplay.year}년 {dateDisplay.month}월 {dateDisplay.day}일 {dateDisplay.dayOfWeek}
          </span>
        </div>
        <div className="flex items-center justify-center gap-3">
          <Clock className="h-5 w-5 text-[var(--color-primary)]" />
          <span className="font-serif text-lg">{dateDisplay.time}</span>
        </div>
      </motion.div>

      {/* Calendar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.1 }}
        className="mx-auto mb-8 max-w-xs rounded-2xl bg-[var(--color-secondary)] p-4"
      >
        {/* Month Header */}
        <div className="mb-4 text-center">
          <span className="font-serif text-lg font-medium text-[var(--color-primary)]">
            {dateDisplay.year}. {String(dateDisplay.month).padStart(2, '0')}
          </span>
        </div>

        {/* Week Days */}
        <div className="mb-2 grid grid-cols-7 gap-1 text-center text-xs">
          {weekDays.map((day, index) => (
            <span
              key={day}
              className={index === 0 ? 'text-red-400' : index === 6 ? 'text-blue-400' : 'text-[var(--color-text-light)]'}
            >
              {day}
            </span>
          ))}
        </div>

        {/* Calendar Grid */}
        <div className="grid grid-cols-7 gap-1 text-center text-sm">
          {calendarDays.map((day, index) => (
            <div
              key={index}
              className={`
                flex h-8 w-8 items-center justify-center rounded-full
                ${day === dateDisplay.day
                  ? 'bg-[var(--color-primary)] font-bold text-white'
                  : day
                    ? 'text-[var(--color-text)]'
                    : ''
                }
                ${day && index % 7 === 0 ? 'text-red-400' : ''}
                ${day && index % 7 === 6 ? 'text-blue-400' : ''}
              `}
            >
              {day}
            </div>
          ))}
        </div>
      </motion.div>

      {/* D-Day Countdown */}
      {!countdown.isExpired && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <div className="flex justify-center gap-4">
            <div className="text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-[var(--color-primary)] font-serif text-2xl font-bold text-white">
                {countdown.days}
              </div>
              <span className="mt-1 block text-xs text-[var(--color-text-light)]">DAYS</span>
            </div>
            <div className="text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-[var(--color-primary)]/80 font-serif text-2xl font-bold text-white">
                {String(countdown.hours).padStart(2, '0')}
              </div>
              <span className="mt-1 block text-xs text-[var(--color-text-light)]">HOURS</span>
            </div>
            <div className="text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-[var(--color-primary)]/60 font-serif text-2xl font-bold text-white">
                {String(countdown.minutes).padStart(2, '0')}
              </div>
              <span className="mt-1 block text-xs text-[var(--color-text-light)]">MINS</span>
            </div>
            <div className="text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-[var(--color-primary)]/40 font-serif text-2xl font-bold text-white">
                {String(countdown.seconds).padStart(2, '0')}
              </div>
              <span className="mt-1 block text-xs text-[var(--color-text-light)]">SECS</span>
            </div>
          </div>
        </motion.div>
      )}

      <HorizontalDivider />

      {/* Venue Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.3 }}
        className="text-center"
      >
        <div className="mb-2 flex items-center justify-center gap-2">
          <MapPin className="h-5 w-5 text-[var(--color-primary)]" />
          <span className="font-serif text-lg font-medium">{venue.name}</span>
        </div>
        <p className="text-sm text-[var(--color-text-light)]">{venue.hall}</p>
        <p className="mt-2 text-sm text-[var(--color-text)]">{venue.roadAddress}</p>
        <p className="text-sm text-[var(--color-text-light)]">Tel. {venue.tel}</p>
      </motion.div>
    </Section>
  );
}
