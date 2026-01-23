import Image from "next/image";

interface AuthButtonProps {
  variant: "kakao" | "phone" | "naver";
  type: "signup" | "login";
}

function AuthButton({ variant, type }: AuthButtonProps) {
  const labels = {
    kakao: {
      signup: "카카오 간편 회원가입",
      login: "카카오 간편 로그인",
    },
    phone: {
      signup: "핸드폰 인증 회원가입",
      login: "핸드폰 인증 로그인",
    },
    naver: {
      signup: "네이버 회원가입",
      login: "네이버 로그인",
    },
  };

  const styles = {
    kakao: "bg-[#FFE500] text-text-black",
    phone: "bg-white border border-icon-gray-light text-text-black",
    naver: "bg-[#04C758] text-white",
  };

  const icons = {
    kakao: "/icons/icon-kakao.svg",
    phone: "/icons/icon-phone.svg",
    naver: "/icons/icon-naver.svg",
  };

  return (
    <button
      className={`relative flex h-[52px] w-full items-center rounded-[10px] px-5 ${styles[variant]}`}
    >
      <div className="relative size-6">
        <Image
          src={icons[variant]}
          alt={variant}
          width={24}
          height={24}
          className="size-full object-contain"
          style={{
            filter:
              variant === "kakao"
                ? "none"
                : variant === "phone"
                  ? "brightness(0) saturate(100%) invert(31%) sepia(0%) saturate(1%) hue-rotate(138deg) brightness(95%) contrast(89%)"
                  : "none",
          }}
        />
      </div>
      <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-base font-semibold leading-[22px]">
        {labels[variant][type]}
      </span>
    </button>
  );
}

interface AuthSectionProps {
  title: string;
  children: React.ReactNode;
}

function AuthSection({ title, children }: AuthSectionProps) {
  return (
    <div className="flex w-full flex-col items-start gap-2.5">
      <p className="w-full text-base font-bold leading-[23px] text-text-black">
        {title}
      </p>
      {children}
    </div>
  );
}

export default function SignupPage() {
  return (
    <div className="flex size-full flex-col items-center">
      <div className="flex w-[780px] min-w-0 flex-1 flex-col gap-9 pb-[100px] pt-10">
        {/* Header Section */}
        <div className="flex w-full flex-col items-center justify-center">
          <div className="flex w-full gap-2.5 border-b border-line-gray-light pb-10">
            <div className="flex w-[692px] flex-col gap-2.5">
              <p className="text-[22px] font-semibold leading-[34px] tracking-[-0.44px] text-grum-blue">
                회원가입
              </p>
              <p className="text-[34px] font-bold leading-[46px] tracking-[-0.68px] text-text-black">
                그럼AI가 처음이에요.
              </p>
              <p className="text-base font-normal leading-[23px] tracking-[-0.32px] text-text-black-50">
                병원갈때AI에 가입했었다면, 그럼AI도 회원가입 없이 이용할 수
                있어요!
              </p>
            </div>
          </div>
        </div>

        {/* Auth Buttons Section */}
        <div className="flex w-full flex-col items-start justify-center">
          <div className="flex w-[460px] flex-col items-center justify-center gap-7">
            {/* Sign Up Section */}
            <AuthSection title="회원가입">
              <AuthButton variant="kakao" type="signup" />
              <AuthButton variant="phone" type="signup" />
            </AuthSection>

            {/* Login Section */}
            <AuthSection title="이미 회원가입 했어요.">
              <AuthButton variant="kakao" type="login" />
              <AuthButton variant="phone" type="login" />
              <AuthButton variant="naver" type="login" />
            </AuthSection>
          </div>
        </div>
      </div>
    </div>
  );
}
