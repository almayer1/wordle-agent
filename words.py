from pathlib import Path
from functools import cache
import random

DATA_DIR = Path(__file__).parent / "wordle_words"

def _clean(words: list[str]) -> list[str]:
    return [word.strip().upper() for word in words if word.strip()]

@cache
def load_answers(path: Path = DATA_DIR / "answers.txt") -> list[str]:
    return _clean(path.read_text().splitlines())

@cache
def load_guesses(path: Path = DATA_DIR / "guesses.txt") -> set[str]:
    return set(load_answers(path))

def pick_answer(answers: list[str], rng: random.Random) -> str:
    return rng.choice(answers)