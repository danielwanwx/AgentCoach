#!/usr/bin/env python3
"""Scrape free HelloInterview pages and save as markdown."""
import browser_cookie3
import json
import os
import re
import sys
import time
from playwright.sync_api import sync_playwright

URLS = [
    # In a Hurry (overview pages)
    "https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction",
    "https://www.hellointerview.com/learn/system-design/in-a-hurry/how-to-prepare",
    "https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery",
    "https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts",
    "https://www.hellointerview.com/learn/system-design/in-a-hurry/key-technologies",
    "https://www.hellointerview.com/learn/system-design/in-a-hurry/patterns",
    "https://www.hellointerview.com/learn/system-design/in-a-hurry/problem-breakdowns",
    # Core Concepts (individual)
    "https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials",
    "https://www.hellointerview.com/learn/system-design/core-concepts/api-design",
    "https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling",
    "https://www.hellointerview.com/learn/system-design/core-concepts/caching",
    "https://www.hellointerview.com/learn/system-design/core-concepts/sharding",
    "https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing",
    "https://www.hellointerview.com/learn/system-design/core-concepts/cap-theorem",
    "https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing",
    "https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know",
    # Patterns
    "https://www.hellointerview.com/learn/system-design/patterns/realtime-updates",
    "https://www.hellointerview.com/learn/system-design/patterns/dealing-with-contention",
    "https://www.hellointerview.com/learn/system-design/patterns/multi-step-processes",
    "https://www.hellointerview.com/learn/system-design/patterns/scaling-reads",
    "https://www.hellointerview.com/learn/system-design/patterns/scaling-writes",
    "https://www.hellointerview.com/learn/system-design/patterns/large-blobs",
    "https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks",
    # Deep Dives (technologies)
    "https://www.hellointerview.com/learn/system-design/deep-dives/redis",
    "https://www.hellointerview.com/learn/system-design/deep-dives/elasticsearch",
    "https://www.hellointerview.com/learn/system-design/deep-dives/kafka",
    "https://www.hellointerview.com/learn/system-design/deep-dives/api-gateway",
    "https://www.hellointerview.com/learn/system-design/deep-dives/cassandra",
    "https://www.hellointerview.com/learn/system-design/deep-dives/dynamodb",
    "https://www.hellointerview.com/learn/system-design/deep-dives/postgres",
    "https://www.hellointerview.com/learn/system-design/deep-dives/flink",
    "https://www.hellointerview.com/learn/system-design/deep-dives/zookeeper",
    "https://www.hellointerview.com/learn/system-design/deep-dives/time-series-databases",
    "https://www.hellointerview.com/learn/system-design/deep-dives/data-structures-for-big-data",
    "https://www.hellointerview.com/learn/system-design/deep-dives/vector-databases",
    # Problem Breakdowns
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-news",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/yelp",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/strava",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-auction",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/camelcamelcamel",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-docs",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-cache",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system",
    "https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring",
]

OUT_DIR = "/Users/javiswan/Projects/Her/kb/hellointerview"

EXTRACT_JS = '''() => {
    // Check for paywall
    const hasBlur = !!document.querySelector('[class*="blur"], [class*="locked"], [class*="paywall"]');
    const bodyText = document.body.innerText;
    const hasPremiumWall = bodyText.includes("Purchase Premium to Keep Reading") || bodyText.includes("Upgrade to unlock");

    // Extract article content
    const selectors = ['article', 'main', '.prose', '.content', '[role="main"]'];
    let content = "";
    for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el && el.innerText.trim().length > 500) {
            content = el.innerText.trim();
            break;
        }
    }
    if (!content) content = document.body.innerText.trim();

    // Extract headings for structure
    const headings = Array.from(document.querySelectorAll('h1,h2,h3,h4')).map(h => ({
        level: parseInt(h.tagName[1]),
        text: h.innerText.trim()
    }));

    const title = document.querySelector('h1')?.innerText?.trim() || document.title;

    return {
        title: title,
        content: content,
        headings: headings,
        is_paywalled: hasBlur || hasPremiumWall,
        char_count: content.length,
    };
}'''


def url_to_filename(url):
    # /learn/system-design/core-concepts/caching -> core-concepts_caching.md
    path = url.split("/learn/system-design/")[-1]
    return path.replace("/", "_") + ".md"


def content_to_markdown(data, url):
    """Convert extracted content to clean markdown."""
    lines = []
    lines.append(f"# {data['title']}")
    lines.append(f"\n> Source: {url}")
    lines.append(f"> Scraped: {time.strftime('%Y-%m-%d')}")
    lines.append("")

    # Clean content: remove nav/footer boilerplate
    content = data["content"]

    # Remove everything before the first heading that matches our title
    title_lower = data["title"].lower()
    content_lines = content.split("\n")
    start_idx = 0
    for i, line in enumerate(content_lines):
        if line.strip().lower() == title_lower:
            start_idx = i
            break

    # Remove footer (starts with "Questions\nMeta SWE" or similar)
    end_idx = len(content_lines)
    for i, line in enumerate(content_lines):
        if line.strip() in ("Questions", "Comments") and i > start_idx + 10:
            # Check if next lines look like footer
            remaining = "\n".join(content_lines[i:i+5])
            if "SWE Interview" in remaining or "Schedule a mock" in remaining or "Learn System Design" in remaining:
                end_idx = i
                break

    clean = "\n".join(content_lines[start_idx:end_idx]).strip()
    lines.append(clean)

    return "\n".join(lines)


def main():
    # Load cookies
    print("Extracting Chrome cookies...")
    cj = browser_cookie3.chrome()
    hi_cookies = [c for c in cj if "hellointerview" in c.domain]
    print(f"  {len(hi_cookies)} HelloInterview cookies found")

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context()

    for c in hi_cookies:
        try:
            ctx.add_cookies([{
                "name": c.name, "value": c.value,
                "domain": c.domain, "path": c.path or "/",
            }])
        except:
            pass

    page = ctx.new_page()

    results = {"free": [], "paywalled": [], "error": []}

    for i, url in enumerate(URLS):
        fname = url_to_filename(url)
        print(f"[{i+1}/{len(URLS)}] {fname}...", end=" ", flush=True)

        try:
            page.goto(url, timeout=20000)
            page.wait_for_load_state("networkidle", timeout=15000)

            data = page.evaluate(EXTRACT_JS)

            if data["is_paywalled"]:
                print(f"PAYWALLED ({data['char_count']} chars)")
                results["paywalled"].append(fname)
                continue

            if data["char_count"] < 500:
                print(f"TOO SHORT ({data['char_count']} chars)")
                results["error"].append(fname)
                continue

            md = content_to_markdown(data, url)
            outpath = os.path.join(OUT_DIR, fname)
            with open(outpath, "w") as f:
                f.write(md)

            print(f"OK ({data['char_count']} chars)")
            results["free"].append(fname)

        except Exception as e:
            print(f"ERROR: {e}")
            results["error"].append(fname)

        time.sleep(0.5)  # Be polite

    browser.close()
    pw.stop()

    # Summary
    print("\n" + "=" * 60)
    print(f"FREE: {len(results['free'])} pages saved")
    print(f"PAYWALLED: {len(results['paywalled'])} pages skipped")
    print(f"ERRORS: {len(results['error'])} pages failed")

    if results["paywalled"]:
        print("\nPaywalled pages:")
        for p in results["paywalled"]:
            print(f"  - {p}")

    # Save manifest
    manifest_path = os.path.join(OUT_DIR, "_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nManifest saved to {manifest_path}")


if __name__ == "__main__":
    main()
