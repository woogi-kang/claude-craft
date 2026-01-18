'use client';

import { motion } from 'framer-motion';
import { Music, Pause, Play } from 'lucide-react';
import { useAudioPlayer } from '@/hooks/useAudioPlayer';
import { WEDDING_INFO } from '@/lib/constants';

export function MusicPlayer() {
  const { music } = WEDDING_INFO;
  const { isPlaying, toggle } = useAudioPlayer(music.src, music.enabled);

  if (!music.enabled) return null;

  return (
    <motion.button
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 1.5 }}
      onClick={toggle}
      className="fixed bottom-6 right-6 z-40 flex h-12 w-12 items-center justify-center rounded-full bg-white shadow-lg transition-transform hover:scale-105"
      aria-label={isPlaying ? '음악 일시정지' : '음악 재생'}
    >
      {isPlaying ? (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
        >
          <Music className="h-5 w-5 text-[var(--color-primary)]" />
        </motion.div>
      ) : (
        <Play className="h-5 w-5 text-[var(--color-primary)] ml-0.5" />
      )}

      {/* Playing indicator */}
      {isPlaying && (
        <motion.div
          className="absolute inset-0 rounded-full border-2 border-[var(--color-primary)]"
          initial={{ scale: 1, opacity: 1 }}
          animate={{ scale: 1.3, opacity: 0 }}
          transition={{ duration: 1, repeat: Infinity }}
        />
      )}
    </motion.button>
  );
}
