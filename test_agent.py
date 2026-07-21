import pytest
from agent import parse_guess

def test_exact_guess_does_not_mutate():
    assert parse_guess("CRANE") == "CRANE"

def test_returns_upper_case():
    assert parse_guess("crane") == "CRANE"

def test_punctuation_removed_and_last_word_extracted():
    assert parse_guess("I'll guess CRANE!") == "CRANE"

def test_invalid_guess():
    assert parse_guess("I don't know") is None

def test_multiple_candidates_takes_last():
    assert parse_guess("CRANE or SLOTH") == "SLOTH"