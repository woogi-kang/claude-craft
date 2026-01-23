"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import {
  IconArrowRightBlue,
  IconArrowRightGray,
  IconToggle,
} from "@/components/icons/icons";

interface ToggleItemProps {
  label: string;
  active?: boolean;
  onToggle?: () => void;
}

function ToggleItem({ label, active = true, onToggle }: ToggleItemProps) {
  return (
    <div className="flex items-center w-full">
      <div className="flex flex-1 items-center gap-[4px]">
        <span className="font-normal text-[15px] leading-[23px] text-[#111111]">
          {label}
        </span>
      </div>
      <button onClick={onToggle} className="shrink-0">
        <IconToggle active={active} />
      </button>
    </div>
  );
}

interface SectionHeaderProps {
  title: string;
  showArrow?: boolean;
  arrowColor?: "blue" | "gray";
  onClick?: () => void;
}

function SectionHeader({
  title,
  showArrow = true,
  arrowColor = "gray",
  onClick,
}: SectionHeaderProps) {
  return (
    <button
      onClick={onClick}
      className="flex items-center justify-between w-full"
    >
      <span className="font-semibold text-[16px] leading-[22px] text-[#111111]">
        {title}
      </span>
      {showArrow && (
        <div className="flex items-center justify-center">
          {arrowColor === "blue" ? (
            <IconArrowRightBlue size={20} />
          ) : (
            <IconArrowRightGray size={20} />
          )}
        </div>
      )}
    </button>
  );
}

interface InputFieldProps {
  label: string;
  placeholder: string;
}

function InputField({ label, placeholder }: InputFieldProps) {
  return (
    <div className="flex flex-col gap-[10px] items-center justify-center w-full">
      <div className="flex flex-col items-start justify-center w-full">
        <span className="font-semibold text-[16px] leading-[22px] text-[#111111]">
          {label}
        </span>
      </div>
      <div className="flex items-center gap-[55px] h-[52px] px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] w-full overflow-hidden">
        <span className="flex-1 font-normal text-[15px] leading-[22px] text-[#999999]">
          {placeholder}
        </span>
      </div>
    </div>
  );
}

function InfoBox({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center p-[14px] bg-[#F5F7FA] rounded-[10px] w-full overflow-hidden">
      <div className="font-normal text-[15px] leading-[22px] text-[#111111] text-center w-full opacity-80">
        {children}
      </div>
    </div>
  );
}

function PrimaryButton({ label }: { label: string }) {
  return (
    <button className="flex items-center justify-center h-[50px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors">
      <span className="font-semibold text-[16px] leading-[22px] text-white">
        {label}
      </span>
    </button>
  );
}

function MyPageSettingsContent() {
  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col gap-[36px] items-center py-[40px] w-[780px]">
        {/* Page Header */}
        <div className="flex gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6] h-[130px]">
          <div className="flex flex-col gap-[10px] items-start w-[692px]">
            <span className="font-semibold text-[22px] leading-[34px] text-[#017AFF] tracking-[-0.44px]">
              그럼AI
            </span>
            <h1 className="font-bold text-[34px] leading-[46px] text-[#111111] tracking-[-0.68px]">
              마이페이지
            </h1>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex gap-[40px] items-start justify-center w-full">
          {/* Left Body - Section Label */}
          <div className="flex flex-col items-start w-[280px] shrink-0">
            <div className="flex flex-col gap-[20px] items-start w-[280px]">
              <div className="flex items-center justify-center w-full">
                <div className="flex flex-col items-start justify-center w-full">
                  <div className="flex flex-col gap-[8px] items-start w-full">
                    <h2 className="font-bold text-[22px] leading-[34px] text-[#111111]">
                      개인정보 및 기타 설정
                    </h2>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Content Area */}
          <div className="flex flex-col flex-1 gap-[28px] items-start min-w-0">
            {/* Notification Settings Section */}
            <div className="flex flex-col gap-[14px] items-start w-full">
              <SectionHeader title="알림설정" arrowColor="gray" />
              <ToggleItem label="AI 답변 알림" active={true} />
              <ToggleItem label="식단 관련 알림" active={true} />
              <div className="flex items-center gap-[10px] w-full">
                <div className="flex flex-1 items-center">
                  <span className="flex-1 font-normal text-[15px] leading-[23px] text-[#111111]">
                    기타 활동 알림
                  </span>
                </div>
                <IconToggle active={true} />
              </div>
            </div>

            {/* Contact Change Section */}
            <div className="flex flex-col gap-[16px] items-start w-full">
              <SectionHeader title="연락처 변경" arrowColor="gray" />
              <div className="flex flex-col gap-[14px] items-start w-full">
                <InfoBox>
                  <p className="mb-0">
                    네이버 계정으로 로그인하셨네요. 연락처 변경을 원하시는 경우에는
                  </p>
                  <p>네이버 계정의 연락처를 변경해주세요.</p>
                </InfoBox>
                <div className="flex flex-col gap-[10px] items-start w-full">
                  <PrimaryButton label="변경" />
                </div>
              </div>
            </div>

            {/* Password Change Section */}
            <div className="flex flex-col gap-[10px] items-start w-full">
              <SectionHeader title="비밀번호 변경" arrowColor="gray" />
              <div className="flex flex-col gap-[14px] items-start w-full">
                <InputField label="현재 비밀번호" placeholder="현재 비밀번호" />
                <div className="flex flex-col gap-[10px] items-center justify-center w-full">
                  <div className="flex flex-col items-start justify-center w-full">
                    <span className="font-semibold text-[16px] leading-[22px] text-[#111111]">
                      변경할 비밀번호
                    </span>
                  </div>
                  <div className="flex items-center gap-[55px] h-[52px] px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] w-full overflow-hidden">
                    <span className="flex-1 font-normal text-[15px] leading-[22px] text-[#999999]">
                      변경할 비밀번호
                    </span>
                  </div>
                  <div className="flex items-center gap-[55px] h-[52px] px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] w-full overflow-hidden">
                    <span className="flex-1 font-normal text-[15px] leading-[22px] text-[#999999]">
                      변경할 비밀번호 확인
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Terms Confirmation Section */}
            <div className="flex flex-col gap-[14px] items-center justify-center overflow-hidden w-full">
              <SectionHeader title="이용약관 확인" arrowColor="blue" />
            </div>

            {/* Optional Consent Change Section */}
            <div className="flex flex-col gap-[14px] items-center justify-center overflow-hidden w-full">
              <SectionHeader title="선택 약관 동의 변경" arrowColor="blue" />
              <ToggleItem label="마케팅 약관 활용 동의" active={true} />
              <ToggleItem label="맞춤형 광고 수집·이용 동의" active={true} />
            </div>

            {/* Account Deletion Section */}
            <div className="flex flex-col gap-[14px] items-center justify-center overflow-hidden w-full">
              <SectionHeader title="회원 탈퇴" arrowColor="blue" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function MyPageSettings() {
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
          {/* My Page Settings Content Area - Flexible */}
          <MyPageSettingsContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
