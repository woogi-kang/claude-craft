"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";

interface GeneratedImage {
  id: string;
  label: string;
  url: string;
}

interface ImageGalleryProps {
  images: GeneratedImage[];
  onDownloadAll?: () => void;
}

export function ImageGallery({ images, onDownloadAll }: ImageGalleryProps) {
  if (images.length === 0) return null;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg">생성된 이미지</CardTitle>
        {onDownloadAll && (
          <Button size="sm" variant="outline" onClick={onDownloadAll}>
            <Download className="mr-1 h-3.5 w-3.5" />
            ZIP 다운로드
          </Button>
        )}
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {images.map((img) => (
            <div
              key={img.id}
              className="group relative overflow-hidden rounded-lg border"
            >
              <img
                src={img.url}
                alt={img.label}
                className="aspect-video w-full object-cover"
              />
              <div className="flex items-center justify-between border-t bg-muted/30 px-3 py-2">
                <span className="text-sm font-medium">{img.label}</span>
                <a
                  href={img.url}
                  download
                  className="text-sm text-primary hover:underline"
                >
                  다운로드
                </a>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
