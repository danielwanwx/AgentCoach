"""Tests for agentcoach/user/jd_store.py"""
import os
import tempfile
import pytest

from agentcoach.user.jd_parser import ParsedJD, Skill
from agentcoach.user.jd_store import JDStore


@pytest.fixture
def store(tmp_path):
    db_path = os.path.join(str(tmp_path), "test_jd.db")
    return JDStore(db_path=db_path)


def _make_jd(company="TestCo", role="SWE", level="L5", required=None, preferred=None):
    return ParsedJD(
        company=company,
        role_title=role,
        level=level,
        required_skills=required or [],
        preferred_skills=preferred or [],
        key_responsibilities=["Build stuff"],
        raw_text="sample jd text",
    )


class TestJDStore:
    def test_save_and_get_active(self, store):
        jd = _make_jd()
        jd_id = store.save_jd("user1", jd)
        assert jd_id > 0

        active = store.get_active_jd("user1")
        assert active is not None
        assert active.company == "TestCo"
        assert active.role_title == "SWE"
        assert active.level == "L5"

    def test_new_jd_deactivates_previous(self, store):
        store.save_jd("user1", _make_jd(company="A"))
        store.save_jd("user1", _make_jd(company="B"))

        active = store.get_active_jd("user1")
        assert active.company == "B"

        jds = store.list_jds("user1")
        active_count = sum(1 for j in jds if j["is_active"])
        assert active_count == 1

    def test_list_jds(self, store):
        store.save_jd("user1", _make_jd(company="A"))
        store.save_jd("user1", _make_jd(company="B"))
        store.save_jd("user1", _make_jd(company="C"))

        jds = store.list_jds("user1")
        assert len(jds) == 3
        companies = {j["company"] for j in jds}
        assert companies == {"A", "B", "C"}

    def test_set_active_jd(self, store):
        id1 = store.save_jd("user1", _make_jd(company="A"))
        id2 = store.save_jd("user1", _make_jd(company="B"))

        # B is active now; switch back to A
        store.set_active_jd("user1", id1)
        active = store.get_active_jd("user1")
        assert active.company == "A"

    def test_delete_jd(self, store):
        id1 = store.save_jd("user1", _make_jd(company="A"))
        store.delete_jd("user1", id1)

        jds = store.list_jds("user1")
        assert len(jds) == 0
        assert store.get_active_jd("user1") is None

    def test_get_active_no_jds(self, store):
        assert store.get_active_jd("user1") is None

    def test_skills_roundtrip(self, store):
        jd = _make_jd(
            required=[Skill(name="Caching", priority="must", category="system_design", mapped_topics=["sd.cache"])],
            preferred=[Skill(name="Kafka", priority="nice_to_have", category="infrastructure", mapped_topics=["sd.mq"])],
        )
        store.save_jd("user1", jd)
        loaded = store.get_active_jd("user1")
        assert len(loaded.required_skills) == 1
        assert loaded.required_skills[0].name == "Caching"
        assert loaded.required_skills[0].mapped_topics == ["sd.cache"]
        assert len(loaded.preferred_skills) == 1
        assert loaded.preferred_skills[0].name == "Kafka"

    def test_user_isolation(self, store):
        store.save_jd("user1", _make_jd(company="A"))
        store.save_jd("user2", _make_jd(company="B"))

        assert store.get_active_jd("user1").company == "A"
        assert store.get_active_jd("user2").company == "B"
        assert len(store.list_jds("user1")) == 1
        assert len(store.list_jds("user2")) == 1
