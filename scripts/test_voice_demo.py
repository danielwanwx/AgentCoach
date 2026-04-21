#!/usr/bin/env python3
"""Test script for macOS TTS + Gemma4 interview demo."""
import subprocess
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentcoach.voice.tts import MacOSTTS


def call_gemma4(prompt: str) -> str:
    """Call Gemma4 via Ollama and return the response."""
    result = subprocess.run(
        ["ollama", "run", "gemma4:31b", prompt],
        capture_output=True,
        text=True,
        timeout=120,
    )
    # Clean up the response (remove thinking tags if present)
    response = result.stdout.strip()
    # Remove "Thinking..." section if present
    if "...done thinking." in response:
        response = response.split("...done thinking.")[-1].strip()
    return response


def main():
    print("=" * 60)
    print("  AgentCoach Voice Demo - macOS TTS + Gemma4")
    print("=" * 60)
    print()

    # Initialize TTS with Samantha voice (clear American English)
    tts = MacOSTTS(voice="Samantha", rate=170)

    # Demo conversations
    conversations = [
        {
            "topic": "System Design Interview",
            "coach_intro": "Welcome to your system design interview. Today we'll design a URL shortener like bit.ly. Let's start with the requirements.",
            "candidate_response": "I'll design a URL shortener. For requirements: we need to generate short URLs, redirect to original URLs, handle high traffic, and track analytics.",
            "followup_prompt": "As an interviewer, give a brief one-sentence follow-up question about handling high traffic for a URL shortener. Be concise.",
        },
        {
            "topic": "Behavioral Interview",
            "coach_intro": "Tell me about a time when you had to deal with a difficult technical decision.",
            "candidate_response": "In my last project, I had to choose between rewriting a legacy system or incrementally refactoring it. I chose incremental refactoring to reduce risk.",
            "followup_prompt": "As an interviewer, ask a brief one-sentence STAR follow-up question about what the outcome was. Be concise.",
        },
    ]

    for i, conv in enumerate(conversations, 1):
        print(f"\n--- Demo {i}: {conv['topic']} ---\n")

        # Coach intro
        print(f"[Coach]: {conv['coach_intro']}")
        tts.speak(conv['coach_intro'])

        # Simulated candidate response
        print(f"\n[Candidate]: {conv['candidate_response']}")

        # Get AI follow-up using Gemma4
        print("\n[Generating follow-up with Gemma4...]")
        followup = call_gemma4(conv['followup_prompt'])
        print(f"\n[Coach - Gemma4]: {followup}")
        tts.speak(followup)

        print()
        import time
        time.sleep(2)  # Brief pause between demos

    # Final summary
    summary = "Great job today! Remember: practice makes perfect. Keep working on your interview skills!"
    print(f"\n[Coach]: {summary}")
    tts.speak(summary)

    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
