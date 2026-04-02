import os
import sys
from dotenv import load_dotenv
from agentcoach.coach import Coach
from agentcoach.memory.store import CoachMemory
from agentcoach.log import setup_logging, get_logger
from agentcoach.cli.menu import _show_menu
from agentcoach.cli.session import _speak, _run_session

logger = get_logger()


def main():
    setup_logging()
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "minimax")
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    model = os.getenv("LLM_MODEL", "")

    if not api_key:
        print("Error: Set LLM_API_KEY in .env")  # UI output
        sys.exit(1)

    # Initialize TTS
    tts_engine_name = os.getenv("TTS_ENGINE", "macos")  # macos, qwen, vibevoice, none
    tts = None
    if tts_engine_name == "macos":
        from agentcoach.voice.tts import MacOSTTS
        tts = MacOSTTS(voice=os.getenv("TTS_VOICE", "Samantha"))
    elif tts_engine_name == "qwen":
        from agentcoach.voice.tts import QwenTTS
        tts = QwenTTS(lazy=True)
    elif tts_engine_name == "vibevoice":
        from agentcoach.voice.tts import VibeVoiceTTS
        tts = VibeVoiceTTS(
            device=os.getenv("TTS_DEVICE", "mps"),
            inference_steps=int(os.getenv("TTS_INFERENCE_STEPS", "15")),
            voice_sample=os.getenv("TTS_VOICE_SAMPLE"),
            lazy=True,
        )
    # tts_engine_name == "none" -> tts stays None

    if tts:
        from agentcoach.voice.tts import AsyncTTSWrapper
        tts = AsyncTTSWrapper(tts)

    # Initialize memory
    mem = CoachMemory()

    # Initialize syllabus, analytics, recommender
    from agentcoach.syllabus.loader import SyllabusLoader
    from agentcoach.analytics.store import AnalyticsStore
    from agentcoach.analytics.recommender import Recommender

    syllabus = SyllabusLoader()
    analytics = AnalyticsStore()
    recommender = Recommender(analytics)
    user_id = "default"  # single user for now

    # Initialize JD store
    from agentcoach.user.jd_store import JDStore
    jd_store = JDStore()

    # Initialize KB
    from agentcoach.kb.store import KnowledgeStore
    kb = KnowledgeStore(use_vectors=False)
    try:
        kb_stats = kb.get_stats()
        kb_active = kb if kb_stats["total_chunks"] > 0 else None
    except Exception:
        kb_active = None

    print("=== AgentCoach -- AI Mock Interview Coach ===")  # UI output
    print(f"Provider: {provider} | TTS: {tts_engine_name}")  # UI output
    if kb_active:
        print(f"Knowledge Base: {kb_stats['total_chunks']} chunks")  # UI output
    print()  # UI output

    # Main menu loop
    while True:
        domain, mode, topic = _show_menu(syllabus, analytics, recommender, user_id, mem=mem, jd_store=jd_store)
        if domain is None:
            break  # user quit

        # Create LLM via router (uses task-specific providers if API keys available)
        from agentcoach.llm.router import LLMRouter
        router = LLMRouter.from_env()
        llm = router.get("coaching")

        # Build mode-specific system prompt hint
        mode_hint = ""
        kb_teaching_text = ""
        if mode == "learn" and topic:
            resources = syllabus.get_resources(topic["id"])
            res_text = "\n".join(f"  - [{r['type']}] {r['title']}: {r.get('url', 'N/A')}" for r in resources)
            mode_hint = f"\nMode: Learn -- Topic: {topic['name']}\nAfter teaching, show these resources for deeper study:\n{res_text}"
            # Pre-fetch KB content for teaching
            if kb_active:
                try:
                    kb_results = kb_active.search(topic["name"], limit=5)
                    if kb_results:
                        kb_teaching_text = "\n\n".join(r["content"][:800] for r in kb_results)
                except Exception:
                    pass
        elif mode == "reinforce" and topic:
            mastery = analytics.get_mastery(user_id, topic["id"])
            mode_hint = f"\nMode: Reinforce -- Topic: {topic['name']} (current mastery: {mastery}%)\nAsk increasingly difficult follow-up questions on this specific topic."
        elif mode == "mock":
            mode_hint = f"\nMode: Mock Interview -- Domain: {syllabus.get_domain_name(domain)}\nConduct a full realistic interview simulation."

        # Map to prompt template key
        if mode == "mock":
            prompt_mode = f"mock_{domain}"
        elif mode in ("learn", "reinforce"):
            prompt_mode = mode
        else:
            prompt_mode = "behavioral"

        # Build memory context with user profile + company info
        memory_ctx = mem.get_context() + mode_hint
        try:
            from agentcoach.user import UserProfileStore
            user_store = UserProfileStore()
            profile_ctx = user_store.format_for_prompt(user_id)
            if profile_ctx:
                memory_ctx += f"\n\n### User Profile\n{profile_ctx}"
        except Exception:
            pass

        # Inject active JD context
        try:
            active_jd = jd_store.get_active_jd(user_id)
            if active_jd:
                from agentcoach.coaching.context_builder import format_jd_for_prompt
                topic_name = topic["name"] if topic else ""
                jd_ctx = format_jd_for_prompt(active_jd, current_topic=topic_name)
                memory_ctx += f"\n\n{jd_ctx}"
        except Exception:
            active_jd = None

        # Inject company profile for mock mode
        if mode == "mock":
            try:
                from agentcoach.companies import format_company_for_prompt
                # Try to detect target company from user profile
                company_ctx = ""
                try:
                    profile = user_store.load(user_id) if 'user_store' in dir() else None
                    if profile and profile.target_companies:
                        company_ctx = format_company_for_prompt(profile.target_companies[0])
                except Exception:
                    pass
                if company_ctx:
                    memory_ctx += f"\n\n{company_ctx}"
            except Exception:
                pass

        coach = Coach(
            llm=llm,
            mode=prompt_mode,
            memory_context=memory_ctx,
            kb_store=kb_active,
            topic_id=topic["id"] if topic else "",
            topic_name=topic["name"] if topic else "",
            kb_teaching_context=kb_teaching_text,
        )

        # Run session
        opening = coach.start()
        print(f"\nCoach: {opening}\n")  # UI output
        _speak(tts, opening)

        _run_session(coach, mem, tts, analytics, user_id, topic, mode, llm, kb_store=kb_active, syllabus=syllabus)
        print()  # UI output — blank line before menu
