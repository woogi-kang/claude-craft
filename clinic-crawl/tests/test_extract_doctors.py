"""Tests for doctor information extraction helpers."""

from __future__ import annotations

from clinic_crawl.models.enums import DoctorRole
from clinic_crawl.scripts.extract_doctors import (
    detect_role,
    extract_career,
    extract_credentials,
    extract_education,
    is_doctor_menu_link,
    parse_doctor_section,
    resolve_photo_url,
)


class TestDetectRole:
    def test_director(self):
        assert detect_role("대표원장 김철수") == DoctorRole.DIRECTOR

    def test_specialist(self):
        assert detect_role("피부과전문의") == DoctorRole.SPECIALIST

    def test_resident(self):
        assert detect_role("전공의 과정 수료") == DoctorRole.RESIDENT

    def test_nurse(self):
        assert detect_role("수간호사 박영희") == DoctorRole.NURSE

    def test_default_specialist(self):
        assert detect_role("no match here") == DoctorRole.SPECIALIST


class TestExtractCredentials:
    def test_specialist_credential(self):
        creds = extract_credentials("피부과 전문의 자격 취득")
        assert len(creds) == 1
        assert creds[0].credential_type == "전문의"

    def test_no_credentials(self):
        creds = extract_credentials("general text with no credentials")
        assert creds == []

    def test_deduplicates(self):
        text = "피부과 전문의, 피부과 전문의"
        creds = extract_credentials(text)
        assert len(creds) == 1


class TestExtractEducation:
    def test_finds_university(self):
        text = "서울대학교 의과대학 졸업\n연세대학교 대학원 석사"
        edu = extract_education(text)
        assert len(edu) == 2

    def test_no_education(self):
        edu = extract_education("general text with no education")
        assert edu == []

    def test_bullet_points(self):
        text = "· 고려대학교 의과대학\n· 서울대학교 대학원 박사"
        edu = extract_education(text)
        assert len(edu) == 2


class TestExtractCareer:
    def test_finds_hospital_career(self):
        text = "서울대병원 인턴\n삼성서울병원 레지던트"
        career = extract_career(text)
        assert len(career) == 2

    def test_finds_clinic_career(self):
        text = "에이클리닉 근무"
        career = extract_career(text)
        assert len(career) == 1

    def test_no_career(self):
        career = extract_career("just some text")
        assert career == []


class TestResolvePhotoUrl:
    def test_absolute_url(self):
        assert (
            resolve_photo_url("https://cdn.com/photo.jpg", "https://site.com")
            == "https://cdn.com/photo.jpg"
        )

    def test_relative_url(self):
        assert (
            resolve_photo_url("/img/doc.jpg", "https://site.com") == "https://site.com/img/doc.jpg"
        )

    def test_none_input(self):
        assert resolve_photo_url(None, "https://site.com") is None

    def test_data_uri_skipped(self):
        assert resolve_photo_url("data:image/png;base64,abc", "https://site.com") is None


class TestParseDoctorSection:
    def test_extracts_name(self):
        html = "<h2>김철수</h2><p>대표원장, 피부과 전문의</p>"
        info = parse_doctor_section(html, "https://clinic.com")
        assert info.name == "김철수"
        assert info.role == DoctorRole.DIRECTOR

    def test_extracts_photo(self):
        html = '<img src="/photos/doc.jpg"><h3>박영희</h3>'
        info = parse_doctor_section(html, "https://clinic.com")
        assert info.photo_url == "https://clinic.com/photos/doc.jpg"


class TestIsDoctorMenuLink:
    def test_korean_keyword(self):
        assert is_doctor_menu_link("의료진 소개") is True

    def test_english_keyword(self):
        assert is_doctor_menu_link("Our Doctors") is True

    def test_unrelated(self):
        assert is_doctor_menu_link("Home") is False
