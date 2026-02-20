"""Compare two crawl databases and generate mismatch report."""
import sqlite3
import csv
import argparse
import json
from pathlib import Path


def get_doctors(db_path: str) -> dict:
    """Get all doctors grouped by hospital_no."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT d.hospital_no, d.name, d.role, d.education_json, d.photo_url, d.ocr_source,
               h.name as hospital_name, h.status
        FROM doctors d
        JOIN hospitals h ON d.hospital_no = h.hospital_no
    """)
    result = {}
    for row in cur.fetchall():
        hno = row["hospital_no"]
        if hno not in result:
            result[hno] = {"hospital": row["hospital_name"], "status": row["status"], "doctors": []}
        result[hno]["doctors"].append({
            "name": row["name"],
            "role": row["role"],
            "education": row["education_json"],
            "photo": bool(row["photo_url"]),
            "ocr": bool(row["ocr_source"]),
        })
    conn.close()
    return result


def get_channels(db_path: str) -> dict:
    """Get all social channels grouped by hospital_no."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT sc.hospital_no, sc.platform, sc.url, sc.extraction_method,
               h.name as hospital_name
        FROM social_channels sc
        JOIN hospitals h ON sc.hospital_no = h.hospital_no
    """)
    result = {}
    for row in cur.fetchall():
        hno = row["hospital_no"]
        if hno not in result:
            result[hno] = {"hospital": row["hospital_name"], "channels": []}
        result[hno]["channels"].append({
            "platform": row["platform"],
            "url": row["url"],
            "method": row["extraction_method"],
        })
    conn.close()
    return result


def compare_doctors(old: dict, new: dict) -> list:
    """Compare doctor data between old and new crawls."""
    mismatches = []
    all_hospitals = set(old.keys()) | set(new.keys())

    for hno in sorted(all_hospitals):
        old_data = old.get(hno, {"hospital": "?", "doctors": []})
        new_data = new.get(hno, {"hospital": "?", "doctors": []})
        hospital = old_data["hospital"] if old_data["hospital"] != "?" else new_data["hospital"]

        old_names = {d["name"] for d in old_data["doctors"]}
        new_names = {d["name"] for d in new_data["doctors"]}

        # Doctors in old but not in new (potential noise or removed)
        only_old = old_names - new_names
        # Doctors in new but not in old (missed or new hires)
        only_new = new_names - old_names
        # Doctors in both
        common = old_names & new_names

        if only_old or only_new:
            mismatches.append({
                "hospital_no": hno,
                "hospital": hospital,
                "type": "doctor",
                "old_count": len(old_names),
                "new_count": len(new_names),
                "only_old": sorted(only_old),
                "only_new": sorted(only_new),
                "common": sorted(common),
                "old_status": old_data.get("status", "?"),
                "new_status": new_data.get("status", "?"),
            })

    return mismatches


def compare_channels(old: dict, new: dict) -> list:
    """Compare social channel data between old and new crawls."""
    mismatches = []
    all_hospitals = set(old.keys()) | set(new.keys())

    for hno in sorted(all_hospitals):
        old_data = old.get(hno, {"hospital": "?", "channels": []})
        new_data = new.get(hno, {"hospital": "?", "channels": []})
        hospital = old_data["hospital"] if old_data["hospital"] != "?" else new_data["hospital"]

        old_set = {(c["platform"], c["url"]) for c in old_data["channels"]}
        new_set = {(c["platform"], c["url"]) for c in new_data["channels"]}

        only_old = old_set - new_set
        only_new = new_set - old_set

        if only_old or only_new:
            mismatches.append({
                "hospital_no": hno,
                "hospital": hospital,
                "type": "channel",
                "old_count": len(old_set),
                "new_count": len(new_set),
                "only_old": sorted(f"{p}|{u}" for p, u in only_old),
                "only_new": sorted(f"{p}|{u}" for p, u in only_new),
                "common_count": len(old_set & new_set),
            })

    return mismatches


def write_report(doctor_mismatches: list, channel_mismatches: list, output: str):
    """Write comparison report as CSV."""
    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "hospital_no", "hospital", "type", "mismatch_category",
            "old_count", "new_count", "detail"
        ])

        for m in doctor_mismatches:
            if m["only_old"]:
                writer.writerow([
                    m["hospital_no"], m["hospital"], "doctor", "only_in_old",
                    m["old_count"], m["new_count"],
                    "; ".join(m["only_old"])
                ])
            if m["only_new"]:
                writer.writerow([
                    m["hospital_no"], m["hospital"], "doctor", "only_in_new",
                    m["old_count"], m["new_count"],
                    "; ".join(m["only_new"])
                ])

        for m in channel_mismatches:
            if m["only_old"]:
                writer.writerow([
                    m["hospital_no"], m["hospital"], "channel", "only_in_old",
                    m["old_count"], m["new_count"],
                    "; ".join(m["only_old"])
                ])
            if m["only_new"]:
                writer.writerow([
                    m["hospital_no"], m["hospital"], "channel", "only_in_new",
                    m["old_count"], m["new_count"],
                    "; ".join(m["only_new"])
                ])


def main():
    parser = argparse.ArgumentParser(description="Compare two crawl databases")
    parser.add_argument("--old", required=True, help="Path to original DB")
    parser.add_argument("--new", required=True, help="Path to re-crawl DB")
    parser.add_argument("--output", default="mismatch_report.csv", help="Output CSV path")
    args = parser.parse_args()

    print(f"Loading old DB: {args.old}")
    old_doctors = get_doctors(args.old)
    old_channels = get_channels(args.old)

    print(f"Loading new DB: {args.new}")
    new_doctors = get_doctors(args.new)
    new_channels = get_channels(args.new)

    print(f"Old: {sum(len(v['doctors']) for v in old_doctors.values())} doctors, "
          f"{sum(len(v['channels']) for v in old_channels.values())} channels")
    print(f"New: {sum(len(v['doctors']) for v in new_doctors.values())} doctors, "
          f"{sum(len(v['channels']) for v in new_channels.values())} channels")

    print("\nComparing doctors...")
    doc_mismatches = compare_doctors(old_doctors, new_doctors)
    print(f"  {len(doc_mismatches)} hospitals with doctor mismatches")

    print("Comparing channels...")
    ch_mismatches = compare_channels(old_channels, new_channels)
    print(f"  {len(ch_mismatches)} hospitals with channel mismatches")

    write_report(doc_mismatches, ch_mismatches, args.output)
    print(f"\nReport saved to: {args.output}")

    # Summary stats
    doc_only_old = sum(len(m["only_old"]) for m in doc_mismatches)
    doc_only_new = sum(len(m["only_new"]) for m in doc_mismatches)
    ch_only_old = sum(len(m["only_old"]) for m in ch_mismatches)
    ch_only_new = sum(len(m["only_new"]) for m in ch_mismatches)

    print(f"\n=== Summary ===")
    print(f"Doctors only in old DB: {doc_only_old} (potential noise or removed)")
    print(f"Doctors only in new DB: {doc_only_new} (missed or new)")
    print(f"Channels only in old DB: {ch_only_old}")
    print(f"Channels only in new DB: {ch_only_new}")


if __name__ == "__main__":
    main()
