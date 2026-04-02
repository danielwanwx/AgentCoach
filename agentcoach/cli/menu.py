def _show_menu(syllabus, analytics, recommender, user_id, mem=None, jd_store=None):
    """Show domain/mode selection. Returns (domain, mode, topic) or (None, None, None) to quit."""
    domains = syllabus.get_domains()

    while True:
        print("--- Main Menu ---")  # UI output
        print("Domains:")  # UI output
        for i, d in enumerate(domains, 1):
            name = syllabus.get_domain_name(d)
            topics = syllabus.get_topics(d)
            progress = analytics.get_progress(user_id, d)
            scored_count = len(progress)
            print(f"  {i}. {name} ({scored_count}/{len(topics)} topics started)")  # UI output
        print()  # UI output
        print("Commands: 'progress <domain>', 'recommend', 'plan', 'quit'")  # UI output
        print("Data:     'import profile <text>', 'import jd <text>', 'load resume <file>',")  # UI output
        print("          'load jd <file>', 'load kb <dir> [category]', 'kb stats', 'kb search <query>'")  # UI output
        print()  # UI output

        try:
            choice = input("Select domain (number) or command: ").strip()
        except (KeyboardInterrupt, EOFError):
            return None, None, None

        choice_lower = choice.lower()

        if choice_lower == "quit":
            return None, None, None

        if choice_lower == "recommend":
            all_topics = []
            for d in domains:
                all_topics.extend(syllabus.get_topics(d))
            if not all_topics:
                print("No topics found in syllabus.\n")  # UI output
                continue
            rec = recommender.recommend(user_id, all_topics, syllabus=syllabus)
            print(f"\nCoach recommends: {rec['mode'].upper()} -- {rec['topic_name']}")  # UI output
            print(f"Reason: {rec['reason']}\n")  # UI output
            continue

        if choice_lower == "plan":
            try:
                from agentcoach.planner import generate_study_plan, format_plan
                all_topics = []
                for d in domains:
                    all_topics.extend([t for t in syllabus.get_topics(d) if t.get("resources")])
                mastery_data = {t["id"]: analytics.get_mastery(user_id, t["id"]) for t in all_topics}
                plan = generate_study_plan(all_topics, mastery_data, days_until_interview=14)
                print(f"\n{format_plan(plan, days_to_show=7)}\n")  # UI output
            except Exception as e:
                print(f"(Plan error: {e})")  # UI output
            continue

        if choice_lower.startswith("progress"):
            parts = choice_lower.split(maxsplit=1)
            if len(parts) < 2:
                for d in domains:
                    _show_progress(syllabus, analytics, user_id, d)
            else:
                query = parts[1]
                matched = [d for d in domains if query in d]
                if matched:
                    _show_progress(syllabus, analytics, user_id, matched[0])
                else:
                    print(f"Unknown domain: {query}")  # UI output
            continue

        # Data import commands
        if choice_lower.startswith("import profile ") and mem:
            text = choice[len("import profile "):].strip()
            mem.save_profile(text)
            print("Profile saved to memory.")  # UI output
            continue

        if choice_lower.startswith("import jd ") and mem:
            text = choice[len("import jd "):].strip()
            mem.save_jd(text)
            print("JD saved to memory.")  # UI output
            continue

        if choice_lower.startswith("load resume ") and mem:
            filepath = choice[len("load resume "):].strip()
            try:
                from agentcoach.memory.importer import import_file
                content = import_file(filepath)
                mem.save_profile(content)
                print(f"Resume loaded from {filepath} and saved to memory.")  # UI output
            except FileNotFoundError as e:
                print(f"Error: {e}")  # UI output
            continue

        if choice_lower.startswith("load jd ") and mem:
            filepath = choice[len("load jd "):].strip()
            try:
                from agentcoach.memory.importer import import_file
                content = import_file(filepath)
                mem.save_jd(content)
                print(f"JD loaded from {filepath} and saved to memory.")  # UI output
            except FileNotFoundError as e:
                print(f"Error: {e}")  # UI output
            continue

        if choice_lower.startswith("load kb "):
            parts = choice[len("load kb "):].strip().split(maxsplit=1)
            dir_path = parts[0]
            cat = parts[1] if len(parts) > 1 else "general"
            try:
                from agentcoach.kb.indexer import index_directory
                from agentcoach.kb.store import KnowledgeStore
                kb = KnowledgeStore()
                print(f"Indexing {dir_path} (category: {cat})...")  # UI output
                stats = index_directory(dir_path, kb, category=cat)
                print(f"Done: {stats['files_processed']} files, {stats['chunks_added']} chunks indexed.")  # UI output
                if stats['errors']:
                    print(f"Errors: {len(stats['errors'])}")  # UI output
            except Exception as e:
                print(f"Error: {e}")  # UI output
            continue

        if choice_lower == "kb stats":
            try:
                from agentcoach.kb.store import KnowledgeStore
                kb = KnowledgeStore()
                stats = kb.get_stats()
                print(f"\nKnowledge Base: {stats['total_chunks']} chunks, {stats['total_sources']} sources")  # UI output
                print(f"Categories: {', '.join(stats['categories']) if stats['categories'] else 'none'}\n")  # UI output
            except Exception as e:
                print(f"Error: {e}")  # UI output
            continue

        if choice_lower.startswith("kb search "):
            query = choice[len("kb search "):].strip()
            try:
                from agentcoach.kb.store import KnowledgeStore
                kb = KnowledgeStore()
                results = kb.search(query, limit=3)
                if results:
                    for i, r in enumerate(results, 1):
                        print(f"\n--- Result {i} [{r['source']} > {r['section']}] ---")  # UI output
                        print(r['content'][:300])  # UI output
                else:
                    print("No results found.")  # UI output
                print()  # UI output
            except Exception as e:
                print(f"Error: {e}")  # UI output
            continue

        # JD commands
        if choice_lower == "jd" and jd_store:
            print("Paste job description text (enter an empty line to finish):")  # UI output
            jd_lines = []
            try:
                while True:
                    line = input()
                    if line == "":
                        break
                    jd_lines.append(line)
            except (KeyboardInterrupt, EOFError):
                pass
            if jd_lines:
                raw_text = "\n".join(jd_lines)
                from agentcoach.user.jd_parser import parse_jd_offline, map_skills_to_topics
                parsed = parse_jd_offline(raw_text)
                jd_id = jd_store.save_jd(user_id, parsed)
                print(f"JD saved (id={jd_id}): {parsed.role_title or 'Untitled'} at {parsed.company or 'Unknown'}")  # UI output
            else:
                print("No text entered.")  # UI output
            continue

        if choice_lower == "jd list" and jd_store:
            jds = jd_store.list_jds(user_id)
            if not jds:
                print("No saved JDs.\n")  # UI output
            else:
                for j in jds:
                    active = " [ACTIVE]" if j["is_active"] else ""
                    print(f"  {j['id']}. {j['company'] or '?'} — {j['role_title'] or '?'} ({j['level'] or '?'}){active}")  # UI output
                print()  # UI output
            continue

        if choice_lower.startswith("jd switch ") and jd_store:
            try:
                jd_id = int(choice_lower.split()[-1])
                jd_store.set_active_jd(user_id, jd_id)
                print(f"Switched active JD to id={jd_id}.")  # UI output
            except (ValueError, IndexError):
                print("Usage: jd switch <id>")  # UI output
            continue

        # Try to parse as domain number
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(domains):
                domain = domains[idx]
            else:
                print("Invalid choice.")  # UI output
                continue
        except ValueError:
            print("Invalid choice.")  # UI output
            continue

        # Now select mode
        print(f"\nDomain: {syllabus.get_domain_name(domain)}")  # UI output
        print("Modes:")  # UI output
        print("  L. Learn -- study resources + quick quiz")  # UI output
        print("  R. Reinforce -- strengthen weak topics")  # UI output
        print("  M. Mock -- full interview simulation")  # UI output
        print("  (or 'back' to return)")  # UI output
        print()  # UI output

        try:
            mode_choice = input("Select mode (L/R/M): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return None, None, None

        if mode_choice == "back":
            continue

        mode_map = {"l": "learn", "r": "reinforce", "m": "mock"}
        mode = mode_map.get(mode_choice)
        if not mode:
            print("Invalid mode.")  # UI output
            continue

        # For learn/reinforce, pick a topic
        topic = None
        if mode in ("learn", "reinforce"):
            topics = syllabus.get_topics(domain)
            rec = recommender.recommend(user_id, topics, syllabus=syllabus)
            print(f"\nCoach suggests: {rec['topic_name']} ({rec['reason']})")  # UI output
            print("Topics:")  # UI output
            for i, t in enumerate(topics, 1):
                mastery = analytics.get_mastery(user_id, t["id"])
                icon = "?" if mastery == 0 else ("X" if mastery < 40 else ("~" if mastery < 70 else "+"))
                score_str = f"{mastery}%" if mastery > 0 else "--"
                print(f"  {i}. [{icon}] {t['name']} {score_str}")  # UI output
            print()  # UI output
            try:
                topic_choice = input("Select topic (number, or Enter for suggestion): ").strip()
            except (KeyboardInterrupt, EOFError):
                return None, None, None

            if not topic_choice:
                topic = syllabus.get_topic(rec["topic_id"])
            else:
                try:
                    tidx = int(topic_choice) - 1
                    if 0 <= tidx < len(topics):
                        topic = topics[tidx]
                    else:
                        print("Invalid choice.")  # UI output
                        continue
                except ValueError:
                    print("Invalid choice.")  # UI output
                    continue

        return domain, mode, topic


def _show_progress(syllabus, analytics, user_id, domain):
    """Display mastery progress for a domain."""
    topics = syllabus.get_topics(domain)
    name = syllabus.get_domain_name(domain)
    print(f"\n=== {name} Progress ===")  # UI output
    total_mastery = 0
    scored_count = 0
    for t in topics:
        mastery = analytics.get_mastery(user_id, t["id"])
        icon = "?" if mastery == 0 else ("X" if mastery < 40 else ("~" if mastery < 70 else "+"))
        score_str = f"{mastery}%" if mastery > 0 else "--"
        print(f"  [{icon}] {t['name']:30s} {score_str}")  # UI output
        total_mastery += mastery
        if mastery > 0:
            scored_count += 1
    avg = total_mastery // len(topics) if topics else 0
    print(f"Overall: {avg}% ({scored_count}/{len(topics)} topics started)\n")  # UI output
