"use client";

import { IconCloseBlue, IconCloseGray, IconPlus } from "@/components/icons/icons";

interface ChatHistoryItemProps {
  title: string;
  date: string;
}

function ChatHistoryItem({ title, date }: ChatHistoryItemProps) {
  return (
    <div className="flex gap-2 h-[60px] items-start pb-2.5 w-full border-b border-[#E5E5EC]">
      <div className="flex flex-1 flex-col justify-between h-12 min-h-px min-w-px font-normal">
        <div className="text-[15px] leading-[23px] text-[#111111] overflow-hidden text-ellipsis whitespace-nowrap">
          {title}
        </div>
        <div className="text-sm leading-5 text-[#999999]">
          {date}
        </div>
      </div>
      <div className="flex items-center justify-center shrink-0">
        <IconCloseGray size={16} />
      </div>
    </div>
  );
}

export function ChatHistory() {
  const historyItems = [
    { title: "위암 3기 치료옵션", date: "1일 전" },
    { title: "싸이모신알파 주사 효과", date: "3일 전" },
    { title: "포도의 간세포 독성", date: "일주일 전" },
    { title: "포도의 간세포 독성", date: "일주일 전" },
  ];

  return (
    <div className="flex flex-col gap-[30px] h-full items-start overflow-hidden px-6 py-10 bg-[#FAFAFA] shrink-0 w-[300px]">
      {/* Title */}
      <div className="flex gap-2.5 items-start w-full">
        <div className="flex-1 font-semibold text-base leading-[22px] text-[#111111] min-h-px min-w-px">
          AI 상담기록
        </div>
        <IconCloseBlue size={20} />
      </div>

      {/* New Question Button */}
      <div className="flex gap-1 h-11 items-center justify-center px-9 py-2.5 rounded-full bg-[#F5F7FA] border border-[#F0F0F6] w-full">
        <IconPlus size={16} />
        <span className="font-normal text-[15px] leading-[23px] text-[#111111] text-center">
          새로운 질문
        </span>
      </div>

      {/* Chat History List */}
      <div className="flex flex-col gap-2.5 items-start w-full">
        {historyItems.map((item, index) => (
          <ChatHistoryItem key={index} title={item.title} date={item.date} />
        ))}
      </div>
    </div>
  );
}
