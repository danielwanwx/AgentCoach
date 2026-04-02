import re
from dataclasses import dataclass, field
from agentcoach.llm.base import LLMAdapter, Message
from agentcoach.prompt.templates import build_system_prompt, QUIZ_STATE_SECTION


def strip_markdown(text: str) -> str:
    """Strip markdown formatting for clean text output (TTS, transcripts)."""
    c = re.sub(r'```[\s\S]*?```', '', text)       # code blocks
    c = re.sub(r'[#*_`~\[\](){}|>]', '', c)       # inline markdown
    c = re.sub(r'---+', '', c)                     # horizontal rules
    c = re.sub(r'\|[^\n]+\|', '', c)               # tables
    c = re.sub(r'https?://\S+', '', c)             # URLs
    c = re.sub(r'\n{3,}', '\n\n', c)               # excessive newlines
    return c.strip()

DIFFICULTY_LABELS = {
    1: "Concept recall",
    2: "Application",
    3: "Edge cases",
    4: "Trade-offs & design",
}

# Adapted from Claude Code's services/compact/prompt.ts — analysis+summary pattern
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

# Pattern to detect Coach entering quiz mode
_QUIZ_START_PATTERNS = re.compile(
    r"\bquiz\b|\bquestion\s*[1-9#]|\blet.s test\b|\btest your\b|\bready.*quiz\b|\bstart.*quiz\b",
    re.IGNORECASE,
)

# Patterns indicating correct/incorrect answers in coach responses
# Match correct/incorrect even through markdown formatting (**correct**, ✓, ✗)
_CORRECT_PATTERNS = re.compile(
    r"\*{0,2}correct\*{0,2}|✓|\bexactly\b|\bgreat answer\b|\bwell done\b|\bspot on\b|\bnailed it\b|\bthat.s right\b",
    re.IGNORECASE,
)
_INCORRECT_PATTERNS = re.compile(
    r"\*{0,2}incorrect\*{0,2}|✗|\bnot quite\b|\bwrong\b|\bnot exactly\b"
    r"|\bmissed\b|\bactually\b.*\bshould\b|\bslightly off\b|\bclose but\b"
    r"|\bnot quite right\b|\boff on\b|\bmixed.{0,15}up\b",
    re.IGNORECASE,
)


@dataclass
class QuizState:
    question_count: int = 0
    correct_count: int = 0
    incorrect_count: int = 0
    difficulty: int = 1  # 1=recall, 2=application, 3=edge-cases, 4=tradeoffs
    weak_concepts: list = field(default_factory=list)
    _consecutive_correct: int = field(default=0, repr=False)
    _quiz_active: bool = field(default=False, repr=False)


class Coach:
    def __init__(self, llm: LLMAdapter, mode: str = "behavioral", memory_context: str = "",
                 kb_store=None, topic_id: str = "", topic_name: str = "",
                 kb_teaching_context: str = ""):
        self.llm = llm
        self.mode = mode
        self.memory_context = memory_context
        self.kb_store = kb_store
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.kb_teaching_context = kb_teaching_context
        self.quiz_state = QuizState()
        system_prompt = build_system_prompt(
            mode, memory_context, kb_teaching_content=kb_teaching_context,
        )
        self.history: list = [Message(role="system", content=system_prompt)]

    def start(self) -> str:
        """Start the interview session. Returns coach's opening message."""
        if self.kb_teaching_context and self.topic_name:
            opening = f"Hi, I'm ready to learn about {self.topic_name}. Please teach me using the provided material."
        else:
            opening = "Hi, I'm ready to start the mock interview. Please begin."
        self.history.append(Message(role="user", content=opening))
        response = self.llm.generate(self.history)
        self.history.append(Message(role="assistant", content=response))
        return response

    def respond(self, user_input: str) -> str:
        """Send user's answer, get coach's next question/feedback."""
        self._compress_history()
        self.history.append(Message(role="user", content=user_input))
        # Search KB for relevant context
        if self.kb_store:
            self._update_kb_context(user_input)
        response = self.llm.generate(self.history)
        self.history.append(Message(role="assistant", content=response))
        # Track quiz state and update system prompt with difficulty hint
        if self.mode in ("learn", "reinforce"):
            self._update_quiz_state(user_input, response)
        return response

    def _compress_history(self):
        """Compress older conversation history when it exceeds HISTORY_MAX.

        Adapted from Claude Code's compact service: uses <analysis>+<summary>
        pattern, strips analysis, keeps system prompt and last 4 messages intact.
        """
        if len(self.history) <= HISTORY_MAX:
            return
        # Slice: everything between system prompt [0] and last 4 messages
        to_compress = self.history[1:-4]
        if not to_compress:
            return
        try:
            compress_msgs = list(to_compress) + [
                Message(role="user", content=COMPRESSION_PROMPT)
            ]
            raw_summary = self.llm.generate(compress_msgs)
            # Strip <analysis>...</analysis>, extract <summary> content
            summary = re.sub(r'<analysis>[\s\S]*?</analysis>', '', raw_summary).strip()
            match = re.search(r'<summary>([\s\S]*?)</summary>', summary)
            if match:
                summary = match.group(1).strip()
            # Replace compressed messages with summary
            self.history[1:-4] = [
                Message(role="user", content=f"[Previous conversation summary]\n{summary}")
            ]
        except Exception:
            pass  # compression failure should not break the session

    def _update_kb_context(self, query: str):
        """Search KB and update system prompt with relevant knowledge."""
        try:
            results = self.kb_store.search(query, limit=3)
            if results:
                kb_text = "\n".join(
                    f"- [{r['section']}] {r['content'][:500]}"
                    for r in results
                )
                updated_prompt = build_system_prompt(
                    self.mode, self.memory_context, kb_context=kb_text,
                    kb_teaching_content=self.kb_teaching_context,
                )
                self.history[0] = Message(role="system", content=updated_prompt)
        except Exception:
            pass  # KB search failure should not break the interview

    def _update_quiz_state(self, user_input: str, response: str):
        """Detect correct/incorrect answers and adjust quiz difficulty.

        Only tracks answers after the coach has entered quiz mode (detected by
        patterns like "quiz", "question 1", "let's test").
        """
        qs = self.quiz_state

        # Check if coach is starting a quiz in this response
        if not qs._quiz_active and _QUIZ_START_PATTERNS.search(response):
            qs._quiz_active = True
            return  # This response introduces the quiz, no scoring yet

        # Don't track during teaching phase
        if not qs._quiz_active:
            return

        # Check only the first 200 chars for the verdict — LLMs typically lead with it
        head = response[:200]
        is_correct = bool(_CORRECT_PATTERNS.search(head))
        is_incorrect = bool(_INCORRECT_PATTERNS.search(head))

        if is_correct and not is_incorrect:
            qs.question_count += 1
            qs.correct_count += 1
            qs._consecutive_correct += 1
            if qs._consecutive_correct >= 2 and qs.difficulty < 4:
                qs.difficulty += 1
                qs._consecutive_correct = 0
        elif is_incorrect:
            qs.question_count += 1
            qs.incorrect_count += 1
            qs._consecutive_correct = 0
            if qs.difficulty > 1:
                qs.difficulty -= 1
            # Extract weak concept hint from response (first sentence after "incorrect"/"actually")
            for line in response.split("."):
                if _INCORRECT_PATTERNS.search(line):
                    concept = line.strip()[:80]
                    if concept and concept not in qs.weak_concepts:
                        qs.weak_concepts.append(concept)
                    break

        # Only update system prompt if we detected a quiz exchange
        if is_correct or is_incorrect:
            self._refresh_system_prompt()

    def _refresh_system_prompt(self):
        """Rebuild system prompt with current quiz state."""
        qs = self.quiz_state
        weak_line = ""
        if qs.weak_concepts:
            weak_line = "Weak areas: " + "; ".join(qs.weak_concepts[-3:])
        quiz_ctx = QUIZ_STATE_SECTION.format(
            question_num=qs.question_count,
            correct=qs.correct_count,
            incorrect=qs.incorrect_count,
            difficulty_label=DIFFICULTY_LABELS.get(qs.difficulty, "Concept recall"),
            weak_concepts_line=weak_line,
        )
        # Get current KB context from history[0] if present
        kb_ctx = ""
        if self.kb_store:
            # Re-use whatever KB context was last set
            pass
        updated = build_system_prompt(
            self.mode, self.memory_context,
            kb_teaching_content=self.kb_teaching_context,
            quiz_state_context=quiz_ctx,
        )
        self.history[0] = Message(role="system", content=updated)

    def get_feedback_summary(self) -> str:
        """Ask the LLM to summarize the session with strengths/weaknesses."""
        if len(self.history) < 5:  # need system + start + assistant + at least one real exchange
            return ""
        self.history.append(Message(
            role="user",
            content="Please provide a brief summary of this interview session. Include: 1) Key strengths demonstrated, 2) Areas for improvement, 3) Overall score out of 10. Be specific and actionable."
        ))
        response = self.llm.generate(self.history)
        return response
