"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import {
  IconCloseCircle,
  IconArrowRightGray,
  IconPlusGray,
  IconArrowDownBlue,
} from "@/components/icons/icons";

interface HealthCheckupItemProps {
  date: string;
  hospital: string;
  onDelete?: () => void;
  onClick?: () => void;
}

function HealthCheckupItem({ date, hospital, onDelete, onClick }: HealthCheckupItemProps) {
  return (
    <div className="flex gap-[10px] h-[50px] items-center w-full border-b border-[#E5E5EC]">
      <button
        onClick={onDelete}
        className="shrink-0 hover:opacity-80 transition-opacity"
        aria-label="Delete record"
      >
        <IconCloseCircle size={20} />
      </button>
      <div className="font-normal text-[16px] leading-[26px] text-[#505050] w-[80px] shrink-0">
        {date}
      </div>
      <div className="flex-1 font-normal text-[16px] leading-[26px] text-[#111111] min-w-0">
        {hospital}
      </div>
      <button
        onClick={onClick}
        className="shrink-0 hover:opacity-80 transition-opacity"
        aria-label="View details"
      >
        <IconArrowRightGray size={20} />
      </button>
    </div>
  );
}

function HealthCheckupResultsContent() {
  const healthCheckups = [
    { date: "25/01/23", hospital: "서울본내과의원" },
    { date: "25/01/23", hospital: "서울본내과의원" },
    { date: "25/01/23", hospital: "서울본내과의원" },
  ];

  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto bg-[#FDFDFD]">
      <div className="flex flex-col gap-[36px] items-center py-[40px] w-[780px]">
        {/* Page Header */}
        <div className="flex gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6] h-[209px]">
          <div className="flex flex-col gap-[10px] items-start flex-1">
            <span className="font-semibold text-[22px] leading-[34px] text-[#017AFF] tracking-[-0.44px] w-full">
              나의 모든 건강, 의료 기록
            </span>
            <h1 className="font-bold text-[34px] leading-[46px] text-[#111111] tracking-[-0.68px] w-full">
              건강 프로필
            </h1>
            <div className="font-normal text-[16px] leading-[23px] text-[#505050] tracking-[-0.32px] w-full">
              <p className="mb-0">국가 건강검진결과만 불러올 수 있어요.</p>
              <p className="mb-0">국가 건강검진과 별도로 진행한 종합건강검진이 있거나, 건강검진 외의 검사결과지가 있다면</p>
              <p>사진을 찍어주시면 기록을 등록할 수 있어요.</p>
            </div>
          </div>
        </div>

        {/* Content Section */}
        <div className="flex flex-col items-start w-full">
          <div className="flex flex-col items-start w-full">
            <div className="flex gap-[40px] items-start justify-center w-full">
              {/* Left Label */}
              <div className="flex flex-col items-start w-[280px] shrink-0 self-stretch">
                <div className="flex flex-col gap-[20px] items-start w-[280px]">
                  <div className="flex h-[164.816px] items-center justify-center w-full">
                    <div className="w-full">
                      <div className="flex flex-col items-start justify-center w-full">
                        <div className="flex flex-col gap-[8px] items-start w-full">
                          <span className="font-semibold text-[16px] leading-[22px] text-[#017AFF] w-full">
                            건강 프로필
                          </span>
                          <h2 className="font-bold text-[22px] leading-[34px] text-[#111111] w-full">
                            건강 검진 결과
                          </h2>
                          <div className="font-normal text-[15px] leading-[23px] text-[#505050] w-full">
                            <p className="mb-0">국가 건강검진결과만 불러올 수 있어요.</p>
                            <p className="mb-0">국가 건강검진과 별도로 진행한 종합건강검진이 있거나, 건강검진 외의 검사결과지가 있다면</p>
                            <p>사진을 찍어주시면 기록을 등록할 수 있어요.</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Content */}
              <div className="flex flex-col flex-1 gap-[24px] items-start min-w-0 min-h-px">
                {/* Update Button */}
                <div className="flex flex-col gap-[10px] items-center justify-center w-full">
                  <button className="flex items-center justify-center h-[52px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors overflow-hidden">
                    <span className="font-semibold text-[16px] leading-[22px] text-white">
                      건강 검진 기록 최신화하기
                    </span>
                  </button>
                </div>

                {/* Search Filters */}
                <div className="flex flex-col gap-[10px] items-start justify-center w-full">
                  <div className="flex gap-[10px] h-[52px] items-center w-full">
                    {/* Period Dropdown */}
                    <div className="flex items-center h-full px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] w-[120px] shrink-0 overflow-hidden">
                      <div className="flex flex-1 gap-[10px] items-center">
                        <span className="flex-1 font-normal text-[15px] leading-[23px] text-[#999999]">
                          기간
                        </span>
                        <IconArrowDownBlue size={20} />
                      </div>
                    </div>

                    {/* Hospital Name Input */}
                    <div className="flex flex-1 items-center h-full px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] overflow-hidden min-w-0">
                      <input
                        type="text"
                        placeholder="병원명"
                        className="flex-1 font-normal text-[15px] leading-[23px] text-[#111111] placeholder:text-[#999999] bg-transparent outline-none"
                      />
                    </div>

                    {/* Search Button */}
                    <button className="flex items-center justify-center h-full px-[14px] bg-[#017AFF] rounded-[10px] w-[80px] shrink-0 hover:bg-[#0066DD] transition-colors overflow-hidden">
                      <span className="font-semibold text-[14px] leading-[20px] text-white">
                        검색
                      </span>
                    </button>
                  </div>
                </div>

                {/* Health Checkup Records List */}
                <div className="flex flex-col items-start w-full">
                  <div className="flex flex-col gap-[20px] items-start w-full">
                    {/* Section Header */}
                    <div className="flex flex-col gap-[10px] items-start w-full">
                      <h3 className="font-semibold text-[16px] leading-[22px] text-[#111111] w-full">
                        내 건강검진 정보
                      </h3>
                    </div>

                    {/* Records List */}
                    <div className="flex flex-col gap-[20px] items-start w-full">
                      <div className="flex flex-col items-start px-[20px] py-[4px] border border-[#E5E5EC] rounded-[10px] w-full">
                        {/* Health Checkup Items */}
                        {healthCheckups.map((record, index) => (
                          <HealthCheckupItem
                            key={index}
                            date={record.date}
                            hospital={record.hospital}
                          />
                        ))}

                        {/* View More Button */}
                        <button className="flex gap-[10px] h-[48px] items-center justify-center w-full hover:opacity-80 transition-opacity">
                          <IconPlusGray size={16} />
                          <span className="font-normal text-[15px] leading-[23px] text-[#111111] text-center">
                            진료 내역 더 보기
                          </span>
                        </button>
                      </div>

                      {/* Delete All Link */}
                      <button className="font-normal text-[15px] leading-[23px] text-[#999999] underline text-center w-full hover:text-[#777777] transition-colors">
                        건강 검진 결과 전체 삭제
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function HealthCheckupResultsPage() {
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
          {/* Health Checkup Results Content Area - Flexible */}
          <HealthCheckupResultsContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
