"""Tests for async SQLite storage layer."""

from __future__ import annotations

import pytest

from clinic_crawl.models.enums import CrawlCategory, CrawlPhase, ExtractionMethod
from clinic_crawl.storage import ClinicStorageManager


class TestUpsertHospital:
    async def test_insert_new(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "Test Clinic")
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.PENDING)
        assert len(hospitals) == 1
        assert hospitals[0]["name"] == "Test Clinic"

    async def test_upsert_updates_phase(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "Test Clinic")
        await storage.upsert_hospital(1, "Test Clinic", phase=CrawlPhase.TRIAGE_DONE)
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.TRIAGE_DONE)
        assert len(hospitals) == 1

    async def test_upsert_preserves_category(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(
            1,
            "Test",
            category=CrawlCategory.CUSTOM_DOMAIN,
        )
        # Update without category should keep the existing one
        await storage.upsert_hospital(1, "Test", phase=CrawlPhase.TRIAGE_DONE)
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.TRIAGE_DONE)
        assert hospitals[0]["category"] == CrawlCategory.CUSTOM_DOMAIN.value


class TestUpdatePhase:
    async def test_updates_phase(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "Test")
        await storage.update_phase(1, CrawlPhase.PRESCAN_DONE)
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.PRESCAN_DONE)
        assert len(hospitals) == 1

    async def test_stores_error_message(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "Test")
        await storage.update_phase(1, CrawlPhase.FAILED, error_message="timeout")
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.FAILED)
        assert hospitals[0]["error_message"] == "timeout"


class TestPhaseCounts:
    async def test_counts(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A")
        await storage.upsert_hospital(2, "B")
        await storage.upsert_hospital(3, "C", phase=CrawlPhase.TRIAGE_DONE)
        counts = await storage.get_phase_counts()
        assert counts["pending"] == 2
        assert counts["triage_done"] == 1


class TestSocialLinks:
    async def test_save_and_retrieve(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "Test")
        await storage.save_social_link(
            hospital_no=1,
            platform="kakao",
            url="https://pf.kakao.com/test",
            extraction_method=ExtractionMethod.PRESCAN_REGEX,
            confidence=0.8,
        )
        links = await storage.get_social_links(1)
        assert len(links) == 1
        assert links[0]["platform"] == "kakao"
        assert links[0]["confidence"] == 0.8

    async def test_ignores_duplicates(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "Test")
        for _ in range(3):
            await storage.save_social_link(
                hospital_no=1,
                platform="kakao",
                url="https://pf.kakao.com/test",
                extraction_method=ExtractionMethod.PRESCAN_REGEX,
            )
        links = await storage.get_social_links(1)
        assert len(links) == 1

    async def test_different_platforms(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "Test")
        await storage.save_social_link(
            1,
            "kakao",
            "https://pf.kakao.com/a",
            ExtractionMethod.PRESCAN_REGEX,
        )
        await storage.save_social_link(
            1,
            "naver_talk",
            "https://talk.naver.com/b",
            ExtractionMethod.DOM_STATIC,
        )
        links = await storage.get_social_links(1)
        assert len(links) == 2


class TestDoctors:
    async def test_save_doctor(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "Test")
        await storage.save_doctor(
            hospital_no=1,
            name="Dr. Kim",
            role="director",
            credentials=[{"credential_type": "전문의", "value": "피부과전문의"}],
            education=["서울대학교 의과대학"],
        )
        # Verify by querying directly
        db = storage._ensure_db()
        cursor = await db.execute("SELECT * FROM doctors WHERE hospital_no = 1")
        rows = await cursor.fetchall()
        assert len(rows) == 1
        assert rows[0]["name"] == "Dr. Kim"


class TestChainPatterns:
    async def test_save_and_get(self, storage: ClinicStorageManager):
        selectors = {"social": ".social-link", "doctor": ".doctor-card"}
        await storage.save_chain_pattern("clinic.com", selectors, sample_hospital_no=1)
        result = await storage.get_chain_pattern("clinic.com")
        assert result == selectors

    async def test_get_nonexistent(self, storage: ClinicStorageManager):
        result = await storage.get_chain_pattern("nonexistent.com")
        assert result is None

    async def test_upsert_updates(self, storage: ClinicStorageManager):
        await storage.save_chain_pattern("clinic.com", {"v": 1}, sample_hospital_no=1)
        await storage.save_chain_pattern("clinic.com", {"v": 2}, sample_hospital_no=1)
        result = await storage.get_chain_pattern("clinic.com")
        assert result == {"v": 2}


class TestRecoverInterrupted:
    async def test_recovers_failed_items(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A", phase=CrawlPhase.PRESCAN_DONE)
        await storage.update_phase(1, CrawlPhase.FAILED, error_message="crash")
        count = await storage.recover_interrupted()
        assert count == 1
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.PRESCAN_DONE)
        assert len(hospitals) == 1
        assert hospitals[0]["error_message"] is None

    async def test_no_failed_items(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A")
        count = await storage.recover_interrupted()
        assert count == 0


class TestBatch:
    async def test_batch_commits_once(self, storage: ClinicStorageManager):
        """Batch groups multiple writes into a single transaction."""
        async with storage.batch():
            for i in range(10):
                await storage.upsert_hospital(i, f"Clinic {i}")
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.PENDING)
        assert len(hospitals) == 10

    async def test_batch_rollback_on_error(self, storage: ClinicStorageManager):
        """Batch rolls back all writes on error."""
        await storage.upsert_hospital(1, "Existing")
        with pytest.raises(ValueError, match="test error"):
            async with storage.batch():
                await storage.upsert_hospital(2, "New")
                raise ValueError("test error")
        # Only the pre-batch hospital should exist
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.PENDING)
        assert len(hospitals) == 1
        assert hospitals[0]["hospital_no"] == 1

    async def test_batch_social_links(self, storage: ClinicStorageManager):
        """Batch works for social link saves."""
        await storage.upsert_hospital(1, "Test")
        async with storage.batch():
            for platform in ("kakao", "naver_talk", "line"):
                await storage.save_social_link(
                    hospital_no=1,
                    platform=platform,
                    url=f"https://example.com/{platform}",
                    extraction_method=ExtractionMethod.PRESCAN_REGEX,
                )
        links = await storage.get_social_links(1)
        assert len(links) == 3

    async def test_non_batch_still_autocommits(self, storage: ClinicStorageManager):
        """Without batch, each write auto-commits."""
        await storage.upsert_hospital(1, "Test")
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.PENDING)
        assert len(hospitals) == 1


class TestReportQueries:
    async def test_get_category_counts(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A", category=CrawlCategory.CUSTOM_DOMAIN)
        await storage.upsert_hospital(2, "B", category=CrawlCategory.CUSTOM_DOMAIN)
        await storage.upsert_hospital(3, "C", category=CrawlCategory.BLOG_NAVER)
        counts = await storage.get_category_counts()
        assert counts["custom_domain"] == 2
        assert counts["blog_naver"] == 1

    async def test_get_social_platform_counts(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A")
        await storage.save_social_link(
            1, "kakao", "https://pf.kakao.com/a", ExtractionMethod.PRESCAN_REGEX
        )
        await storage.save_social_link(
            1, "kakao", "https://pf.kakao.com/b", ExtractionMethod.PRESCAN_REGEX
        )
        await storage.save_social_link(1, "line", "https://line.me/x", ExtractionMethod.DOM_STATIC)
        counts = await storage.get_social_platform_counts()
        assert counts["kakao"] == 2
        assert counts["line"] == 1

    async def test_get_hospitals_with_social_count(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A")
        await storage.upsert_hospital(2, "B")
        await storage.save_social_link(
            1, "kakao", "https://pf.kakao.com/a", ExtractionMethod.PRESCAN_REGEX
        )
        assert await storage.get_hospitals_with_social_count() == 1

    async def test_get_doctor_stats(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A")
        await storage.upsert_hospital(2, "B")
        await storage.save_doctor(1, "Dr. Kim", "director")
        await storage.save_doctor(1, "Dr. Lee", "specialist")
        await storage.save_doctor(2, "Dr. Park", "director")
        hospitals, total = await storage.get_doctor_stats()
        assert hospitals == 2
        assert total == 3

    async def test_get_chain_domain_count(self, storage: ClinicStorageManager):
        await storage.save_chain_pattern("a.com", {}, 1)
        await storage.save_chain_pattern("b.com", {}, 2)
        assert await storage.get_chain_domain_count() == 2

    async def test_get_top_chains(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A", chain_domain="a.com")
        await storage.upsert_hospital(2, "B", chain_domain="a.com")
        await storage.upsert_hospital(3, "C", chain_domain="b.com")
        chains = await storage.get_top_chains(limit=1)
        assert "a.com" in chains
        assert len(chains) == 1

    async def test_get_extraction_method_counts(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A")
        await storage.save_social_link(
            1, "kakao", "https://pf.kakao.com/a", ExtractionMethod.PRESCAN_REGEX
        )
        await storage.save_social_link(1, "line", "https://line.me/x", ExtractionMethod.DOM_STATIC)
        counts = await storage.get_extraction_method_counts()
        assert counts["prescan_regex"] == 1
        assert counts["dom_static"] == 1

    async def test_get_total_hospitals(self, storage: ClinicStorageManager):
        await storage.upsert_hospital(1, "A")
        await storage.upsert_hospital(2, "B")
        assert await storage.get_total_hospitals() == 2

    async def test_empty_report_queries(self, storage: ClinicStorageManager):
        assert await storage.get_category_counts() == {}
        assert await storage.get_social_platform_counts() == {}
        assert await storage.get_hospitals_with_social_count() == 0
        hospitals, total = await storage.get_doctor_stats()
        assert hospitals == 0
        assert total == 0
        assert await storage.get_chain_domain_count() == 0
        assert await storage.get_top_chains() == {}
        assert await storage.get_extraction_method_counts() == {}
        assert await storage.get_total_hospitals() == 0


class TestStorageNotInitialized:
    def test_ensure_db_raises(self, tmp_config):
        mgr = ClinicStorageManager(tmp_config)
        with pytest.raises(RuntimeError, match="not initialized"):
            mgr._ensure_db()
