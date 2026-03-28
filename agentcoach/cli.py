import os
import sys
from dotenv import load_dotenv
from agentcoach.coach import Coach


def main():
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "minimax")
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    model = os.getenv("LLM_MODEL", "")

    if not api_key:
        print("Error: Set LLM_API_KEY in .env")
        sys.exit(1)

    print("=== AgentCoach — AI Mock Interview Coach ===")
    print(f"Provider: {provider}")
    print("Mode: Behavioral Interview")
    print("Type 'quit' to exit")
    print()

    if provider == "gemini":
        from agentcoach.llm.gemini import GeminiAdapter
        llm = GeminiAdapter(api_key=api_key, model=model or "gemini-2.0-flash")
    else:
        from agentcoach.llm.openai_compat import OpenAICompatAdapter
        llm = OpenAICompatAdapter(api_key=api_key, provider=provider, model=model)
    coach = Coach(llm=llm, mode="behavioral")

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

        response = coach.respond(user_input)
        print(f"\nCoach: {response}\n")


if __name__ == "__main__":
    main()
