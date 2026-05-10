import pytest

from utils.text_processing import clean_text, get_restricted_words


# ── clean_text ─────────────────────────────────────────────────────────────────

def test_clean_text_removes_punctuation():
    assert clean_text("Hello, world!") == "Hello world"


def test_clean_text_removes_all_punctuation_types():
    assert clean_text("one. two? three!") == "one two three"


def test_clean_text_keeps_letters_and_digits():
    result = clean_text("abc123")
    assert result == "abc123"


def test_clean_text_empty_string():
    assert clean_text("") == ""


def test_clean_text_only_punctuation_returns_empty():
    assert clean_text("!@#$%^&*()") == ""


def test_clean_text_preserves_spaces():
    result = clean_text("hello world")
    assert "hello" in result
    assert "world" in result


# ── get_restricted_words ───────────────────────────────────────────────────────

def test_get_restricted_words_missing_file_returns_empty_set():
    result = get_restricted_words("nonexistent_path/file.txt")
    assert result == set()


def test_get_restricted_words_returns_set(tmp_path):
    f = tmp_path / "words.txt"
    f.write_text("spam, junk, toxic\nbad, ugly", encoding="utf-8")
    result = get_restricted_words(str(f))
    assert isinstance(result, set)
    assert "spam" in result
    assert "junk" in result
    assert "toxic" in result
    assert "bad" in result


def test_get_restricted_words_lowercased(tmp_path):
    f = tmp_path / "words.txt"
    f.write_text("Spam, JUNK", encoding="utf-8")
    result = get_restricted_words(str(f))
    assert "spam" in result
    assert "junk" in result


def test_get_restricted_words_strips_whitespace(tmp_path):
    f = tmp_path / "words.txt"
    f.write_text("  word1 , word2  ", encoding="utf-8")
    result = get_restricted_words(str(f))
    assert "word1" in result
    assert "word2" in result