import re
from agentcoach.llm.base import LLMAdapter, Message
from agentcoach.prompt.templates import build_system_prompt
from agentcoach.coaching.quiz_state import QuizState, DIFFICULTY_LABELS
from agentcoach.coaching.compressor import compress_history
from agentcoach.coaching.context_builder import (
    update_kb_context, refresh_system_prompt, inject_strategy,
)


def strip_markdown(text: str) -> str:
    """Strip markdown formatting for clean text output (TTS, transcripts)."""
    c = re.sub(r'```[\s\S]*?```', '', text)       # code blocks
    c = re.sub(r'[#*_`~\[\](){}|>]', '', c)       # inline markdown
    c = re.sub(r'---+', '', c)                     # horizontal rules
    c = re.sub(r'\|[^\n]+\|', '', c)               # tables
    c = re.sub(r'https?://\S+', '', c)             # URLs
    c = re.sub(r'\n{3,}', '\n\n', c)               # excessive newlines
    return c.strip()


class Coach:
    def __init__(self, llm: LLMAdapter, mode: str = "behavioral", memory_context: str = "",
                 kb_store=None, topic_id: str = "", topic_name: str = "",
                 kb_teaching_context: str = "", mock_reference_context: str = ""):
        self.llm = llm
        self.mode = mode
        self.memory_context = memory_context
        self.kb_store = kb_store
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.kb_teaching_context = kb_teaching_context
        self.mock_reference_context = mock_reference_context
        self.quiz_state = QuizState()
        system_prompt = build_system_prompt(
            mode, memory_context, kb_teaching_content=kb_teaching_context,
            mock_reference_content=mock_reference_context,
            topic_id=topic_id, topic_name=topic_name,
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
        compress_history(self.history, self.llm)
        self.history.append(Message(role="user", content=user_input))
        # Search KB for relevant context
        if self.kb_store:
            update_kb_context(
                self.kb_store, user_input, self.mode,
                self.memory_context, self.kb_teaching_context, self.history,
                topic_id=self.topic_id, topic_name=self.topic_name,
                mock_reference_context=self.mock_reference_context,
            )
        # Select and inject teaching strategy for learn/reinforce modes
        self._current_strategy = None
        if self.mode in ("learn", "reinforce"):
            self._current_strategy = inject_strategy(
                self.mode, self.quiz_state, user_input, len(self.history),
            )
        # Build messages: add strategy hint if active
        if self._current_strategy:
            msgs = list(self.history)
            msgs.insert(-1, Message(role="user", content=f"[Teaching instruction for coach: {self._current_strategy}]"))
            response = self.llm.generate(msgs)
        else:
            response = self.llm.generate(self.history)
        self.history.append(Message(role="assistant", content=response))
        # Track quiz state and update system prompt with difficulty hint
        if self.mode in ("learn", "reinforce"):
            self._update_quiz_state(user_input, response)
        return response

    def _update_quiz_state(self, user_input: str, response: str):
        """Detect correct/incorrect answers and adjust quiz difficulty.

        Uses the quiz evaluator module for answer assessment. Falls back to
        pattern matching if the evaluator module is not available.
        """
        from agentcoach.coaching.quiz_evaluator import (
            evaluate_answer_with_patterns, detect_quiz_start,
        )
        qs = self.quiz_state

        # Check if coach is starting a quiz in this response
        if not qs._quiz_active and detect_quiz_start(response):
            qs._quiz_active = True
            return

        # Don't track during teaching phase
        if not qs._quiz_active:
            return

        # Evaluate the answer using pattern matching (fast, no extra LLM call)
        evaluation = evaluate_answer_with_patterns(response)
        if evaluation is None:
            return  # Can't determine -- skip

        is_correct = evaluation["is_correct"]
        is_incorrect = not is_correct

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
            # Extract weak concept hint from first sentence of feedback
            from agentcoach.coaching.quiz_evaluator import _INCORRECT_PATTERNS
            for line in response.split("."):
                if _INCORRECT_PATTERNS.search(line):
                    concept = line.strip()[:80]
                    if concept and concept not in qs.weak_concepts:
                        qs.weak_concepts.append(concept)
                    break

        # Only update system prompt if we detected a quiz exchange
        if is_correct or is_incorrect:
            refresh_system_prompt(
                self.quiz_state, self.mode, self.memory_context,
                self.kb_teaching_context, self.history,
                topic_id=self.topic_id, topic_name=self.topic_name,
                mock_reference_context=self.mock_reference_context,
            )

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

    def wrap_up(self) -> str:
        """Force a full structured close to the session.

        This is the method a runner should call when it decides the
        conversation is over (turn budget exhausted, user typed "done", etc).
        It produces a canonical close: recap, top strengths with evidence,
        top improvements with evidence, and a 1.0-5.0 score on the same
        rubric the external judge uses, with rationale. Unlike
        ``get_feedback_summary`` it does not require a minimum history
        length -- callers are expected to only call it when a session has
        actually happened.
        """
        if len(self.history) < 3:
            return ""
        instruction = (
            "The session is ending now. Produce the CLOSING WRAP-UP in this "
            "exact structure, in plain prose suitable for speech:\n\n"
            "RECAP: Two sentences describing what we covered.\n"
            "STRENGTHS: Three specific things the candidate did well, each tied "
            "to something they actually said.\n"
            "TO IMPROVE: Three specific things to work on, each tied to a gap "
            "or hesitation in what they actually said.\n"
            "SCORE: A number from 1.0 to 5.0 (one decimal allowed) on the same "
            "1-5 rubric the judge uses, followed by a one-line justification. "
            "Format exactly: 'SCORE: X.Y/5 - <reason>'.\n\n"
            "Do NOT ask another question. Do NOT continue the interview. "
            "This is the final message."
        )
        self.history.append(Message(role="user", content=instruction))
        response = self.llm.generate(self.history)
        if response:
            self.history.append(Message(role="assistant", content=response))
        return response
