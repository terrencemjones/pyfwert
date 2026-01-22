"""Tests for text modifiers."""

import pytest
from pyfwert.modifiers import (
    apply_modifier,
    bracket,
    obscure,
    random_case,
    scramble_word,
    pig_latin,
    swap_initials,
    stutter,
)


class TestApplyModifier:
    """Test the apply_modifier function."""

    def test_uppercase(self):
        """Test uppercase modifier."""
        assert apply_modifier("hello", "uppercase") == "HELLO"
        assert apply_modifier("hello", "ucase") == "HELLO"

    def test_lowercase(self):
        """Test lowercase modifier."""
        assert apply_modifier("HELLO", "lowercase") == "hello"
        assert apply_modifier("HELLO", "lcase") == "hello"

    def test_propercase(self):
        """Test propercase modifier."""
        assert apply_modifier("hello world", "propercase") == "Hello World"

    def test_sentencecase(self):
        """Test sentencecase modifier."""
        assert apply_modifier("HELLO WORLD", "sentencecase") == "Hello world"

    def test_reverse(self):
        """Test reverse modifier."""
        assert apply_modifier("hello", "reverse") == "olleh"

    def test_a_modifier(self):
        """Test article 'a' modifier."""
        assert apply_modifier("dog", "a") == "a dog"
        assert apply_modifier("elephant", "a") == "an elephant"

    def test_quote(self):
        """Test quote modifier."""
        assert apply_modifier("hello", "quote") == '"hello"'

    def test_hide(self):
        """Test hide modifier."""
        assert apply_modifier("hello", "hide") == ""

    def test_repeat(self):
        """Test repeat modifier."""
        assert apply_modifier("ab", "repeat", ["2"]) == "ababab"

    def test_left(self):
        """Test left modifier."""
        assert apply_modifier("hello", "left", ["3"]) == "hel"

    def test_right(self):
        """Test right modifier."""
        assert apply_modifier("hello", "right", ["3"]) == "llo"

    def test_mid(self):
        """Test mid modifier."""
        assert apply_modifier("hello", "mid", ["2", "3"]) == "ell"

    def test_replace(self):
        """Test replace modifier."""
        assert apply_modifier("hello", "replace", ["l", "r"]) == "herro"

    def test_num2words(self):
        """Test num2words modifier."""
        result = apply_modifier("42", "num2words")
        assert "forty" in result.lower()
        assert "two" in result.lower()

    def test_romannumeral(self):
        """Test romannumeral modifier."""
        assert apply_modifier("4", "romannumeral") == "IV"
        assert apply_modifier("9", "romannumeral") == "IX"

    def test_unknown_modifier_raises(self):
        """Test that unknown modifiers raise ValueError."""
        with pytest.raises(ValueError):
            apply_modifier("hello", "nonexistent_modifier")

    def test_empty_word(self):
        """Test modifiers on empty string."""
        assert apply_modifier("", "uppercase") == ""


class TestBracket:
    """Test the bracket function."""

    def test_default_brackets(self):
        """Test bracketing with default brackets."""
        result = bracket("hello")
        assert result.startswith(tuple("[ < ( | \\ * { / \\ <- -".split()))
        assert "hello" in result

    def test_custom_brackets(self):
        """Test bracketing with custom brackets."""
        result = bracket("hello", "< > ( )")
        assert result in ["<hello>", "(hello)"]


class TestObscure:
    """Test the obscure function."""

    def test_obscure_modifies(self):
        """Test that obscure modifies the word."""
        # Run multiple times as it's random
        modified = False
        for _ in range(20):
            result = obscure("hello")
            if result != "hello":
                modified = True
                break
        # Should have modified at least once in 20 tries
        assert modified

    def test_obscure_empty(self):
        """Test obscure on empty string."""
        # Should not raise
        result = obscure("")
        assert result == ""


class TestRandomCase:
    """Test the random_case function."""

    def test_random_case_produces_variation(self):
        """Test that random case produces variation."""
        results = set()
        for _ in range(50):
            result = random_case("hello")
            results.add(result)
        # Should have multiple different results
        assert len(results) > 1


class TestScrambleWord:
    """Test the scramble_word function."""

    def test_scramble_length_preserved(self):
        """Test that scramble preserves length."""
        result = scramble_word("hello", 5)
        assert len(result) == 5

    def test_scramble_characters_preserved(self):
        """Test that scramble preserves characters."""
        result = scramble_word("hello", 10)
        assert sorted(result) == sorted("hello")


class TestPigLatin:
    """Test the pig_latin function."""

    def test_vowel_start(self):
        """Test pig latin for word starting with vowel."""
        assert pig_latin("apple") == "appleyay"

    def test_consonant_start(self):
        """Test pig latin for word starting with consonant."""
        assert pig_latin("hello") == "ellohay"

    def test_multiple_words(self):
        """Test pig latin for multiple words."""
        result = pig_latin("hello world")
        assert "ellohay" in result
        assert "orldway" in result

    def test_capitalization_preserved(self):
        """Test that capitalization is preserved."""
        result = pig_latin("Hello")
        assert result[0].isupper()


class TestSwapInitials:
    """Test the swap_initials function."""

    def test_swap_two_words(self):
        """Test swapping initials of two words."""
        result = swap_initials("hello world")
        assert result == "wello horld"

    def test_single_word(self):
        """Test swap with single word."""
        result = swap_initials("hello")
        assert result == "hello"


class TestStutter:
    """Test the stutter function."""

    def test_stutter_repeats(self):
        """Test that stutter adds repetition."""
        result = stutter("hello")
        # Should be longer than original
        assert len(result) >= len("hello")
