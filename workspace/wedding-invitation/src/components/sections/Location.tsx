'use client';

import { motion } from 'framer-motion';
import { Car, Bus, Train, MapPin, Navigation, Clock } from 'lucide-react';
import { Section, SectionTitle, HorizontalDivider } from '@/components/common/Section';
import { Button } from '@/components/ui/Button';
import { WEDDING_INFO } from '@/lib/constants';

export function Location() {
  const { venue, shuttle } = WEDDING_INFO;

  const openNaverMap = () => {
    const url = `https://map.naver.com/v5/search/${encodeURIComponent(venue.roadAddress)}`;
    window.open(url, '_blank');
  };

  const openKakaoMap = () => {
    const url = `https://map.kakao.com/link/search/${encodeURIComponent(venue.roadAddress)}`;
    window.open(url, '_blank');
  };

  const openTMap = () => {
    const url = `https://apis.openapi.sk.com/tmap/app/routes?appKey=YOUR_TMAP_KEY&goalname=${encodeURIComponent(venue.name)}&goalx=${venue.coordinates.lng}&goaly=${venue.coordinates.lat}`;
    window.open(url, '_blank');
  };

  return (
    <Section id="location" background="secondary">
      <SectionTitle title="오시는 길" subtitle="LOCATION" />

      {/* Map Embed */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="mb-6 overflow-hidden rounded-xl"
      >
        <iframe
          src={`https://map.kakao.com/link/map/${venue.name},${venue.coordinates.lat},${venue.coordinates.lng}`}
          width="100%"
          height="250"
          style={{ border: 0 }}
          allowFullScreen
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
          title="웨딩홀 위치"
          className="w-full"
        />
      </motion.div>

      {/* Venue Address */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.1 }}
        className="mb-6 text-center"
      >
        <div className="mb-2 flex items-center justify-center gap-2">
          <MapPin className="h-4 w-4 text-[var(--color-primary)]" />
          <span className="font-medium">{venue.name}</span>
        </div>
        <p className="text-sm text-[var(--color-text-light)]">{venue.roadAddress}</p>
        <p className="text-xs text-[var(--color-text-light)]">({venue.address})</p>
      </motion.div>

      {/* Map Buttons */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.2 }}
        className="mb-8 flex justify-center gap-2"
      >
        <Button variant="secondary" size="sm" onClick={openNaverMap}>
          <Navigation className="h-4 w-4" />
          네이버지도
        </Button>
        <Button variant="secondary" size="sm" onClick={openKakaoMap}>
          <Navigation className="h-4 w-4" />
          카카오맵
        </Button>
        <Button variant="secondary" size="sm" onClick={openTMap}>
          <Navigation className="h-4 w-4" />
          티맵
        </Button>
      </motion.div>

      <HorizontalDivider />

      {/* Transportation Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.3 }}
        className="space-y-4"
      >
        {/* Subway */}
        <div className="rounded-xl bg-white p-4">
          <div className="mb-2 flex items-center gap-2">
            <Train className="h-5 w-5 text-[var(--color-primary)]" />
            <span className="font-medium">지하철</span>
          </div>
          <p className="text-sm text-[var(--color-text-light)]">{venue.subway}</p>
        </div>

        {/* Bus */}
        <div className="rounded-xl bg-white p-4">
          <div className="mb-2 flex items-center gap-2">
            <Bus className="h-5 w-5 text-[var(--color-primary)]" />
            <span className="font-medium">버스</span>
          </div>
          <p className="text-sm text-[var(--color-text-light)]">{venue.bus}</p>
        </div>

        {/* Parking */}
        <div className="rounded-xl bg-white p-4">
          <div className="mb-2 flex items-center gap-2">
            <Car className="h-5 w-5 text-[var(--color-primary)]" />
            <span className="font-medium">주차</span>
          </div>
          <p className="text-sm text-[var(--color-text-light)]">{venue.parking}</p>
        </div>
      </motion.div>

      {/* Shuttle Bus Info */}
      {shuttle.available && (
        <>
          <HorizontalDivider className="my-8" />

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4 }}
          >
            <h3 className="mb-4 text-center font-serif text-lg font-medium text-[var(--color-primary)]">
              셔틀버스 안내
            </h3>

            <div className="space-y-4">
              {shuttle.routes.map((route, index) => (
                <div key={index} className="rounded-xl bg-white p-4">
                  <div className="mb-2 flex items-center gap-2">
                    <Bus className="h-5 w-5 text-[var(--color-accent)]" />
                    <span className="font-medium">{route.name}</span>
                  </div>
                  <p className="mb-2 text-sm text-[var(--color-text)]">
                    <MapPin className="mr-1 inline h-3 w-3" />
                    {route.departure}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {route.times.map((time, i) => (
                      <span
                        key={i}
                        className="inline-flex items-center gap-1 rounded-full bg-[var(--color-secondary)] px-3 py-1 text-xs"
                      >
                        <Clock className="h-3 w-3" />
                        {time}
                      </span>
                    ))}
                  </div>
                  <p className="mt-2 text-xs text-[var(--color-text-light)]">{route.duration}</p>
                </div>
              ))}
            </div>
          </motion.div>
        </>
      )}
    </Section>
  );
}
