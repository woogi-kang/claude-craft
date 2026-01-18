'use client';

import { Heart } from 'lucide-react';
import { WEDDING_INFO } from '@/lib/constants';

export function Footer() {
  const { groom, bride } = WEDDING_INFO;

  return (
    <footer className="bg-[var(--color-secondary)] py-12 text-center">
      <div className="mb-4 flex items-center justify-center gap-2">
        <span className="font-serif text-lg">{groom.name}</span>
        <Heart className="h-4 w-4 text-rose-400" fill="currentColor" />
        <span className="font-serif text-lg">{bride.name}</span>
      </div>

      <p className="text-xs text-[var(--color-text-light)]">
        Thank you for celebrating with us
      </p>

      <div className="mt-8 text-xs text-[var(--color-text-light)]">
        <p>Made with love</p>
        <p className="mt-1">© {new Date().getFullYear()} Wedding Invitation</p>
      </div>
    </footer>
  );
}
