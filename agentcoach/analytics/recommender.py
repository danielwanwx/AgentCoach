"""Recommender — suggests what to learn/practice next based on mastery, prerequisites, and recency."""
from datetime import datetime
from agentcoach.analytics.store import AnalyticsStore


class Recommender:
    LEARN_THRESHOLD = 40
    REINFORCE_THRESHOLD = 70

    def __init__(self, store: AnalyticsStore):
        self.store = store

    def recommend(self, user_id: str, topics: list, syllabus=None) -> dict:
        """Recommend next topic + mode based on mastery, prerequisites, and recency.

        Args:
            syllabus: optional SyllabusLoader for prerequisite lookups.

        Returns: {"topic_id": str, "topic_name": str, "mode": str, "mastery": int, "reason": str}
        """
        now = datetime.utcnow()
        candidates = []
        for topic in topics:
            tid = topic["id"]
            mastery = self.store.get_mastery(user_id, tid)

            # Skip topics with unmet prerequisites
            if syllabus and not self._prerequisites_met(tid, user_id, syllabus):
                continue

            # Compute days since last practiced
            last = self.store.get_last_practiced(user_id, tid)
            if last:
                try:
                    days_since = (now - datetime.fromisoformat(last)).total_seconds() / 86400.0
                except (ValueError, TypeError):
                    days_since = 0.0
            else:
                days_since = 999.0  # never practiced → high recency urgency

            # Priority score: urgency (low mastery) + recency (long since practiced)
            urgency = 1.0 - mastery / 100.0
            recency = min(days_since / 60.0, 1.0)  # caps at 60 days
            priority = 0.6 * urgency + 0.4 * recency

            candidates.append({
                "topic_id": tid,
                "topic_name": topic["name"],
                "mastery": mastery,
                "priority": priority,
            })

        if not candidates:
            # All topics blocked by prerequisites — fall back to first topic
            topic = topics[0]
            return {
                "topic_id": topic["id"],
                "topic_name": topic["name"],
                "mastery": 0,
                "mode": "learn",
                "reason": "Starting from fundamentals",
            }

        # Pick highest priority
        candidates.sort(key=lambda x: x["priority"], reverse=True)
        pick = candidates[0]

        if pick["mastery"] < self.LEARN_THRESHOLD:
            mode = "learn"
            reason = f"Score {pick['mastery']}% — needs study"
        elif pick["mastery"] < self.REINFORCE_THRESHOLD:
            mode = "reinforce"
            reason = f"Score {pick['mastery']}% — needs practice"
        else:
            mode = "mock"
            reason = "Ready for mock interview"

        return {
            "topic_id": pick["topic_id"],
            "topic_name": pick["topic_name"],
            "mastery": pick["mastery"],
            "mode": mode,
            "reason": reason,
        }

    def _prerequisites_met(self, topic_id: str, user_id: str, syllabus) -> bool:
        """Check if all prerequisite topics have mastery >= LEARN_THRESHOLD."""
        topic = syllabus.get_topic(topic_id)
        if not topic:
            return True
        for prereq_id in topic.get("prerequisites", []):
            if self.store.get_mastery(user_id, prereq_id) < self.LEARN_THRESHOLD:
                return False
        return True
