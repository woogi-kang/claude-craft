"use client";

import {
  Icon3DChat,
  Icon3DProfile,
  Icon3DMenu,
  Icon3DSetting,
  IconSecret,
  IconSearch,
  IconMic,
  IconPhoto,
  IconSend,
  IconCloseBlue,
} from "@/components/icons/icons";

interface ActionButtonProps {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
}

function ActionButton({ icon, label, active = false }: ActionButtonProps) {
  return (
    <div
      className={`flex gap-2 h-10 items-center justify-center px-4 rounded-[28px] border shrink-0 ${
        active
          ? "bg-white border-[#017AFF]"
          : "bg-white border-[#F0F0F6]"
      }`}
    >
      <div className="flex flex-col h-5 items-start justify-center">
        <span
          className={`font-normal text-sm leading-5 ${
            active ? "text-[#017AFF]" : "text-[#505050]"
          }`}
        >
          {label}
        </span>
      </div>
      {icon}
    </div>
  );
}

interface FeatureButtonProps {
  icon: React.ReactNode;
  label: string;
}

function FeatureButton({ icon, label }: FeatureButtonProps) {
  return (
    <div className="flex gap-2 h-[50px] items-center justify-center px-5 rounded-[28px] bg-white border border-[#F0F0F6] shrink-0">
      <div className="flex items-center justify-center shrink-0">
        {icon}
      </div>
      <div className="flex flex-col items-start justify-center">
        <span className="font-normal text-[15px] leading-[23px] text-[#111111] text-center">
          {label}
        </span>
      </div>
    </div>
  );
}

export function MainChat() {
  return (
    <div className="flex flex-1 flex-col h-full items-center min-h-px min-w-px overflow-auto">
      <div className="flex flex-1 flex-col gap-[30px] items-center justify-center min-h-px min-w-px pb-[100px] pt-10 w-full max-w-[640px] px-4">
        {/* Title Section */}
        <div className="flex gap-2.5 items-start pb-10 w-full border-b border-[#F0F0F6]">
          <div className="flex flex-col gap-2.5 items-start w-full">
            <div className="font-bold text-[34px] leading-[46px] tracking-[-0.68px] text-[#111111] w-full">
              <p className="mb-0">그럼,</p>
              <p className="mb-0">건강 질문부터 시작해보세요!</p>
            </div>
          </div>
        </div>

        {/* Input Section */}
        <div className="flex flex-col gap-4 items-start pt-9 w-full">
          {/* Action Buttons */}
          <div className="flex gap-2 items-start w-full">
            <ActionButton
              icon={<IconSecret size={16} />}
              label="비밀 대화"
              active={true}
            />
            <ActionButton icon={<IconSearch size={16} />} label="심층답변" />
            <ActionButton icon={<IconMic size={16} />} label="말로하기" />
          </div>

          {/* Input Box */}
          <div className="flex flex-col gap-2.5 items-center justify-end px-5 py-3.5 rounded-[20px] bg-white border border-[#F0F0F6] shadow-[0px_-5px_20px_0px_rgba(0,0,0,0.02)] w-full">
            <div className="flex items-end justify-center w-full">
              <div className="flex flex-1 items-center min-h-px min-w-px py-[7px]">
                <p className="flex-1 font-normal text-base leading-[22px] text-[#767676] min-h-px min-w-px">
                  증상, 음식, 약 무엇이든 물어보세요!
                </p>
              </div>
            </div>
            <div className="flex items-center justify-between w-full">
              <IconPhoto size={40} />
              <div className="flex gap-2.5 items-center">
                <div className="flex gap-2 h-10 items-center justify-center px-4 rounded-[28px] bg-white border border-[#F0F0F6] shrink-0">
                  <div className="flex flex-col h-5 items-start justify-center">
                    <span className="font-normal text-sm leading-5 text-[#017AFF]">
                      일반 답변
                    </span>
                  </div>
                  <IconCloseBlue size={16} />
                </div>
                <IconSend size={40} />
              </div>
            </div>
          </div>

          {/* Feature Buttons */}
          <div className="flex gap-2.5 items-start w-full">
            <FeatureButton icon={<Icon3DChat size={18} />} label="그럼AI 소개" />
            <FeatureButton icon={<Icon3DProfile size={16} />} label="건강 프로필" />
            <FeatureButton icon={<Icon3DMenu size={17} />} label="실시간 응급실 찾기" />
            <FeatureButton icon={<Icon3DSetting size={17} />} label="더 보기" />
          </div>
        </div>
      </div>
    </div>
  );
}
