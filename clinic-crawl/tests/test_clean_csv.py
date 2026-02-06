"""Tests for clean_csv utilities."""

from __future__ import annotations

from clinic_crawl.models.csv_row import SkinClinicRow
from clinic_crawl.scripts.clean_csv import build_url_map, load_csv


class TestBuildUrlMap:
    def test_maps_first_url(self):
        rows = [
            SkinClinicRow(
                no=1,
                name="Clinic A",
                hospital_type="피부과",
                homepage="https://clinica.com",
            ),
            SkinClinicRow(
                no=2,
                name="Clinic B",
                hospital_type="피부과",
            ),
        ]
        url_map = build_url_map(rows)
        assert url_map == {1: "https://clinica.com"}

    def test_empty_rows(self):
        assert build_url_map([]) == {}

    def test_no_urls(self):
        rows = [
            SkinClinicRow(no=1, name="Clinic A", hospital_type="피부과"),
        ]
        assert build_url_map(rows) == {}


class TestLoadCsvEncodings:
    def test_cp949_encoding(self, tmp_path):
        csv_file = tmp_path / "test.csv"
        csv_file.write_bytes("NO,병원/약국명,병원/약국구분\n1,테스트,피부과\n".encode("cp949"))
        rows = load_csv(csv_file)
        assert len(rows) == 1
        assert rows[0].name == "테스트"


class TestLoadCsv:
    def test_load_valid_csv(self, tmp_path):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "NO,병원/약국명,병원/약국구분,홈페이지\n"
            "1,Test Clinic,피부과,https://test.com\n"
            "2,Other Clinic,피부과,\n",
            encoding="utf-8-sig",
        )
        rows = load_csv(csv_file)
        assert len(rows) == 2
        assert rows[0].name == "Test Clinic"
        assert rows[0].homepage == "https://test.com"

    def test_load_with_invalid_rows(self, tmp_path):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "NO,병원/약국명,병원/약국구분\n1,Test Clinic,피부과\nnot_a_number,Bad,Data\n",
            encoding="utf-8-sig",
        )
        rows = load_csv(csv_file)
        # First row valid, second fails validation
        assert len(rows) == 1
