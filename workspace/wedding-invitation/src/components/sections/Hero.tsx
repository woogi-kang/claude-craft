'use client';

import { motion } from 'framer-motion';
import { ChevronDown, Heart } from 'lucide-react';
import { WEDDING_INFO } from '@/lib/constants';
import { useCountdown } from '@/hooks/useCountdown';

export function Hero() {
  const { groom, bride, dateDisplay, date } = WEDDING_INFO;
  const countdown = useCountdown(date);

  return (
    <section className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden">
      {/* Background */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: 'url(/images/hero-bg.jpg)',
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-black/20 to-black/40" />
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center px-6 text-center text-white">
        {/* Date */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-6 font-serif text-sm tracking-[0.3em] opacity-90"
        >
          {dateDisplay.year}.{String(dateDisplay.month).padStart(2, '0')}.
          {String(dateDisplay.day).padStart(2, '0')} {dateDisplay.dayOfWeek}
        </motion.p>

        {/* Names */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-8 flex items-center gap-4"
        >
          <span className="font-serif text-3xl font-medium tracking-wider sm:text-4xl">
            {groom.name}
          </span>
          <Heart className="h-6 w-6 animate-heartbeat text-rose-300" fill="currentColor" />
          <span className="font-serif text-3xl font-medium tracking-wider sm:text-4xl">
            {bride.name}
          </span>
        </motion.div>

        {/* English Names */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mb-12 font-serif text-base tracking-[0.2em] opacity-80"
        >
          {groom.englishName} & {bride.englishName}
        </motion.p>

        {/* D-Day Counter */}
        {!countdown.isExpired && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="flex items-center gap-1 rounded-full bg-white/20 px-6 py-3 backdrop-blur-sm"
          >
            <span className="text-sm opacity-90">결혼식까지</span>
            <span className="ml-2 font-serif text-2xl font-semibold">
              D-{countdown.days}
            </span>
          </motion.div>
        )}

        {countdown.isExpired && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="rounded-full bg-white/20 px-6 py-3 backdrop-blur-sm"
          >
            <span className="font-serif text-lg">We got married!</span>
          </motion.div>
        )}
      </div>

      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="absolute bottom-8 left-1/2 z-10 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          <ChevronDown className="h-8 w-8 text-white/70" />
        </motion.div>
      </motion.div>
    </section>
  );
}
