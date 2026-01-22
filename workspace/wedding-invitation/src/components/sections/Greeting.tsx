'use client';

import { Phone, MessageCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { Section, SectionTitle, HorizontalDivider } from '@/components/common/Section';
import { WEDDING_INFO } from '@/lib/constants';
import { callPhone, sendSms } from '@/lib/utils';

export function Greeting() {
  const { groom, bride, greeting } = WEDDING_INFO;

  return (
    <Section id="greeting" background="white">
      <SectionTitle title={greeting.title} subtitle="INVITATION" />

      {/* Message */}
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ delay: 0.2 }}
        className="mb-10 text-center"
      >
        <p className="whitespace-pre-line font-serif text-sm leading-relaxed text-[var(--color-text)] sm:text-base">
          {greeting.message}
        </p>
      </motion.div>

      <HorizontalDivider />

      {/* Parents Names */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.3 }}
        className="space-y-4 text-center"
      >
        {/* Groom's Parents */}
        <div className="flex items-center justify-center gap-2 text-sm">
          <span className="text-[var(--color-text-light)]">
            {groom.fatherDeceased ? '故 ' : ''}{groom.father}
            {' · '}
            {groom.motherDeceased ? '故 ' : ''}{groom.mother}
          </span>
          <span className="text-[var(--color-primary)]">의 아들</span>
          <span className="font-medium">{groom.name}</span>
        </div>

        {/* Bride's Parents */}
        <div className="flex items-center justify-center gap-2 text-sm">
          <span className="text-[var(--color-text-light)]">
            {bride.fatherDeceased ? '故 ' : ''}{bride.father}
            {' · '}
            {bride.motherDeceased ? '故 ' : ''}{bride.mother}
          </span>
          <span className="text-[var(--color-primary)]">의 딸</span>
          <span className="font-medium">{bride.name}</span>
        </div>
      </motion.div>

      {/* Contact Buttons */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.4 }}
        className="mt-10 grid grid-cols-2 gap-4"
      >
        {/* Groom Contact */}
        <div className="rounded-xl bg-[var(--color-secondary)] p-4 text-center">
          <p className="mb-2 text-xs text-[var(--color-text-light)]">신랑에게 연락하기</p>
          <p className="mb-3 font-medium">{groom.name}</p>
          <div className="flex justify-center gap-2">
            <button
              onClick={() => callPhone(groom.phone)}
              className="flex h-9 w-9 items-center justify-center rounded-full bg-[var(--color-primary)] text-white transition-transform hover:scale-105"
              aria-label="전화하기"
            >
              <Phone className="h-4 w-4" />
            </button>
            <button
              onClick={() => sendSms(groom.phone)}
              className="flex h-9 w-9 items-center justify-center rounded-full bg-[var(--color-accent)] text-white transition-transform hover:scale-105"
              aria-label="문자하기"
            >
              <MessageCircle className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Bride Contact */}
        <div className="rounded-xl bg-[var(--color-secondary)] p-4 text-center">
          <p className="mb-2 text-xs text-[var(--color-text-light)]">신부에게 연락하기</p>
          <p className="mb-3 font-medium">{bride.name}</p>
          <div className="flex justify-center gap-2">
            <button
              onClick={() => callPhone(bride.phone)}
              className="flex h-9 w-9 items-center justify-center rounded-full bg-[var(--color-primary)] text-white transition-transform hover:scale-105"
              aria-label="전화하기"
            >
              <Phone className="h-4 w-4" />
            </button>
            <button
              onClick={() => sendSms(bride.phone)}
              className="flex h-9 w-9 items-center justify-center rounded-full bg-[var(--color-accent)] text-white transition-transform hover:scale-105"
              aria-label="문자하기"
            >
              <MessageCircle className="h-4 w-4" />
            </button>
          </div>
        </div>
      </motion.div>
    </Section>
  );
}
