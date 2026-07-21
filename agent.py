import httpx

"""
stateless llm calls, better for wordle
"""

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
        cleaned = word.rstrip(".!").upper()
        if len(cleaned) == 5 and cleaned.isalpha():
            extracted.append(cleaned)

    #provided no valid guess
    if not extracted:
        return None
    # Intuition - last word is most likely to be the guess
    return extracted[-1]

if __name__ == "__main__":
    fake = [("CRANE", [0, 1, 0, 2, 0]), ("SLOTH", [1, 0, 0, 0, 0])]
    print(build_prompt(fake))