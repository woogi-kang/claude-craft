"use client";

import Image from "next/image";
import { useState } from "react";
import {
  IconQuestionCircle,
  IconCheckCircleGray,
} from "@/components/icons/icons";

interface CheckboxRowProps {
  label: string;
  checked: boolean;
  onChange: () => void;
}

function CheckboxRow({ label, checked, onChange }: CheckboxRowProps) {
  return (
    <button
      type="button"
      onClick={onChange}
      className="flex h-10 w-[460px] items-center gap-2.5 rounded-lg"
    >
      <IconQuestionCircle size={20} variant="gray" />
      <span className="flex-1 text-left text-[15px] font-normal leading-[23px] text-text-black">
        {label}
      </span>
      <IconCheckCircleGray size={20} checked={checked} />
    </button>
  );
}

export default function MedicalRecordIntegrationPage() {
  const [excludeSensitive, setExcludeSensitive] = useState(true);

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
              <div className="flex w-[280px] flex-col gap-5 items-start">
                <div className="flex h-[164.816px] w-full items-center justify-center">
                  <div className="flex w-full flex-col items-start justify-center">
                    <div className="flex w-full flex-col gap-2 items-start">
                      <p className="w-full text-[22px] font-bold leading-[34px] text-text-black">
                        의료 기록 연동
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Body */}
            <div className="flex flex-1 flex-col gap-6 items-start">
              {/* 3D Image + Description */}
              <div className="flex w-full flex-col gap-6 items-center justify-center overflow-hidden">
                {/* 3D Image */}
                <div className="flex w-full items-center justify-center overflow-hidden">
                  <div className="relative h-[126px] w-[120px]">
                    <Image
                      src="/images/3d-medical-record.png"
                      alt="Medical Record"
                      fill
                      className="object-cover"
                    />
                  </div>
                </div>

                {/* Description Text */}
                <div className="w-full text-center text-base font-semibold leading-[22px] text-text-black opacity-80">
                  <p>심사평가원, 건강보험공단에서 사용자의 의료기록을 연동하면</p>
                  <p>더 자세한 상담이 가능합니다.</p>
                  <p>(연동하지 않으셔도 서비스 이용이 가능합니다.)</p>
                </div>

                {/* Info Box */}
                <div className="flex w-full flex-col items-center justify-center overflow-hidden rounded-[10px] bg-button-gray p-3.5">
                  <p className="w-full text-center text-[15px] font-normal leading-[23px] text-text-black">
                    심사평가원, 건강보험공단에서 각 한 번씩
                    <br />총 2번의 정보를 연동해야 해요!
                  </p>
                </div>
              </div>

              {/* Checkbox + Button */}
              <div className="flex flex-col gap-2.5 items-start">
                <CheckboxRow
                  label="민감한 질병 연동 제외하기"
                  checked={excludeSensitive}
                  onChange={() => setExcludeSensitive(!excludeSensitive)}
                />
                <button
                  type="button"
                  className="flex h-[50px] w-[460px] items-center justify-center overflow-hidden rounded-[10px] bg-grum-blue px-5"
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
    </div>
  );
}
