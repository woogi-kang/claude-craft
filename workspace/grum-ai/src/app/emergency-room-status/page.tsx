"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import {
  IconShareGray,
  IconDownloadGray,
  IconArrowDownGray,
} from "@/components/icons/icons";

interface IconButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
}

function IconButton({ children, onClick }: IconButtonProps) {
  return (
    <button
      onClick={onClick}
      className="flex items-center justify-center w-[35px] h-[35px] bg-[#F5F7FA] rounded-full hover:bg-[#E5E5EC] transition-colors"
    >
      {children}
    </button>
  );
}

interface SearchInputProps {
  label: string;
  placeholder: string;
  type?: "dropdown" | "text";
}

function SearchInput({ label, placeholder, type = "text" }: SearchInputProps) {
  return (
    <div className="flex flex-col gap-[10px] items-center justify-center w-full">
      <div className="flex flex-col justify-center w-full">
        <p className="font-semibold text-[16px] leading-[22px] text-[#111111]">
          {label}
        </p>
      </div>
      <div className="flex gap-[10px] h-[52px] items-center w-full">
        <div className="flex flex-1 h-full items-center px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] overflow-hidden">
          <div className="flex flex-1 gap-[10px] items-center">
            <p className="flex-1 font-normal text-[15px] leading-[23px] text-[#999999]">
              {placeholder}
            </p>
            {type === "dropdown" && <IconArrowDownGray size={20} />}
          </div>
        </div>
        <button className="flex items-center justify-center h-full w-[100px] px-[14px] bg-[#017AFF] rounded-[10px] hover:bg-[#0066DD] transition-colors">
          <span className="font-semibold text-[15px] leading-[23px] text-white">
            검색
          </span>
        </button>
      </div>
    </div>
  );
}

function NearbySearchButton() {
  return (
    <div className="flex flex-col gap-[10px] items-center justify-center w-full">
      <div className="flex gap-[10px] items-start w-full">
        <p className="font-semibold text-[16px] leading-[22px] text-[#111111]">
          가까운 병원 검색
        </p>
      </div>
      <button className="flex items-center justify-center h-[52px] px-[20px] w-full bg-[#017AFF] rounded-[10px] hover:bg-[#0066DD] transition-colors">
        <span className="font-semibold text-[16px] leading-[22px] text-white">
          내 주변 검색
        </span>
      </button>
    </div>
  );
}

function EmergencyRoomStatusContent() {
  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col items-center py-[40px] w-[780px]">
        <div className="flex flex-col gap-[50px] items-start w-full overflow-hidden">
          {/* Page Header */}
          <div className="flex gap-[10px] items-start pb-[40px] w-full h-[186px] border-b border-[#F0F0F6]">
            <div className="flex flex-col gap-[10px] items-start w-[692px] shrink-0">
              <p className="font-semibold text-[22px] leading-[34px] text-[#017AFF] tracking-[-0.44px]">
                통합 응급정보 인트라넷
              </p>
              <h1 className="font-bold text-[34px] leading-[46px] text-[#111111] tracking-[-0.68px]">
                응급실 실시간 현황
              </h1>
              <p className="font-normal text-[16px] leading-[23px] text-[#505050] tracking-[-0.32px]">
                중증 응급질환인 경우, 실시간 병상 수와 관련없이
                <br />
                즉시 119에 전화하시길 바랍니다.
              </p>
            </div>
            <div className="flex gap-[8px] items-center justify-end shrink-0">
              <IconButton>
                <IconShareGray size={20} />
              </IconButton>
              <IconButton>
                <IconDownloadGray size={20} />
              </IconButton>
            </div>
          </div>

          {/* Search Section */}
          <div className="flex gap-[36px] items-start justify-center w-full">
            {/* Left Body - Title */}
            <div className="flex flex-col items-start w-[280px] shrink-0">
              <h2 className="font-bold text-[24px] leading-[34px] text-[#111111]">
                응급실 검색
              </h2>
            </div>

            {/* Right Body - Search Inputs */}
            <div className="flex flex-1 flex-col gap-[28px] items-start min-w-0">
              <SearchInput
                label="지역별로 검색"
                placeholder="시/도 선택"
                type="dropdown"
              />
              <SearchInput
                label="병원명으로 검색"
                placeholder="병원명을 검색하세요."
                type="text"
              />
              <NearbySearchButton />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function EmergencyRoomStatusPage() {
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
          {/* Emergency Room Status Content Area - Flexible */}
          <EmergencyRoomStatusContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
