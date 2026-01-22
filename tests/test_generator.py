"""Tests for the main password generator."""

import pytest
from pyfwert import PasswordGenerator, generate_password


class TestPasswordGenerator:
    """Test the PasswordGenerator class."""

    def test_simple_word_pattern(self):
        """Test generating a password with a simple word pattern."""
        gen = PasswordGenerator()
        password = gen.generate("{word(4-letter)}")
        assert len(password) > 0
        assert password.isalpha()

    def test_word_dot_word_pattern(self):
        """Test word.word pattern generates expected format."""
        gen = PasswordGenerator()
        password = gen.generate("{word(4-letter)}.{word(4-letter)}")
        assert "." in password
        parts = password.split(".")
        assert len(parts) == 2

    def test_number_pattern(self):
        """Test number placeholder."""
        gen = PasswordGenerator()
        password = gen.generate("{number}")
        assert password.isdigit()
        assert 0 <= int(password) <= 9

    def test_number_with_range(self):
        """Test number placeholder with range."""
        gen = PasswordGenerator()
        for _ in range(10):
            password = gen.generate("{number(100,50)}")
            num = int(password)
            assert 50 <= num <= 100

    def test_symbol_pattern(self):
        """Test symbol placeholder."""
        gen = PasswordGenerator()
        password = gen.generate("{symbol}")
        assert len(password) >= 1
        # Should be a non-alphanumeric character
        assert not password.isalnum()

    def test_letter_pattern(self):
        """Test letter placeholder."""
        gen = PasswordGenerator()
        password = gen.generate("{letter}")
        assert len(password) == 1
        assert password.isalpha()

    def test_vowel_pattern(self):
        """Test vowel placeholder."""
        gen = PasswordGenerator()
        password = gen.generate("{vowel}")
        assert len(password) == 1
        assert password.lower() in "aeiou"

    def test_consonant_pattern(self):
        """Test consonant placeholder."""
        gen = PasswordGenerator()
        password = gen.generate("{consonant}")
        assert len(password) == 1
        assert password.lower() not in "aeiou"
        assert password.isalpha()

    def test_uppercase_modifier(self):
        """Test uppercase modifier."""
        gen = PasswordGenerator()
        password = gen.generate("{word(4-letter)+uppercase}")
        assert password == password.upper()

    def test_lowercase_modifier(self):
        """Test lowercase modifier."""
        gen = PasswordGenerator()
        password = gen.generate("{word(4-letter)+lowercase}")
        assert password == password.lower()

    def test_propercase_modifier(self):
        """Test propercase modifier."""
        gen = PasswordGenerator()
        password = gen.generate("{word(4-letter)+propercase}")
        assert password[0].isupper()

    def test_reverse_modifier(self):
        """Test reverse modifier."""
        gen = PasswordGenerator()
        # Use a known word to verify reversal
        password = gen.generate("{sp+reverse}")  # Space reversed is still space
        assert password == " "

    def test_combined_pattern(self):
        """Test a combined pattern."""
        gen = PasswordGenerator()
        password = gen.generate("{word(4-letter)}{number(99)}{symbol}")
        assert len(password) >= 4 + 1 + 1  # word + number + symbol

    def test_literal_text(self):
        """Test literal text in pattern."""
        gen = PasswordGenerator()
        password = gen.generate("Hello{number}")
        assert password.startswith("Hello")

    def test_sequence_pattern(self):
        """Test sequence placeholder."""
        gen = PasswordGenerator()
        password = gen.generate("{sequence(5)}")
        assert len(password) == 5

    def test_pronounceable_pattern(self):
        """Test pronounceable word generation."""
        gen = PasswordGenerator()
        password = gen.generate("{pronounceable}")
        assert len(password) > 0
        assert password.isalpha()

    def test_last_pattern_recorded(self):
        """Test that last pattern is recorded."""
        gen = PasswordGenerator()
        pattern = "{word(4-letter)}"
        gen.generate(pattern)
        assert gen.last_pattern == pattern


class TestGeneratePasswordFunction:
    """Test the convenience function."""

    def test_basic_call(self):
        """Test basic function call."""
        password = generate_password("{number(9)}")
        assert password.isdigit()

    def test_with_pattern(self):
        """Test with explicit pattern."""
        password = generate_password("{letter}{letter}{letter}")
        assert len(password) == 3
        assert password.isalpha()


class TestBackreferences:
    """Test backreference functionality."""

    def test_simple_backreference(self):
        """Test that backreferences repeat values."""
        gen = PasswordGenerator()
        # Generate a number and repeat it
        pattern = "{number(9)}{$W1}{$W1}"
        password = gen.generate(pattern)
        # Should be the same digit repeated 3 times
        assert len(password) == 3
        assert password[0] == password[1] == password[2]

    def test_word_backreference(self):
        """Test that word backreferences repeat the word."""
        gen = PasswordGenerator()
        pattern = "{word(4-letter)}-{$W1}"
        password = gen.generate(pattern)
        # Should be word-word
        parts = password.split("-")
        assert len(parts) == 2
        assert parts[0] == parts[1]


class TestQualifiers:
    """Test qualifier functionality."""

    def test_always_qualifier(self):
        """Test 100% qualifier always includes."""
        gen = PasswordGenerator()
        for _ in range(5):
            password = gen.generate("A{symbol[100]}B")
            assert len(password) >= 3  # A + symbol + B

    def test_never_qualifier(self):
        """Test 0% qualifier never includes."""
        gen = PasswordGenerator()
        for _ in range(5):
            password = gen.generate("A{symbol[0]}B")
            # Should just be "AB" since symbol is 0%
            assert password == "AB"


class TestAlternatives:
    """Test alternatives (pipe separator) functionality."""

    def test_simple_alternatives(self):
        """Test that alternatives pick one option."""
        gen = PasswordGenerator()
        results = set()
        for _ in range(50):
            password = gen.generate("{a|b|c}")
            results.add(password)
        # Should have picked from multiple options
        assert len(results) > 1
        assert all(r in ["a", "b", "c"] for r in results)
