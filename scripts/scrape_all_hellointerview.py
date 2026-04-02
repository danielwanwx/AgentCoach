#!/usr/bin/env python3
"""Scrape ALL HelloInterview Learn pages (Premium) and save as markdown."""
import browser_cookie3
import json
import os
import time
from collections import defaultdict
from playwright.sync_api import sync_playwright

OUT_BASE = "/Users/javiswan/Projects/Her/kb/hellointerview"

EXTRACT_JS = '''() => {
    const hasBlur = !!document.querySelector('[class*="blur"], [class*="locked"], [class*="paywall"]');
    const bodyText = document.body.innerText;
    const hasPremiumWall = bodyText.includes("Purchase Premium to Keep Reading") || bodyText.includes("Upgrade to unlock");

    const selectors = ['article', 'main', '.prose', '.content', '[role="main"]'];
    let content = "";
    for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el && el.innerText.trim().length > 300) { content = el.innerText.trim(); break; }
    }
    if (!content) content = document.body.innerText.trim();

    const title = document.querySelector('h1')?.innerText?.trim() || document.title;

    return {
        title: title,
        content: content,
        is_paywalled: hasBlur || hasPremiumWall,
        char_count: content.length,
    };
}'''


def discover_urls(page, section_name, entry_url):
    """Navigate to entry page and discover all sub-page URLs."""
    try:
        page.goto(entry_url, timeout=20000)
        page.wait_for_load_state("networkidle", timeout=15000)
    except:
        return []

    links = page.evaluate(f'''() => {{
        const anchors = document.querySelectorAll('a[href*="/learn/{section_name}"]');
        return [...new Set(Array.from(anchors).map(a => a.href))]
            .filter(h => !h.endsWith("/vote") && !h.endsWith("/") && h !== "{entry_url}")
            .sort();
    }}''')
    return links


def url_to_path(url, section):
    """Convert URL to file path: section/subsection_page.md"""
    path = url.split(f"/learn/{section}/")[-1] if f"/learn/{section}/" in url else url.split("/")[-1]
    return path.replace("/", "_") + ".md"


def scrape_page(page, url, out_dir, fname):
    """Scrape a single page. Returns status string."""
    try:
        page.goto(url, timeout=25000)
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception as e:
        return "timeout"

    try:
        data = page.evaluate(EXTRACT_JS)
    except:
        return "error"

    if data["is_paywalled"]:
        return "paywalled"
    if data["char_count"] < 300:
        return "too_short"

    # Clean content
    content = data["content"]
    title = data["title"]

    # Strip nav/footer boilerplate
    lines = content.split("\n")
    start = 0
    for i, line in enumerate(lines):
        if line.strip().lower() == title.lower():
            start = i
            break

    end = len(lines)
    for i, line in enumerate(lines):
        if i > start + 10 and line.strip() in ("Questions", "Comments"):
            remaining = "\n".join(lines[i:i+5])
            if "SWE Interview" in remaining or "Schedule a mock" in remaining:
                end = i
                break

    clean = "\n".join(lines[start:end]).strip()

    md = f"# {title}\n\n> Source: {url}\n> Scraped: {time.strftime('%Y-%m-%d')}\n\n{clean}"

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, fname), "w") as f:
        f.write(md)

    return f"ok:{data['char_count']}"


def main():
    print("Extracting Chrome cookies...")
    cj = browser_cookie3.chrome()
    hi_cookies = [c for c in cj if "hellointerview" in c.domain]
    print(f"  {len(hi_cookies)} cookies")

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context()
    for c in hi_cookies:
        try:
            ctx.add_cookies([{"name": c.name, "value": c.value, "domain": c.domain, "path": c.path or "/"}])
        except:
            pass

    page = ctx.new_page()

    # Define all sections
    sections = {
        "system-design": "https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction",
        "ml-system-design": "https://www.hellointerview.com/learn/ml-system-design/in-a-hurry/introduction",
        "low-level-design": "https://www.hellointerview.com/learn/low-level-design/in-a-hurry/introduction",
        "code": "https://www.hellointerview.com/learn/code",
        "behavioral": "https://www.hellointerview.com/learn/behavioral/course/why-the-behavioral-matters",
        "ai-coding": "https://www.hellointerview.com/learn/ai-coding/fundamentals/codebase-orientation",
        "salary-negotiation": "https://www.hellointerview.com/learn/salary-negotiation/introduction",
    }

    # Blog URLs (separately discovered)
    blog_urls = []

    all_results = {}
    total_saved = 0
    total_paywalled = 0
    total_errors = 0

    # Phase 1: Discover all URLs
    print("\n--- Phase 1: Discovering URLs ---")
    section_urls = {}
    for section, entry in sections.items():
        urls = discover_urls(page, section, entry)
        # Also include the entry URL itself
        urls = [entry] + [u for u in urls if u != entry]
        section_urls[section] = urls
        print(f"  {section}: {len(urls)} pages")

    # Discover blog
    try:
        page.goto("https://www.hellointerview.com/blog", timeout=20000)
        page.wait_for_load_state("networkidle", timeout=15000)
        blog_urls = page.evaluate('''() => {
            return [...new Set(Array.from(document.querySelectorAll('a[href*="/blog/"]')).map(a => a.href))].sort();
        }''')
        section_urls["blog"] = blog_urls
        print(f"  blog: {len(blog_urls)} posts")
    except:
        print("  blog: discovery failed")

    total_pages = sum(len(v) for v in section_urls.values())
    print(f"\nTotal: {total_pages} pages to scrape")

    # Phase 2: Scrape everything
    print("\n--- Phase 2: Scraping ---")
    page_num = 0

    # Check which system-design pages already exist and are not paywalled
    existing = set()
    sd_dir = os.path.join(OUT_BASE, "system-design")
    if os.path.isdir(sd_dir):
        for f in os.listdir(sd_dir):
            if f.endswith(".md"):
                fpath = os.path.join(sd_dir, f)
                size = os.path.getsize(fpath)
                if size > 2000:  # Skip small/placeholder files
                    existing.add(f)

    for section, urls in section_urls.items():
        out_dir = os.path.join(OUT_BASE, section)
        os.makedirs(out_dir, exist_ok=True)
        results = {"ok": [], "paywalled": [], "error": []}

        print(f"\n  [{section}]")
        for url in urls:
            page_num += 1
            if section == "blog":
                fname = url.split("/blog/")[-1].replace("/", "_") + ".md"
            else:
                fname = url_to_path(url, section)

            # Skip already-scraped system-design free pages
            if section == "system-design" and fname in existing:
                # Move existing files to subdirectory
                old_path = os.path.join(OUT_BASE, fname)
                new_path = os.path.join(out_dir, fname)
                if os.path.exists(old_path) and not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"    [{page_num}/{total_pages}] {fname} MOVED")
                    results["ok"].append(fname)
                    continue
                elif os.path.exists(new_path):
                    print(f"    [{page_num}/{total_pages}] {fname} EXISTS")
                    results["ok"].append(fname)
                    continue

            print(f"    [{page_num}/{total_pages}] {fname}...", end=" ", flush=True)
            status = scrape_page(page, url, out_dir, fname)

            if status.startswith("ok:"):
                chars = status.split(":")[1]
                print(f"OK ({chars} chars)")
                results["ok"].append(fname)
                total_saved += 1
            elif status == "paywalled":
                print("PAYWALLED")
                results["paywalled"].append(fname)
                total_paywalled += 1
            elif status == "timeout":
                print("TIMEOUT - retrying...")
                time.sleep(2)
                status2 = scrape_page(page, url, out_dir, fname)
                if status2.startswith("ok:"):
                    print(f"    RETRY OK ({status2.split(':')[1]} chars)")
                    results["ok"].append(fname)
                    total_saved += 1
                else:
                    print(f"    RETRY FAILED: {status2}")
                    results["error"].append(fname)
                    total_errors += 1
            else:
                print(f"SKIP ({status})")
                results["error"].append(fname)
                total_errors += 1

            time.sleep(0.3)

        all_results[section] = results
        ok = len(results["ok"])
        pw_count = len(results["paywalled"])
        err = len(results["error"])
        print(f"  {section}: {ok} saved, {pw_count} paywalled, {err} errors")

    browser.close()
    pw.stop()

    # Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    for section, r in all_results.items():
        print(f"  {section}: {len(r['ok'])} ok / {len(r['paywalled'])} paywalled / {len(r['error'])} err")
    print(f"\n  TOTAL: {total_saved} saved, {total_paywalled} paywalled, {total_errors} errors")

    # Save manifest
    manifest = os.path.join(OUT_BASE, "_manifest_full.json")
    with open(manifest, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n  Manifest: {manifest}")


if __name__ == "__main__":
    main()
