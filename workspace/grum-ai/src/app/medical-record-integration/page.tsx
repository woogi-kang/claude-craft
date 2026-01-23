"use client";

import Image from "next/image";
import { useState } from "react";
import {
  IconArrowDownBlue,
  IconCloseCircle,
} from "@/components/icons/icons";

type AuthProvider = "toss" | "kakao" | "pass";

interface AuthProviderCardProps {
  provider: AuthProvider;
  selected: boolean;
  onSelect: () => void;
}

function AuthProviderCard({ provider, selected, onSelect }: AuthProviderCardProps) {
  const providerData = {
    toss: { icon: "/images/toss-icon.png", label: "토스" },
    kakao: { icon: "/images/kakao-icon.png", label: "카카오" },
    pass: { icon: "/images/pass-icon.png", label: "패스" },
  };

  const { icon, label } = providerData[provider];

  return (
    <button
      type="button"
      onClick={onSelect}
      className={`flex w-[103.667px] flex-1 flex-col items-center justify-center gap-1 rounded-xl border p-3 ${
        selected
          ? "border-grum-blue"
          : "border-line-gray"
      }`}
    >
      <div
        className={`relative size-11 rounded-xl ${
          selected ? "shadow-[0px_4px_10px_0px_rgba(1,122,255,0.2)]" : ""
        }`}
      >
        <Image
          src={icon}
          alt={label}
          fill
          className="rounded-xl object-cover"
        />
      </div>
      <span
        className={`text-[15px] leading-[23px] ${
          selected
            ? "font-semibold text-grum-blue"
            : "font-normal text-text-black"
        }`}
      >
        {label}
      </span>
    </button>
  );
}

interface InputFieldProps {
  label: string;
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
}

function InputField({ label, placeholder, value, onChange }: InputFieldProps) {
  return (
    <div className="flex w-full flex-col items-center justify-center gap-2.5">
      <div className="flex w-full flex-col items-start justify-center">
        <p className="w-full text-base font-semibold leading-[22px] text-text-black">
          {label}
        </p>
      </div>
      <div className="flex h-[52px] w-full items-center overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5">
        <input
          type="text"
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="flex-1 bg-transparent text-[15px] font-normal leading-[23px] text-text-black placeholder:text-text-gray focus:outline-none"
        />
      </div>
    </div>
  );
}

export default function MedicalRecordIntegrationPage() {
  const [name, setName] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [ssnBack, setSsnBack] = useState("");
  const [carrier, setCarrier] = useState("KT");
  const [phone, setPhone] = useState("010-3456-7890");
  const [selectedProvider, setSelectedProvider] = useState<AuthProvider>("toss");

  return (
    <div className="flex size-full flex-col items-center">
      <div className="flex w-[780px] min-w-0 flex-1 flex-col gap-9 py-10">
        {/* Header Section */}
        <div className="flex w-full gap-2.5 border-b border-line-gray-light pb-10">
          <div className="flex flex-1 flex-col gap-2.5">
            <p className="text-[22px] font-semibold leading-[34px] tracking-[-0.44px] text-grum-blue">
              의료 기록 연동
            </p>
            <p className="text-[34px] font-bold leading-[46px] tracking-[-0.68px] text-text-black">
              의료 기록을 연동해보세요!
            </p>
            <div className="text-base font-normal leading-[23px] tracking-[-0.32px] text-text-black-50">
              <p>
                심사평가원, 건강보험공단에서 의료기록을 연동하면, 내 증상에 딱
                맞는 자세한 상담을 해드릴게요.
              </p>
              <p>(연동하지 않으셔도 서비스 이용이 가능합니다.)</p>
            </div>
          </div>
        </div>

        {/* Content Section */}
        <div className="flex w-full flex-col items-start">
          <div className="flex w-full items-start justify-center gap-10">
            {/* Left Body */}
            <div className="flex w-[280px] flex-col items-start self-stretch">
              <div className="flex w-[280px] flex-col items-start gap-5">
                <div className="flex h-[164.816px] w-full items-center justify-center">
                  <div className="flex w-full flex-col items-start justify-center">
                    <div className="flex w-full flex-col items-start gap-2">
                      <p className="w-full text-[22px] font-bold leading-[34px] text-text-black">
                        의료 기록 연동
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Body - Form */}
            <div className="flex flex-1 flex-col items-start gap-7">
              {/* Name Input */}
              <InputField
                label="이름"
                placeholder="이름을 입력해주세요."
                value={name}
                onChange={setName}
              />

              {/* Resident Registration Number */}
              <div className="flex w-full flex-col items-center justify-center gap-2.5">
                <p className="w-full text-base font-semibold leading-[22px] text-text-black">
                  주민등록번호
                </p>
                <div className="flex h-[52px] w-full items-center justify-center gap-[15px]">
                  <div className="flex h-full flex-1 items-center overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5">
                    <input
                      type="text"
                      placeholder="생년월일 6자리"
                      value={birthDate}
                      onChange={(e) => setBirthDate(e.target.value)}
                      maxLength={6}
                      className="flex-1 bg-transparent text-[15px] font-normal leading-[23px] text-text-black placeholder:text-text-gray focus:outline-none"
                    />
                  </div>
                  <div className="h-0.5 w-2.5 bg-[#D9D9D9]" />
                  <div className="flex h-full flex-1 items-center overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5">
                    <input
                      type="password"
                      placeholder="●●●●●●●"
                      value={ssnBack}
                      onChange={(e) => setSsnBack(e.target.value)}
                      maxLength={7}
                      className="flex-1 bg-transparent text-[15px] font-normal leading-[22px] tracking-[1.5px] text-text-black placeholder:text-text-gray focus:outline-none"
                    />
                  </div>
                </div>
              </div>

              {/* Contact */}
              <div className="flex w-full flex-col items-center justify-center gap-2.5">
                <p className="w-full text-base font-semibold leading-[22px] text-text-black">
                  연락처
                </p>
                <div className="flex h-[52px] w-full items-center gap-2.5">
                  {/* Carrier Dropdown */}
                  <div className="flex h-[52px] w-[100px] items-center overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5">
                    <div className="flex flex-1 items-center gap-2.5">
                      <span className="flex-1 text-[15px] font-normal leading-[23px] text-text-black">
                        {carrier}
                      </span>
                      <IconArrowDownBlue size={20} />
                    </div>
                  </div>

                  {/* Phone Number Input */}
                  <div className="flex h-[52px] flex-1 items-center gap-2.5 overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5">
                    <input
                      type="tel"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      className="flex-1 bg-transparent text-[15px] font-normal leading-[23px] text-text-black focus:outline-none"
                    />
                    <button
                      type="button"
                      onClick={() => setPhone("")}
                      className="shrink-0"
                    >
                      <IconCloseCircle size={20} />
                    </button>
                  </div>
                </div>
              </div>

              {/* Simple Authentication */}
              <div className="flex w-full flex-col items-start gap-2.5">
                <p className="w-full text-base font-semibold leading-[22px] text-text-black">
                  간편 인증
                </p>
                <div className="flex w-full items-center justify-center gap-6">
                  <AuthProviderCard
                    provider="toss"
                    selected={selectedProvider === "toss"}
                    onSelect={() => setSelectedProvider("toss")}
                  />
                  <AuthProviderCard
                    provider="kakao"
                    selected={selectedProvider === "kakao"}
                    onSelect={() => setSelectedProvider("kakao")}
                  />
                  <AuthProviderCard
                    provider="pass"
                    selected={selectedProvider === "pass"}
                    onSelect={() => setSelectedProvider("pass")}
                  />
                </div>
              </div>

              {/* Connect Button */}
              <button
                type="button"
                className="flex h-[50px] w-full items-center justify-center overflow-hidden rounded-[10px] bg-grum-blue px-5"
              >
                <span className="text-base font-semibold leading-[22px] text-white">
                  연동하기
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
