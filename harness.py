import json
import random
import time
from pathlib import Path
from dataclasses import asdict
from datetime import datetime

from prompts import PROMPTS
from scorers import SCORERS
from words import load_guesses, load_answers
from engine import Game
from agent import play_game
from report import build_table, write_table

RUN_DIR = Path(__file__).parent / "runs"
RUN_DIR.mkdir(exist_ok=True)

def run_eval(config: dict) -> dict:
    model_name = config["model_name"]
    prompt_fn = PROMPTS[config["prompt_name"]]
    rng = random.Random(config["seed"])
    n = config["n"]
    answer_set = rng.sample(load_answers(), n)
    valid_guesses = load_guesses()

    # run and score games
    records: list[dict] = []
    start = time.perf_counter()
    for i, answer in enumerate(answer_set):
        game = Game(answer, valid_guesses)
        result = play_game(game, model_name, prompt_fn)
        records.append({
            "answer": answer,
            "scores": {name: fn(result) for name, fn in SCORERS.items()},
            "result": asdict(result),
        })
        print(f"game {i + 1}: {"won" if result.won else "lost"}", flush=True)
    elapsed = time.perf_counter() - start

    return {
        "config": config,
        "answers": answer_set,
        "records": records,
        "summary": aggregate(records, elapsed)
    }

def aggregate(records: list[dict], elapsed: float) -> dict:
    n = len(records)
    (win_rate,
     avg_guesses_when_won,
     avg_invalid_per_game,
     avg_repeats_per_game,
     avg_invalid_length_per_game,
     avg_non_ascii_per_game,
     ) = None, None, None, None, None, None
    if n > 0:
        win_rate = sum(r["scores"]["won"] for r in records) / n
        won_guesses = [r["scores"]["guesses_used"] for r in records if r["scores"]["won"]]
        avg_guesses_when_won = sum(won_guesses) / len(won_guesses) if won_guesses else None
        avg_invalid_per_game = sum(r["scores"]["invalid_count"] for r in records) / n
        avg_repeats_per_game = sum(r["scores"]["repeated_guesses"] for r in records) / n
        avg_invalid_length_per_game = sum(r["scores"]["invalid_length_count"] for r in records) / n
        avg_non_ascii_per_game = sum(r["scores"]["non_ascii_count"] for r in records) / n
    return {
        "n": n,
        "win_rate": win_rate,
        "time": elapsed,
        "avg_guesses_when_won": avg_guesses_when_won,
        "avg_invalid_per_game": avg_invalid_per_game,
        "avg_repeats_per_game": avg_repeats_per_game,
        "avg_invalid_length_per_game": avg_invalid_length_per_game,
        "avg_non_ascii_per_game": avg_non_ascii_per_game,
    }

def save_run(data: dict) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = RUN_DIR / f"{data["config"]["prompt_name"]}_{data["config"]["model_name"]}_{timestamp}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return path

if __name__ == "__main__":
    config = {"model_name": "qwen2.5:3b", "prompt_name": "v4", "n": 100, "seed": 42}
    data = run_eval(config)
    table = build_table(data["summary"])
    run_path = save_run(data)
    markdown_path = write_table(table)
    print(table)
