import os
import sys
from dotenv import load_dotenv
from agentcoach.coach import Coach
from agentcoach.memory.store import CoachMemory


def _speak(tts, text: str):
    if tts:
        try:
            tts.speak(text)
        except Exception as e:
            print(f"(TTS error: {e})")


def _end_session(coach, mem):
    """Generate and save feedback if there was meaningful conversation."""
    if len(coach.history) > 2:
        print("\nGenerating session feedback...")
        feedback = coach.get_feedback_summary()
        if feedback:
            print(f"\n{feedback}\n")
            mem.save_feedback(feedback)
            print("Feedback saved to memory.")


def _show_menu(syllabus, analytics, recommender, user_id, mem=None):
    """Show domain/mode selection. Returns (domain, mode, topic) or (None, None, None) to quit."""
    domains = syllabus.get_domains()

    while True:
        print("--- Main Menu ---")
        print("Domains:")
        for i, d in enumerate(domains, 1):
            name = syllabus.get_domain_name(d)
            topics = syllabus.get_topics(d)
            progress = analytics.get_progress(user_id, d)
            scored_count = len(progress)
            print(f"  {i}. {name} ({scored_count}/{len(topics)} topics started)")
        print()
        print("Commands: 'progress <domain>', 'recommend', 'quit'")
        print("Data:     'import profile <text>', 'import jd <text>', 'load resume <file>',")
        print("          'load jd <file>', 'load kb <dir> [category]', 'kb stats', 'kb search <query>'")
        print()

        try:
            choice = input("Select domain (number) or command: ").strip()
        except (KeyboardInterrupt, EOFError):
            return None, None, None

        choice_lower = choice.lower()

        if choice_lower == "quit":
            return None, None, None

        if choice_lower == "recommend":
            all_topics = []
            for d in domains:
                all_topics.extend(syllabus.get_topics(d))
            if not all_topics:
                print("No topics found in syllabus.\n")
                continue
            rec = recommender.recommend(user_id, all_topics)
            print(f"\nCoach recommends: {rec['mode'].upper()} — {rec['topic_name']}")
            print(f"Reason: {rec['reason']}\n")
            continue

        if choice_lower.startswith("progress"):
            parts = choice_lower.split(maxsplit=1)
            if len(parts) < 2:
                for d in domains:
                    _show_progress(syllabus, analytics, user_id, d)
            else:
                query = parts[1]
                matched = [d for d in domains if query in d]
                if matched:
                    _show_progress(syllabus, analytics, user_id, matched[0])
                else:
                    print(f"Unknown domain: {query}")
            continue

        # Data import commands
        if choice_lower.startswith("import profile ") and mem:
            text = choice[len("import profile "):].strip()
            mem.save_profile(text)
            print("Profile saved to memory.")
            continue

        if choice_lower.startswith("import jd ") and mem:
            text = choice[len("import jd "):].strip()
            mem.save_jd(text)
            print("JD saved to memory.")
            continue

        if choice_lower.startswith("load resume ") and mem:
            filepath = choice[len("load resume "):].strip()
            try:
                from agentcoach.memory.importer import import_file
                content = import_file(filepath)
                mem.save_profile(content)
                print(f"Resume loaded from {filepath} and saved to memory.")
            except FileNotFoundError as e:
                print(f"Error: {e}")
            continue

        if choice_lower.startswith("load jd ") and mem:
            filepath = choice[len("load jd "):].strip()
            try:
                from agentcoach.memory.importer import import_file
                content = import_file(filepath)
                mem.save_jd(content)
                print(f"JD loaded from {filepath} and saved to memory.")
            except FileNotFoundError as e:
                print(f"Error: {e}")
            continue

        if choice_lower.startswith("load kb "):
            parts = choice[len("load kb "):].strip().split(maxsplit=1)
            dir_path = parts[0]
            cat = parts[1] if len(parts) > 1 else "general"
            try:
                from agentcoach.kb.indexer import index_directory
                from agentcoach.kb.store import KnowledgeStore
                kb = KnowledgeStore()
                print(f"Indexing {dir_path} (category: {cat})...")
                stats = index_directory(dir_path, kb, category=cat)
                print(f"Done: {stats['files_processed']} files, {stats['chunks_added']} chunks indexed.")
                if stats['errors']:
                    print(f"Errors: {len(stats['errors'])}")
            except Exception as e:
                print(f"Error: {e}")
            continue

        if choice_lower == "kb stats":
            try:
                from agentcoach.kb.store import KnowledgeStore
                kb = KnowledgeStore()
                stats = kb.get_stats()
                print(f"\nKnowledge Base: {stats['total_chunks']} chunks, {stats['total_sources']} sources")
                print(f"Categories: {', '.join(stats['categories']) if stats['categories'] else 'none'}\n")
            except Exception as e:
                print(f"Error: {e}")
            continue

        if choice_lower.startswith("kb search "):
            query = choice[len("kb search "):].strip()
            try:
                from agentcoach.kb.store import KnowledgeStore
                kb = KnowledgeStore()
                results = kb.search(query, limit=3)
                if results:
                    for i, r in enumerate(results, 1):
                        print(f"\n--- Result {i} [{r['source']} > {r['section']}] ---")
                        print(r['content'][:300])
                else:
                    print("No results found.")
                print()
            except Exception as e:
                print(f"Error: {e}")
            continue

        # Try to parse as domain number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(domains):
                domain = domains[idx]
            else:
                print("Invalid choice.")
                continue
        except ValueError:
            print("Invalid choice.")
            continue

        # Now select mode
        print(f"\nDomain: {syllabus.get_domain_name(domain)}")
        print("Modes:")
        print("  L. Learn — study resources + quick quiz")
        print("  R. Reinforce — strengthen weak topics")
        print("  M. Mock — full interview simulation")
        print("  (or 'back' to return)")
        print()

        try:
            mode_choice = input("Select mode (L/R/M): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return None, None, None

        if mode_choice == "back":
            continue

        mode_map = {"l": "learn", "r": "reinforce", "m": "mock"}
        mode = mode_map.get(mode_choice)
        if not mode:
            print("Invalid mode.")
            continue

        # For learn/reinforce, pick a topic
        topic = None
        if mode in ("learn", "reinforce"):
            topics = syllabus.get_topics(domain)
            rec = recommender.recommend(user_id, topics)
            print(f"\nCoach suggests: {rec['topic_name']} ({rec['reason']})")
            print("Topics:")
            for i, t in enumerate(topics, 1):
                mastery = analytics.get_mastery(user_id, t["id"])
                icon = "?" if mastery == 0 else ("X" if mastery < 40 else ("~" if mastery < 70 else "+"))
                score_str = f"{mastery}%" if mastery > 0 else "--"
                print(f"  {i}. [{icon}] {t['name']} {score_str}")
            print()
            try:
                topic_choice = input("Select topic (number, or Enter for suggestion): ").strip()
            except (KeyboardInterrupt, EOFError):
                return None, None, None

            if not topic_choice:
                topic = syllabus.get_topic(rec["topic_id"])
            else:
                try:
                    tidx = int(topic_choice) - 1
                    if 0 <= tidx < len(topics):
                        topic = topics[tidx]
                    else:
                        print("Invalid choice.")
                        continue
                except ValueError:
                    print("Invalid choice.")
                    continue

        return domain, mode, topic


def _show_progress(syllabus, analytics, user_id, domain):
    """Display mastery progress for a domain."""
    topics = syllabus.get_topics(domain)
    name = syllabus.get_domain_name(domain)
    print(f"\n=== {name} Progress ===")
    total_mastery = 0
    scored_count = 0
    for t in topics:
        mastery = analytics.get_mastery(user_id, t["id"])
        icon = "?" if mastery == 0 else ("X" if mastery < 40 else ("~" if mastery < 70 else "+"))
        score_str = f"{mastery}%" if mastery > 0 else "--"
        print(f"  [{icon}] {t['name']:30s} {score_str}")
        total_mastery += mastery
        if mastery > 0:
            scored_count += 1
    avg = total_mastery // len(topics) if topics else 0
    print(f"Overall: {avg}% ({scored_count}/{len(topics)} topics started)\n")


def _score_and_save(coach, analytics, user_id, topic, mode, llm):
    """Score the session and save results if there was enough conversation."""
    if len(coach.history) > 4:
        try:
            from agentcoach.analytics.scorer import Scorer
            print("Analyzing session performance...")
            scorer = Scorer(llm)
            topic_id = topic["id"] if topic else ""
            scores = scorer.score_session(coach.history, mode=mode, topic_id=topic_id)
            if scores:
                print("\n--- Session Scores ---")
                for s in scores:
                    analytics.record_score(user_id, s["topic_id"], s["score_delta"], mode, s["evidence"])
                    sign = "+" if s["score_delta"] > 0 else ""
                    print(f"  {s['topic_id']}: {sign}{s['score_delta']} — {s['evidence']}")
                print()
        except Exception as e:
            print(f"(Scoring error: {e})")


def _run_session(coach, mem, tts, analytics, user_id, topic, mode, llm):
    """Run an interactive session until user quits."""
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            _end_session(coach, mem)
            _score_and_save(coach, analytics, user_id, topic, mode, llm)
            print("\nSession ended.")
            return

        if not user_input:
            continue
        if user_input.lower() in ("quit", "done", "exit"):
            _end_session(coach, mem)
            _score_and_save(coach, analytics, user_id, topic, mode, llm)
            print("Session ended.")
            return
        if user_input.lower() == "memory":
            ctx = mem.get_context()
            print(f"\n{ctx}\n" if ctx else "No memory stored yet.\n")
            continue

        response = coach.respond(user_input)
        print(f"\nCoach: {response}\n")
        _speak(tts, response)


def main():
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "minimax")
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    model = os.getenv("LLM_MODEL", "")

    if not api_key:
        print("Error: Set LLM_API_KEY in .env")
        sys.exit(1)

    # Initialize TTS
    tts_engine_name = os.getenv("TTS_ENGINE", "macos")  # macos, qwen, none
    tts = None
    if tts_engine_name == "macos":
        from agentcoach.voice.tts import MacOSTTS
        tts = MacOSTTS(voice=os.getenv("TTS_VOICE", "Samantha"))
    elif tts_engine_name == "qwen":
        from agentcoach.voice.tts import QwenTTS
        tts = QwenTTS(lazy=True)
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

    # Initialize KB
    from agentcoach.kb.store import KnowledgeStore
    kb = KnowledgeStore(use_vectors=False)
    try:
        kb_stats = kb.get_stats()
        kb_active = kb if kb_stats["total_chunks"] > 0 else None
    except Exception:
        kb_active = None

    print("=== AgentCoach — AI Mock Interview Coach ===")
    print(f"Provider: {provider} | TTS: {tts_engine_name}")
    if kb_active:
        print(f"Knowledge Base: {kb_stats['total_chunks']} chunks")
    print()

    # Main menu loop
    while True:
        domain, mode, topic = _show_menu(syllabus, analytics, recommender, user_id, mem=mem)
        if domain is None:
            break  # user quit

        # Create LLM
        if provider == "gemini":
            from agentcoach.llm.gemini import GeminiAdapter
            llm = GeminiAdapter(api_key=api_key, model=model or "gemini-2.0-flash")
        else:
            from agentcoach.llm.openai_compat import OpenAICompatAdapter
            llm = OpenAICompatAdapter(api_key=api_key, provider=provider, model=model)

        # Build mode-specific system prompt hint
        mode_hint = ""
        if mode == "learn" and topic:
            resources = syllabus.get_resources(topic["id"])
            res_text = "\n".join(f"  - [{r['type']}] {r['title']}: {r.get('url', 'N/A')}" for r in resources)
            mode_hint = f"\nMode: Learn — Topic: {topic['name']}\nFirst show these resources, then quiz with 3-5 questions:\n{res_text}"
        elif mode == "reinforce" and topic:
            mastery = analytics.get_mastery(user_id, topic["id"])
            mode_hint = f"\nMode: Reinforce — Topic: {topic['name']} (current mastery: {mastery}%)\nAsk increasingly difficult follow-up questions on this specific topic."
        elif mode == "mock":
            mode_hint = f"\nMode: Mock Interview — Domain: {syllabus.get_domain_name(domain)}\nConduct a full realistic interview simulation."

        # Map to prompt template key
        if mode == "mock":
            prompt_mode = f"mock_{domain}"
        elif mode in ("learn", "reinforce"):
            prompt_mode = mode
        else:
            prompt_mode = "behavioral"

        coach = Coach(
            llm=llm,
            mode=prompt_mode,
            memory_context=mem.get_context() + mode_hint,
            kb_store=kb_active,
        )

        # Run session
        opening = coach.start()
        print(f"\nCoach: {opening}\n")
        _speak(tts, opening)

        _run_session(coach, mem, tts, analytics, user_id, topic, mode, llm)
        print()  # blank line before returning to menu


if __name__ == "__main__":
    main()
