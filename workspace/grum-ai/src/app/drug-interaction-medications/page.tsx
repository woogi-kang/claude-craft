"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import { IconCloseGray, IconExclamationCircle } from "@/components/icons/icons";
import { useState } from "react";

interface MedicationItemProps {
  name: string;
  onRemove: () => void;
}

function MedicationItem({ name, onRemove }: MedicationItemProps) {
  return (
    <div className="flex gap-[10px] h-[50px] items-center w-full border-b border-[#E5E5EC]">
      <div className="flex-1 min-w-0 min-h-px font-normal text-[16px] leading-[26px] text-[#111111]">
        {name}
      </div>
      <button
        onClick={onRemove}
        className="shrink-0 w-[20px] h-[20px] overflow-hidden flex items-center justify-center"
        aria-label={`${name} 삭제`}
      >
        <IconCloseGray size={20} />
      </button>
    </div>
  );
}

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

function SubTitleSection({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col gap-[14px] items-start w-full">
      <div className="flex gap-[10px] items-center w-full">
        <p className="flex-1 min-w-0 min-h-px font-semibold text-[16px] leading-[22px] text-[#111111]">
          {title}
        </p>
      </div>
      {children}
    </div>
  );
}

function EmptyStateBox({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center justify-center p-[14px] bg-[#F5F7FA] rounded-[10px] w-full overflow-hidden">
      <p className="font-normal text-[15px] leading-[22px] text-[#111111] text-center w-full opacity-80">
        {message}
      </p>
    </div>
  );
}

function SearchInput({
  placeholder,
  onSubmit,
}: {
  placeholder: string;
  onSubmit: (value: string) => void;
}) {
  const [value, setValue] = useState("");

  const handleSubmit = () => {
    if (value.trim()) {
      onSubmit(value.trim());
      setValue("");
    }
  };

  return (
    <div className="flex flex-col gap-[10px] items-center justify-center w-full">
      <div className="w-full font-semibold text-[16px] leading-[22px] text-[#111111]">
        <p>약물 검색</p>
      </div>
      <div className="flex gap-[10px] h-[52px] items-center w-full">
        <div className="flex flex-1 h-full items-center px-[14px] bg-[#F5F7FA] border border-[#E5E5EC] rounded-[10px] min-w-0 min-h-px overflow-hidden">
          <div className="flex flex-1 gap-[10px] items-center min-w-0 min-h-px">
            <input
              type="text"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              placeholder={placeholder}
              className="flex-1 min-w-0 min-h-px font-normal text-[15px] leading-[23px] text-[#111111] placeholder:text-[#999999] bg-transparent outline-none"
            />
          </div>
        </div>
        <button
          onClick={handleSubmit}
          className="flex items-center justify-center h-full w-[100px] px-[14px] bg-[#017AFF] rounded-[10px] overflow-hidden shrink-0 hover:bg-[#0066DD] transition-colors"
        >
          <span className="font-semibold text-[15px] leading-[23px] text-white">
            입력
          </span>
        </button>
      </div>
    </div>
  );
}

function InfoButton({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="flex gap-[10px] h-[40px] items-center justify-center px-[20px] w-full bg-[#F5F7FA] border border-[#E5E5EC] rounded-[25px]">
      <IconExclamationCircle size={20} variant="blue" />
      <div className="flex items-center shrink-0">
        <span className="font-semibold text-[15px] leading-[23px] text-[#111111]">
          {label}
        </span>
      </div>
      <div className="flex flex-1 items-center justify-center min-w-0 min-h-px">
        <span className="flex-1 min-w-0 min-h-px font-normal text-[15px] leading-[23px] text-[#767676] text-right">
          {value}
        </span>
      </div>
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
      <span className="font-semibold text-[16px] leading-[22px] text-white text-center">
        {label}
      </span>
    </button>
  );
}

function DrugInteractionMedicationsContent() {
  const [medications, setMedications] = useState([
    { id: 1, name: "온미환" },
    { id: 2, name: "아트정" },
    { id: 3, name: "이노콜정" },
  ]);

  const handleRemoveMedication = (id: number) => {
    setMedications(medications.filter((med) => med.id !== id));
  };

  const handleAddMedication = (name: string) => {
    const newId = Math.max(...medications.map((m) => m.id), 0) + 1;
    setMedications([...medications, { id: newId, name }]);
  };

  const handleClearAll = () => {
    setMedications([]);
  };

  const handleUpdateRecords = () => {
    console.log("Update medical records clicked");
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
            {/* Recently Prescribed Medications */}
            <SubTitleSection title="최근 처방된 약">
              <div className="flex flex-col gap-[14px] items-start w-full">
                <EmptyStateBox message="최근 처방되어 복용중인 약을 찾을 수 없습니다." />
              </div>
            </SubTitleSection>

            {/* Medication Search and List */}
            <div className="flex flex-col gap-[14px] items-start w-full">
              <SearchInput
                placeholder="약물 이름을 입력해주세요."
                onSubmit={handleAddMedication}
              />

              {/* Medication List */}
              <div className="flex flex-col gap-[14px] items-start w-full">
                <div className="flex flex-col gap-[14px] items-start w-full">
                  <div className="flex flex-col gap-[20px] items-start w-full">
                    <div className="flex flex-col gap-[10px] items-start w-full">
                      <div className="flex flex-col gap-[10px] items-start w-full">
                        {medications.map((med) => (
                          <MedicationItem
                            key={med.id}
                            name={med.name}
                            onRemove={() => handleRemoveMedication(med.id)}
                          />
                        ))}
                      </div>
                    </div>

                    {/* Clear All Link */}
                    <div className="w-full text-center">
                      <button
                        onClick={handleClearAll}
                        className="font-normal text-[15px] leading-[23px] text-[#999999] underline hover:text-[#767676] transition-colors"
                      >
                        진료 정보 전체 삭제
                      </button>
                    </div>
                  </div>

                  {/* Sync Date Info Button */}
                  <InfoButton label="처방 약물 연동 일자" value="25.07.11" />
                </div>

                {/* Primary CTA Button */}
                <PrimaryButton
                  label="진료기록 최신화하기"
                  onClick={handleUpdateRecords}
                />
              </div>
            </div>
          </SectionRow>
        </div>
      </div>
    </div>
  );
}

export default function DrugInteractionMedicationsPage() {
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
          {/* Drug Interaction Medications Content Area - Flexible */}
          <DrugInteractionMedicationsContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
