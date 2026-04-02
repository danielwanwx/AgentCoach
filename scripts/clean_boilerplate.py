#!/usr/bin/env python3
"""Strip nav sidebar and footer boilerplate from scraped HelloInterview markdown files."""
import os
import re
import glob

KB_DIR = "/Users/javiswan/Projects/Her/kb/hellointerview"

# Nav boilerplate patterns (lines to remove if found in sequence)
NAV_PATTERNS = [
    "Limited Time Offer",
    "Back to Main",
    "LEARN SYSTEM DESIGN",
    "LEARN ML SYSTEM DESIGN",
    "LEARN LOW LEVEL DESIGN",
    "LEARN CODE",
    "LEARN BEHAVIORAL",
    "Daniel Wan",
    "Recognition",
    "Search\n⌘K",
    "Pricing",
    "Become a Coach",
    "Get Premium",
    "Tutor",
]

# Footer CTA patterns
FOOTER_PATTERNS = [
    "Schedule a mock interview",
    "Schedule A Mock Interview",
    "Meet with a FAANG",
    "Questions\nMeta SWE Interview",
    "Google SWE Interview Questions",
    "OpenAI SWE Interview Questions",
    "Engineering Manager (EM) Interview Questions",
    "Gift Mock Interviews",
    "Gift Premium",
    "Our Coaches",
    "Hello Interview Premium",
    "Terms and Conditions",
    "Privacy Policy",
    "Product Support",
    "7511 Greenwood Ave",
    "© 2026 Optick Labs",
    "Learn\nLearn System Design",
    "Learn System Design\nLearn DSA",
    "Learn DSA\nLearn Behavioral",
]


def clean_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    original_len = len(content)
    lines = content.split("\n")

    # Find the actual content start (after metadata lines)
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith("> Scraped:") or line.startswith("> Source:"):
            content_start = i + 1
            continue
        if i <= content_start + 1 and line.strip() == "":
            content_start = i + 1
            continue

    # Find where nav boilerplate ends (look for the actual title/content)
    # The pattern is: metadata -> nav junk -> actual content starting with title
    nav_end = content_start
    in_nav = False
    for i in range(content_start, min(content_start + 80, len(lines))):
        line = lines[i].strip()
        if any(pat in line for pat in NAV_PATTERNS):
            in_nav = True
            nav_end = i + 1
            continue
        # Skip empty lines in nav area
        if in_nav and line == "":
            nav_end = i + 1
            continue
        # If we hit nav-like short lines (menu items), keep skipping
        if in_nav and len(line) < 40 and not line.startswith("#"):
            nav_end = i + 1
            continue
        # Stop when we hit actual content (heading or long paragraph)
        if in_nav and (line.startswith("#") or len(line) > 80):
            break

    # Find footer start
    footer_start = len(lines)
    for i in range(len(lines) - 1, max(len(lines) - 60, 0), -1):
        line = lines[i].strip()
        if any(pat in line for pat in FOOTER_PATTERNS):
            footer_start = min(footer_start, i)

    # Also check for "Comments" section at the end (usually last section)
    for i in range(len(lines) - 1, max(len(lines) - 30, 0), -1):
        if lines[i].strip() == "Comments":
            footer_start = min(footer_start, i)
            break

    # Reconstruct: metadata + clean content
    metadata = lines[:content_start]
    clean_content = lines[nav_end:footer_start]

    # Strip trailing empty lines from clean content
    while clean_content and clean_content[-1].strip() == "":
        clean_content.pop()

    result = "\n".join(metadata + [""] + clean_content) + "\n"

    chars_removed = original_len - len(result)
    if chars_removed > 50:
        with open(filepath, "w") as f:
            f.write(result)
        return chars_removed
    return 0


def main():
    md_files = glob.glob(os.path.join(KB_DIR, "**/*.md"), recursive=True)
    # Exclude manifest
    md_files = [f for f in md_files if not f.endswith("_manifest.json")]

    total_cleaned = 0
    total_removed = 0

    for filepath in sorted(md_files):
        removed = clean_file(filepath)
        if removed > 0:
            total_cleaned += 1
            total_removed += removed
            rel = os.path.relpath(filepath, KB_DIR)
            if removed > 2000:
                print(f"  CLEANED {rel}: -{removed} chars")

    print(f"\nTotal: {total_cleaned}/{len(md_files)} files cleaned, {total_removed/1024:.0f} KB removed")


if __name__ == "__main__":
    main()
