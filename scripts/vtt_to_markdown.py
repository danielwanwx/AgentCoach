#!/usr/bin/env python3
"""Convert VTT subtitle files to clean markdown transcripts."""
import os
import re
import glob

VTT_DIR = "/Users/javiswan/Projects/Her/kb/hellointerview-youtube"
OUT_DIR = "/Users/javiswan/Projects/Her/kb/hellointerview-youtube/transcripts"


def parse_vtt(filepath):
    """Parse VTT file, deduplicate lines, return clean text."""
    with open(filepath, "r") as f:
        content = f.read()

    # Remove VTT header
    content = re.sub(r'^WEBVTT\n.*?\n\n', '', content, flags=re.DOTALL)

    # Extract text lines (skip timestamps and positioning)
    lines = []
    seen = set()
    for block in content.split("\n\n"):
        text_lines = []
        for line in block.strip().split("\n"):
            # Skip timestamps and position tags
            if re.match(r'^\d{2}:\d{2}', line):
                continue
            if line.startswith("align:") or line.startswith("position:"):
                continue
            # Clean HTML tags
            clean = re.sub(r'<[^>]+>', '', line).strip()
            if clean and clean not in seen:
                seen.add(clean)
                text_lines.append(clean)
        lines.extend(text_lines)

    return " ".join(lines)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    vtt_files = glob.glob(os.path.join(VTT_DIR, "*.vtt"))
    print(f"Processing {len(vtt_files)} VTT files...")

    for vtt_path in sorted(vtt_files):
        fname = os.path.basename(vtt_path)
        # Extract title and video ID
        match = re.match(r'(.+?)\s*\[([A-Za-z0-9_-]+)\]\.en\.vtt$', fname)
        if match:
            title = match.group(1).strip()
            video_id = match.group(2)
        else:
            title = fname.replace(".en.vtt", "")
            video_id = ""

        transcript = parse_vtt(vtt_path)
        if len(transcript) < 100:
            print(f"  SKIP (too short): {title}")
            continue

        # Create markdown
        md_name = re.sub(r'[^\w\s-]', '', title).strip().replace(" ", "-").lower()[:80] + ".md"
        md_path = os.path.join(OUT_DIR, md_name)

        yt_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else ""

        md_content = f"# {title}\n\n"
        md_content += f"> Source: HelloInterview YouTube\n"
        if yt_url:
            md_content += f"> Video: {yt_url}\n"
        md_content += f"> Type: Video Transcript\n\n"

        # Split transcript into paragraphs (~500 chars each for readability)
        words = transcript.split()
        paragraphs = []
        current = []
        char_count = 0
        for word in words:
            current.append(word)
            char_count += len(word) + 1
            if char_count > 500 and word.endswith(('.', '?', '!')):
                paragraphs.append(" ".join(current))
                current = []
                char_count = 0
        if current:
            paragraphs.append(" ".join(current))

        md_content += "\n\n".join(paragraphs)

        with open(md_path, "w") as f:
            f.write(md_content)

        print(f"  OK: {md_name} ({len(transcript)} chars)")

    print(f"\nDone. Transcripts in {OUT_DIR}")
    # Count
    md_files = glob.glob(os.path.join(OUT_DIR, "*.md"))
    total_chars = sum(os.path.getsize(f) for f in md_files)
    print(f"  {len(md_files)} transcripts, {total_chars/1024/1024:.1f} MB total")


if __name__ == "__main__":
    main()
