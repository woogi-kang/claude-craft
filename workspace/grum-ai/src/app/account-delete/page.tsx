"use client";

import { useState } from "react";
import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import {
  IconArrowDownBlue,
  IconCheckCircleGray,
} from "@/components/icons/icons";

interface SelectInputProps {
  label: string;
  placeholder: string;
  onClick?: () => void;
}

function SelectInput({ label, placeholder, onClick }: SelectInputProps) {
  return (
    <div className="flex flex-col gap-[10px] w-full">
      <div className="flex flex-col justify-center w-full">
        <span className="font-semibold text-[16px] leading-[22px] text-[#111111]">
          {label}
        </span>
      </div>
      <button
        onClick={onClick}
        className="flex items-center gap-[10px] h-[52px] px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] w-full"
      >
        <span className="flex-1 text-left font-normal text-[15px] leading-[23px] text-[#999999]">
          {placeholder}
        </span>
        <IconArrowDownBlue size={20} />
      </button>
    </div>
  );
}

interface CheckboxProps {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}

function Checkbox({ label, checked, onChange }: CheckboxProps) {
  return (
    <button
      onClick={() => onChange(!checked)}
      className="flex items-center gap-[10px] w-full"
    >
      <IconCheckCircleGray size={20} checked={checked} />
      <span className="flex-1 text-left font-normal text-[15px] leading-[23px] text-[#111111]">
        {label}
      </span>
    </button>
  );
}

interface ButtonProps {
  label: string;
  variant: "primary" | "secondary";
  onClick?: () => void;
  disabled?: boolean;
}

function Button({ label, variant, onClick, disabled }: ButtonProps) {
  const baseStyles =
    "flex items-center justify-center flex-1 h-[52px] px-[24px] py-[14px] rounded-[12px] transition-colors";
  const variantStyles =
    variant === "primary"
      ? "bg-[#017AFF] hover:bg-[#0066DD] text-white"
      : "bg-[#F5F7FA] border border-[#E5E5EC] text-[#999999] hover:bg-[#EBEEF2]";

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyles} ${variantStyles}`}
    >
      <span className="font-semibold text-[16px] leading-[22px]">{label}</span>
    </button>
  );
}

function AccountDeleteContent() {
  const [isChecked, setIsChecked] = useState(false);

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

        {/* Main Content */}
        <div className="flex gap-[40px] items-start justify-center w-full">
          {/* Left Body */}
          <div className="flex flex-col items-start w-[280px] shrink-0">
            <div className="flex flex-col gap-[20px] items-start w-full">
              <div className="flex flex-col gap-[8px] items-start w-full">
                <span className="font-semibold text-[16px] leading-[22px] text-[#017AFF]">
                  탈퇴하기
                </span>
                <h2 className="font-bold text-[22px] leading-[34px] text-[#111111]">
                  계정 삭제
                </h2>
                <p className="font-normal text-[15px] leading-[23px] text-[#505050]">
                  계정 기록이 모두 삭제됩니다.
                </p>
              </div>
            </div>
          </div>

          {/* Right Body */}
          <div className="flex flex-col flex-1 gap-[28px] items-start min-w-0">
            {/* Important Notice Section */}
            <div className="flex flex-col gap-[14px] items-center justify-center w-full">
              <div className="flex flex-col items-start justify-center w-full">
                <span className="font-semibold text-[16px] leading-[22px] text-[#111111]">
                  중요 안내 사항
                </span>
              </div>
              <div className="flex flex-col gap-[14px] items-start w-full">
                <div className="flex flex-col gap-[8px] items-center justify-center p-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] w-full">
                  <ul className="list-disc pl-[22px] w-full">
                    <li className="font-normal text-[15px] leading-[23px] text-[#505050]">
                      현재 계정과 연동된 정보는 계정을 삭제한 후에는 복구할 수
                      없습니다.
                    </li>
                    <li className="font-normal text-[15px] leading-[23px] text-[#505050]">
                      자세한 내용은 개인정보 처리방침을 참고해주세요.
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Withdrawal Reason Select */}
            <SelectInput
              label="탈퇴 사유"
              placeholder="탈퇴 사유를 선택해주세요."
            />

            {/* Bottom Section */}
            <div className="flex flex-col gap-[10px] items-center justify-center w-full">
              {/* Checkbox */}
              <div className="flex items-center w-full">
                <Checkbox
                  label="네, 보든 중요 사항을 검토하였습니다."
                  checked={isChecked}
                  onChange={setIsChecked}
                />
              </div>

              {/* Buttons */}
              <div className="flex gap-[10px] items-center justify-center h-[52px] w-full">
                <Button label="취소" variant="secondary" />
                <Button label="탈퇴 신청" variant="primary" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function AccountDeletePage() {
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
          {/* Account Delete Content Area - Flexible */}
          <AccountDeleteContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
