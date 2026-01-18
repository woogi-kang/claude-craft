'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Play } from 'lucide-react';
import { Section, SectionTitle } from '@/components/common/Section';
import { WEDDING_INFO } from '@/lib/constants';

export function Video() {
  const { video } = WEDDING_INFO;
  const [isPlaying, setIsPlaying] = useState(false);

  if (!video.enabled) return null;

  return (
    <Section id="video" background="secondary">
      <SectionTitle title={video.title} subtitle="VIDEO" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="relative overflow-hidden rounded-xl"
      >
        {!isPlaying ? (
          // Thumbnail
          <div
            className="relative aspect-video cursor-pointer"
            onClick={() => setIsPlaying(true)}
          >
            <img
              src={`https://img.youtube.com/vi/${video.youtubeId}/maxresdefault.jpg`}
              alt={video.title}
              className="h-full w-full object-cover"
            />
            <div className="absolute inset-0 flex items-center justify-center bg-black/30">
              <motion.div
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="flex h-16 w-16 items-center justify-center rounded-full bg-white/90 shadow-lg"
              >
                <Play className="h-8 w-8 text-[var(--color-primary)] ml-1" fill="currentColor" />
              </motion.div>
            </div>
          </div>
        ) : (
          // YouTube Player
          <div className="aspect-video">
            <iframe
              src={`https://www.youtube.com/embed/${video.youtubeId}?autoplay=1&rel=0`}
              title={video.title}
              className="h-full w-full"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        )}
      </motion.div>
    </Section>
  );
}
