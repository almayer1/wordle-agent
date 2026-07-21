import random

from prompts import PROMPTS
from scorers import SCORERS
from words import load_guesses, load_answers
from engine import Game
from agent import play_game

def run_eval(config: dict) -> dict:
    model_name = config["model_name"]
    prompt_fn = PROMPTS[config["prompt_name"]]
    rng = random.Random(config["seed"])
    n = config["n"]
    answer_set = rng.sample(load_answers(), n)
    valid_guesses = load_guesses()

    # run and score games
    records: list[dict] = []
    for answer in answer_set:
        game = Game(answer, valid_guesses)
        result = play_game(game, model_name, prompt_fn)
        records.append({
            "answer": answer,
            "scores": {name: fn(result) for name, fn in SCORERS.items()},
            "result": result,
        })

    return {
        "config": config,
        "answers": answer_set,
        "records": records,
        "summary": aggregate(records)
    }

def aggregate(records: list[dict]) -> dict:
    n = len(records)
    win_rate, avg_guesses_when_won, avg_invalid_per_game, avg_repeats_per_game = None, None, None, None
    if n > 0:
        win_rate = sum(r["scores"]["won"] for r in records) / n
        won_guesses = [r["scores"]["guesses_used"] for r in records if r["scores"]["won"]]
        avg_guesses_when_won = sum(won_guesses) / len(won_guesses) if won_guesses else None
        avg_invalid_per_game = sum(r["scores"]["invalid_count"] for r in records) / n
        avg_repeats_per_game = sum(r["scores"]["repeated_guesses"] for r in records) / n
    return {
        "n": n,
        "win_rate": win_rate,
        "avg_guesses_when_won": avg_guesses_when_won,
        "avg_invalid_per_game": avg_invalid_per_game,
        "avg_repeats_per_game": avg_repeats_per_game,
    }

if __name__ == "__main__":
    config = {"model_name": "qwen2.5:3b", "prompt_name": "v1", "n": 5, "seed": 42}
    data = run_eval(config)
    print(data["summary"])
    print(data["records"])
