"use client";

import Image from "next/image";
import {
  IconLogoBlue,
  Icon3DProfile,
  IconCopy,
  IconCloseGray,
  IconShare,
  IconArrowRightGray,
  IconCloseCircle,
  IconPhoto,
  IconSend,
  IconCloseBlue,
} from "@/components/icons/icons";

// User message with image
function UserMessage() {
  return (
    <div className="flex flex-col gap-2.5 items-end w-full">
      {/* Image */}
      <div className="relative w-[150px] h-[96px] rounded-xl overflow-hidden">
        <Image
          src="/images/sample-skin.png"
          alt="User uploaded image"
          fill
          className="object-cover"
        />
      </div>
      {/* Text bubble */}
      <div className="flex flex-col items-start justify-center px-4 py-3 rounded-bl-2xl rounded-br-2xl rounded-tl-2xl bg-gradient-to-b from-[#6EB2FE] to-[#017AFF] border border-[rgba(0,62,129,0.02)]">
        <p className="text-[15px] leading-[22px] text-white font-normal">
          이거 두드러기야?
        </p>
      </div>
    </div>
  );
}

// AI Response message
function AIResponse() {
  return (
    <div className="flex flex-col gap-2.5 items-start justify-center w-full">
      {/* Logo */}
      <IconLogoBlue className="shrink-0" />

      {/* Response content */}
      <div className="flex flex-col items-start justify-center py-3 w-full rounded-tl-[6px] rounded-tr-xl rounded-bl-xl rounded-br-xl">
        <div className="text-base leading-[30px] text-[#111111] font-normal w-full">
          <p className="mb-0">안녕하세요.</p>
          <p className="mb-0">저는 맞춤 건강 상담해드리는 그럼이에요.</p>
          <p className="mb-0">&nbsp;</p>
          <p className="mb-0">가슴 통증과 기침의 잠재적 원인에 대해 알려드릴게요.</p>
          <p className="mb-0">몇 가지 흔한 원인들은 다음과 같습니다.</p>
          <ul className="list-disc ml-6 mt-0">
            <li>
              <span className="leading-[30px]">
                감기 또는 독감: 가장 흔한 원인 중 하나로, 기침과 함께 인후통, 콧물, 발열 등의 증상이 동반될 수 있습니다. 가슴 통증은 심한 기침으로 인해 근육통처럼 나타나기도 합니다.
              </span>
            </li>
            <li>
              <span className="leading-[30px]">
                기관지염: 기관지에 염증이 생긴 상태로, 심한 기침과 함께 가래, 숨 가쁨, 가슴 답답함 등의 증상이 나타날 수 있습니다.
              </span>
            </li>
          </ul>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-2.5 items-center">
        <div className="flex gap-1 items-center cursor-pointer">
          <IconCopy size={16} />
          <span className="text-sm leading-5 text-[#505050] text-center">복사</span>
        </div>
        <div className="flex gap-1 items-center cursor-pointer">
          <IconCloseGray size={16} />
          <span className="text-[15px] leading-[23px] text-[#505050] text-center">지우기</span>
        </div>
        <div className="flex gap-1 items-center cursor-pointer">
          <IconShare size={16} />
          <span className="text-sm leading-5 text-[#505050] text-center">공유</span>
        </div>
      </div>
    </div>
  );
}

// Medical records link button
function MedicalRecordsButton() {
  return (
    <div className="flex flex-col items-center justify-center w-full">
      <button className="flex gap-2 h-[52px] items-center justify-center px-5 rounded-[28px] bg-[#017AFF]">
        <div className="flex items-center justify-center shrink-0">
          <Icon3DProfile size={16} />
        </div>
        <span className="text-[15px] leading-[23px] text-white font-semibold text-center">
          의료기록 연동 바로가기
        </span>
      </button>
    </div>
  );
}

// Follow-up questions section
function FollowUpQuestions() {
  const questions = [
    "두드러기는 옮는 피부병인가요?",
    "두드러기와 아토피의 차이는 무엇인가요? 두줄일때 어떤식으로 나오는지 만약 두드러기와  두줄일때 어떤식으로 나오는지 만약 두드러기와 두줄일때 어떤식으로 나오는지 만약 두드러기와",
    "음식으로 인해 갑자기 두드러기가 생길 수 있나요?",
  ];

  return (
    <div className="flex flex-col gap-2.5 items-start w-full">
      <h3 className="text-lg leading-6 text-[#017AFF] font-bold w-full">
        이어서 질문해보세요!
      </h3>
      <div className="flex flex-col gap-2.5 items-start w-full">
        {questions.map((question, index) => (
          <div
            key={index}
            className="flex gap-2.5 items-center py-2.5 w-full border-b border-[#E5E5EC] cursor-pointer hover:bg-gray-50 transition-colors"
          >
            <p className="flex-1 text-base leading-[26px] text-[#111111] font-normal min-h-px min-w-px">
              {question}
            </p>
            <IconArrowRightGray size={20} className="shrink-0" />
          </div>
        ))}
      </div>
    </div>
  );
}

// Chat input with images
function ChatInput() {
  return (
    <div className="flex flex-col gap-4 items-start pt-9 w-full">
      <div className="flex flex-col gap-2.5 items-center justify-end px-5 py-3.5 rounded-[20px] bg-white border border-[#F0F0F6] shadow-[0px_-5px_20px_0px_rgba(0,0,0,0.02)] w-full">
        {/* Input text and images */}
        <div className="flex flex-col gap-2.5 items-center justify-end w-full max-w-[600px]">
          {/* Input text */}
          <div className="flex items-center py-[7px] w-full">
            <p className="flex-1 text-base leading-[22px] text-[#111111] font-normal min-h-px min-w-px">
              이거 두드러기야?
            </p>
          </div>

          {/* Attached images */}
          <div className="flex gap-2 items-center w-full">
            {[1, 2].map((_, index) => (
              <div key={index} className="relative w-[70px] h-[50px] rounded-xl overflow-hidden shrink-0">
                <Image
                  src="/images/sample-skin.png"
                  alt="Attached image"
                  fill
                  className="object-cover"
                />
                <div className="absolute top-1 right-1 cursor-pointer">
                  <IconCloseCircle size={20} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Input actions */}
        <div className="flex items-center justify-between w-full">
          <IconPhoto size={40} />
          <div className="flex gap-2.5 items-center">
            <div className="flex gap-2 h-10 items-center justify-center px-4 rounded-[28px] bg-white border border-[#F0F0F6] shrink-0">
              <span className="text-sm leading-5 text-[#017AFF] font-normal">
                일반 답변
              </span>
              <IconCloseBlue size={16} />
            </div>
            <IconSend size={40} active />
          </div>
        </div>
      </div>
    </div>
  );
}

export function ChatConversation() {
  return (
    <div className="flex flex-1 flex-col h-full items-center min-h-px min-w-px overflow-auto">
      <div className="flex flex-col gap-[30px] items-end py-10 w-[640px]">
        {/* User message */}
        <UserMessage />

        {/* AI Response */}
        <AIResponse />

        {/* Medical records button */}
        <MedicalRecordsButton />

        {/* Follow-up questions */}
        <FollowUpQuestions />

        {/* Chat input */}
        <ChatInput />
      </div>
    </div>
  );
}
