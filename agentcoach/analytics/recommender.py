"""Recommender — suggests what to learn/practice next based on mastery scores."""
from agentcoach.analytics.store import AnalyticsStore


class Recommender:
    LEARN_THRESHOLD = 40
    REINFORCE_THRESHOLD = 70

    def __init__(self, store: AnalyticsStore):
        self.store = store

    def recommend(self, user_id: str, topics: list) -> dict:
        """Recommend next topic + mode based on mastery scores.

        Returns: {"topic_id": str, "topic_name": str, "mode": str, "mastery": int, "reason": str}
        """
        scored = []
        for topic in topics:
            tid = topic["id"]
            mastery = self.store.get_mastery(user_id, tid)
            scored.append({
                "topic_id": tid,
                "topic_name": topic["name"],
                "mastery": mastery,
            })

        # Priority: unstarted topics first
        unstarted = [s for s in scored if s["mastery"] == 0]
        if unstarted:
            pick = unstarted[0]
            return {**pick, "mode": "learn", "reason": "Not started yet"}

        # Find lowest scoring topic
        scored.sort(key=lambda x: x["mastery"])
        pick = scored[0]

        if pick["mastery"] < self.LEARN_THRESHOLD:
            return {**pick, "mode": "learn", "reason": f"Score {pick['mastery']}% — needs study"}
        elif pick["mastery"] < self.REINFORCE_THRESHOLD:
            return {**pick, "mode": "reinforce", "reason": f"Score {pick['mastery']}% — needs practice"}
        else:
            return {**pick, "mode": "mock", "reason": "Ready for mock interview"}
