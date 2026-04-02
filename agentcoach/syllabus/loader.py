"""Syllabus loader — reads YAML topic trees with resources."""
import os
import yaml


class SyllabusLoader:
    def __init__(self, data_dir: str = ""):
        if not data_dir:
            data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.data_dir = data_dir
        self._syllabi = {}
        self._topic_index = {}
        self._load_all()

    def _load_all(self):
        if not os.path.isdir(self.data_dir):
            return
        for fname in os.listdir(self.data_dir):
            if not fname.endswith((".yaml", ".yml")):
                continue
            path = os.path.join(self.data_dir, fname)
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            domain = data["domain"]
            self._syllabi[domain] = data
            self._index_topics(data["topics"], domain)

    def _index_topics(self, topics, domain, parent_id=""):
        for topic in topics:
            tid = topic["id"]
            self._topic_index[tid] = {
                "id": tid,
                "name": topic["name"],
                "domain": domain,
                "parent": parent_id,
                "resources": topic.get("resources", []),
                "difficulty_level": topic.get("difficulty_level", 1),
                "prerequisites": topic.get("prerequisites", []),
            }
            children = topic.get("children", [])
            if children:
                self._index_topics(children, domain, parent_id=tid)

    def get_domains(self) -> list:
        return list(self._syllabi.keys())

    def get_domain_name(self, domain: str) -> str:
        if domain in self._syllabi:
            return self._syllabi[domain]["name"]
        return domain

    def get_topics(self, domain: str) -> list:
        return [t for t in self._topic_index.values() if t["domain"] == domain]

    def get_topic(self, topic_id: str):
        return self._topic_index.get(topic_id)

    def get_resources(self, topic_id: str) -> list:
        topic = self.get_topic(topic_id)
        if topic is None:
            return []
        return topic["resources"]
