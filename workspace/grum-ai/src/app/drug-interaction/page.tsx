"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import { IconCheckCircleGray } from "@/components/icons/icons";
import Image from "next/image";
import { useState } from "react";

interface SectionRowProps {
  title: string;
  children: React.ReactNode;
}

function SectionRow({ title, children }: SectionRowProps) {
  return (
    <div className="flex gap-[40px] items-start justify-center w-full">
      {/* Left Label */}
      <div className="flex flex-col items-start w-[280px] shrink-0 self-stretch">
        <div className="flex flex-col gap-[20px] items-start w-[280px]">
          <div className="flex h-[164.816px] items-center justify-center w-full">
            <div className="w-full">
              <div className="flex flex-col items-start justify-center w-full">
                <div className="flex flex-col gap-[8px] items-start w-full">
                  <h2 className="font-bold text-[22px] leading-[34px] text-[#111111] w-full">
                    {title}
                  </h2>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Right Content */}
      <div className="flex flex-col flex-1 min-w-0 min-h-px gap-[28px] items-start">
        {children}
      </div>
    </div>
  );
}

function InfoBox({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center p-[14px] bg-[#F5F7FA] rounded-[10px] w-full overflow-hidden">
      <p className="font-normal text-[15px] leading-[23px] text-[#111111] text-center w-full">
        {children}
      </p>
    </div>
  );
}

function PrimaryButton({
  label,
  onClick,
}: {
  label: string;
  onClick?: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="flex items-center justify-center h-[52px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors overflow-hidden"
    >
      <span className="font-semibold text-[16px] leading-[22px] text-white">
        {label}
      </span>
    </button>
  );
}

interface ServiceAgreementProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
}

function ServiceAgreement({ checked, onChange }: ServiceAgreementProps) {
  return (
    <div className="flex items-center w-full">
      <div className="flex flex-1 gap-[10px] items-center">
        <button
          onClick={() => onChange(!checked)}
          className="flex items-center justify-center"
        >
          <IconCheckCircleGray size={20} checked={checked} />
        </button>
        <span className="flex-1 font-normal text-[15px] leading-[23px] text-[#111111]">
          서비스 이용 동의 (필수)
        </span>
      </div>
    </div>
  );
}

function DrugInteractionContent() {
  const [agreed, setAgreed] = useState(true);

  const handlePrescriptionSync = () => {
    if (agreed) {
      console.log("Prescription sync clicked");
    }
  };

  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col gap-[36px] items-center py-[40px] w-[780px]">
        {/* Page Header */}
        <div className="flex gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6] h-[163px]">
          <div className="flex flex-col gap-[10px] items-start w-[692px]">
            <span className="font-semibold text-[22px] leading-[34px] text-[#017AFF] tracking-[-0.44px] w-full">
              그럼 식단 관리
            </span>
            <h1 className="font-bold text-[34px] leading-[46px] text-[#111111] tracking-[-0.68px] w-full">
              약물과 상호작용
            </h1>
            <p className="font-normal text-[16px] leading-[23px] text-[#505050] tracking-[-0.32px] w-full">
              복용중인 약물과 함께 먹으면 안 되는 음식들을 알려드려요!
            </p>
          </div>
        </div>

        {/* Content Sections */}
        <div className="flex flex-col items-start w-full">
          <SectionRow title="복용 중인 약을 알려주세요.">
            {/* 3D Image and Info Section */}
            <div className="flex flex-col gap-[24px] items-center justify-center w-full overflow-hidden">
              {/* 3D Image */}
              <div className="flex items-center justify-center h-[120px] w-full overflow-hidden">
                <div className="relative w-[160px] h-[160px]">
                  <Image
                    src="/images/3d-pill-fruit.png"
                    alt="Pill and Fruit"
                    width={160}
                    height={160}
                    className="object-cover"
                  />
                </div>
              </div>

              {/* Info Box */}
              <InfoBox>
                처방 받은 약을 심사평가원에서 자동으로 불러오거나 직접 입력해주세요.
              </InfoBox>
            </div>

            {/* Agreement and Button Section */}
            <div className="flex flex-col items-start w-full">
              <div className="flex flex-col gap-[10px] items-center justify-center w-full">
                <ServiceAgreement checked={agreed} onChange={setAgreed} />
                <PrimaryButton
                  label="처방 약물 연동"
                  onClick={handlePrescriptionSync}
                />
              </div>
            </div>
          </SectionRow>
        </div>
      </div>
    </div>
  );
}

export default function DrugInteractionPage() {
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
          {/* Drug Interaction Content Area - Flexible */}
          <DrugInteractionContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
