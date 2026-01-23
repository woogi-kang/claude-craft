"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import { IconArrowRightGray, IconCloseCircle } from "@/components/icons/icons";

interface FamilyMemberItemProps {
  name: string;
  relation: string;
  onClick?: () => void;
}

function FamilyMemberItem({ name, relation, onClick }: FamilyMemberItemProps) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-[10px] h-[50px] w-full border-b border-[#E5E5EC]"
    >
      <IconCloseCircle size={20} />
      <span className="flex-1 font-normal text-[16px] leading-[26px] text-[#111111] text-left">
        {relation} ({name})
      </span>
      <IconArrowRightGray size={20} />
    </button>
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

function FamilyHealthProfileContent() {
  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col gap-[36px] items-center py-[40px] w-[780px]">
        {/* Page Header */}
        <div className="flex gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6] h-[186px]">
          <div className="flex flex-col gap-[10px] items-start w-[692px]">
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

        {/* Content Body */}
        <div className="flex flex-col items-start w-full">
          <div className="flex gap-[40px] items-start justify-center w-full">
            {/* Left Body */}
            <div className="flex flex-col items-start shrink-0 w-[280px] self-stretch">
              <div className="flex flex-col gap-[20px] items-start w-[280px]">
                <div className="flex h-[164.816px] items-center justify-center w-full">
                  <div className="w-full">
                    <div className="flex flex-col items-start justify-center w-full">
                      <div className="flex flex-col gap-[8px] items-start w-full">
                        <span className="font-semibold text-[16px] leading-[22px] text-[#017AFF] w-full">
                          가족 관계 등록
                        </span>
                        <h2 className="font-bold text-[22px] leading-[34px] text-[#111111] w-full">
                          가족 건강 프로필 만들기
                        </h2>
                        <p className="font-normal text-[15px] leading-[23px] text-[#505050] w-full">
                          가족들의 건강프로필을 만들면 AI가 자녀, 부모님 질문에도 맞춤 답변을 해드릴 수 있습니다.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Body */}
            <div className="flex flex-col flex-1 gap-[24px] items-start min-h-px min-w-px">
              {/* Add Family Button */}
              <div className="flex flex-col gap-[10px] items-center justify-center w-full">
                <PrimaryButton label="가족 추가" />
              </div>

              {/* Family List Section */}
              <div className="flex flex-col gap-[20px] items-start w-full">
                <div className="flex flex-col gap-[10px] items-start w-full">
                  <span className="font-semibold text-[16px] leading-[22px] text-[#111111] w-full">
                    건강 프로필
                  </span>
                  <div className="flex flex-col gap-[10px] items-start w-full">
                    <FamilyMemberItem relation="아내" name="김아내" />
                    <FamilyMemberItem relation="자녀" name="홍길동" />
                    <FamilyMemberItem relation="반려동물" name="멍멍" />
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

export default function FamilyHealthProfilePage() {
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
          {/* Family Health Profile Content Area - Flexible */}
          <FamilyHealthProfileContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
