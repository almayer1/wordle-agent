from collections import Counter

class Game:
    WORD_LENGTH = 5
    MAX_GUESSES = 6

    def __init__(self, answer: str, valid_guesses: set[str]):
        self.answer = self._clean(answer)
        self._validate_shape(self.answer)
        self.guesses: list[tuple[str, list[int]]] = []
        self.valid_guesses = valid_guesses

    def __repr__(self):
        return f"Game(answer={self.answer!r}, guesses={self.num_guesses})"

    @property
    def num_guesses(self) -> int:
        return len(self.guesses)

    @property
    def guesses_remaining(self) -> int:
        return self.MAX_GUESSES - self.num_guesses

    @property
    def is_won(self) -> bool:
        return self.num_guesses > 0 and self.guesses[-1][1] == [2] * self.WORD_LENGTH

    # cleans agents guess, only capitalizes and strips white case, erros beyond that should be fixed on the agent side
    @staticmethod
    def _clean(word: str) -> str:
        return word.strip().upper()

    def _validate_shape(self, word: str) -> None:
        if len(word) != self.WORD_LENGTH:
            raise ValueError(f"answer must be {self.WORD_LENGTH} letters, got {len(word)} letters")
        if not word.isalpha():
            raise ValueError(f"answer must be alpha, got {word!r}")

    def _validate_guess(self, word: str) -> None:
        self._validate_shape(word)
        if word not in self.valid_guesses:
            raise ValueError(f"guess must be in word bank, got {word!r}")

    # need to score guess and return useful info
    def guess(self, guess: str) -> list[int]:
        """
        Score a guess against the answer.

        Returns one int per position:
        0 = letter absent,
        1 = present but wrong position,
        2 = correct position.

        Raises ValueError if the word isn't a legal guess or
        the game is already over.
        """

        if self.num_guesses >= self.MAX_GUESSES:
            raise ValueError("game is over")

        guess = self._clean(guess)
        self._validate_guess(guess)

        c = Counter(self.answer)
        result: list[int | None] = [None] * self.WORD_LENGTH
        # mark exact matches and decrement letter count
        for i, letter in enumerate(guess):
            if letter == self.answer[i]:
                result[i] = 2
                c[letter] -= 1

        # only mark contained in word matches as 1 if enough letter count
        for i, letter in enumerate(guess):
            if result[i] is not None:
                continue
            if c[letter] > 0:
                result[i] = 1
                c[letter] -= 1
            else:
                result[i] = 0

        self.guesses.append((guess, result))
        return list(result)


