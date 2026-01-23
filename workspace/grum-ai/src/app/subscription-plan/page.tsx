"use client";

import { LeftSidebar, StatusBar, ChatHistory } from "@/components/layout";
import { IconExclamationCircle, IconCheckCircleGray } from "@/components/icons/icons";

interface PlanFeatureProps {
  icon: "x10" | "robot";
  text: string;
}

function IconX10({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      width="24"
      height="16"
      viewBox="0 0 24 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect width="24" height="16" rx="4" fill="#00B493" />
      <text
        x="12"
        y="12"
        textAnchor="middle"
        fill="white"
        fontSize="10"
        fontWeight="bold"
        fontFamily="system-ui"
      >
        X10
      </text>
    </svg>
  );
}

function IconRobot({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      width="18"
      height="18"
      viewBox="0 0 18 18"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M9 1V3M3 7H15C15.5523 7 16 7.44772 16 8V15C16 15.5523 15.5523 16 15 16H3C2.44772 16 2 15.5523 2 15V8C2 7.44772 2.44772 7 3 7ZM5.5 11.5C6.05228 11.5 6.5 11.0523 6.5 10.5C6.5 9.94772 6.05228 9.5 5.5 9.5C4.94772 9.5 4.5 9.94772 4.5 10.5C4.5 11.0523 4.94772 11.5 5.5 11.5ZM12.5 11.5C13.0523 11.5 13.5 11.0523 13.5 10.5C13.5 9.94772 13.0523 9.5 12.5 9.5C11.9477 9.5 11.5 9.94772 11.5 10.5C11.5 11.0523 11.9477 11.5 12.5 11.5ZM7 13.5H11"
        stroke="#505050"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M5 7V5C5 4.44772 5.44772 4 6 4H12C12.5523 4 13 4.44772 13 5V7"
        stroke="#505050"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

function PlanFeature({ icon, text }: PlanFeatureProps) {
  return (
    <div className="flex items-center gap-[10px]">
      {icon === "x10" ? (
        <IconX10 />
      ) : (
        <IconRobot />
      )}
      <span className="font-normal text-[14px] leading-[20px] text-[#505050]">
        {text}
      </span>
    </div>
  );
}

interface SubscriptionPlanCardProps {
  name: string;
  period: string;
  originalPrice: string;
  discountedPrice: string;
  features: PlanFeatureProps[];
  isSelected: boolean;
  onSelect: () => void;
}

function SubscriptionPlanCard({
  name,
  period,
  originalPrice,
  discountedPrice,
  features,
  isSelected,
  onSelect,
}: SubscriptionPlanCardProps) {
  return (
    <button
      onClick={onSelect}
      className={`flex flex-col gap-[20px] p-[24px] rounded-[12px] border-2 w-full text-left transition-colors ${
        isSelected
          ? "border-[#017AFF] bg-white"
          : "border-[#E5E5EC] bg-white hover:border-[#B5BFCD]"
      }`}
    >
      {/* Plan Header */}
      <div className="flex items-center justify-between w-full">
        <div className="flex flex-col gap-[8px]">
          <span className="font-bold text-[18px] leading-[26px] text-[#111111]">
            {name}
          </span>
          <div className="flex items-center gap-[12px]">
            <span className="font-medium text-[15px] leading-[22px] text-[#767676]">
              {period}
            </span>
            <div className="flex items-center gap-[8px]">
              <span className="font-normal text-[15px] leading-[22px] text-[#B5BFCD] line-through">
                {originalPrice}
              </span>
              <span className="font-normal text-[15px] leading-[22px] text-[#767676]">
                →
              </span>
              <span className="font-semibold text-[16px] leading-[22px] text-[#111111]">
                {discountedPrice}
              </span>
            </div>
          </div>
        </div>
        <IconCheckCircleGray size={24} checked={isSelected} />
      </div>

      {/* Divider */}
      <div className="w-full h-px bg-[#F0F0F6]" />

      {/* Features */}
      <div className="flex flex-col gap-[12px]">
        {features.map((feature, index) => (
          <PlanFeature key={index} icon={feature.icon} text={feature.text} />
        ))}
      </div>
    </button>
  );
}

interface SectionRowProps {
  title: string;
  children: React.ReactNode;
}

function SectionRow({ title, children }: SectionRowProps) {
  return (
    <div className="flex gap-[40px] items-start w-full">
      {/* Left Label */}
      <div className="flex flex-col items-start w-[280px] shrink-0">
        <h2 className="font-bold text-[22px] leading-[34px] text-[#111111] tracking-[-0.68px]">
          {title}
        </h2>
      </div>
      {/* Right Content */}
      <div className="flex flex-col flex-1 min-w-0">{children}</div>
    </div>
  );
}

interface StatusBadgeProps {
  label: string;
  rightText?: string;
}

function StatusBadge({ label, rightText }: StatusBadgeProps) {
  return (
    <div className="flex items-center gap-[10px] h-[52px] px-[20px] bg-[#F5F7FA] rounded-[10px] w-full">
      <IconExclamationCircle size={20} variant="blue" />
      <span className="font-semibold text-[15px] leading-[23px] text-[#111111]">
        {label}
      </span>
      <div className="flex-1 flex items-center justify-end">
        {rightText && (
          <span className="font-normal text-[15px] leading-[23px] text-[#767676]">
            {rightText}
          </span>
        )}
      </div>
    </div>
  );
}

function PrimaryButton({ label }: { label: string }) {
  return (
    <button className="flex items-center justify-center h-[50px] px-[20px] bg-[#017AFF] rounded-[10px] w-full hover:bg-[#0066DD] transition-colors">
      <span className="font-semibold text-[16px] leading-[22px] text-white">
        {label}
      </span>
    </button>
  );
}

function SubscriptionPlanContent() {
  const plusFeatures: PlanFeatureProps[] = [
    { icon: "x10", text: "10배 더 많은 하루 이용량" },
    { icon: "robot", text: "더 똑똑한 AI 모델을 사용한 답변" },
  ];

  const premiumFeatures: PlanFeatureProps[] = [
    { icon: "x10", text: "10배 더 많은 하루 이용량" },
    { icon: "robot", text: "더 똑똑한 AI 모델을 사용한 답변" },
  ];

  return (
    <div className="flex flex-col items-center w-full h-full overflow-auto">
      <div className="flex flex-col gap-[36px] items-center py-[40px] w-[780px]">
        {/* Page Header */}
        <div className="flex flex-col gap-[10px] items-start pb-[40px] w-full border-b border-[#F0F0F6]">
          <span className="font-semibold text-[22px] leading-[34px] text-[#017AFF] tracking-[-0.44px]">
            유료 플랜
          </span>
          <h1 className="font-bold text-[34px] leading-[46px] text-[#111111] tracking-[-0.68px]">
            더 나은 답변, 더 많은 이용량
          </h1>
          <p className="font-normal text-[16px] leading-[24px] text-[#767676]">
            커피 한잔 정도의 비용으로 내 건강 챙겨주는 그럼 AI를 충분히 경험 해보세요.
          </p>
        </div>

        {/* Content Sections */}
        <div className="flex flex-col gap-[28px] items-start w-full">
          {/* Subscription Plan Section */}
          <SectionRow title="유료 플랜">
            <div className="flex flex-col gap-[28px] w-full">
              {/* Status Badge */}
              <StatusBadge label="플러스 이용 중" rightText="다음 결제일 : 25.07.11" />

              {/* Plan Cards */}
              <div className="flex flex-col gap-[18px] w-full">
                <SubscriptionPlanCard
                  name="플러스"
                  period="1 개월"
                  originalPrice="8,500"
                  discountedPrice="6,500원"
                  features={plusFeatures}
                  isSelected={true}
                  onSelect={() => {}}
                />

                <SubscriptionPlanCard
                  name="프리미엄"
                  period="1 개월"
                  originalPrice="8,500"
                  discountedPrice="6,500원"
                  features={premiumFeatures}
                  isSelected={false}
                  onSelect={() => {}}
                />
              </div>

              {/* CTA Button */}
              <PrimaryButton label="구독 결제 신청" />
            </div>
          </SectionRow>
        </div>
      </div>
    </div>
  );
}

export default function SubscriptionPlanPage() {
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
          {/* Subscription Plan Content Area - Flexible */}
          <SubscriptionPlanContent />

          {/* Chat History Sidebar - 300px fixed width */}
          <ChatHistory />
        </div>
      </div>
    </div>
  );
}
