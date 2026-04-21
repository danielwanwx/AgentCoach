#!/usr/bin/env python3
"""Quick voice test - try different macOS voices."""
import subprocess
import sys

def test_voices():
    """Test different macOS voices with sample text."""
    voices = [
        ("Samantha", "en_US", "Hello! I'm Samantha, a clear American voice."),
        ("Daniel", "en_GB", "Hello! I'm Daniel, a British English voice."),
        ("Karen", "en_AU", "G'day mate! I'm Karen from Australia."),
        ("Moira", "en_IE", "Hello! I'm Moira, an Irish voice."),
    ]

    print("Testing macOS Voices for AgentCoach")
    print("=" * 50)

    for voice, locale, text in voices:
        print(f"\nTesting: {voice} ({locale})")
        result = subprocess.run(
            ["say", "-v", voice, "-r", "170", text],
            capture_output=True,
        )
        if result.returncode != 0:
            print(f"  -> Voice {voice} not available, skipping")
        else:
            print(f"  -> OK")

    # Interview sample
    print("\n" + "=" * 50)
    print("Interview Sample with Samantha:")
    print("=" * 50)

    interview_text = """
    Let's design a distributed cache system.
    First, tell me about the requirements.
    What kind of data will we be caching?
    What's our expected read to write ratio?
    """

    print(interview_text)
    subprocess.run(["say", "-v", "Samantha", "-r", "165", interview_text])

    print("\nVoice test complete!")


if __name__ == "__main__":
    test_voices()
