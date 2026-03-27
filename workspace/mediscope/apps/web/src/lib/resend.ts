import { Resend } from "resend";

function getResend() {
  return new Resend(process.env.RESEND_API_KEY ?? "");
}

interface SendReportEmailParams {
  to: string;
  name: string;
  hospitalName: string;
  auditUrl: string;
  totalScore: number;
  grade: string;
  reportUrl: string;
  pdfUrl?: string;
}

export async function sendReportEmail({
  to,
  name,
  hospitalName,
  auditUrl,
  totalScore,
  grade,
  reportUrl,
  pdfUrl,
}: SendReportEmailParams) {
  return getResend().emails.send({
    from: "CheckYourHospital <onboarding@resend.dev>",
    to,
    subject: `[CheckYourHospital] ${hospitalName || auditUrl} 진단 리포트 (${totalScore}점 ${grade}등급)`,
    html: `
      <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 600px; margin: 0 auto; padding: 40px 20px;">
        <h1 style="color: #2563eb; margin-bottom: 8px;">CheckYourHospital</h1>
        <p style="color: #6b7280; margin-bottom: 32px;">AI 병원 홈페이지 진단 리포트</p>

        <p>${name}님, 안녕하세요.</p>
        <p><strong>${hospitalName || auditUrl}</strong>의 홈페이지 진단이 완료되었습니다.</p>

        <div style="background: #f8fafc; border-radius: 12px; padding: 24px; margin: 24px 0; text-align: center;">
          <div style="font-size: 48px; font-weight: bold; color: #1e293b;">${totalScore}</div>
          <div style="color: #6b7280;">/100점</div>
          <div style="display: inline-block; margin-top: 8px; padding: 4px 16px; border-radius: 20px; background: ${grade === "A" ? "#dcfce7" : grade === "B" ? "#dbeafe" : grade === "C" ? "#fef9c3" : "#fee2e2"}; color: ${grade === "A" ? "#166534" : grade === "B" ? "#1e40af" : grade === "C" ? "#854d0e" : "#991b1b"}; font-weight: bold;">
            등급: ${grade}
          </div>
        </div>

        <a href="${reportUrl}" style="display: block; background: #2563eb; color: white; text-align: center; padding: 14px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; margin: 24px 0;">
          상세 리포트 보기
        </a>
        ${pdfUrl ? `<a href="${pdfUrl}" style="display: block; background: #16a34a; color: white; text-align: center; padding: 14px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; margin: 0 0 24px 0;">PDF 리포트 다운로드</a>` : ""}

        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 32px 0;" />

        <p style="color: #6b7280; font-size: 14px;">
          문의: contact@checkyourhospital.com<br/>
          © 2026 CheckYourHospital. All rights reserved.
        </p>
      </div>
    `,
  });
}

const FOLLOW_UP_TEMPLATES: Record<
  string,
  {
    subject: (h: string) => string;
    body: (p: {
      name: string;
      hospitalName: string;
      totalScore: number;
    }) => string;
  }
> = {
  followup_1: {
    subject: (h) => `[CheckYourHospital] ${h} 리포트 확인하셨나요?`,
    body: ({ name, hospitalName, totalScore }) => `
      <p>${name}님, 안녕하세요.</p>
      <p>진단 리포트는 확인하셨나요?</p>
      <p><strong>${hospitalName}</strong>의 현재 점수는 <strong>${totalScore}점</strong>입니다.
      동일 진료과 상위 병원들의 평균 점수는 75점으로, 개선의 여지가 있습니다.</p>
      <p><strong>무료 30분 상담</strong>을 통해 구체적인 개선 방안을 안내해드리겠습니다.</p>`,
  },
  followup_2: {
    subject: (h) => `[CheckYourHospital] ${h} 무료 상담을 제안드립니다`,
    body: ({ name, hospitalName, totalScore }) => `
      <p>${name}님, 안녕하세요.</p>
      <p><strong>${hospitalName}</strong>의 홈페이지 진단 점수(${totalScore}점)를 기반으로,
      구체적인 개선 로드맵을 준비했습니다.</p>
      <p>30분 무료 상담에서 다음을 안내해드립니다:</p>
      <ul>
        <li>즉시 개선 가능한 항목 (1주 내)</li>
        <li>중기 개선 계획 (1-3개월)</li>
        <li>예상 ROI 및 비용</li>
      </ul>`,
  },
  followup_3: {
    subject: (h) => `[CheckYourHospital] 경쟁 병원은 이미 시작했습니다`,
    body: ({ name, hospitalName }) => `
      <p>${name}님, 안녕하세요.</p>
      <p><strong>${hospitalName}</strong>과 같은 진료과의 다른 병원들이
      SEO 최적화를 통해 해외 환자 유입을 늘리고 있습니다.</p>
      <p>성공 사례를 공유해드리겠습니다. 지금 상담을 예약해보세요.</p>`,
  },
  rediagnose: {
    subject: (h) => `[CheckYourHospital] ${h} 한 달이 지났습니다`,
    body: ({ name, hospitalName }) => `
      <p>${name}님, 안녕하세요.</p>
      <p><strong>${hospitalName}</strong>의 마지막 진단 후 한 달이 지났습니다.</p>
      <p>검색 엔진의 알고리즘은 지속적으로 변화합니다.
      다시 진단하여 현재 상태를 확인해보세요.</p>`,
  },
};

export async function sendFollowUpEmail({
  to,
  name,
  hospitalName,
  totalScore,
  template = "followup_1",
}: {
  to: string;
  name: string;
  hospitalName: string;
  totalScore: number;
  template?: string;
}) {
  const tmpl = FOLLOW_UP_TEMPLATES[template] ?? FOLLOW_UP_TEMPLATES.followup_1;

  return getResend().emails.send({
    from: "CheckYourHospital <onboarding@resend.dev>",
    to,
    subject: tmpl.subject(hospitalName),
    html: `
      <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 600px; margin: 0 auto; padding: 40px 20px;">
        <h1 style="color: #2563eb; margin-bottom: 8px;">CheckYourHospital</h1>
        ${tmpl.body({ name, hospitalName, totalScore })}
        <a href="${process.env.NEXT_PUBLIC_BASE_URL || process.env.VERCEL_URL || "http://localhost:3000"}" style="display: block; background: #2563eb; color: white; text-align: center; padding: 14px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; margin: 24px 0;">
          무료 상담 예약하기
        </a>
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 32px 0;" />
        <p style="color: #6b7280; font-size: 14px;">© 2026 CheckYourHospital. All rights reserved.</p>
      </div>
    `,
  });
}
