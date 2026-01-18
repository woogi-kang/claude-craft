'use client';

import { motion } from 'framer-motion';
import { ClipboardCheck, ExternalLink } from 'lucide-react';
import { Section, SectionTitle } from '@/components/common/Section';
import { Button } from '@/components/ui/Button';
import { WEDDING_INFO } from '@/lib/constants';

export function RSVP() {
  const { rsvp } = WEDDING_INFO;

  if (!rsvp.enabled) return null;

  const openRSVPForm = () => {
    window.open(rsvp.formUrl, '_blank');
  };

  return (
    <Section id="rsvp" background="white">
      <SectionTitle title="참석 의사 전달" subtitle="RSVP" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center"
      >
        <div className="mb-6 flex justify-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-secondary)]">
            <ClipboardCheck className="h-8 w-8 text-[var(--color-primary)]" />
          </div>
        </div>

        <p className="mb-6 text-sm text-[var(--color-text-light)]">
          참석 여부를 미리 알려주시면
          <br />
          예식 준비에 큰 도움이 됩니다
        </p>

        <Button onClick={openRSVPForm} size="lg">
          참석 의사 전달하기
          <ExternalLink className="h-4 w-4" />
        </Button>
      </motion.div>
    </Section>
  );
}
