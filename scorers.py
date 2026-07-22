from agent import GameResult

def won(result: GameResult) -> bool:
    return result.won

def guesses_used(result: GameResult) -> int | None:
    if not result.won:
        return None
    return len(result.guesses)

def invalid_count(result: GameResult) -> int:
    return sum(1 for a in result.attempts if a["error"])

def repeated_guesses(result: GameResult) -> int:
    guesses = [g for g, _ in result.guesses]
    return len(guesses) - len(set(guesses))

def invalid_length_count(result: GameResult) -> int:
    return sum(1 for a in result.attempts if len(a["raw"]) != 5)

def non_ascii_count(result: GameResult) -> int:
    return sum(1 for a in result.attempts if not a["raw"].isascii() )

SCORERS = {
    "won": won,
    "guesses_used": guesses_used,
    "invalid_count": invalid_count,
    "repeated_guesses": repeated_guesses,
    "invalid_length_count": invalid_length_count,
    "non_ascii_count": non_ascii_count
}