'use client';

import { useState, useRef, useEffect, useCallback } from 'react';

interface AudioPlayerResult {
  isPlaying: boolean;
  toggle: () => void;
  play: () => void;
  pause: () => void;
}

export function useAudioPlayer(src: string, autoPlay: boolean = false): AudioPlayerResult {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    audioRef.current = new Audio(src);
    audioRef.current.loop = true;
    audioRef.current.volume = 0.5;

    const audio = audioRef.current;

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => setIsPlaying(false);

    audio.addEventListener('play', handlePlay);
    audio.addEventListener('pause', handlePause);

    // Auto play on first user interaction
    if (autoPlay) {
      const handleUserInteraction = () => {
        audio.play().catch(() => {
          // Autoplay blocked, user needs to click
        });
        document.removeEventListener('click', handleUserInteraction);
        document.removeEventListener('touchstart', handleUserInteraction);
      };

      document.addEventListener('click', handleUserInteraction);
      document.addEventListener('touchstart', handleUserInteraction);
    }

    return () => {
      audio.removeEventListener('play', handlePlay);
      audio.removeEventListener('pause', handlePause);
      audio.pause();
      audioRef.current = null;
    };
  }, [src, autoPlay]);

  const play = useCallback(() => {
    audioRef.current?.play().catch(() => {
      // Handle autoplay restriction
    });
  }, []);

  const pause = useCallback(() => {
    audioRef.current?.pause();
  }, []);

  const toggle = useCallback(() => {
    if (isPlaying) {
      pause();
    } else {
      play();
    }
  }, [isPlaying, play, pause]);

  return { isPlaying, toggle, play, pause };
}
