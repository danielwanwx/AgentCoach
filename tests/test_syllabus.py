import os
import tempfile
import yaml
from agentcoach.syllabus.loader import SyllabusLoader

SAMPLE_SYLLABUS = {
    "domain": "system_design",
    "name": "System Design",
    "topics": [
        {
            "id": "system_design.core_concepts",
            "name": "Core Concepts",
            "children": [
                {
                    "id": "system_design.caching",
                    "name": "Caching",
                    "resources": [
                        {"type": "video", "title": "Caching Explained", "url": "https://youtube.com/example"},
                        {"type": "article", "title": "Redis Caching Guide", "url": "https://example.com/redis"},
                    ],
                },
                {
                    "id": "system_design.cap_theorem",
                    "name": "CAP Theorem",
                    "resources": [
                        {"type": "article", "title": "CAP Theorem Explained", "url": "https://example.com/cap"},
                    ],
                },
            ],
        },
    ],
}

def _write_sample(tmpdir):
    os.makedirs(os.path.join(tmpdir, "data"), exist_ok=True)
    path = os.path.join(tmpdir, "data", "system_design.yaml")
    with open(path, "w") as f:
        yaml.dump(SAMPLE_SYLLABUS, f)
    return tmpdir

def test_load_domains(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    domains = loader.get_domains()
    assert "system_design" in domains

def test_get_topics(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    topics = loader.get_topics("system_design")
    ids = [t["id"] for t in topics]
    assert "system_design.caching" in ids
    assert "system_design.cap_theorem" in ids

def test_get_topic(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    topic = loader.get_topic("system_design.caching")
    assert topic is not None
    assert topic["name"] == "Caching"
    assert len(topic["resources"]) == 2

def test_get_resources(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    resources = loader.get_resources("system_design.caching")
    assert len(resources) == 2
    assert resources[0]["type"] == "video"

def test_get_topic_not_found(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    topic = loader.get_topic("nonexistent")
    assert topic is None
