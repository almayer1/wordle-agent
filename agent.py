import httpx
import random
from pathlib import Path

from engine import Game
from dataclasses import dataclass
from words import load_answers, load_guesses, pick_answer

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

def convert_symbolic(history: list[tuple[str, list[int]]]) -> str:
    result = "STATE: "
    for item in history:
        guess = item[0]
        score = item[1]
        result += guess + " -> "
        for num in score:
            if num == 0:
                result += "⬛"
            elif num == 1:
                result += "🟨"
            elif num == 2:
                result += "🟩"
        result += ", "
    result += "\n"
    return result

def build_prompt(history: list[tuple[str, list[int]]]) -> str:
    task = "TASK: You are playing wordle, your goal is to guess the hidden answer\n"
    rules = "RULES: You can only guess 5 letter words. For every guess you make you will get a result. Results are structured as symbols: GUESS -> ⬛⬛🟨🟩⬛. ⬛: letter is not contained in answer, 🟨: letter is in answer but not in the correct position, 🟩: letter is in correct position\n"
    state = convert_symbolic(history)
    output_format = "OUTPUT FORMAT: Output only your next guess."
    return task + rules + state + output_format

def parse_guess(raw: str) -> str | None:
    words = raw.split()
    extracted = []
    for i, word in enumerate(words):
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

    @property
    def invalid_count(self) -> int:
        count = 0
        for attempt in self.attempts:
            if attempt["error"]:
                count += 1
        return count

def play_game(game: Game, model_name: str = DEFAULT_MODEL) -> GameResult:
    attempts = []
    for turn in range(game.MAX_GUESSES):
        if game.is_won:
            break
        error = None

        prompt = build_prompt(game.guesses)
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
    result = play_game(game)
    print(result)