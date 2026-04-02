"""Study planner — generates personalized learning plans based on user profile and mastery."""
from datetime import datetime, timedelta
from typing import Optional


def generate_study_plan(
    syllabus_topics: list,
    mastery_data: dict,
    days_until_interview: int = 14,
    target_company: str = "",
    sessions_per_day: int = 2,
    active_jd=None,
) -> list:
    """Generate a day-by-day study plan.

    Args:
        syllabus_topics: list of topic dicts from SyllabusLoader
        mastery_data: {topic_id: mastery_percent}
        days_until_interview: countdown
        target_company: optional company name for topic prioritization
        sessions_per_day: how many study sessions per day
        active_jd: optional ParsedJD for JD-based topic weighting

    Returns:
        list of {day, date, sessions: [{topic_id, topic_name, mode, reason}]}
    """
    # Build JD topic sets for weighting
    jd_required_topics = set()
    jd_preferred_topics = set()
    if active_jd:
        for s in active_jd.required_skills:
            jd_required_topics.update(s.mapped_topics)
        for s in active_jd.preferred_skills:
            jd_preferred_topics.update(s.mapped_topics)

    # Score each topic by urgency
    scored = []
    for t in syllabus_topics:
        tid = t["id"]
        mastery = mastery_data.get(tid, 0)
        difficulty = t.get("difficulty_level", 1)

        # Gap = how far from mastery target (70% for reinforcement threshold)
        gap = max(0, 70 - mastery)
        # Priority: higher difficulty topics need more time
        urgency = gap * (1 + difficulty * 0.2)

        # JD weighting
        if active_jd:
            if tid in jd_required_topics:
                urgency *= 2.0
            elif tid in jd_preferred_topics:
                urgency *= 1.5
            else:
                urgency *= 0.5
        # Determine mode
        if mastery == 0:
            mode = "learn"
        elif mastery < 40:
            mode = "learn"
        elif mastery < 70:
            mode = "reinforce"
        else:
            mode = "mock"

        scored.append({
            "topic_id": tid,
            "topic_name": t["name"],
            "mastery": mastery,
            "mode": mode,
            "urgency": urgency,
            "difficulty": difficulty,
        })

    # Sort by urgency (highest first)
    scored.sort(key=lambda x: x["urgency"], reverse=True)

    # Build day-by-day plan
    plan = []
    today = datetime.now().date()
    topic_idx = 0

    for day_num in range(days_until_interview):
        date = today + timedelta(days=day_num)
        sessions = []

        for _ in range(sessions_per_day):
            if topic_idx >= len(scored):
                # Cycle back for review
                topic_idx = 0
            topic = scored[topic_idx]

            reason = ""
            if topic["mastery"] == 0:
                reason = "Not started yet"
            elif topic["mastery"] < 40:
                reason = f"Low mastery ({topic['mastery']}%)"
            elif topic["mastery"] < 70:
                reason = f"Needs practice ({topic['mastery']}%)"
            else:
                reason = "Mock practice"

            sessions.append({
                "topic_id": topic["topic_id"],
                "topic_name": topic["topic_name"],
                "mode": topic["mode"],
                "reason": reason,
            })
            topic_idx += 1

        # Add a weekly mock on days 6, 13
        if day_num > 0 and day_num % 7 == 6:
            sessions.append({
                "topic_id": "full_mock",
                "topic_name": "Full Mock Interview",
                "mode": "mock",
                "reason": "Weekly full simulation",
            })

        plan.append({
            "day": day_num + 1,
            "date": date.isoformat(),
            "sessions": sessions,
        })

    return plan


def format_plan(plan: list, days_to_show: int = 7) -> str:
    """Format study plan for display."""
    lines = [f"📅 Study Plan ({len(plan)} days)\n"]
    for day in plan[:days_to_show]:
        lines.append(f"Day {day['day']} ({day['date']}):")
        for s in day["sessions"]:
            icon = {"learn": "📖", "reinforce": "🔄", "mock": "🎤"}.get(s["mode"], "📝")
            lines.append(f"  {icon} {s['mode'].upper()}: {s['topic_name']} — {s['reason']}")
        lines.append("")
    if len(plan) > days_to_show:
        lines.append(f"  ... and {len(plan) - days_to_show} more days")
    return "\n".join(lines)
