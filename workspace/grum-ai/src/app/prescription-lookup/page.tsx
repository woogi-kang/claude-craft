"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import {
  IconArrowDownBlue,
  IconArrowRightGray,
  IconPlusGray,
} from "@/components/icons/icons";

interface MedicalRecordItemProps {
  date: string;
  pharmacyName: string;
  onClick?: () => void;
}

function MedicalRecordItem({ date, pharmacyName, onClick }: MedicalRecordItemProps) {
  return (
    <button
      onClick={onClick}
      className="flex gap-[10px] h-[50px] items-center w-full border-b border-[#F0F0F6]"
    >
      <span className="font-normal text-[16px] leading-[26px] text-[#505050] w-[80px] shrink-0">
        {date}
      </span>
      <span className="flex-1 font-normal text-[16px] leading-[26px] text-[#111111] text-left">
        {pharmacyName}
      </span>
      <IconArrowRightGray size={20} />
    </button>
  );
}

function PrescriptionLookupContent() {
  const medicalRecords = [
    { date: "25/01/23", pharmacyName: "서울본내과의원" },
    { date: "25/01/23", pharmacyName: "서울본내과의원" },
    { date: "25/01/23", pharmacyName: "서울본내과의원" },
  ];

  return (
    <div className="flex flex-col items-center flex-1 min-w-0 min-h-px h-full overflow-auto bg-[#FDFDFD]">
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
              <p className="mb-0">진료내역 중 비급여 진료항목은 불러올 수 없어요.</p>
              <p className="mb-0">또한 병원에서 심사평가원에 청구(보고)를 늦게 하는 경우에는 건강프로필을 업데이트해도 보이지 않을 수 있습니다.</p>
              <p>병원 사정에 따라 1-2개월까지 청구를 늦게 하는 경우가 있으니 참고해주세요.</p>
            </div>
          </div>
        </div>

        {/* Content Section */}
        <div className="flex flex-col items-start w-full">
          <div className="flex flex-col items-start w-full">
            <div className="flex gap-[40px] items-start justify-center w-full">
              {/* Left Body - Label Area */}
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
                            처방 받은 약 조회
                          </h2>
                          <div className="font-normal text-[15px] leading-[23px] text-[#505050] w-full">
                            <p className="mb-0">의사 처방을 받지 않고</p>
                            <p>약국에서 별도 구매한 약은 조회할 수 없어요.</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Content Area */}
              <div className="flex flex-col flex-1 gap-[24px] items-start min-w-0 min-h-px">
                {/* Primary Button */}
                <div className="flex flex-col gap-[10px] items-center justify-center w-full">
                  <button className="flex items-center justify-center h-[52px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors overflow-hidden">
                    <span className="font-semibold text-[16px] leading-[22px] text-white">
                      처방 내역 최신화하기
                    </span>
                  </button>
                </div>

                {/* Filter Inputs */}
                <div className="flex flex-col gap-[10px] items-start justify-center w-full">
                  <div className="flex gap-[10px] h-[52px] items-center w-full">
                    {/* Period Dropdown */}
                    <div className="flex items-center h-full w-[120px] shrink-0 px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] overflow-hidden">
                      <div className="flex flex-1 gap-[10px] items-center">
                        <span className="flex-1 font-normal text-[15px] leading-[23px] text-[#999999]">
                          기간
                        </span>
                        <IconArrowDownBlue size={20} />
                      </div>
                    </div>

                    {/* Pharmacy Name Input */}
                    <div className="flex flex-1 items-center h-full min-w-0 px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] overflow-hidden">
                      <span className="font-normal text-[15px] leading-[23px] text-[#999999]">
                        약국명
                      </span>
                    </div>

                    {/* Search Button */}
                    <button className="flex items-center justify-center h-full w-[80px] shrink-0 px-[14px] bg-[#017AFF] rounded-[10px] hover:bg-[#0066DD] transition-colors overflow-hidden">
                      <span className="font-semibold text-[14px] leading-[20px] text-white">
                        검색
                      </span>
                    </button>
                  </div>
                </div>

                {/* Medical Records Section */}
                <div className="flex flex-col items-start w-full">
                  <div className="flex flex-col gap-[20px] items-start w-full">
                    {/* Section Header */}
                    <div className="flex flex-col gap-[10px] items-start w-full">
                      <h3 className="font-semibold text-[16px] leading-[22px] text-[#111111] w-full">
                        내 진료 정보
                      </h3>
                      <p className="font-normal text-[14px] leading-[20px] text-[#505050] w-full">
                        연동을 원하지 않는 진료 내역은 삭제할 수 있어요.
                      </p>
                    </div>

                    {/* Records List */}
                    <div className="flex flex-col gap-[20px] items-start w-full">
                      <div className="flex flex-col items-start px-[20px] py-[4px] w-full border border-[#F0F0F6] rounded-[10px]">
                        {medicalRecords.map((record, index) => (
                          <MedicalRecordItem
                            key={index}
                            date={record.date}
                            pharmacyName={record.pharmacyName}
                          />
                        ))}

                        {/* Load More Button */}
                        <button className="flex gap-[10px] h-[48px] items-center justify-center w-full hover:bg-[#FAFAFA] transition-colors">
                          <IconPlusGray size={16} />
                          <span className="font-normal text-[15px] leading-[23px] text-[#111111] text-center">
                            더 보기
                          </span>
                        </button>
                      </div>

                      {/* Delete All Link */}
                      <button className="font-normal text-[15px] leading-[23px] text-[#999999] underline text-center w-full hover:text-[#777777] transition-colors">
                        진료 정보 전체 삭제
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

export default function PrescriptionLookupPage() {
  return (
    <div className="flex items-start h-screen w-full">
      {/* Left Sidebar - 300px fixed width */}
      <LeftSidebar />

      {/* Main Body - Flexible */}
      <div className="flex flex-1 flex-col h-full items-start min-h-px min-w-px overflow-hidden">
        {/* Status Bar - 80px height */}
        <StatusBar />

        {/* Main Content Area */}
        <div className="flex flex-1 items-start justify-between min-h-px min-w-px overflow-hidden w-full">
          {/* Prescription Lookup Content Area - Flexible */}
          <PrescriptionLookupContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
