import sqlite3
import csv

conn = sqlite3.connect('data/clinic-results/hospitals.db')
cur = conn.cursor()

report = []
report.append('# 서울 피부과 클리닉 크롤링 데이터 분석 리포트\n')
report.append('## 1. 전체 현황\n')

cur.execute('SELECT status, COUNT(*) FROM hospitals GROUP BY status ORDER BY COUNT(*) DESC')
rows = cur.fetchall()
total = sum(r[1] for r in rows)
report.append(f'- 총 크롤링 병원: {total:,}개')
for s, c in rows:
    pct = c / total * 100
    report.append(f'  - {s}: {c:,}개 ({pct:.1f}%)')

cur.execute('SELECT COUNT(*) FROM social_channels')
ch_total = cur.fetchone()[0]
report.append(f'- 총 소셜 채널: {ch_total:,}개')

cur.execute('SELECT COUNT(*) FROM doctors')
doc_total = cur.fetchone()[0]
cur.execute('SELECT COUNT(DISTINCT hospital_no) FROM doctors')
doc_hospitals = cur.fetchone()[0]
report.append(f'- 총 의사 정보: {doc_total:,}명 ({doc_hospitals:,}개 병원)')

# District mapping from CSV
hospital_districts = {}
with open('data/clinic-results/skin_clinics.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        addr = row.get('소재지주소', '')
        no = row.get('\ufeffNO', '') or row.get('NO', '')
        if '서울' in addr and no:
            for part in addr.split():
                if part.endswith('구'):
                    hospital_districts[no] = part
                    break

# Per-district stats
cur.execute('SELECT hospital_no, status FROM hospitals')
db_hospitals = cur.fetchall()

district_stats = {}
for hno, status in db_hospitals:
    district = hospital_districts.get(str(hno), '기타')
    if district not in district_stats:
        district_stats[district] = {'success': 0, 'partial': 0, 'total': 0}
    district_stats[district]['total'] += 1
    if status == 'success':
        district_stats[district]['success'] += 1
    elif status == 'partial':
        district_stats[district]['partial'] += 1

cur.execute('SELECT hospital_no, COUNT(*) FROM social_channels GROUP BY hospital_no')
ch_by_hospital = dict(cur.fetchall())

cur.execute('SELECT hospital_no, COUNT(*) FROM doctors GROUP BY hospital_no')
doc_by_hospital = dict(cur.fetchall())

district_channels = {}
district_doctors = {}
for hno, _ in db_hospitals:
    district = hospital_districts.get(str(hno), '기타')
    district_channels[district] = district_channels.get(district, 0) + ch_by_hospital.get(hno, 0)
    district_doctors[district] = district_doctors.get(district, 0) + doc_by_hospital.get(hno, 0)

report.append('\n## 2. 구별 크롤링 현황\n')
report.append('| 구 | 총 병원 | Success | Partial | 채널 수 | 의사 수 |')
report.append('|---|--------|---------|---------|--------|--------|')
for district in sorted(district_stats.keys(), key=lambda d: district_stats[d]['total'], reverse=True):
    s = district_stats[district]
    ch = district_channels.get(district, 0)
    doc = district_doctors.get(district, 0)
    report.append(f'| {district} | {s["total"]} | {s["success"]} | {s["partial"]} | {ch} | {doc} |')

# Platform distribution
report.append('\n## 3. 소셜 플랫폼 분포\n')
report.append('| 플랫폼 | 채널 수 | 비율 |')
report.append('|-------|--------|------|')
cur.execute('SELECT platform, COUNT(*) as cnt FROM social_channels GROUP BY platform ORDER BY cnt DESC')
for platform, cnt in cur.fetchall():
    pct = cnt / ch_total * 100
    report.append(f'| {platform} | {cnt:,} | {pct:.1f}% |')

# CMS platforms
report.append('\n## 4. CMS 플랫폼 분포\n')
report.append('| CMS | 병원 수 |')
report.append('|-----|--------|')
cur.execute("""SELECT cms_platform, COUNT(*) as cnt FROM hospitals
    WHERE cms_platform IS NOT NULL AND cms_platform != ''
    GROUP BY cms_platform ORDER BY cnt DESC LIMIT 15""")
for cms, cnt in cur.fetchall():
    report.append(f'| {cms} | {cnt} |')

# Extraction methods
report.append('\n## 5. 채널 추출 방법\n')
report.append('| 방법 | 채널 수 | 비율 |')
report.append('|------|--------|------|')
cur.execute('SELECT extraction_method, COUNT(*) as cnt FROM social_channels GROUP BY extraction_method ORDER BY cnt DESC')
for method, cnt in cur.fetchall():
    pct = cnt / ch_total * 100
    report.append(f'| {method} | {cnt:,} | {pct:.1f}% |')

# Top hospitals by channel count
report.append('\n## 6. 채널 수 Top 10 병원\n')
report.append('| 병원명 | 채널 수 |')
report.append('|-------|--------|')
cur.execute("""SELECT h.name, COUNT(sc.id) as cnt
    FROM hospitals h JOIN social_channels sc ON h.hospital_no = sc.hospital_no
    GROUP BY h.hospital_no ORDER BY cnt DESC LIMIT 10""")
for name, cnt in cur.fetchall():
    report.append(f'| {name} | {cnt} |')

# Top hospitals by doctor count
report.append('\n## 7. 의사 수 Top 10 병원\n')
report.append('| 병원명 | 의사 수 |')
report.append('|-------|--------|')
cur.execute("""SELECT h.name, COUNT(d.id) as cnt
    FROM hospitals h JOIN doctors d ON h.hospital_no = d.hospital_no
    GROUP BY h.hospital_no ORDER BY cnt DESC LIMIT 10""")
for name, cnt in cur.fetchall():
    report.append(f'| {name} | {cnt} |')

# Doctor stats
report.append('\n## 8. 의사 정보 통계\n')
cur.execute('SELECT COUNT(DISTINCT hospital_no) FROM doctors')
doc_h = cur.fetchone()[0]
report.append(f'- 의사 정보 보유 병원: {doc_h}개 ({doc_h/total*100:.1f}%)')
report.append(f'- 병원당 평균 의사 수: {doc_total/doc_h:.1f}명')

cur.execute("SELECT COUNT(*) FROM doctors WHERE role IS NOT NULL AND role != ''")
with_role = cur.fetchone()[0]
report.append(f'- 역할 정보 보유: {with_role}명 ({with_role/doc_total*100:.1f}%)')

cur.execute("SELECT COUNT(*) FROM doctors WHERE education_json IS NOT NULL AND education_json != '[]' AND education_json != ''")
with_edu = cur.fetchone()[0]
report.append(f'- 학력 정보 보유: {with_edu}명 ({with_edu/doc_total*100:.1f}%)')

cur.execute("SELECT COUNT(*) FROM doctors WHERE photo_url IS NOT NULL AND photo_url != ''")
with_photo = cur.fetchone()[0]
report.append(f'- 사진 정보 보유: {with_photo}명 ({with_photo/doc_total*100:.1f}%)')

cur.execute("SELECT COUNT(*) FROM doctors WHERE ocr_source = 1")
with_ocr = cur.fetchone()[0]
report.append(f'- OCR 추출: {with_ocr}명 ({with_ocr/doc_total*100:.1f}%)')

# Hospital channel distribution
report.append('\n## 9. 병원별 채널 수 분포\n')
report.append('| 채널 수 | 병원 수 |')
report.append('|--------|--------|')
cur.execute("""SELECT channel_count, COUNT(*) as hospital_count FROM (
    SELECT hospital_no, COUNT(*) as channel_count FROM social_channels GROUP BY hospital_no
) GROUP BY channel_count ORDER BY channel_count""")
for ch_cnt, h_cnt in cur.fetchall():
    report.append(f'| {ch_cnt} | {h_cnt} |')

conn.close()

output = '\n'.join(report)
with open('data/clinic-results/exports/analysis_report.md', 'w') as f:
    f.write(output)

print(f'Report saved to: data/clinic-results/exports/analysis_report.md')
print(f'Total lines: {len(report)}')
