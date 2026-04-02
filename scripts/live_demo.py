#!/usr/bin/env python3
"""Live tutoring demo — realistic multi-turn caching session.

Two voices for the conversation:
  User:  macOS "Samantha" — student voice
  Coach: VibeVoice 1.5B  — instructor voice (cloned from reference)

Usage:
    python3 scripts/live_demo.py              # with voice
    python3 scripts/live_demo.py --no-voice   # text only (fast)
"""
from __future__ import annotations
import os, sys, re, subprocess, tempfile, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv
load_dotenv()

from agentcoach.llm.openai_compat import OpenAICompatAdapter
from agentcoach.coach import Coach
from agentcoach.analytics.store import AnalyticsStore
from agentcoach.analytics.scorer import Scorer
from agentcoach.kb.store import KnowledgeStore


# ── TTS helpers ────────────────────────────────────────────────

def _strip_md(text: str) -> str:
    c = re.sub(r'[#*_`~\[\](){}|>]', '', text)
    c = re.sub(r'https?://\S+', '', c)
    c = re.sub(r'[\U0001f300-\U0001f9ff\u2705\u274c\u2611\u2610]', '', c)
    c = re.sub(r'<[^>]+>', '', c)
    c = re.sub(r'---+', '', c)
    c = re.sub(r'\n{2,}', '. ', c)
    c = re.sub(r'\n', ' ', c)
    return re.sub(r'\s{2,}', ' ', c).strip()


def _truncate(text: str, n: int) -> str:
    if len(text) <= n:
        return text
    cut = text[:n].rfind('.')
    return text[:cut + 1] if cut > 60 else text[:n]


def say_user(text: str, on: bool):
    if not on:
        return
    subprocess.run(["say", "-v", "Samantha", "-r", "170",
                    _truncate(_strip_md(text), 500)], check=False)


def say_coach(text: str, tts, on: bool):
    if not on or tts is None:
        return
    try:
        tts.speak(_truncate(_strip_md(text), 350))
    except Exception as e:
        print(f"  [TTS error: {e}]")


# ── KB from qmd ───────────────────────────────────────────────

def load_kb_from_qmd(kb: KnowledgeStore):
    """Pull real caching content from the user's qmd KB."""
    result = subprocess.run(["qmd", "get", "#ccdec4", "--full"],
                            capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        # fallback
        kb.add_chunk(
            content="Caching improves page load times. Strategies: cache-aside, write-through, write-behind, refresh-ahead. Cache invalidation is hard — use TTL or event-driven approaches.",
            source="fallback", section="Overview", category="system_design")
        return

    sections = re.split(r'\n(?=#{1,3} )', result.stdout.strip())
    for sec in sections:
        lines = sec.strip().split('\n')
        title = lines[0].lstrip('#').strip() if lines else "Cache"
        body = '\n'.join(lines[1:]).strip()
        # skip image-only or short sections
        body_text = re.sub(r'<[^>]+>', '', body).strip()
        if len(body_text) > 50:
            kb.add_chunk(content=body_text[:1200], source="system-design-primer",
                         section=title, category="system_design")

    stats = kb.get_stats()
    print(f"  KB: {stats['total_chunks']} chunks from system-design-primer/cache.md")


# ── The conversation ───────────────────────────────────────────

def run_session(llm, kb, analytics, tts, voice_on):
    # Pre-fetch teaching material
    kb_results = kb.search("cache aside write through write behind", limit=5)
    kb_teaching = "\n\n".join(r["content"][:600] for r in kb_results)

    coach = Coach(
        llm=llm, mode="learn", kb_store=kb,
        topic_id="system_design.caching",
        topic_name="Caching Strategies",
        kb_teaching_context=kb_teaching,
    )

    def exchange(user_text):
        """One round: print user → speak user → get coach response → print → speak coach."""
        # User turn
        print(f"\n{'─'*55}")
        print(f"  🧑 You:\n  {user_text}")
        print(f"{'─'*55}")
        say_user(user_text, voice_on)
        time.sleep(0.3)

        # Coach turn
        response = coach.respond(user_text)
        print(f"\n{'─'*55}")
        print(f"  🎓 Coach:\n  {response}")
        qs = coach.quiz_state
        if qs.question_count > 0:
            print(f"\n  [Quiz: Q={qs.question_count} ✓={qs.correct_count} ✗={qs.incorrect_count} diff={qs.difficulty}]")
        print(f"{'─'*55}")
        say_coach(response, tts, voice_on)
        time.sleep(0.2)
        return response

    # ── Opening ────────────────────────────────────────────────
    print(f"\n{'─'*55}")
    print(f"  🎓 Coach (opening):")
    opening = coach.start()
    print(f"  {opening}")
    print(f"{'─'*55}")
    say_coach(opening, tts, voice_on)

    # ── Turn 1: natural self-intro ─────────────────────────────
    exchange(
        "Hey! So I'm Javi, I'm prepping for system design interviews. "
        "I've used Redis a bit at work for session storage but honestly "
        "I don't really understand the different caching patterns that well. "
        "Like, I know cache-aside exists but I couldn't explain the difference "
        "between write-through and write-behind if someone asked me."
    )

    # ── Turn 2: asking a clarifying question ───────────────────
    exchange(
        "Wait, so you mentioned caching at different levels — client, CDN, "
        "web server, database. Can you explain what caching at the object level "
        "means versus caching at the query level? I've only ever done query-level "
        "caching and I'm not sure when you'd pick one over the other."
    )

    # ── Turn 3: attempting an explanation (mostly correct) ─────
    exchange(
        "Okay so for cache-aside, the way I understand it is... the app checks "
        "the cache first, and if it's a miss, the app itself goes to the database, "
        "gets the data, and then writes it back into the cache for next time. "
        "The cache doesn't talk to the database at all, the app is the middleman. "
        "Is that right?"
    )

    # ── Turn 4: making a mistake ───────────────────────────────
    exchange(
        "And for write-through, I think the app writes to the database first, "
        "and then some background job picks it up and updates the cache later, "
        "so the write is fast because the cache update is async. Right?"
    )

    # ── Turn 5: correcting after coach feedback ────────────────
    exchange(
        "Oh shoot, I mixed those up. So write-through is the synchronous one — "
        "the cache writes to the data store before returning, which makes writes "
        "slower but the cache is always consistent. And write-behind is the async "
        "one where you could lose data if the cache goes down before flushing. "
        "That's a pretty big tradeoff."
    )

    # ── Turn 6: going deeper ──────────────────────────────────
    exchange(
        "Okay that makes sense now. But here's what I'm struggling with — "
        "in a real system, how do you decide which strategy to use? "
        "Like if I'm designing a social media feed, should I use cache-aside "
        "or write-through? And what about cache invalidation, "
        "everyone says it's the hardest problem."
    )

    # ── Turn 7: synthesis attempt ─────────────────────────────
    exchange(
        "Let me try to put it together. For a read-heavy social feed, "
        "I'd probably use cache-aside with Redis, because most requests are reads "
        "and cache-aside is lazy — it only loads on miss. I'd set a TTL of maybe "
        "five minutes so stale posts eventually refresh. For the write path when "
        "someone creates a new post, I'd invalidate the relevant cache keys "
        "through a message queue event. Does that make sense as an approach?"
    )

    # ── Turn 8: reflection + next steps ───────────────────────
    exchange(
        "This was really helpful, thanks. I think my main gap is still around "
        "the hot key problem — like what happens when a celebrity posts and "
        "millions of people hit the same cache key. Can we do a focused "
        "practice session on that next time?"
    )

    return coach


# ── Main ───────────────────────────────────────────────────────

def main():
    voice_on = "--no-voice" not in sys.argv

    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    provider = os.getenv("LLM_PROVIDER", "minimax")
    model_name = os.getenv("LLM_MODEL", "")
    if not api_key:
        print("Error: Set LLM_API_KEY"); sys.exit(1)

    if provider == "gemini":
        from agentcoach.llm.gemini import GeminiAdapter
        llm = GeminiAdapter(api_key=api_key, model=model_name or "gemini-2.0-flash")
    else:
        llm = OpenAICompatAdapter(api_key=api_key, provider=provider, model=model_name)

    tmpdir = tempfile.mkdtemp()
    analytics = AnalyticsStore(db_path=os.path.join(tmpdir, "a.db"))
    kb = KnowledgeStore(db_path=os.path.join(tmpdir, "kb.db"), use_vectors=False)

    print("Setting up...")
    load_kb_from_qmd(kb)

    tts = None
    if voice_on:
        ref = "/tmp/karpathy_ref.wav"
        if not os.path.exists(ref):
            print(f"  ⚠ {ref} not found — coach voice without cloning")
            ref = None
        print("  Loading VibeVoice 1.5B...")
        from agentcoach.voice.tts import VibeVoiceTTS
        tts = VibeVoiceTTS(device="mps", cfg_scale=1.5, voice_sample=ref, lazy=True)

    print()
    print("=" * 55)
    print("  LIVE SESSION: Learning Caching Strategies")
    print("  KB: system-design-primer/cache.md (real content)")
    if voice_on:
        print("  🔊 You=Samantha | Coach=VibeVoice")
    print("=" * 55)

    coach = run_session(llm, kb, analytics, tts, voice_on)

    # Score
    print(f"\n{'='*55}")
    print("  SCORING")
    print(f"{'='*55}")
    scorer = Scorer(llm, kb_store=kb)
    scores = scorer.score_session(coach.history, mode="learn", topic_id="system_design.caching")
    for s in scores:
        analytics.record_score("u1", s["topic_id"], s["score_delta"], "learn", s["evidence"])
        sign = "+" if s["score_delta"] > 0 else ""
        print(f"  {s['topic_id']}: {sign}{s['score_delta']} — {s['evidence']}")

    mastery = analytics.get_mastery("u1", "system_design.caching")
    print(f"\n  Mastery: {mastery}%")
    wrap = f"Session complete. Your caching mastery is now {mastery} percent."
    print(f"  🎓 {wrap}")
    say_coach(wrap, tts, voice_on)

    print(f"\n{'='*55}")
    print("  DONE")
    print(f"{'='*55}")

    import shutil
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
