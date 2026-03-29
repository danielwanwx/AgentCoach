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
    # tts_engine_name == "none" → tts stays None

    if tts:
        from agentcoach.voice.tts import AsyncTTSWrapper
        tts = AsyncTTSWrapper(tts)

    # Initialize memory and load context
    mem = CoachMemory()
    memory_context = mem.get_context()

    # Initialize KB store
    from agentcoach.kb.store import KnowledgeStore
    kb = KnowledgeStore(use_vectors=False)  # Start with FTS only, vector optional
    try:
        kb_stats = kb.get_stats()
        if kb_stats["total_chunks"] > 0:
            kb_active = kb
            print(f"Knowledge Base: {kb_stats['total_chunks']} chunks loaded")
        else:
            kb_active = None
    except Exception:
        kb_active = None

    print("=== AgentCoach — AI Mock Interview Coach ===")
    print(f"Provider: {provider}")
    print(f"TTS: {tts_engine_name}")
    print("Mode: Behavioral Interview")
    print("Type 'quit' to exit")
    print("Commands: 'import profile <text>', 'import jd <text>', 'load resume <file>', 'load jd <file>',")
    print("          'load kb <dir> [category]', 'kb stats', 'kb search <query>', 'memory', 'voice on', 'voice off'")
    print()

    if provider == "gemini":
        from agentcoach.llm.gemini import GeminiAdapter
        llm = GeminiAdapter(api_key=api_key, model=model or "gemini-2.0-flash")
    else:
        from agentcoach.llm.openai_compat import OpenAICompatAdapter
        llm = OpenAICompatAdapter(api_key=api_key, provider=provider, model=model)
    coach = Coach(llm=llm, mode="behavioral", memory_context=memory_context, kb_store=kb_active)

    # Start interview
    opening = coach.start()
    print(f"Coach: {opening}\n")
    _speak(tts, opening)

    def _end_session(coach, mem):
        """Generate and save feedback if there was meaningful conversation."""
        if len(coach.history) > 2:
            print("\nGenerating session feedback...")
            feedback = coach.get_feedback_summary()
            if feedback:
                print(f"\n{feedback}\n")
                mem.save_feedback(feedback)
                print("Feedback saved to memory.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            _end_session(coach, mem)
            print("\nSession ended.")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            _end_session(coach, mem)
            print("Session ended. Good luck with your interviews!")
            break

        if user_input.lower().startswith("import profile "):
            text = user_input[len("import profile "):].strip()
            mem.save_profile(text)
            print("Profile saved to memory.")
            continue

        if user_input.lower().startswith("import jd "):
            text = user_input[len("import jd "):].strip()
            mem.save_jd(text)
            print("JD saved to memory.")
            continue

        if user_input.lower() == "memory":
            ctx = mem.get_context()
            if ctx:
                print(f"\n{ctx}\n")
            else:
                print("No memory stored yet.\n")
            continue

        if user_input.lower().startswith("load resume "):
            filepath = user_input[len("load resume "):].strip()
            try:
                from agentcoach.memory.importer import import_file
                content = import_file(filepath)
                mem.save_profile(content)
                print(f"Resume loaded from {filepath} and saved to memory.")
            except FileNotFoundError as e:
                print(f"Error: {e}")
            continue

        if user_input.lower().startswith("load jd "):
            filepath = user_input[len("load jd "):].strip()
            try:
                from agentcoach.memory.importer import import_file
                content = import_file(filepath)
                mem.save_jd(content)
                print(f"JD loaded from {filepath} and saved to memory.")
            except FileNotFoundError as e:
                print(f"Error: {e}")
            continue

        if user_input.lower().startswith("load kb "):
            parts = user_input[len("load kb "):].strip().split(maxsplit=1)
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

        if user_input.lower() == "kb stats":
            try:
                from agentcoach.kb.store import KnowledgeStore
                kb = KnowledgeStore()
                stats = kb.get_stats()
                print(f"\nKnowledge Base: {stats['total_chunks']} chunks, {stats['total_sources']} sources")
                print(f"Categories: {', '.join(stats['categories']) if stats['categories'] else 'none'}\n")
            except Exception as e:
                print(f"Error: {e}")
            continue

        if user_input.lower().startswith("kb search "):
            query = user_input[len("kb search "):].strip()
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

        if user_input.lower() == "voice on":
            if not tts:
                from agentcoach.voice.tts import MacOSTTS, AsyncTTSWrapper
                tts = AsyncTTSWrapper(MacOSTTS())
            print("Voice enabled.")
            continue

        if user_input.lower() == "voice off":
            tts = None
            print("Voice disabled.")
            continue

        response = coach.respond(user_input)
        print(f"\nCoach: {response}\n")
        _speak(tts, response)


if __name__ == "__main__":
    main()
