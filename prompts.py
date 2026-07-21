
def render_symbolic(history: list[tuple[str, list[int]]]) -> str:
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

def build_prompt_v1(history: list[tuple[str, list[int]]]) -> str:
    task = "TASK: You are playing wordle, your goal is to guess the hidden answer\n"
    rules = "RULES: You can only guess 5 letter words. For every guess you make you will get a result. Results are structured as symbols: GUESS -> ⬛⬛🟨🟩⬛. ⬛: letter is not contained in answer, 🟨: letter is in answer but not in the correct position, 🟩: letter is in correct position\n"
    state = render_symbolic(history)
    output_format = "OUTPUT FORMAT: Output only your next guess."
    return task + rules + state + output_format

PROMPTS = {"v1": build_prompt_v1}