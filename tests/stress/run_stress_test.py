#!/usr/bin/env python3
"""Entry point for AgentCoach stress tests.

Usage:
    python3 tests/stress/run_stress_test.py --scenario 1
    python3 tests/stress/run_stress_test.py --scenario 1 --no-voice --min-turns 2
    python3 tests/stress/run_stress_test.py --all --no-voice
"""
import argparse
import sys
import os

# Ensure project root is on sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from tests.stress.scenarios import SCENARIOS
from tests.stress.stress_runner import run_scenario, generate_report


def main():
    parser = argparse.ArgumentParser(description="AgentCoach Stress Test Runner")
    parser.add_argument(
        "--scenario", type=int, default=None,
        help="Run a specific scenario (1-8). Omit to list scenarios.",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Run all 8 scenarios sequentially.",
    )
    parser.add_argument(
        "--no-voice", action="store_true",
        help="Disable macOS TTS voice output.",
    )
    parser.add_argument(
        "--min-turns", type=int, default=None,
        help="Override the minimum number of conversation turns.",
    )
    args = parser.parse_args()

    voice = not args.no_voice

    # List scenarios if no selection made
    if args.scenario is None and not args.all:
        print("Available scenarios:")
        for i, s in enumerate(SCENARIOS, 1):
            print(f"  {i}. {s.name} [{s.mode}] -- {s.topic_id} ({s.min_turns} turns)")
        print(f"\nUsage: python3 {sys.argv[0]} --scenario N [--no-voice] [--min-turns N]")
        return

    # Determine which scenarios to run
    if args.all:
        to_run = list(enumerate(SCENARIOS, 1))
    else:
        idx = args.scenario
        if idx < 1 or idx > len(SCENARIOS):
            print(f"Error: scenario must be 1-{len(SCENARIOS)}, got {idx}")
            sys.exit(1)
        to_run = [(idx, SCENARIOS[idx - 1])]

    # Run scenarios
    results = []
    for num, scenario in to_run:
        print(f"\n>>> Running scenario {num}/{len(SCENARIOS)}: {scenario.name}")
        try:
            result = run_scenario(
                scenario,
                voice=voice,
                min_turns_override=args.min_turns,
            )
            results.append(result)
        except Exception as e:
            print(f"  FAILED: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                "scenario": scenario.name,
                "topic_id": scenario.topic_id,
                "mode": scenario.mode,
                "company": scenario.company,
                "turns": 0,
                "elapsed_seconds": 0,
                "history_length": 0,
                "scores": [],
                "quality": {"overall": 0, "notes": f"FAILED: {e}"},
            })

    # Generate report
    if results:
        report_path = generate_report(results)
        print(f"\nDone. {len(results)} scenario(s) completed.")
        print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
