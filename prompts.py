from engine import Game

History = list[tuple[str, list[int]]]

def render_symbolic(history: History) -> str:
    result = ""
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
    return result

def render_explicit(history: History) -> str:
    # [(CRANE, [0, 0, 1, 1, 2]), (BRAIN, [2, 2, 2, 1, 1])]
    result = []
    for guess, score in history:
        word = []
        for letter, digit in zip(guess, score):
            if digit == 0:
                word.append(f"{letter}: not in word")
            elif digit == 1:
                word.append(f"{letter}: in word")
            else:
                word.append(f"{letter}: correct position")
        result.append(", ".join(word))
    return "\n".join(result)

def render_summary(history: History) -> str:
    if len(history) == 0:
        return ""
    ever_grey = set()
    ever_marked = set()
    known = [None] * Game.WORD_LENGTH
    must_include = {}

    for guess, score in history:
        for i, letter in enumerate(guess):
            if score[i] == 0:
                ever_grey.add(letter)
            elif score[i] == 1:
                ever_marked.add(letter)
                if letter not in must_include:
                    must_include[letter] = []
                must_include[letter].append(str(i + 1))
            elif score[i] == 2:
                ever_marked.add(letter)
                known[i] = letter
    ruled_out = ever_grey - ever_marked
    return _convert_summary({"known": known, "ruled_out": ruled_out, "must_include": must_include})

def _convert_summary(summary: dict[str, set | dict | list]) -> str:
    known = "Known: " + "".join(letter if letter is not None else "_" for letter in summary["known"])
    ruled_out = "Ruled out: " + ", ".join(summary["ruled_out"])
    mi_parts = []
    for letter, pos in summary["must_include"].items():
        mi_parts.append(f"{letter} (not in position " + ", ".join(pos) + ")")
    must_include = "Must include " + ", ".join(mi_parts)
    return known + ". " + ruled_out + ". " + must_include

def v1(history: History) -> str:
    task = "TASK: You are playing wordle, your goal is to guess the hidden answer\n"
    rules = "RULES: You can only guess 5 letter words. For every guess you make you will get a result. Results are structured as symbols: GUESS -> ⬛⬛🟨🟩⬛. ⬛: letter is not contained in answer, 🟨: letter is in answer but not in the correct position, 🟩: letter is in correct position\n"
    state = render_symbolic(history)
    output_format = "OUTPUT FORMAT: Output only your next guess."
    return task + rules + state + output_format

#reinforced word length and added row breaks
def v2(history: History) -> str:
    prompt = []
    task = "TASK: You are playing wordle, your goal is to guess the hidden answer"
    rules = "RULES: Your guess must be exactly 5 letters. For every guess you make you will get a result. Results are structured as symbols: GUESS -> ⬛⬛🟨🟩⬛. ⬛: letter is not contained in answer, 🟨: letter is in answer but not in the correct position, 🟩: letter is in correct position"
    state = "State: " + render_symbolic(history)
    output_format = "OUTPUT FORMAT: Output only your 5 letter guess"
    prompt.append(task)
    prompt.append(rules)
    prompt.append(state)
    prompt.append(output_format)
    return "\n---------------\n".join(prompt)

# change history state
def v3(history: History) -> str:
    prompt = []
    task = "TASK: You are playing wordle, your goal is to guess the hidden answer"
    rules = "RULES: Your guess must be exactly 5 letters. You must use past guesses to reason a new guess"
    state = "STATE: " + render_explicit(history)
    output_format = "OUTPUT FORMAT: Output only your 5 letter guess"
    prompt.append(task)
    prompt.append(rules)
    prompt.append(state)
    prompt.append(output_format)
    return "\n---------------\n".join(prompt)

def v4(history: History) -> str:
    prompt = []
    task = "TASK -> You are playing wordle, your goal is to guess the hidden answer"
    rules = "RULES -> Your guess must be exactly 5 letters. You must use current state to reason a new guess"
    state = "STATE -> " + render_summary(history)
    output_format = "OUTPUT FORMAT: Output only your 5 letter guess"
    prompt.append(task)
    prompt.append(rules)
    prompt.append(state)
    prompt.append(output_format)
    return "\n---------------\n".join(prompt)

PROMPTS = {
    "v1": v1,
    "v2": v2,
    "v3": v3,
    "v4": v4,
}

if __name__ == "__main__":
    fake = [("CRANE", [0, 0, 1, 1, 2]), ("SLOTH", [1, 0, 0, 0, 0])]
    print(v4(fake))