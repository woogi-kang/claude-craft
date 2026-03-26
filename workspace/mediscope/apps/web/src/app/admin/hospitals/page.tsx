"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Hospital {
  id: string;
  name: string;
  url: string;
  specialty: string | null;
  region: string | null;
  latest_score: number | null;
  created_at: string;
}

export default function AdminHospitalsPage() {
  const { data: hospitals, isLoading } = useQuery<Hospital[]>({
    queryKey: ["admin-hospitals"],
    queryFn: async () => {
      const res = await fetch("/api/admin/hospitals");
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">병원 관리</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            병원 목록{" "}
            {hospitals && (
              <span className="text-muted-foreground font-normal">
                ({hospitals.length}건)
              </span>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p className="text-muted-foreground">로딩 중...</p>
          ) : !hospitals?.length ? (
            <p className="text-muted-foreground">등록된 병원이 없습니다.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left">
                    <th className="pb-3 pr-4 font-medium">병원명</th>
                    <th className="pb-3 pr-4 font-medium">URL</th>
                    <th className="pb-3 pr-4 font-medium">전문분야</th>
                    <th className="pb-3 pr-4 font-medium">지역</th>
                    <th className="pb-3 pr-4 font-medium">점수</th>
                    <th className="pb-3 font-medium">등록일</th>
                  </tr>
                </thead>
                <tbody>
                  {hospitals.map((hospital) => (
                    <tr key={hospital.id} className="border-b last:border-0">
                      <td className="py-3 pr-4">
                        <Link
                          href={`/admin/hospitals/${hospital.id}`}
                          className="font-medium text-primary hover:underline"
                        >
                          {hospital.name}
                        </Link>
                      </td>
                      <td className="py-3 pr-4 font-mono text-xs text-muted-foreground">
                        {hospital.url}
                      </td>
                      <td className="py-3 pr-4">{hospital.specialty ?? "-"}</td>
                      <td className="py-3 pr-4">{hospital.region ?? "-"}</td>
                      <td className="py-3 pr-4">
                        {hospital.latest_score !== null ? (
                          <Badge variant="outline">
                            {hospital.latest_score}점
                          </Badge>
                        ) : (
                          "-"
                        )}
                      </td>
                      <td className="py-3 text-muted-foreground">
                        {new Date(hospital.created_at).toLocaleDateString(
                          "ko-KR",
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
