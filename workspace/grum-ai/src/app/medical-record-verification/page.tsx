"use client";

import Image from "next/image";

interface FAQBoxProps {
  title: string;
  description: string | React.ReactNode;
}

function FAQBox({ title, description }: FAQBoxProps) {
  return (
    <div className="flex w-full flex-col gap-2 overflow-hidden rounded-[10px] border border-line-gray bg-button-gray p-3.5">
      <p className="w-full text-[15px] font-normal leading-[23px] text-text-black">
        {title}
      </p>
      <div className="w-full text-[15px] font-normal leading-[23px] text-text-black-50">
        {description}
      </div>
    </div>
  );
}

export default function MedicalRecordVerificationPage() {
  return (
    <div className="flex size-full flex-col items-center bg-[#fdfdfd]">
      <div className="flex w-[780px] min-w-0 flex-1 flex-col gap-7 py-10">
        {/* Header Section */}
        <div className="flex w-full gap-2.5 border-b border-line-gray-light pb-10">
          <div className="flex w-[692px] flex-col gap-2.5">
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

        {/* Section 1: KakaoTalk Verification */}
        <div className="flex w-full flex-col items-start">
          <div className="flex w-full items-start justify-center gap-10">
            {/* Left Body */}
            <div className="flex w-[280px] flex-col items-start self-stretch">
              <div className="flex w-[280px] flex-col items-start gap-5">
                <div className="flex h-[164.816px] w-full items-center justify-center">
                  <div className="flex w-full flex-col items-start justify-center">
                    <div className="flex w-full flex-col items-start gap-2">
                      <div className="w-full text-[22px] font-bold leading-[34px] text-text-black">
                        <p>카카오톡으로</p>
                        <p>인증 요청을 보냈어요.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Body - FAQ & Button */}
            <div className="flex flex-1 flex-col items-start gap-3.5">
              {/* FAQ Section */}
              <div className="flex w-full flex-col items-center justify-center gap-3.5">
                {/* FAQ Title */}
                <div className="flex w-full flex-col items-start justify-center">
                  <p className="w-full text-base font-semibold leading-[22px] text-text-black">
                    문제가 생겼나요?
                  </p>
                </div>

                {/* FAQ Boxes */}
                <div className="flex w-full flex-col items-start gap-3.5 text-[15px] font-normal leading-[23px]">
                  <FAQBox
                    title="인증 요청 중 오류가 생겼어요."
                    description="카카오톡, 토스, PASS에 등록된 정보가 본인 정보와 일치하는지 확인해 주세요."
                  />
                  <FAQBox
                    title="인증 요청 메시지(알림)가 오지 않아요."
                    description={
                      <ul className="list-disc">
                        <li className="ms-[22.5px]">
                          카카오톡, 토스, PASS 앱을 설치해주세요.
                        </li>
                        <li className="ms-[22.5px]">
                          앱 알림을 받을 수 있도록 앱 설정 또는 휴대폰 환경 설정을
                          확인해 주세요.
                        </li>
                        <li className="ms-[22.5px]">
                          카카오톡, 토스, PASS 앱이 설치된 다른 휴대폰이 있다면,
                          해당 기기의 알림을 확인해주세요.
                        </li>
                      </ul>
                    }
                  />
                </div>
              </div>

              {/* Primary Button */}
              <button
                type="button"
                className="flex h-[52px] w-full items-center justify-center overflow-hidden rounded-[10px] bg-grum-blue px-5"
              >
                <span className="text-base font-semibold leading-[22px] text-white">
                  간편 인증 완료
                </span>
              </button>

              {/* Retry Link */}
              <div className="flex w-full justify-center">
                <button
                  type="button"
                  className="text-[15px] font-normal leading-[23px] text-text-gray underline decoration-solid"
                >
                  인증 요청 다시 보내기
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Section 2: Toss Verification */}
        <div className="flex w-full flex-col items-start">
          <div className="flex w-full items-start justify-center gap-10">
            {/* Left Body */}
            <div className="flex w-[280px] flex-col items-start self-stretch">
              <div className="flex w-[280px] flex-col items-start gap-5">
                <div className="flex h-[164.816px] w-full items-center justify-center">
                  <div className="flex w-full flex-col items-start justify-center">
                    <div className="flex w-full flex-col items-start gap-2">
                      <p className="w-full text-[22px] font-bold leading-[34px] text-text-black">
                        마지막이에요!
                      </p>
                      <p className="w-full text-[15px] font-normal leading-[23px] text-text-black-50">
                        건강보험공단에서 최근 10년간 국가건강검진 결과를 한번 더
                        연동합니다.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Body - Toss Verification */}
            <div className="flex flex-1 flex-col items-start gap-3.5">
              {/* 3D Image + Description Box */}
              <div className="flex w-full flex-col items-center justify-center gap-6 overflow-hidden">
                {/* Toss Logo */}
                <div className="flex h-[120px] w-full items-center justify-center overflow-hidden">
                  <div className="relative size-[120px]">
                    <Image
                      src="/images/toss-symbol.png"
                      alt="Toss"
                      fill
                      className="object-cover"
                    />
                  </div>
                </div>

                {/* Description Box */}
                <div className="flex w-full flex-col items-center justify-center overflow-hidden rounded-[10px] bg-button-gray p-3.5">
                  <div className="w-full text-center text-[15px] font-normal leading-[23px] text-[#323435]">
                    <p>방금했던 토스 간편인증을</p>
                    <p>한 번 만 더 진행해주세요!</p>
                  </div>
                </div>
              </div>

              {/* Verification Button */}
              <button
                type="button"
                className="flex h-[50px] w-full items-center justify-center overflow-hidden rounded-[10px] bg-grum-blue px-5"
              >
                <span className="text-base font-semibold leading-[22px] text-white">
                  한 번 더 인증요청
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
