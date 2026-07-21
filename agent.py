import httpx
import random

from engine import Game
from dataclasses import dataclass
from words import load_answers, load_guesses, pick_answer
from prompts import PROMPTS

"""
stateless llm calls, better for wordle
"""

DEFAULT_MODEL = "qwen2.5:3b"

def call_llm(model_name: str, prompt: str) -> str:
    response = httpx.post(
        "http://localhost:11434/api/generate",
        json={"model": model_name, "prompt": prompt, "stream": False},
        timeout=60
    )
    response.raise_for_status()
    data = response.json()
    return data["response"]

def parse_guess(raw: str) -> str | None:
    words = raw.split()
    extracted = []
    for word in words:
        cleaned = word.rstrip(".!'").upper()
        if len(cleaned) == 5 and cleaned.isalpha():
            extracted.append(cleaned)

    #provided no valid guess
    if not extracted:
        return None
    # Intuition - last word is most likely to be the guess
    return extracted[-1]

@dataclass
class GameResult:
    won: bool
    guesses: list[tuple[str, list[int]]]
    attempts: list[dict[str, str | None]]

def play_game(game: Game, model_name: str, prompt_fn) -> GameResult:
    attempts = []
    for turn in range(game.MAX_GUESSES):
        if game.is_won:
            break
        error = None

        prompt = prompt_fn(game.guesses)
        response = call_llm(model_name, prompt)
        guess = parse_guess(response)

        # failure logic
        if guess is None:
            error = "llm responded with no valid guess"
        else:
            try:
                game.guess(guess)
            except ValueError as e:
                error = str(e)
        attempts.append({"raw": response, "guess": guess, "error": error})
    return GameResult(won=game.is_won, guesses=game.guesses, attempts=attempts)

if __name__ == "__main__":
    answers = load_answers()
    guesses = load_guesses()
    game = Game(pick_answer(answers, random.Random(42)), guesses)
    result = play_game(game, model_name=DEFAULT_MODEL, prompt_fn = PROMPTS["v1"])
    print(result)