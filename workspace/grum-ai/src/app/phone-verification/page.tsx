"use client";

import Image from "next/image";
import { useState } from "react";

interface InputFieldProps {
  label: string;
  placeholder: string;
  value?: string;
  onChange?: (value: string) => void;
  showClear?: boolean;
  onClear?: () => void;
}

function InputField({
  label,
  placeholder,
  value = "",
  onChange,
  showClear = false,
  onClear,
}: InputFieldProps) {
  return (
    <div className="flex w-full flex-col items-center justify-center gap-2.5">
      <div className="flex w-full flex-col items-start justify-center">
        <p className="w-full text-base font-semibold leading-[22px] text-text-black">
          {label}
        </p>
      </div>
      <div className="flex h-[52px] w-full items-center overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5">
        <div className="flex flex-1 items-center">
          <input
            type="text"
            placeholder={placeholder}
            value={value}
            onChange={(e) => onChange?.(e.target.value)}
            className="flex-1 bg-transparent text-[15px] leading-[23px] text-text-black placeholder:text-text-gray focus:outline-none"
          />
          {showClear && value && (
            <button onClick={onClear} className="ml-2.5 shrink-0">
              <Image
                src="/icons/icon-close-circle-gray-fill.svg"
                alt="Clear"
                width={20}
                height={20}
              />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

interface ResidentNumberInputProps {
  birthDate: string;
  onBirthDateChange: (value: string) => void;
  genderDigit: string;
  onGenderDigitChange: (value: string) => void;
}

function ResidentNumberInput({
  birthDate,
  onBirthDateChange,
  genderDigit,
  onGenderDigitChange,
}: ResidentNumberInputProps) {
  return (
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
            onChange={(e) => onBirthDateChange(e.target.value)}
            maxLength={6}
            className="flex-1 bg-transparent text-[15px] leading-[23px] text-text-black placeholder:text-text-gray focus:outline-none"
          />
        </div>
        <div className="h-0.5 w-2.5 shrink-0 bg-[#d9d9d9]" />
        <div className="relative flex h-full flex-1 items-center overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5">
          <input
            type="password"
            value={genderDigit}
            onChange={(e) => onGenderDigitChange(e.target.value)}
            maxLength={7}
            className="relative z-10 flex-1 bg-transparent text-[15px] leading-[22px] tracking-[1.5px] text-text-black focus:outline-none"
          />
          {!genderDigit && (
            <span className="pointer-events-none absolute left-3.5 text-[15px] leading-[22px] tracking-[1.5px] text-text-gray">
              ●●●●●●●
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

interface PhoneInputProps {
  carrier: string;
  onCarrierChange: (value: string) => void;
  phoneNumber: string;
  onPhoneNumberChange: (value: string) => void;
  onClear: () => void;
}

function PhoneInput({
  carrier,
  onCarrierChange,
  phoneNumber,
  onPhoneNumberChange,
  onClear,
}: PhoneInputProps) {
  const [showCarrierDropdown, setShowCarrierDropdown] = useState(false);
  const carriers = ["SKT", "KT", "LG U+", "SKT 알뜰폰", "KT 알뜰폰", "LG U+ 알뜰폰"];

  return (
    <div className="flex w-full flex-col items-center justify-center gap-2.5">
      <p className="w-full text-base font-semibold leading-[22px] text-text-black">
        연락처
      </p>
      <div className="flex h-[52px] w-full items-center gap-2.5">
        {/* Carrier Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowCarrierDropdown(!showCarrierDropdown)}
            className="flex h-[52px] w-[100px] items-center overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5"
          >
            <div className="flex flex-1 items-center gap-2.5">
              <span className="flex-1 text-left text-[15px] leading-[23px] text-text-black">
                {carrier}
              </span>
              <Image
                src="/icons/icon-arrow-down-blue.svg"
                alt="Dropdown"
                width={20}
                height={20}
              />
            </div>
          </button>
          {showCarrierDropdown && (
            <div className="absolute left-0 top-full z-10 mt-1 w-[140px] rounded-[10px] border border-line-gray bg-white py-2 shadow-lg">
              {carriers.map((c) => (
                <button
                  key={c}
                  onClick={() => {
                    onCarrierChange(c);
                    setShowCarrierDropdown(false);
                  }}
                  className="w-full px-3.5 py-2 text-left text-[15px] leading-[23px] text-text-black hover:bg-button-gray"
                >
                  {c}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Phone Number Input */}
        <div className="flex h-[52px] flex-1 items-center gap-2.5 overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5">
          <input
            type="tel"
            placeholder="010-0000-0000"
            value={phoneNumber}
            onChange={(e) => onPhoneNumberChange(e.target.value)}
            className="flex-1 bg-transparent text-[15px] leading-[23px] text-text-black placeholder:text-text-gray focus:outline-none"
          />
          {phoneNumber && (
            <button onClick={onClear} className="shrink-0">
              <Image
                src="/icons/icon-close-circle-gray-fill.svg"
                alt="Clear"
                width={20}
                height={20}
              />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

interface VerificationCodeInputProps {
  code: string;
  onCodeChange: (value: string) => void;
  timeRemaining: string;
  onResend: () => void;
}

function VerificationCodeInput({
  code,
  onCodeChange,
  timeRemaining,
  onResend,
}: VerificationCodeInputProps) {
  return (
    <div className="flex w-full flex-col items-center justify-center gap-2.5">
      <p className="w-full text-base font-semibold leading-[22px] text-text-black">
        인증번호
      </p>
      <div className="flex h-[52px] w-full items-center gap-2.5">
        <div className="flex h-full flex-1 items-center overflow-hidden rounded-[10px] border border-line-gray bg-button-gray px-3.5">
          <div className="flex flex-1 items-center gap-2.5">
            <input
              type="text"
              placeholder="인증번호 6자리"
              value={code}
              onChange={(e) => onCodeChange(e.target.value)}
              maxLength={6}
              className="flex-1 bg-transparent text-[15px] leading-[23px] text-text-black placeholder:text-text-gray focus:outline-none"
            />
            <span className="w-10 shrink-0 text-center text-[13px] leading-[18px] text-[#FF2B64]">
              {timeRemaining}
            </span>
          </div>
        </div>
        <button
          onClick={onResend}
          className="flex h-full w-[100px] items-center justify-center overflow-hidden rounded-[10px] bg-grum-blue px-3.5"
        >
          <span className="text-[15px] font-semibold leading-[23px] text-white">
            재전송
          </span>
        </button>
      </div>
    </div>
  );
}

interface PrimaryButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
}

function PrimaryButton({ children, onClick }: PrimaryButtonProps) {
  return (
    <button
      onClick={onClick}
      className="relative flex h-[52px] w-full items-center justify-center overflow-hidden rounded-[10px] bg-grum-blue px-5"
    >
      <span className="text-base font-semibold leading-[22px] text-white">
        {children}
      </span>
    </button>
  );
}

interface FormSectionProps {
  label: string;
  title: string;
  children: React.ReactNode;
}

function FormSection({ label, title, children }: FormSectionProps) {
  return (
    <div className="flex w-full items-start justify-center gap-10">
      {/* Left Label */}
      <div className="flex w-[280px] shrink-0 flex-col items-start">
        <div className="flex w-[280px] flex-col items-start gap-5">
          <div className="flex w-full items-center justify-center">
            <div className="flex w-full flex-col items-start justify-center">
              <div className="flex w-full flex-col items-start gap-2">
                <p className="w-full text-base font-semibold leading-[22px] text-grum-blue">
                  {label}
                </p>
                <p className="w-full text-[22px] font-bold leading-[34px] text-text-black">
                  {title}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Content */}
      <div className="flex min-w-0 flex-1 flex-col items-start gap-7">
        {children}
      </div>
    </div>
  );
}

export default function PhoneVerificationPage() {
  // Form state
  const [name, setName] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [genderDigit, setGenderDigit] = useState("");
  const [carrier, setCarrier] = useState("KT");
  const [phoneNumber, setPhoneNumber] = useState("010-3456-7890");
  const [verificationCode, setVerificationCode] = useState("");
  const [timeRemaining] = useState("02:59");

  return (
    <div className="flex size-full flex-col items-center">
      <div className="flex w-[780px] shrink-0 flex-col items-center gap-8 py-10">
        {/* Header Section */}
        <div className="flex h-[163px] w-full items-start gap-2.5 border-b border-line-gray-light pb-10">
          <div className="flex w-[692px] flex-col items-start gap-2.5">
            <p className="w-full text-[22px] font-semibold leading-[34px] tracking-[-0.44px] text-grum-blue">
              회원가입
            </p>
            <p className="w-full text-[34px] font-bold leading-[46px] tracking-[-0.68px] text-text-black">
              그럼AI가 처음이에요.
            </p>
            <p className="w-full text-base font-normal leading-[23px] tracking-[-0.32px] text-text-black-50">
              병원갈때AI에 가입했었다면, 그럼AI도 회원가입 없이 이용할 수 있어요!
            </p>
          </div>
        </div>

        {/* Form Sections */}
        <div className="flex w-full flex-col items-start gap-7">
          {/* Section 1: Identity Verification - Information Input */}
          <div className="flex w-full items-start justify-center py-3">
            <FormSection label="본인인증" title="정보를 입력해주세요.">
              <InputField
                label="이름"
                placeholder="이름을 입력해주세요."
                value={name}
                onChange={setName}
              />
              <ResidentNumberInput
                birthDate={birthDate}
                onBirthDateChange={setBirthDate}
                genderDigit={genderDigit}
                onGenderDigitChange={setGenderDigit}
              />
              <PhoneInput
                carrier={carrier}
                onCarrierChange={setCarrier}
                phoneNumber={phoneNumber}
                onPhoneNumberChange={setPhoneNumber}
                onClear={() => setPhoneNumber("")}
              />
              <PrimaryButton>본인 인증하기</PrimaryButton>
            </FormSection>
          </div>

          {/* Section 2: Identity Verification - Verification Code */}
          <FormSection label="본인인증" title="인증번호를 입력해주세요.">
            <VerificationCodeInput
              code={verificationCode}
              onCodeChange={setVerificationCode}
              timeRemaining={timeRemaining}
              onResend={() => console.log("Resend verification code")}
            />
            <PrimaryButton>인증 완료</PrimaryButton>
          </FormSection>

          {/* Section 3: Terms Agreement */}
          <FormSection label="약관동의" title="약관에 동의해주세요.">
            <div className="h-[440px] w-full" />
          </FormSection>
        </div>
      </div>
    </div>
  );
}
