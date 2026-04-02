from dataclasses import dataclass, field

DIFFICULTY_LABELS = {
    1: "Concept recall",
    2: "Application",
    3: "Edge cases",
    4: "Trade-offs & design",
}


@dataclass
class QuizState:
    question_count: int = 0
    correct_count: int = 0
    incorrect_count: int = 0
    difficulty: int = 1  # 1=recall, 2=application, 3=edge-cases, 4=tradeoffs
    weak_concepts: list = field(default_factory=list)
    _consecutive_correct: int = field(default=0, repr=False)
    _quiz_active: bool = field(default=False, repr=False)
