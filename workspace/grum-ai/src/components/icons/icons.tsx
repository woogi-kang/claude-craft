"use client";

import Image from "next/image";

interface IconProps {
  className?: string;
  size?: number;
}

export function Icon3DChat({ className, size = 20 }: IconProps) {
  return (
    <div className={className}>
      <Image
        src="/images/3d-chat.png"
        alt="Chat"
        width={size}
        height={size}
        className="object-contain"
      />
    </div>
  );
}

export function Icon3DFood({ className, size = 20 }: IconProps) {
  return (
    <div className={className}>
      <Image
        src="/images/3d-food.png"
        alt="Food"
        width={size}
        height={size}
        className="object-contain"
      />
    </div>
  );
}

export function Icon3DProfile({ className, size = 20 }: IconProps) {
  return (
    <div className={className}>
      <Image
        src="/images/3d-profile.png"
        alt="Profile"
        width={size}
        height={size}
        className="object-contain"
      />
    </div>
  );
}

export function Icon3DMenu({ className, size = 20 }: IconProps) {
  return (
    <div className={className}>
      <Image
        src="/images/3d-menu.png"
        alt="Menu"
        width={size}
        height={size}
        className="object-contain"
      />
    </div>
  );
}

export function Icon3DSetting({ className, size = 20 }: IconProps) {
  return (
    <div className={className}>
      <Image
        src="/images/3d-setting.png"
        alt="Setting"
        width={size}
        height={size}
        className="object-contain"
      />
    </div>
  );
}

export function IconArrowDown({ className, size = 20 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M5 7.5L10 12.5L15 7.5"
        stroke="#65788E"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconArrowRight({ className, size = 20 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 9 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M1 1L8 8L1 15"
        stroke="#B5BFCD"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconMenu({ className, size = 24 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 19 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M1.5 1.5H17.5M1.5 10H17.5M1.5 18.5H17.5"
        stroke="#B5BFCD"
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function IconChat({ className, size = 24 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path d="M14.5 12C15.327 12 16 11.327 16 10.5V1.5C16 0.673 15.327 0 14.5 0H1.5C0.673 0 0 0.673 0 1.5V15C0 15.412 0.470396 15.6472 0.800012 15.4L5.333 12H14.5Z" fill="#B5BFCD"/>
      <path d="M18.5 6H18V12.001C18 13.101 17.107 13.994 16.01 14H6V14.5C6 15.327 6.673 16 7.5 16H14.667L19.2 19.4C19.5296 19.6472 20 19.412 20 19V7.5C20 6.673 19.327 6 18.5 6Z" fill="#B5BFCD"/>
    </svg>
  );
}

export function IconUser({ className, size = 24 }: IconProps) {
  return (
    <div
      className={`flex items-center justify-center rounded-full bg-[#DBE0E7] ${className}`}
      style={{ width: size, height: size }}
    >
      <svg
        width={size * 0.5}
        height={size * 0.52}
        viewBox="0 0 12 12"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fillRule="evenodd"
          clipRule="evenodd"
          d="M8.56683 2.85513C8.56687 3.2301 8.49305 3.60142 8.34959 3.94787C8.20613 4.29432 7.99583 4.60912 7.73071 4.87429C7.46558 5.13947 7.15083 5.34983 6.80441 5.49337C6.45799 5.6369 6.08669 5.71079 5.71171 5.71083C4.95441 5.71091 4.22809 5.41015 3.69254 4.87471C3.15699 4.33927 2.85608 3.61301 2.856 2.85571C2.85596 2.48073 2.92978 2.10942 3.07324 1.76297C3.21671 1.41652 3.427 1.10172 3.69213 0.836538C4.22757 0.300989 4.95382 7.73697e-05 5.71113 1.49177e-08C6.46843 -7.73399e-05 7.19475 0.300686 7.7303 0.836126C8.26584 1.37157 8.56676 2.09782 8.56683 2.85513M5.71142 6.58437C1.5995 6.58437 0 9.20121 0 10.4186C0 11.6355 3.40492 11.9598 5.71142 11.9598C8.01792 11.9598 11.4228 11.6355 11.4228 10.4186C11.4228 9.20121 9.82333 6.58437 5.71142 6.58437Z"
          fill="white"
        />
      </svg>
    </div>
  );
}

export function IconCloseBlue({ className, size = 16 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M12 4L4 12M4 4L12 12"
        stroke="#017AFF"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconCloseGray({ className, size = 16 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M12 4L4 12M4 4L12 12"
        stroke="#B5BFCD"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconPlus({ className, size = 16 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M8 3V13M3 8H13"
        stroke="#65788E"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconSecret({ className, size = 16 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect x="3" y="7" width="10" height="7" rx="1" stroke="#017AFF" strokeWidth="1.5" />
      <path
        d="M5 7V5C5 3.34315 6.34315 2 8 2C9.65685 2 11 3.34315 11 5V7"
        stroke="#017AFF"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function IconSearch({ className, size = 16 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle cx="7" cy="7" r="4.5" stroke="#65788E" strokeWidth="1.5" />
      <path d="M10.5 10.5L14 14" stroke="#65788E" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

export function IconMic({ className, size = 16 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect x="5" y="1" width="6" height="9" rx="3" stroke="#65788E" strokeWidth="1.5" />
      <path d="M3 7V8C3 10.7614 5.23858 13 8 13C10.7614 13 13 10.7614 13 8V7" stroke="#65788E" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M8 13V15" stroke="#65788E" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

export function IconPhoto({ className, size = 40 }: IconProps) {
  return (
    <div
      className={`flex items-center justify-center rounded-full bg-[#F0F0F6] ${className}`}
      style={{ width: size, height: size }}
    >
      <svg
        width={size * 0.525}
        height={size * 0.475}
        viewBox="0 0 21 19"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M0 4.42857C0 3.78447 0.263392 3.16676 0.732233 2.71131C1.20107 2.25587 1.83696 2 2.5 2H17.5C18.163 2 18.7989 2.25587 19.2678 2.71131C19.7366 3.16676 20 3.78447 20 4.42857V16.5714C20 17.2155 19.7366 17.8332 19.2678 18.2887C18.7989 18.7441 18.163 19 17.5 19H2.5C1.83696 19 1.20107 18.7441 0.732233 18.2887C0.263392 17.8332 0 17.2155 0 16.5714V4.42857ZM1.25 15.3571V16.5714C1.25 16.8935 1.3817 17.2023 1.61612 17.4301C1.85054 17.6578 2.16848 17.7857 2.5 17.7857H17.5C17.8315 17.7857 18.1495 17.6578 18.3839 17.4301C18.6183 17.2023 18.75 16.8935 18.75 16.5714V12.3214L14.0288 9.95721C13.9115 9.90017 13.7788 9.88038 13.6494 9.90065C13.5199 9.92092 13.4003 9.98021 13.3075 10.0701L8.67 14.5751L5.345 12.4234C5.22495 12.3458 5.08095 12.3109 4.93742 12.3246C4.79389 12.3383 4.65967 12.3998 4.5575 12.4987L1.25 15.3571ZM7.5 7.46429C7.5 6.98121 7.30246 6.51792 6.95083 6.17634C6.59919 5.83476 6.12228 5.64286 5.625 5.64286C5.12772 5.64286 4.65081 5.83476 4.29917 6.17634C3.94754 6.51792 3.75 6.98121 3.75 7.46429C3.75 7.94736 3.94754 8.41065 4.29917 8.75223C4.65081 9.09381 5.12772 9.28571 5.625 9.28571C6.12228 9.28571 6.59919 9.09381 6.95083 8.75223C7.30246 8.41065 7.5 7.94736 7.5 7.46429Z" fill="#DBE0E7"/>
        <path d="M21 4C21 6.20914 19.2091 8 17 8C14.7909 8 13 6.20914 13 4C13 1.79086 14.7909 0 17 0C19.2091 0 21 1.79086 21 4Z" fill="#017AFF"/>
        <path d="M19 3.5C19.2761 3.5 19.5 3.72386 19.5 4C19.5 4.27614 19.2761 4.5 19 4.5H15C14.7239 4.5 14.5 4.27614 14.5 4C14.5 3.72386 14.7239 3.5 15 3.5H19Z" fill="white"/>
        <path d="M17.5 6C17.5 6.27614 17.2761 6.5 17 6.5C16.7239 6.5 16.5 6.27614 16.5 6V2C16.5 1.72386 16.7239 1.5 17 1.5C17.2761 1.5 17.5 1.72386 17.5 2V6Z" fill="white"/>
      </svg>
    </div>
  );
}

export function IconSend({ className, size = 40, active = false }: IconProps & { active?: boolean }) {
  return (
    <div
      className={`flex items-center justify-center rounded-full ${active ? 'bg-[#017AFF]' : 'bg-[#F0F0F6]'} ${className}`}
      style={{ width: size, height: size }}
    >
      <svg
        width={size * 0.5}
        height={size * 0.5}
        viewBox="0 0 21 21"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M20.3722 0.219017C20.4794 0.32632 20.5515 0.463614 20.5791 0.612779C20.6067 0.761944 20.5884 0.915966 20.5267 1.05452L12.0412 20.1465C11.9819 20.28 11.8849 20.3933 11.7621 20.4725C11.6393 20.5517 11.4961 20.5932 11.35 20.5921C11.2039 20.591 11.0613 20.5473 10.9397 20.4662C10.8182 20.3852 10.7229 20.2704 10.6657 20.136L7.60416 12.987L0.453656 9.92402C0.319744 9.86642 0.205519 9.77104 0.124953 9.64955C0.0443864 9.52806 0.000970933 9.38573 1.60955e-05 9.23996C-0.000938742 9.09419 0.0406085 8.9513 0.119576 8.82876C0.198544 8.70623 0.31151 8.60937 0.444656 8.55002L19.5367 0.0645175C19.675 0.00308931 19.8287 -0.0150281 19.9776 0.0125477C20.1265 0.0401236 20.2635 0.112101 20.3707 0.219017H20.3722Z"
          fill={active ? 'white' : '#DBE0E7'}
        />
      </svg>
    </div>
  );
}

export function IconExternal({ className, size = 20 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M15 10.8333V15.8333C15 16.2754 14.8244 16.6993 14.5118 17.0118C14.1993 17.3244 13.7754 17.5 13.3333 17.5H4.16667C3.72464 17.5 3.30072 17.3244 2.98816 17.0118C2.67559 16.6993 2.5 16.2754 2.5 15.8333V6.66667C2.5 6.22464 2.67559 5.80072 2.98816 5.48816C3.30072 5.17559 3.72464 5 4.16667 5H9.16667"
        stroke="#65788E"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M12.5 2.5H17.5V7.5"
        stroke="#65788E"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M8.33333 11.6667L17.5 2.5"
        stroke="#65788E"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconCopy({ className, size = 16 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect x="5" y="5" width="9" height="9" rx="1.5" stroke="#65788E" strokeWidth="1.5" />
      <path
        d="M11 2H3.5C2.67157 2 2 2.67157 2 3.5V11"
        stroke="#65788E"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function IconShare({ className, size = 16 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 18 17"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M1 8.5V14.5C1 15.0523 1.44772 15.5 2 15.5H16C16.5523 15.5 17 15.0523 17 14.5V8.5"
        stroke="#65788E"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M9 1V10.5M9 1L5 5M9 1L13 5"
        stroke="#65788E"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconCloseCircle({ className, size = 20 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle cx="10" cy="10" r="8" fill="#B5BFCD" />
      <path
        d="M7 7L13 13M13 7L7 13"
        stroke="white"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconArrowRightGray({ className, size = 20 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M7.5 5L12.5 10L7.5 15"
        stroke="#B5BFCD"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function IconLogoBlue({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      width="26"
      height="26"
      viewBox="0 0 26 26"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M13.8584 13.3301V25.6701C16.2384 25.6701 18.5674 24.9693 20.5549 23.6536C22.5425 22.3379 24.1021 20.4656 25.0429 18.2676C25.9836 16.0696 26.2657 13.6401 25.8536 11.2878C25.4415 8.93553 24.3537 6.76102 22.7212 5.03008L13.8584 13.3301Z"
        fill="#017AFF"
      />
      <path
        d="M0 11.6343C0 14.8082 1.20535 17.8523 3.35112 20.1031C5.49689 22.354 8.40068 23.6191 11.4286 23.6191V11.6343H0Z"
        fill="#017AFF"
      />
    </svg>
  );
}

export function IconExclamationCircle({ className, size = 20, variant = "gray" }: IconProps & { variant?: "gray" | "blue" }) {
  const fillColor = variant === "blue" ? "#017AFF" : "#B5BFCD";
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle cx="10" cy="10" r="9" fill={fillColor} />
      <path
        d="M10 5.5V11"
        stroke="white"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <circle cx="10" cy="14" r="1" fill="white" />
    </svg>
  );
}

export function IconArrowRightBlue({ className, size = 20 }: IconProps) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M7.5 5L12.5 10L7.5 15"
        stroke="#017AFF"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
