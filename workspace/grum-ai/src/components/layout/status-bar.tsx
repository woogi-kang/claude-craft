"use client";

import Image from "next/image";
import { IconUser, IconArrowRight, IconChat, IconMenu } from "@/components/icons/icons";

export function StatusBar() {
  return (
    <div className="flex h-20 items-center justify-between overflow-hidden px-[30px] bg-white w-full">
      {/* Left - Logo */}
      <div className="flex flex-1 items-center min-h-px min-w-px overflow-hidden">
        <div className="flex gap-5 h-10 items-center w-20">
          <div className="relative flex-1 min-h-px min-w-px aspect-[434/131]">
            <Image
              src="/images/logo-text.png"
              alt="Grum AI"
              fill
              className="object-cover"
            />
          </div>
        </div>
      </div>

      {/* Right - Actions */}
      <div className="flex flex-1 gap-4 items-center justify-end min-h-px min-w-px">
        {/* Login Button */}
        <div className="flex gap-2.5 h-[50px] items-center justify-center overflow-hidden px-2.5 rounded-full bg-[#F5F7FA] shrink-0">
          <IconUser size={24} />
          <div className="flex gap-2.5 h-5 items-center">
            <span className="font-normal text-[15px] leading-[23px] text-[#111111]">
              로그인 해주세요
            </span>
            <IconArrowRight size={20} />
          </div>
        </div>

        {/* Chat Icon */}
        <IconChat size={24} />

        {/* Menu Icon */}
        <IconMenu size={24} />
      </div>
    </div>
  );
}
