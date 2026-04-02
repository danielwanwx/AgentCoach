import re
from agentcoach.llm.base import Message

# Adapted from Claude Code's services/compact/prompt.ts -- analysis+summary pattern
COMPRESSION_PROMPT = """Summarize this tutoring conversation. Wrap your thinking in <analysis> tags, then output in <summary> tags.

<analysis>
[Review each exchange: what was asked, what the user answered, whether correct/incorrect]
</analysis>

<summary>
1. Topic and Intent: What topic is being studied, what the user wants to learn
2. User Answers: List ALL user answers and whether correct/incorrect
3. Key Concepts Covered: Concepts explained by the coach
4. Weak Areas: Concepts the user struggled with or got wrong
5. Quiz Progress: Questions asked, difficulty level, score so far
6. Current State: What was being discussed right before this summary
</summary>"""

HISTORY_MAX = 12  # compress when history exceeds this many messages


def compress_history(history: list, llm) -> list:
    """Compress older conversation history when it exceeds HISTORY_MAX.

    Adapted from Claude Code's compact service: uses <analysis>+<summary>
    pattern, strips analysis, keeps system prompt and last 4 messages intact.

    Modifies history in-place and returns it.
    """
    if len(history) <= HISTORY_MAX:
        return history
    # Slice: everything between system prompt [0] and last 4 messages
    to_compress = history[1:-4]
    if not to_compress:
        return history
    try:
        compress_msgs = list(to_compress) + [
            Message(role="user", content=COMPRESSION_PROMPT)
        ]
        raw_summary = llm.generate(compress_msgs)
        # Strip <analysis>...</analysis>, extract <summary> content
        summary = re.sub(r'<analysis>[\s\S]*?</analysis>', '', raw_summary).strip()
        match = re.search(r'<summary>([\s\S]*?)</summary>', summary)
        if match:
            summary = match.group(1).strip()
        # Replace compressed messages with summary
        history[1:-4] = [
            Message(role="user", content=f"[Previous conversation summary]\n{summary}")
        ]
    except Exception:
        pass  # compression failure should not break the session
    return history
