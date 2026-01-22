'use client';

import { Section, SectionTitle } from '@/components/common/Section';
import { WEDDING_INFO } from '@/lib/constants';

export function Guestbook() {
  const { guestbook } = WEDDING_INFO;

  if (!guestbook.enabled) return null;

  // Giscus 스크립트를 로드하는 방식
  // 실제 사용 시 giscus.app에서 설정 후 repo, repoId, category, categoryId 값을 변경해야 함

  return (
    <Section id="guestbook" background="secondary">
      <SectionTitle title="방명록" subtitle="GUESTBOOK" />

      <div className="rounded-xl bg-white p-4">
        <p className="mb-4 text-center text-sm text-[var(--color-text-light)]">
          축하 메시지를 남겨주세요
        </p>

        {/* Giscus Comment Widget */}
        {/*
          실제 사용 시 아래 주석을 해제하고 giscus 설정을 완료해야 합니다.
          https://giscus.app 에서 설정 후 스크립트를 추가하세요.
        */}
        <div className="min-h-[200px] rounded-lg bg-[var(--color-secondary)] p-4">
          <p className="text-center text-sm text-[var(--color-text-light)]">
            방명록 기능을 사용하려면
            <br />
            <a
              href="https://giscus.app"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[var(--color-primary)] underline"
            >
              Giscus
            </a>
            {' '}설정을 완료해 주세요
          </p>
        </div>

        {/* 실제 Giscus 위젯 예시 */}
        {/*
        <script
          src="https://giscus.app/client.js"
          data-repo={guestbook.repo}
          data-repo-id={guestbook.repoId}
          data-category={guestbook.category}
          data-category-id={guestbook.categoryId}
          data-mapping="pathname"
          data-strict="0"
          data-reactions-enabled="1"
          data-emit-metadata="0"
          data-input-position="bottom"
          data-theme="light"
          data-lang="ko"
          crossOrigin="anonymous"
          async
        />
        */}
      </div>
    </Section>
  );
}
