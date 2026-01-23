"use client";

import { useState } from "react";
import Image from "next/image";
import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import {
  IconPinLocation,
  IconArrowRightSmall,
  IconSearchMono,
} from "@/components/icons/icons";

interface FilterTabProps {
  label: string;
  value?: string;
  hasArrow?: boolean;
  isActive?: boolean;
}

function FilterTab({ label, value, hasArrow = true, isActive = false }: FilterTabProps) {
  return (
    <div className="flex items-center gap-[8px] px-[12px] py-[6px]">
      <span className={`font-normal text-[14px] leading-[20px] ${isActive ? 'text-[#111111]' : 'text-[#767676]'}`}>
        {label}
      </span>
      {value && (
        <div className="flex items-center gap-[4px]">
          <span className={`font-semibold text-[14px] leading-[20px] ${isActive ? 'text-[#017AFF]' : 'text-[#111111]'}`}>
            {value}
          </span>
          {hasArrow && <IconArrowRightSmall size={10} />}
        </div>
      )}
      {!value && hasArrow && <IconArrowRightSmall size={10} />}
    </div>
  );
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center w-[464px] bg-white rounded-[12px]">
      {/* Empty State Illustration */}
      <div className="flex flex-col items-center pt-[20px] pb-[14px]">
        <div className="relative w-[140px] h-[140px]">
          <Image
            src="/images/empty-states/emergency-room-search.png"
            alt="검색 결과 없음"
            fill
            className="object-contain"
          />
        </div>
      </div>

      {/* Empty State Text */}
      <p className="font-bold text-[18px] leading-[26px] text-[#111111] text-center">
        해당하는 응급실이 없어요.
      </p>

      {/* Info Box */}
      <div className="flex items-center justify-center w-[420px] mt-[14px] p-[12px] bg-[#F5F7FA] rounded-[10px]">
        <p className="font-normal text-[14px] leading-[22px] text-[#767676] text-center">
          &quot;내 주변&quot; 버튼을 눌러 근처 응급실을 찾거나<br />
          병원명, 지역을 다시 설정해주세요.
        </p>
      </div>
    </div>
  );
}

interface BedRowProps {
  label: string;
  available: number;
  total: number;
  isHighlighted?: boolean;
}

function BedRow({ label, available, total, isHighlighted = false }: BedRowProps) {
  return (
    <div className="flex items-center h-[26px]">
      <div className="w-[272px]">
        <span className="font-normal text-[14px] leading-[22px] text-[#505050]">
          {label}
        </span>
      </div>
      <div className="w-[60px] text-right">
        <span className={`font-semibold text-[14px] leading-[22px] ${isHighlighted ? 'text-[#017AFF]' : 'text-[#017AFF]'}`}>
          {available}
        </span>
      </div>
      <div className="w-[60px] text-right">
        <span className="font-normal text-[14px] leading-[22px] text-[#767676]">
          {total}
        </span>
      </div>
    </div>
  );
}

function HospitalCard() {
  return (
    <div className="flex flex-col w-[464px] bg-white rounded-[12px] overflow-hidden border border-[#E5E5EC]">
      {/* Hospital Image */}
      <div className="relative w-full h-[270px]">
        <Image
          src="/images/hospitals/severance-hospital.jpg"
          alt="연세대학교 의과대학 세브란스병원"
          fill
          className="object-cover"
        />
        {/* Distance Badge */}
        <div className="absolute left-[16px] bottom-[16px] flex items-center justify-center px-[10px] py-[4px] bg-[#017AFF] rounded-[6px]">
          <span className="font-semibold text-[14px] leading-[20px] text-white">
            2.1km
          </span>
        </div>
        {/* Time Badge */}
        <div className="absolute right-[16px] bottom-[16px] flex items-center gap-[4px]">
          <span className="font-normal text-[12px] leading-[18px] text-white/80">
            기준 시점
          </span>
          <span className="font-semibold text-[14px] leading-[20px] text-white">
            03:08
          </span>
        </div>
      </div>

      {/* Hospital Info */}
      <div className="flex flex-col p-[16px] gap-[20px]">
        {/* Hospital Name and Address */}
        <div className="flex flex-col gap-[4px]">
          <h3 className="font-bold text-[18px] leading-[28px] text-[#111111]">
            연세대학교 의과대학 세브란스병원
          </h3>
          <div className="flex items-center gap-[4px]">
            <IconPinLocation size={14} />
            <span className="font-normal text-[14px] leading-[22px] text-[#767676]">
              서울특별시 서대문구 연세로 50-1 (신촌동)
            </span>
          </div>
        </div>

        {/* Bed Availability Table */}
        <div className="flex flex-col gap-[4px]">
          {/* Table Header */}
          <div className="flex items-center h-[32px] border-b border-[#E5E5EC]">
            <div className="w-[272px]" />
            <div className="w-[60px] text-right">
              <span className="font-semibold text-[12px] leading-[24px] text-[#767676]">
                전여 병상
              </span>
            </div>
            <div className="w-[60px] text-right">
              <span className="font-semibold text-[12px] leading-[24px] text-[#767676]">
                총 병상
              </span>
            </div>
          </div>

          {/* Table Rows */}
          <div className="flex flex-col gap-[4px] pt-[4px]">
            <BedRow label="응급실" available={4} total={20} />
            <BedRow label="수술실" available={2} total={3} />
            <BedRow label="신생아 중환자실" available={2} total={52} />
            <BedRow label="입원실" available={456} total={1893} isHighlighted />
          </div>

          {/* Medical Imaging */}
          <div className="flex items-center h-[26px] pt-[8px] border-t border-[#E5E5EC] mt-[8px]">
            <div className="w-[272px]">
              <span className="font-normal text-[14px] leading-[22px] text-[#505050]">
                영상 검사
              </span>
            </div>
            <div className="w-[60px] text-right">
              <span className="font-semibold text-[12px] leading-[22px] text-[#017AFF]">
                CT 가능
              </span>
            </div>
            <div className="w-[60px] text-right">
              <span className="font-semibold text-[12px] leading-[22px] text-[#017AFF]">
                MRI 가능
              </span>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-[12px]">
          <button className="flex-1 h-[48px] flex items-center justify-center bg-[#F5F7FA] rounded-[10px] hover:bg-[#E5E5EC] transition-colors">
            <span className="font-semibold text-[15px] leading-[22px] text-[#767676]">
              응급실 공지
            </span>
          </button>
          <button className="flex-1 h-[48px] flex items-center justify-center bg-[#017AFF] rounded-[10px] hover:bg-[#0066DD] transition-colors">
            <span className="font-semibold text-[15px] leading-[22px] text-white">
              네이버 지도
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}

function EmergencyRoomStatusContent() {
  // State to control empty state display - set to true for empty state demo
  const [showEmptyState, setShowEmptyState] = useState(true);
  const resultCount = showEmptyState ? 0 : 49;

  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col items-center py-[40px] w-[780px]">
        <div className="flex flex-col gap-[50px] items-start w-full overflow-hidden">
          {/* Page Header */}
          <div className="flex flex-col gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6]">
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

          {/* Main Content - Two Column Layout */}
          <div className="flex gap-[36px] items-start w-full">
            {/* Left Column - Search */}
            <div className="flex flex-col gap-[30px] w-[280px] shrink-0">
              {/* Title Section */}
              <div className="flex flex-col gap-[10px]">
                <h2 className="font-bold text-[24px] leading-[34px] text-[#111111]">
                  응급실 검색
                </h2>
                <p className="font-normal text-[14px] leading-[22px] text-[#767676]">
                  처방받은 약을 심사평가원에서
                  <br />
                  자동으로 불러오거나 직접 입력해주세요.
                </p>
              </div>

              {/* Search Input */}
              <div className="flex items-center h-[50px] px-[16px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px]">
                <input
                  type="text"
                  placeholder="병원명을 검색하세요"
                  className="flex-1 bg-transparent text-[14px] leading-[22px] text-[#111111] placeholder:text-[#999999] outline-none"
                />
                <IconSearchMono size={20} />
              </div>
            </div>

            {/* Right Column - Results */}
            <div className="flex flex-col gap-[10px] flex-1 min-w-0">
              {/* Filter Tabs */}
              <div className="flex items-center">
                <FilterTab label="내 주변" hasArrow />
                <FilterTab label="지역" value="전체" isActive />
                <FilterTab label="세부지역" value="전체" />
              </div>

              {/* Results Count and Sort */}
              <div className="flex items-center justify-between h-[40px]">
                <div className="flex items-center gap-[4px]">
                  <span className="font-semibold text-[14px] leading-[20px] text-[#111111]">
                    전체
                  </span>
                  <span className="font-bold text-[14px] leading-[16px] text-[#017AFF]">
                    {resultCount}
                  </span>
                </div>
                <div className="flex items-center gap-[4px]">
                  <span className="font-normal text-[14px] leading-[20px] text-[#767676]">
                    거리순
                  </span>
                  <IconArrowRightSmall size={12} className="rotate-90" />
                </div>
              </div>

              {/* Hospital Cards or Empty State */}
              <div className="flex flex-col gap-[16px]">
                {showEmptyState ? (
                  <EmptyState />
                ) : (
                  <HospitalCard />
                )}
              </div>
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
