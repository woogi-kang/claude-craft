"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";

interface SectionRowProps {
  title: string;
  subtitle?: string;
  description?: string;
  children: React.ReactNode;
}

function SectionRow({ title, subtitle, description, children }: SectionRowProps) {
  return (
    <div className="flex gap-[40px] items-start justify-center w-full">
      {/* Left Label */}
      <div className="flex flex-col items-start w-[280px] shrink-0 self-stretch">
        <div className="flex flex-col gap-[20px] items-start w-[280px]">
          <div className="flex h-[164.816px] items-center justify-center w-full">
            <div className="w-full">
              <div className="flex flex-col items-start justify-center w-full">
                <div className="flex flex-col gap-[8px] items-start w-full">
                  {subtitle && (
                    <span className="font-semibold text-[16px] leading-[22px] text-[#017AFF] w-full">
                      {subtitle}
                    </span>
                  )}
                  <h2 className="font-bold text-[22px] leading-[34px] text-[#111111] w-full">
                    {title}
                  </h2>
                  {description && (
                    <p className="font-normal text-[15px] leading-[23px] text-[#505050] w-full">
                      {description}
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Right Content */}
      <div className="flex flex-col flex-1 min-w-0 min-h-px items-start">
        {children}
      </div>
    </div>
  );
}

function InfoBox({ children, opacity = false }: { children: React.ReactNode; opacity?: boolean }) {
  return (
    <div className="flex flex-col items-center justify-center p-[14px] bg-[#F5F7FA] rounded-[10px] w-full overflow-hidden">
      <div className={`font-normal text-[15px] leading-[22px] text-[#111111] text-center w-full ${opacity ? 'opacity-80' : ''}`}>
        {children}
      </div>
    </div>
  );
}

function GrayButton({ label }: { label: string }) {
  return (
    <button className="flex items-center justify-center h-[50px] px-[20px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] w-full hover:bg-[#EBEEF3] transition-colors overflow-hidden">
      <span className="font-semibold text-[16px] leading-[22px] text-[#999999]">
        {label}
      </span>
    </button>
  );
}

function PrimaryButton({ label }: { label: string }) {
  return (
    <button className="flex items-center justify-center h-[50px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors overflow-hidden">
      <span className="font-semibold text-[16px] leading-[22px] text-white">
        {label}
      </span>
    </button>
  );
}

function HealthProfileFamilyViewContent() {
  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col gap-[36px] items-center py-[40px] w-[780px]">
        {/* Page Header */}
        <div className="flex gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6] h-[186px]">
          <div className="flex flex-col gap-[10px] items-start flex-1 min-w-0 min-h-px">
            <span className="font-semibold text-[22px] leading-[34px] text-[#017AFF] tracking-[-0.44px] w-full">
              나의 모든 건강, 의료 기록
            </span>
            <h1 className="font-bold text-[34px] leading-[46px] text-[#111111] tracking-[-0.68px] w-full">
              건강 프로필
            </h1>
            <p className="font-normal text-[16px] leading-[23px] text-[#505050] tracking-[-0.32px] w-full">
              심사평가원, 건강보험공단에서 내 의료기록을 자동으로 가져와서 저장하면,
              <br />
              나에게 딱 맞는 설명을 해드릴 수 있습니다. (연동하지 않으셔도 서비스 이용이 가능합니다.)
            </p>
          </div>
        </div>

        {/* Content Sections */}
        <div className="flex flex-col gap-[28px] items-start w-full">
          {/* Section 1: Family Member Health Profile */}
          <SectionRow
            title="홍버들님 건강 프로필"
            subtitle="아버지"
            description={`나와 가족의 건강, 이제 '건강프로필'로\nAI가 평생 관리해드립니다!`}
          >
            <div className="flex flex-col gap-[14px] items-start w-full">
              <div className="flex flex-col gap-[14px] items-start w-full">
                <InfoBox>
                  더 나은 AI답변, 식단추천 등에 활용하고, 응급상황시 필요한 정보를 빠르게 전달할 수 있도록 흩어져있던 건강기록을 정리했어요.
                </InfoBox>
                <div className="flex flex-col gap-[10px] items-start w-full">
                  <GrayButton label="가족별 건강 프로필 확인" />
                </div>
              </div>
            </div>
          </SectionRow>

          {/* Section 2: Additional Records */}
          <SectionRow title="추가 기록">
            <div className="flex flex-col gap-[14px] items-start w-full">
              <div className="flex flex-col gap-[14px] items-start w-full">
                <InfoBox opacity>
                  <p className="mb-0">자동 연동된 병원 진료기록 외에 그럼AI가</p>
                  <p className="mb-0">참고해야할 질병, 증상이 있으시면 기입해주세요.</p>
                </InfoBox>
                <div className="flex flex-col gap-[10px] items-start w-full">
                  <PrimaryButton label="추가 병력 직접 입력" />
                </div>
              </div>
            </div>
          </SectionRow>
        </div>
      </div>
    </div>
  );
}

export default function HealthProfileFamilyViewPage() {
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
          {/* Health Profile Family View Content Area - Flexible */}
          <HealthProfileFamilyViewContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
