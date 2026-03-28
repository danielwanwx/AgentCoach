import os
import sys
from dotenv import load_dotenv
from agentcoach.llm.gemini import GeminiAdapter
from agentcoach.coach import Coach


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Set GEMINI_API_KEY in .env or environment")
        sys.exit(1)

    print("=== AgentCoach — AI Mock Interview Coach ===")
    print("Mode: Behavioral Interview")
    print("Type 'quit' to exit, 'feedback' for session summary")
    print()

    llm = GeminiAdapter(api_key=api_key)
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
