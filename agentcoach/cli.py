import os
import sys
from dotenv import load_dotenv
from agentcoach.coach import Coach
from agentcoach.memory.store import CoachMemory


def main():
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "minimax")
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    model = os.getenv("LLM_MODEL", "")

    if not api_key:
        print("Error: Set LLM_API_KEY in .env")
        sys.exit(1)

    # Initialize memory and load context
    mem = CoachMemory()
    memory_context = mem.get_context()

    print("=== AgentCoach — AI Mock Interview Coach ===")
    print(f"Provider: {provider}")
    print("Mode: Behavioral Interview")
    print("Type 'quit' to exit")
    print("Commands: 'import profile <text>', 'import jd <text>', 'load resume <file>', 'load jd <file>', 'memory'")
    print()

    if provider == "gemini":
        from agentcoach.llm.gemini import GeminiAdapter
        llm = GeminiAdapter(api_key=api_key, model=model or "gemini-2.0-flash")
    else:
        from agentcoach.llm.openai_compat import OpenAICompatAdapter
        llm = OpenAICompatAdapter(api_key=api_key, provider=provider, model=model)
    coach = Coach(llm=llm, mode="behavioral", memory_context=memory_context)

    # Start interview
    opening = coach.start()
    print(f"Coach: {opening}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
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

        response = coach.respond(user_input)
        print(f"\nCoach: {response}\n")


if __name__ == "__main__":
    main()
