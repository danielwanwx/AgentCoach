#!/usr/bin/env python3
"""
Live Interview Simulation - Real-time conversation between Coach and Candidate.

Coach: Gemma4 as Senior SDE Interviewer
Candidate: Gemma4 as SDE candidate (real-time response based on coach's questions)

Features:
- 10+ rounds of dynamic conversation
- macOS TTS for audio playback
- Performance metrics (latency, quality)
- Final comprehensive evaluation
"""
import subprocess
import time
import sys
import os
import json
from dataclasses import dataclass, field
from typing import List

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class Turn:
    """Single conversation turn."""
    role: str
    content: str
    latency_ms: float
    timestamp: float


@dataclass
class InterviewSession:
    """Track the entire interview session."""
    topic: str
    turns: List[Turn] = field(default_factory=list)
    start_time: float = 0
    end_time: float = 0

    def add_turn(self, role: str, content: str, latency_ms: float):
        self.turns.append(Turn(
            role=role,
            content=content,
            latency_ms=latency_ms,
            timestamp=time.time()
        ))

    def get_conversation_history(self) -> str:
        """Get formatted conversation history for context."""
        history = []
        for turn in self.turns:
            history.append(f"{turn.role}: {turn.content}")
        return "\n\n".join(history)


class MacOSTTS:
    """macOS Text-to-Speech."""
    def __init__(self, voice: str = "Samantha", rate: int = 175):
        self.voice = voice
        self.rate = rate

    def speak(self, text: str, voice_override: str = None):
        voice = voice_override or self.voice
        # Clean text for TTS
        clean = text.replace('"', '').replace('`', '').replace('*', '')
        subprocess.run(
            ["say", "-v", voice, "-r", str(self.rate), clean],
            check=False,
        )


def call_llm(prompt: str, system_prompt: str = "") -> tuple[str, float]:
    """Call Gemma4 and return (response, latency_ms)."""
    start = time.time()

    full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

    result = subprocess.run(
        ["ollama", "run", "gemma4:31b", full_prompt],
        capture_output=True,
        text=True,
        timeout=180,
    )

    latency_ms = (time.time() - start) * 1000
    response = result.stdout.strip()

    # Remove thinking section if present
    if "...done thinking." in response:
        response = response.split("...done thinking.")[-1].strip()

    return response, latency_ms


def run_interview():
    """Run the live interview simulation."""
    print("=" * 70)
    print("  LIVE INTERVIEW SIMULATION")
    print("  Coach (Interviewer) vs Candidate - System Design Interview")
    print("=" * 70)
    print()

    # Initialize
    tts = MacOSTTS(voice="Samantha", rate=170)
    session = InterviewSession(topic="System Design: Design a Rate Limiter")
    session.start_time = time.time()

    # System prompts
    COACH_SYSTEM = """You are a Senior SDE interviewer at a top tech company conducting a system design interview.
You are interviewing a candidate for a Senior SDE position.
Topic: Design a Rate Limiter

Rules:
- Ask focused, probing questions
- Follow up on the candidate's answers
- Challenge assumptions when appropriate
- Keep responses concise (2-3 sentences max)
- Be professional but rigorous
- Progress through: requirements -> high-level design -> deep dives -> trade-offs

Current conversation history will be provided. Continue the interview naturally."""

    CANDIDATE_SYSTEM = """You are an experienced SDE candidate interviewing for a Senior SDE position.
You are in a system design interview about designing a Rate Limiter.

Rules:
- Answer thoughtfully and technically
- Show your thought process
- Be concise but thorough (3-5 sentences)
- Ask clarifying questions when needed
- Demonstrate senior-level thinking
- Be honest if you need to think about something

Current conversation history will be provided. Respond naturally to the interviewer's latest question."""

    # Interview rounds
    MIN_ROUNDS = 12
    round_num = 0

    # Opening
    print("\n[Starting Interview...]\n")
    opening = "Welcome to your system design interview. Today we'll be designing a Rate Limiter. This is a common component in distributed systems. Before we dive in, could you tell me what you understand about rate limiting and why it's important?"

    print(f"[COACH]: {opening}")
    tts.speak(opening)
    session.add_turn("COACH", opening, 0)

    while round_num < MIN_ROUNDS:
        round_num += 1
        print(f"\n{'─' * 50}")
        print(f"Round {round_num}")
        print(f"{'─' * 50}")

        # Candidate responds
        history = session.get_conversation_history()
        candidate_prompt = f"""Conversation so far:
{history}

Now respond to the interviewer's latest question/comment. Be a strong Senior SDE candidate."""

        print("\n[Candidate thinking...]")
        candidate_response, candidate_latency = call_llm(candidate_prompt, CANDIDATE_SYSTEM)

        print(f"\n[CANDIDATE] ({candidate_latency:.0f}ms): {candidate_response}")
        tts.speak(candidate_response, voice_override="Daniel")  # British voice for candidate
        session.add_turn("CANDIDATE", candidate_response, candidate_latency)

        # Small pause
        time.sleep(1)

        # Coach responds
        history = session.get_conversation_history()

        # Add progression hints based on round
        progression = ""
        if round_num == 3:
            progression = "\n\nNote: Move to high-level architecture discussion."
        elif round_num == 6:
            progression = "\n\nNote: Start deep dive into a specific component."
        elif round_num == 9:
            progression = "\n\nNote: Discuss trade-offs and edge cases."
        elif round_num == 11:
            progression = "\n\nNote: Wrap up with final questions."

        coach_prompt = f"""Conversation so far:
{history}
{progression}

Continue the interview. Ask a follow-up question or probe deeper based on the candidate's response."""

        print("\n[Coach thinking...]")
        coach_response, coach_latency = call_llm(coach_prompt, COACH_SYSTEM)

        print(f"\n[COACH] ({coach_latency:.0f}ms): {coach_response}")
        tts.speak(coach_response)
        session.add_turn("COACH", coach_response, coach_latency)

        time.sleep(0.5)

    # Final evaluation
    session.end_time = time.time()

    print("\n")
    print("=" * 70)
    print("  INTERVIEW COMPLETE - GENERATING EVALUATION")
    print("=" * 70)

    # Get comprehensive evaluation from Gemma4
    eval_prompt = f"""You just conducted a Senior SDE system design interview. Here is the full transcript:

{session.get_conversation_history()}

Provide a comprehensive evaluation with:

1. **Overall Score**: X/10

2. **Technical Depth** (1-10):
   - Score and brief justification

3. **Communication** (1-10):
   - Score and brief justification

4. **Problem Solving** (1-10):
   - Score and brief justification

5. **Senior-Level Thinking** (1-10):
   - Score and brief justification

6. **Key Strengths**:
   - List 3 strengths

7. **Areas for Improvement**:
   - List 3 areas

8. **Hire Recommendation**: Strong Hire / Hire / Lean Hire / Lean No Hire / No Hire

Be honest and rigorous in your evaluation."""

    print("\n[Generating evaluation...]")
    evaluation, eval_latency = call_llm(eval_prompt)

    print("\n" + "─" * 70)
    print("CANDIDATE EVALUATION")
    print("─" * 70)
    print(evaluation)

    # Performance metrics
    print("\n" + "─" * 70)
    print("PERFORMANCE METRICS")
    print("─" * 70)

    total_duration = session.end_time - session.start_time
    coach_turns = [t for t in session.turns if t.role == "COACH"]
    candidate_turns = [t for t in session.turns if t.role == "CANDIDATE"]

    coach_latencies = [t.latency_ms for t in coach_turns if t.latency_ms > 0]
    candidate_latencies = [t.latency_ms for t in candidate_turns]

    print(f"""
Interview Statistics:
  Total Duration:      {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)
  Total Rounds:        {round_num}
  Coach Turns:         {len(coach_turns)}
  Candidate Turns:     {len(candidate_turns)}

Latency Analysis:
  Coach Avg Latency:      {sum(coach_latencies)/len(coach_latencies):.0f}ms
  Coach Min Latency:      {min(coach_latencies):.0f}ms
  Coach Max Latency:      {max(coach_latencies):.0f}ms

  Candidate Avg Latency:  {sum(candidate_latencies)/len(candidate_latencies):.0f}ms
  Candidate Min Latency:  {min(candidate_latencies):.0f}ms
  Candidate Max Latency:  {max(candidate_latencies):.0f}ms

Model Used: Gemma4:31b (19GB)
TTS Engine: macOS (Samantha + Daniel)
""")

    # Speak summary
    summary = f"Interview complete. The candidate received an overall evaluation. Total interview time was {total_duration/60:.1f} minutes with {round_num} rounds of discussion."
    tts.speak(summary)

    print("=" * 70)
    print("  SIMULATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_interview()
