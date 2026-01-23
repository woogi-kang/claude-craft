"use client";

import Image from "next/image";
import {
  Icon3DChat,
  Icon3DFood,
  Icon3DProfile,
  Icon3DMenu,
  IconArrowDown,
  IconExternal,
} from "@/components/icons/icons";

interface SidebarSectionProps {
  icon: React.ReactNode;
  title: string;
  items?: string[];
  expanded?: boolean;
}

function SidebarSection({ icon, title, items, expanded = true }: SidebarSectionProps) {
  return (
    <div className="flex flex-col gap-5 items-center overflow-hidden pt-5 px-6 w-[300px]">
      <div className="flex gap-2.5 items-start w-full">
        <div className="flex items-center justify-center shrink-0">
          {icon}
        </div>
        <div className="flex-1 font-semibold text-base leading-[22px] text-[#111111]">
          {title}
        </div>
        <IconArrowDown className={`shrink-0 transition-transform ${expanded ? '' : '-rotate-90'}`} size={20} />
      </div>
      {expanded && items && items.length > 0 && (
        <div className="flex flex-col gap-4 w-full">
          {items.map((item, index) => (
            <div key={index} className="flex items-center pl-[30px] w-full">
              <div className="font-normal text-[15px] leading-[23px] text-[#111111] w-[200px]">
                {item}
              </div>
            </div>
          ))}
        </div>
      )}
      <div className="h-0 w-[260px] border-b border-[#E5E5EC]" />
    </div>
  );
}

function SidebarLink({ icon, title }: { icon: React.ReactNode; title: string }) {
  return (
    <div className="flex gap-2.5 items-start w-full cursor-pointer hover:opacity-80 transition-opacity">
      <div className="flex items-center justify-center shrink-0">
        {icon}
      </div>
      <div className="font-semibold text-[15px] leading-normal text-[#505050] w-[200px]">
        {title}
      </div>
      <div className="flex items-center justify-center shrink-0">
        <IconExternal size={20} />
      </div>
    </div>
  );
}

export function LeftSidebar() {
  return (
    <div className="flex flex-col justify-between items-start bg-[#FAFAFA] shrink-0 w-[300px] h-[1285px]">
      {/* Top Section */}
      <div className="flex flex-col items-start w-full">
        {/* Logo */}
        <div className="flex h-20 items-center overflow-hidden px-6 w-full">
          <div className="relative h-[31px] w-[30px] shrink-0">
            <Image
              src="/images/logo-icon.png"
              alt="Grum AI Logo"
              fill
              className="object-cover"
            />
          </div>
        </div>

        {/* AI Section */}
        <SidebarSection
          icon={<Icon3DChat size={18} />}
          title="AI 상담"
          expanded={true}
        />

        {/* Food Section */}
        <SidebarSection
          icon={<Icon3DFood size={16} />}
          title="음식"
          items={["나에게 맞는 음식 찾기", "약이랑 먹으면 안 되는 음식"]}
          expanded={true}
        />

        {/* My Info Section */}
        <SidebarSection
          icon={<Icon3DProfile size={16} />}
          title="내 정보"
          items={[
            "마이페이지",
            "건강프로필 (의료정보 연동)",
            "가족별 건강프로필",
            "병원 이용내역 확인",
            "처방받은 약",
          ]}
          expanded={true}
        />

        {/* Others Section */}
        <SidebarSection
          icon={<Icon3DMenu size={17} />}
          title="기타"
          items={["실시간 응급실 찾기", "자가진단"]}
          expanded={true}
        />

        {/* Logout */}
        <div className="flex flex-col h-[60px] items-center justify-center overflow-hidden px-6 w-[300px]">
          <div className="flex items-center pl-[30px] w-full">
            <div className="font-semibold text-[15px] leading-[23px] text-[#999999] text-center w-[200px]">
              로그아웃
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="flex flex-col gap-8 h-[354px] items-start justify-end bg-[#FAFAFA] w-full">
        {/* Links */}
        <div className="flex flex-col gap-5 items-center pt-5 px-6 w-full">
          <SidebarLink
            icon={
              <Image
                src="/images/3d-chat.png"
                alt="Chat"
                width={18}
                height={18}
                className="object-contain"
              />
            }
            title="카카오톡 문의"
          />
          <SidebarLink
            icon={
              <Image
                src="/images/3d-app.png"
                alt="App"
                width={18}
                height={18}
                className="object-contain"
              />
            }
            title="어플리케이션"
          />
          <div className="h-0 w-[260px] border-b border-[#E5E5EC]" />
        </div>

        {/* Footer */}
        <div className="flex flex-col gap-3.5 items-start pb-10 pt-5 px-6 w-full">
          <div className="flex flex-col gap-[5px] items-start w-full">
            <div className="font-semibold text-sm leading-5 text-[#767676]">이용약관</div>
            <div className="font-semibold text-sm leading-5 text-[#767676]">개인정보처리방침</div>
            <div className="font-semibold text-sm leading-5 text-[#767676]">입점문의</div>
          </div>
          <div className="flex flex-col gap-2.5 items-start w-full">
            <div className="font-normal text-[13px] leading-[18px] text-[#999999] w-full">
              PLAAD inc.<br />
              contact@galddae.com<br />
              02.6959.4528
            </div>
            <div className="font-semibold text-[13px] leading-[18px] text-[#999999]">
              &copy; 2025 plaad inc.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
