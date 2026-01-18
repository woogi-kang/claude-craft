'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Copy, Check } from 'lucide-react';
import { toast } from 'sonner';
import { Section, SectionTitle } from '@/components/common/Section';
import { WEDDING_INFO } from '@/lib/constants';
import { copyToClipboard } from '@/lib/utils';
import type { AccountInfo } from '@/types';

interface AccountCardProps {
  title: string;
  accounts: AccountInfo[];
  isOpen: boolean;
  onToggle: () => void;
}

function AccountCard({ title, accounts, isOpen, onToggle }: AccountCardProps) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleCopy = async (account: AccountInfo, index: number) => {
    const success = await copyToClipboard(account.number);
    if (success) {
      setCopiedIndex(index);
      toast.success('계좌번호가 복사되었습니다');
      setTimeout(() => setCopiedIndex(null), 2000);
    } else {
      toast.error('복사에 실패했습니다');
    }
  };

  return (
    <div className="overflow-hidden rounded-xl bg-white">
      {/* Header */}
      <button
        onClick={onToggle}
        className="flex w-full items-center justify-between p-4 text-left transition-colors hover:bg-[var(--color-secondary)]"
      >
        <span className="font-medium text-[var(--color-text)]">{title}</span>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <ChevronDown className="h-5 w-5 text-[var(--color-text-light)]" />
        </motion.div>
      </button>

      {/* Content */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <div className="space-y-3 border-t border-[var(--color-border)] p-4">
              {accounts.map((account, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between rounded-lg bg-[var(--color-secondary)] p-3"
                >
                  <div>
                    <p className="text-xs text-[var(--color-text-light)]">
                      {account.bank}
                    </p>
                    <p className="font-medium">{account.number}</p>
                    <p className="text-xs text-[var(--color-text-light)]">
                      {account.holder}
                    </p>
                  </div>
                  <button
                    onClick={() => handleCopy(account, index)}
                    className="flex h-10 w-10 items-center justify-center rounded-full bg-[var(--color-primary)] text-white transition-transform hover:scale-105"
                    aria-label="계좌번호 복사"
                  >
                    {copiedIndex === index ? (
                      <Check className="h-4 w-4" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </button>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export function Account() {
  const { groom, bride } = WEDDING_INFO;
  const [openSection, setOpenSection] = useState<'groom' | 'bride' | null>(null);

  const groomAccounts: AccountInfo[] = [
    groom.account,
    groom.fatherAccount,
    groom.motherAccount,
  ];

  const brideAccounts: AccountInfo[] = [
    bride.account,
    bride.fatherAccount,
    bride.motherAccount,
  ];

  return (
    <Section id="account" background="white">
      <SectionTitle title="마음 전하실 곳" subtitle="ACCOUNT" />

      <motion.p
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="mb-8 text-center text-sm text-[var(--color-text-light)]"
      >
        축하의 마음을 담아 축의금을 전달해 보세요
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="space-y-4"
      >
        {/* Groom Side */}
        <AccountCard
          title={`신랑측 계좌번호`}
          accounts={groomAccounts}
          isOpen={openSection === 'groom'}
          onToggle={() => setOpenSection(openSection === 'groom' ? null : 'groom')}
        />

        {/* Bride Side */}
        <AccountCard
          title={`신부측 계좌번호`}
          accounts={brideAccounts}
          isOpen={openSection === 'bride'}
          onToggle={() => setOpenSection(openSection === 'bride' ? null : 'bride')}
        />
      </motion.div>
    </Section>
  );
}
