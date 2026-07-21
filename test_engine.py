import pytest
from engine import Game

def test_exact_match_returns_all_greens():
    game = Game("CRANE", {"CRANE"})
    assert game.guess("CRANE") == [2, 2, 2, 2, 2]

def test_no_shared_letters_returns_all_greys():
    game = Game("PLANE", {"HICKS"})
    assert game.guess("HICKS") == [0, 0, 0, 0, 0]

def test_letter_in_wrong_position_returns_yellow():
    game = Game("PLANE", {"LICKS"})
    assert game.guess("LICKS") == [1, 0, 0, 0, 0]

def test_green_consumes_letter_before_yellows():
    game = Game("ABIDE", {"GEESE"})
    assert game.guess("GEESE") == [0, 0, 0, 0, 2]

def test_duplicate_guess_letter_marks_only_available_count():
    game = Game("ABIDE", {"BREED"})
    assert game.guess("BREED") == [1, 0, 1, 0, 1]

def test_guess_outside_word_bank_raises():
    game = Game("ABIDE", {"PLANE"})
    with pytest.raises(ValueError):
        game.guess("CRANE")

def test_guess_after_max_guesses_raises():
    game = Game("ABIDE", {"PLANE", "CRANE", "BRAIN", "DRAIN", "HURRY", "SANDY", "HANDY"})
    game.guess("PLANE")
    game.guess("CRANE")
    game.guess("BRAIN")
    game.guess("DRAIN")
    game.guess("HURRY")
    game.guess("SANDY")
    with pytest.raises(ValueError):
        game.guess("HANDY")