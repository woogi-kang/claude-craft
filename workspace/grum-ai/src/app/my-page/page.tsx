"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import {
  IconExclamationCircle,
  IconArrowRightBlue,
} from "@/components/icons/icons";

interface SettingsItemProps {
  label: string;
  onClick?: () => void;
}

function SettingsItem({ label, onClick }: SettingsItemProps) {
  return (
    <button
      onClick={onClick}
      className="flex items-center justify-between w-full group"
    >
      <span className="font-semibold text-[16px] leading-[22px] text-[#111111]">
        {label}
      </span>
      <IconArrowRightBlue size={20} />
    </button>
  );
}

interface SectionRowProps {
  title: string;
  children: React.ReactNode;
}

function SectionRow({ title, children }: SectionRowProps) {
  return (
    <div className="flex gap-[36px] items-start justify-center w-full">
      {/* Left Label */}
      <div className="flex flex-col items-start w-[280px] shrink-0">
        <h2 className="font-bold text-[22px] leading-[34px] text-[#111111] tracking-[-0.68px]">
          {title}
        </h2>
      </div>
      {/* Right Content */}
      <div className="flex flex-col flex-1 min-w-0">{children}</div>
    </div>
  );
}

function StatusBadge({ label }: { label: string }) {
  return (
    <div className="flex items-center justify-center gap-[10px] h-[40px] px-[20px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[25px] w-full">
      <IconExclamationCircle size={20} />
      <span className="font-semibold text-[15px] leading-[23px] text-[#111111]">
        {label}
      </span>
      <div className="flex-1" />
    </div>
  );
}

function PrimaryButton({ label }: { label: string }) {
  return (
    <button className="flex items-center justify-center h-[52px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors">
      <span className="font-semibold text-[16px] leading-[22px] text-white">
        {label}
      </span>
    </button>
  );
}

function MyPageContent() {
  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col gap-[36px] items-center py-[40px] w-[780px]">
        {/* Page Header */}
        <div className="flex flex-col gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6]">
          <span className="font-semibold text-[22px] leading-[34px] text-[#017AFF] tracking-[-0.44px]">
            그럼AI
          </span>
          <h1 className="font-bold text-[34px] leading-[46px] text-[#111111] tracking-[-0.68px]">
            마이페이지
          </h1>
        </div>

        {/* Content Sections */}
        <div className="flex flex-col gap-[28px] items-start w-full">
          {/* Health Profile Section */}
          <SectionRow title="건강 프로필">
            <div className="flex flex-col gap-[10px] w-full">
              <StatusBadge label="미이용" />
              <PrimaryButton label="건강프로필 확인" />
            </div>
          </SectionRow>

          {/* Subscription Plan Section */}
          <SectionRow title="구독 플랜">
            <div className="flex flex-col gap-[10px] w-full">
              <StatusBadge label="미이용" />
              <PrimaryButton label="플랜 변경 및 확인" />
            </div>
          </SectionRow>

          {/* Personal Info & Settings Section */}
          <SectionRow title="개인정보 및 기타 설정">
            <div className="flex flex-col gap-[24px] w-full">
              <SettingsItem label="알림 설정" />
              <SettingsItem label="연락처 변경" />
              <SettingsItem label="비밀번호 변경" />
              <SettingsItem label="이용약관 확인" />
              <SettingsItem label="선택 약관 동의 변경" />
              <SettingsItem label="회원 탈퇴" />
            </div>
          </SectionRow>
        </div>
      </div>
    </div>
  );
}

export default function MyPage() {
  return (
    <div className="flex items-start h-screen w-full">
      {/* Left Sidebar - 300px fixed width */}
      <LeftSidebar />

      {/* Main Body - Flexible */}
      <div className="flex flex-1 flex-col h-full items-start min-h-px min-w-px overflow-hidden">
        {/* Status Bar - 80px height */}
        <StatusBar />

        {/* Main Content Area */}
        <div className="flex flex-1 items-start justify-between min-h-px min-w-px overflow-hidden w-full bg-[#FDFDFD]">
          {/* My Page Content Area - Flexible */}
          <MyPageContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
