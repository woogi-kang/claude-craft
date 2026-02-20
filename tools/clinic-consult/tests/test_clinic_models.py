"""Tests for clinic data models."""

from __future__ import annotations

from src.clinic.models import ClinicInfo, DoctorInfo


class TestDoctorInfo:
    """Test DoctorInfo frozen dataclass."""

    def test_basic_creation(self) -> None:
        doc = DoctorInfo(name="Kim")
        assert doc.name == "Kim"
        assert doc.name_english is None
        assert doc.role == "specialist"
        assert doc.education == []
        assert doc.career == []
        assert doc.credentials == []

    def test_full_creation(self) -> None:
        doc = DoctorInfo(
            name="Park",
            name_english="Park",
            role="director",
            education=["Seoul National University"],
            career=["10 years dermatology"],
            credentials=["Board Certified"],
        )
        assert doc.name == "Park"
        assert doc.name_english == "Park"
        assert doc.role == "director"
        assert len(doc.education) == 1

    def test_frozen(self) -> None:
        doc = DoctorInfo(name="Kim")
        import dataclasses

        assert dataclasses.is_dataclass(doc)
        # Frozen dataclass should reject attribute assignment
        import pytest

        with pytest.raises(dataclasses.FrozenInstanceError):
            doc.name = "Lee"  # type: ignore[misc]


class TestClinicInfo:
    """Test ClinicInfo frozen dataclass."""

    def test_basic_creation(self) -> None:
        clinic = ClinicInfo(hospital_no=1, name="Seoul Skin Clinic")
        assert clinic.hospital_no == 1
        assert clinic.name == "Seoul Skin Clinic"
        assert clinic.kakao_url is None
        assert clinic.phone is None
        assert clinic.doctors == []

    def test_frozen(self) -> None:
        clinic = ClinicInfo(hospital_no=1, name="Clinic")
        import dataclasses
        import pytest

        with pytest.raises(dataclasses.FrozenInstanceError):
            clinic.name = "Other"  # type: ignore[misc]

    def test_has_kakao_true(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"kakao": "https://pf.kakao.com/_abcdef"},
        )
        assert clinic.has_kakao is True

    def test_has_kakao_false(self) -> None:
        clinic = ClinicInfo(hospital_no=1, name="Clinic")
        assert clinic.has_kakao is False

    def test_kakao_chat_url_adds_chat_suffix(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"kakao": "https://pf.kakao.com/_abcdef"},
        )
        assert clinic.kakao_chat_url == "https://pf.kakao.com/_abcdef/chat"

    def test_kakao_chat_url_preserves_existing_chat(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"kakao": "https://pf.kakao.com/_abcdef/chat"},
        )
        assert clinic.kakao_chat_url == "https://pf.kakao.com/_abcdef/chat"

    def test_kakao_chat_url_strips_fragment(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"kakao": "https://pf.kakao.com/_abcdef#section"},
        )
        assert clinic.kakao_chat_url == "https://pf.kakao.com/_abcdef/chat"

    def test_kakao_chat_url_strips_trailing_slash(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"kakao": "https://pf.kakao.com/_abcdef/"},
        )
        assert clinic.kakao_chat_url == "https://pf.kakao.com/_abcdef/chat"

    def test_kakao_chat_url_none_when_no_url(self) -> None:
        clinic = ClinicInfo(hospital_no=1, name="Clinic")
        assert clinic.kakao_chat_url is None

    # --- Multi-platform tests ---

    def test_has_line(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"line": "https://line.me/R/ti/p/@clinic123"},
        )
        assert clinic.has_line is True
        assert clinic.has_kakao is False

    def test_multi_platform(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={
                "kakao": "https://pf.kakao.com/_abcdef",
                "line": "https://line.me/R/ti/p/@clinic123",
            },
        )
        assert clinic.has_kakao is True
        assert clinic.has_line is True
        assert clinic.has_platform("kakao") is True
        assert clinic.has_platform("line") is True
        assert clinic.has_platform("wechat") is False

    def test_get_contact_url(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"kakao": "https://pf.kakao.com/_abcdef"},
        )
        assert clinic.get_contact_url("kakao") == "https://pf.kakao.com/_abcdef"
        assert clinic.get_contact_url("line") is None

    def test_get_chat_url_line(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"line": "https://line.me/R/ti/p/@clinic123"},
        )
        chat_url = clinic.get_chat_url("line")
        assert chat_url == "https://line.me/R/ti/p/@clinic123"

    def test_backward_compat_kakao_url_property(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"kakao": "https://pf.kakao.com/_test"},
        )
        assert clinic.kakao_url == "https://pf.kakao.com/_test"

    def test_line_url_property(self) -> None:
        clinic = ClinicInfo(
            hospital_no=1,
            name="Clinic",
            contact_urls={"line": "https://line.me/R/ti/p/@test"},
        )
        assert clinic.line_url == "https://line.me/R/ti/p/@test"
