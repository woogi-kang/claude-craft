"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
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
      <p className="font-normal text-[15px] leading-[22px] text-[#111111] text-center w-full opacity-80">
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
      className="flex items-center justify-center h-[50px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors overflow-hidden"
    >
      <span className="font-semibold text-[16px] leading-[22px] text-white">
        {label}
      </span>
    </button>
  );
}

function SecondaryButton({
  label,
  onClick,
}: {
  label: string;
  onClick?: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="flex items-center justify-center h-[50px] px-[20px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] w-full hover:bg-[#EBEEF3] transition-colors overflow-hidden"
    >
      <span className="font-semibold text-[16px] leading-[22px] text-[#999999]">
        {label}
      </span>
    </button>
  );
}

interface FoodInputSectionProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

function FoodInputSection({ value, onChange, onSubmit }: FoodInputSectionProps) {
  return (
    <div className="flex flex-col gap-[10px] items-center justify-center w-full">
      <div className="flex flex-col font-semibold justify-center text-[16px] leading-[22px] text-[#111111] w-full">
        <span>음식 추가입력</span>
      </div>
      <div className="flex gap-[10px] h-[52px] items-center w-full">
        <div className="flex flex-1 h-full items-center px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] overflow-hidden">
          <input
            type="text"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder="음식 이름을 입력해주세요."
            className="flex-1 font-normal text-[15px] leading-[23px] text-[#111111] placeholder:text-[#999999] bg-transparent outline-none"
          />
        </div>
        <button
          onClick={onSubmit}
          className="flex items-center justify-center h-full w-[100px] px-[14px] bg-[#017AFF] rounded-[10px] hover:bg-[#0066DD] transition-colors overflow-hidden"
        >
          <span className="font-semibold text-[15px] leading-[23px] text-white">
            입력
          </span>
        </button>
      </div>
    </div>
  );
}

function FoodCompatibilityContent() {
  const [foodInput, setFoodInput] = useState("");

  const handleFoodInputSubmit = () => {
    if (foodInput.trim()) {
      console.log("Food submitted:", foodInput);
      setFoodInput("");
    }
  };

  const handlePhotoUpload = () => {
    console.log("Photo upload clicked");
  };

  const handleManualInput = () => {
    console.log("Manual input clicked");
  };

  const handleNextStep = () => {
    console.log("Next step clicked");
  };

  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col gap-[36px] items-center py-[40px] w-[780px]">
        {/* Page Header */}
        <div className="flex gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6] h-[209px]">
          <div className="flex flex-col gap-[10px] items-start w-[692px]">
            <span className="font-semibold text-[22px] leading-[34px] text-[#017AFF] tracking-[-0.44px] w-full">
              그럼 식단 관리
            </span>
            <h1 className="font-bold text-[34px] leading-[46px] text-[#111111] tracking-[-0.68px] w-full">
              주의해야 할 음식
            </h1>
            <div className="font-normal text-[16px] leading-[23px] text-[#505050] tracking-[-0.32px] w-full">
              <p className="mb-0">내 건강상태에 맞춰서 주의해야 하는 음식을 알려드려요.</p>
              <p className="mb-0">
                식약처에 등록된 음식 성분표, 영양 정보와 내 건강기록을 함께 고려하여
              </p>
              <p>음식 궁합을 매우 주의, 주의, 보통, 안심 4단계로 구분해드릴게요.</p>
            </div>
          </div>
        </div>

        {/* Content Sections */}
        <div className="flex flex-col items-start w-full">
          {/* Section: Food Compatibility Search */}
          <SectionRow title="음식 궁합 찾아보기">
            {/* Upload Section */}
            <div className="flex flex-col gap-[14px] items-start w-full">
              <div className="flex flex-col gap-[14px] items-start w-full">
                <InfoBox>
                  한 장에 여러 개가 있어도 되고, 한 번에 여러 장 올려도 괜찮아요.
                </InfoBox>
                <div className="flex flex-col gap-[10px] items-start w-full">
                  <PrimaryButton label="사진 업로드" onClick={handlePhotoUpload} />
                  <SecondaryButton
                    label="음식 직접 입력하기"
                    onClick={handleManualInput}
                  />
                </div>
              </div>
            </div>

            {/* Food Input Section */}
            <div className="flex flex-col gap-[14px] items-start w-full">
              <FoodInputSection
                value={foodInput}
                onChange={setFoodInput}
                onSubmit={handleFoodInputSubmit}
              />
              <div className="flex flex-col gap-[14px] items-start w-full">
                <div className="flex flex-col gap-[14px] items-start w-full">
                  <InfoBox>
                    <span className="block mb-0">사진 속 음식이 잘못되었다면,</span>
                    <span className="block">
                      음식 옆 X표를 누르고 정확한 음식명을 입력해주세요.
                    </span>
                  </InfoBox>
                  <div className="flex flex-col gap-[10px] items-start w-full">
                    <PrimaryButton label="다음 단계" onClick={handleNextStep} />
                  </div>
                </div>
              </div>
            </div>
          </SectionRow>
        </div>
      </div>
    </div>
  );
}

export default function FoodCompatibilityPage() {
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
          {/* Food Compatibility Content Area - Flexible */}
          <FoodCompatibilityContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
