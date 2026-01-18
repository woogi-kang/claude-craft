'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface SectionProps {
  children: React.ReactNode;
  className?: string;
  id?: string;
  background?: 'default' | 'white' | 'secondary';
}

export function Section({
  children,
  className,
  id,
  background = 'default',
}: SectionProps) {
  const bgColors = {
    default: 'bg-[var(--color-background)]',
    white: 'bg-white',
    secondary: 'bg-[var(--color-secondary)]',
  };

  return (
    <motion.section
      id={id}
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className={cn('section', bgColors[background], className)}
    >
      <div className="mx-auto max-w-lg">{children}</div>
    </motion.section>
  );
}

interface SectionTitleProps {
  title: string;
  subtitle?: string;
  className?: string;
}

export function SectionTitle({ title, subtitle, className }: SectionTitleProps) {
  return (
    <div className={cn('mb-10', className)}>
      <h2 className="section-title">{title}</h2>
      {subtitle && <p className="section-subtitle">{subtitle}</p>}
    </div>
  );
}

export function Divider({ className }: { className?: string }) {
  return <div className={cn('divider', className)} />;
}

export function HorizontalDivider({ className }: { className?: string }) {
  return <div className={cn('divider-horizontal', className)} />;
}
