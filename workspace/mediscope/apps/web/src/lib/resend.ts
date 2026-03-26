import { Resend } from "resend";

export const resend = new Resend(process.env.RESEND_API_KEY);

interface SendReportEmailParams {
  to: string;
  name: string;
  hospitalName: string;
  auditUrl: string;
  totalScore: number;
  grade: string;
  reportUrl: string;
}

export async function sendReportEmail({
  to,
  name,
  hospitalName,
  auditUrl,
  totalScore,
  grade,
  reportUrl,
}: SendReportEmailParams) {
  return resend.emails.send({
    from: "CheckYourHospital <noreply@checkyourhospital.com>",
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

        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 32px 0;" />

        <p style="color: #6b7280; font-size: 14px;">
          문의: contact@checkyourhospital.com<br/>
          © 2026 CheckYourHospital. All rights reserved.
        </p>
      </div>
    `,
  });
}

export async function sendFollowUpEmail({
  to,
  name,
  hospitalName,
  totalScore,
}: {
  to: string;
  name: string;
  hospitalName: string;
  totalScore: number;
}) {
  return resend.emails.send({
    from: "CheckYourHospital <noreply@checkyourhospital.com>",
    to,
    subject: `[CheckYourHospital] ${hospitalName} 개선 방안을 알려드립니다`,
    html: `
      <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 600px; margin: 0 auto; padding: 40px 20px;">
        <h1 style="color: #2563eb; margin-bottom: 8px;">CheckYourHospital</h1>

        <p>${name}님, 안녕하세요.</p>
        <p>진단 리포트는 확인하셨나요?</p>
        <p><strong>${hospitalName}</strong>의 현재 점수는 <strong>${totalScore}점</strong>입니다.
        동일 진료과 상위 병원들의 평균 점수는 75점으로, 개선의 여지가 있습니다.</p>

        <p><strong>무료 30분 상담</strong>을 통해 구체적인 개선 방안을 안내해드리겠습니다.</p>

        <a href="https://checkyourhospital.com" style="display: block; background: #2563eb; color: white; text-align: center; padding: 14px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; margin: 24px 0;">
          무료 상담 예약하기
        </a>

        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 32px 0;" />
        <p style="color: #6b7280; font-size: 14px;">© 2026 CheckYourHospital</p>
      </div>
    `,
  });
}
