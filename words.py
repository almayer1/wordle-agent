from pathlib import Path
from functools import cache
import random

def _clean(words: list[str]) -> list[str]:
    return [word.strip().upper() for word in words if word.strip()]

def load_answers(path: Path) -> list[str]:
    return _clean(path.read_text().splitlines())

@cache
def load_guesses(path: Path) -> set[str]:
    return set(load_answers(path))

def pick_answer(answers: list[str], rng: random.Random) -> str:
    return rng.choice(answers)