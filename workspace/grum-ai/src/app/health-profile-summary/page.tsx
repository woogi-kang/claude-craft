"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import {
  IconExclamationCircle,
  IconArrowRightGray,
} from "@/components/icons/icons";

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
      <div className="flex flex-col flex-1 min-w-0 min-h-px items-start">
        {children}
      </div>
    </div>
  );
}

interface StatusBadgeActiveProps {
  label: string;
  updateDate: string;
}

function StatusBadgeActive({ label, updateDate }: StatusBadgeActiveProps) {
  return (
    <div className="flex items-center gap-[10px] h-[52px] px-[20px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[25px] w-full">
      <IconExclamationCircle size={20} variant="blue" />
      <span className="font-semibold text-[15px] leading-[24px] text-[#111111]">
        {label}
      </span>
      <div className="flex flex-1 h-[24px] items-center justify-end">
        <span className="font-normal text-[15px] leading-[24px] text-[#767676] text-right">
          {updateDate}
        </span>
      </div>
    </div>
  );
}

interface RecordInputProps {
  label: string;
  date: string;
  value: string;
}

function RecordInput({ label, date, value }: RecordInputProps) {
  return (
    <div className="flex flex-col gap-[10px] items-center justify-center w-full">
      <div className="flex gap-[10px] items-start w-full">
        <span className="font-semibold text-[16px] leading-[22px] text-[#111111]">
          {label}
        </span>
      </div>
      <div className="flex h-[50px] items-center w-full">
        <div className="flex flex-1 h-[52px] items-center px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] overflow-hidden">
          <div className="flex flex-1 items-center gap-[10px]">
            <span className="font-normal text-[14px] leading-[20px] text-[#505050] w-[60px]">
              {date}
            </span>
            <span className="flex-1 font-normal text-[15px] leading-[23px] text-[#111111]">
              {value}
            </span>
          </div>
        </div>
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
    <button className="flex items-center justify-center h-[52px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors overflow-hidden">
      <span className="font-semibold text-[16px] leading-[22px] text-white">
        {label}
      </span>
    </button>
  );
}

function SecondaryButton({ label }: { label: string }) {
  return (
    <button className="flex items-center justify-center h-[52px] px-[20px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] w-full hover:bg-[#EBEEF3] transition-colors overflow-hidden">
      <span className="font-semibold text-[16px] leading-[22px] text-[#999999]">
        {label}
      </span>
    </button>
  );
}

function PrimaryButtonSmall({ label }: { label: string }) {
  return (
    <button className="flex items-center justify-center h-[50px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors overflow-hidden">
      <span className="font-semibold text-[16px] leading-[22px] text-white">
        {label}
      </span>
    </button>
  );
}

interface ListItemProps {
  label: string;
  onClick?: () => void;
}

function ListItem({ label, onClick }: ListItemProps) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-[10px] h-[50px] w-full border-b border-[#E5E5EC]"
    >
      <span className="flex-1 font-normal text-[16px] leading-[26px] text-[#111111] text-left">
        {label}
      </span>
      <IconArrowRightGray size={20} />
    </button>
  );
}

function HealthProfileSummaryContent() {
  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col gap-[36px] items-center py-[40px] w-[780px]">
        {/* Page Header */}
        <div className="flex gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6] h-[163px]">
          <div className="flex flex-col gap-[10px] items-start w-[692px]">
            <span className="font-semibold text-[22px] leading-[34px] text-[#017AFF] tracking-[-0.44px] w-full">
              나의 모든 건강, 의료 기록
            </span>
            <h1 className="font-bold text-[34px] leading-[46px] text-[#111111] tracking-[-0.68px] w-full">
              건강 프로필
            </h1>
            <p className="font-normal text-[16px] leading-[23px] text-[#505050] tracking-[-0.32px] w-full">
              나와 가족의 건강, 이제 &apos;건강프로필&apos;로 AI가 평생 관리해드립니다!
            </p>
          </div>
        </div>

        {/* Content Sections */}
        <div className="flex flex-col gap-[28px] items-start w-full">
          {/* Section 1: Health Profile */}
          <SectionRow title="건강 프로필">
            <div className="flex flex-col gap-[28px] items-start w-full">
              {/* Status Badge */}
              <StatusBadgeActive
                label="이용 중"
                updateDate="최근 업데이트일 : 26.02.11"
              />

              {/* Recent Medical Records */}
              <RecordInput
                label="최근 진료 기록"
                date="25/01/23"
                value="본내과의원 외 25건"
              />

              {/* Recent Health Checkup Records */}
              <RecordInput
                label="최근 국가 건강검진 기록"
                date="25/01/23"
                value="사과내과의원"
              />

              {/* Buttons */}
              <div className="flex flex-col gap-[10px] items-start w-full">
                <PrimaryButton label="건강프로필 업데이트" />
                <SecondaryButton label="가족별 건강프로필 확인" />
              </div>
            </div>
          </SectionRow>

          {/* Section 2: Additional Medical History */}
          <SectionRow title="추가 병력 직접 입력하기">
            <div className="flex flex-col items-start w-full">
              <div className="flex flex-col gap-[14px] items-start w-full">
                <div className="flex flex-col gap-[14px] items-start w-full">
                  <InfoBox>
                    <p className="mb-0">자동 연동된 병원 진료기록 외에 그럼AI가</p>
                    <p className="mb-0">참고해야할 질병, 증상이 있으시면 기입해주세요.</p>
                  </InfoBox>
                  <div className="flex flex-col gap-[10px] items-start w-full">
                    <PrimaryButtonSmall label="추가 병력 저장" />
                  </div>
                </div>
              </div>
            </div>
          </SectionRow>

          {/* Section 3: Details */}
          <SectionRow title="상세">
            <div className="flex flex-col gap-[20px] items-start w-full">
              <div className="flex flex-col gap-[10px] items-start w-full">
                <div className="flex flex-col gap-[10px] items-start w-full">
                  <ListItem label="진료 기록" />
                  <ListItem label="처방 받은 약" />
                  <ListItem label="국가건강검진 결과" />
                </div>
              </div>
              <button className="font-normal text-[15px] leading-[23px] text-[#999999] underline text-center w-full hover:text-[#777777] transition-colors">
                진료 정보 전체 삭제
              </button>
            </div>
          </SectionRow>
        </div>
      </div>
    </div>
  );
}

export default function HealthProfileSummaryPage() {
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
          {/* Health Profile Summary Content Area - Flexible */}
          <HealthProfileSummaryContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
