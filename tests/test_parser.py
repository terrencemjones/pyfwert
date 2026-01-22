"""Tests for pattern parsing."""

import pytest
from pyfwert.parser import (
    parse_pattern,
    check_pattern,
    parse_placeholder_content,
    escape_pattern,
)


class TestParsePattern:
    """Test pattern parsing."""

    def test_simple_placeholder(self):
        """Test parsing a simple placeholder."""
        placeholders = parse_pattern("{word}")
        assert len(placeholders) == 2  # placeholder + master
        assert "word" in placeholders[0].normalized_pattern

    def test_multiple_placeholders(self):
        """Test parsing multiple placeholders."""
        placeholders = parse_pattern("{word}.{number}")
        # 2 placeholders + 1 master
        assert len(placeholders) == 3

    def test_nested_placeholders(self):
        """Test parsing nested placeholders."""
        placeholders = parse_pattern("{word({animal})}")
        # Nested structure
        assert len(placeholders) >= 2

    def test_literal_text_preserved(self):
        """Test that literal text is preserved."""
        placeholders = parse_pattern("Hello {word} World")
        master = placeholders[-1]
        assert "Hello" in master.normalized_pattern or "Hello" in master.original_pattern

    def test_escape_sequences(self):
        """Test escape sequences are handled."""
        result = escape_pattern("\\{escaped\\}")
        assert "#lbr#" in result
        assert "#rbr#" in result


class TestCheckPattern:
    """Test pattern validation."""

    def test_valid_pattern(self):
        """Test that valid patterns pass."""
        assert check_pattern("{word}") == ""
        assert check_pattern("{word}.{number}") == ""
        assert check_pattern("Hello {world}") == ""

    def test_empty_pattern(self):
        """Test that empty pattern fails."""
        result = check_pattern("")
        assert "Error" in result

    def test_mismatched_braces(self):
        """Test that mismatched braces fail."""
        result = check_pattern("{word")
        assert "Error" in result or "Unmatched" in result

    def test_unmatched_brackets(self):
        """Test that unmatched brackets fail."""
        result = check_pattern("{word[50}")
        assert "Error" in result

    def test_unmatched_parens(self):
        """Test that unmatched parentheses fail."""
        result = check_pattern("{word(animal}")
        assert "Error" in result


class TestParsePlaceholderContent:
    """Test placeholder content parsing."""

    def test_simple_name(self):
        """Test parsing a simple placeholder name."""
        result = parse_placeholder_content("word")
        assert result["name"] == "word"
        assert result["params"] == []
        assert result["modifiers"] == []

    def test_with_parameters(self):
        """Test parsing placeholder with parameters."""
        result = parse_placeholder_content("word(animal)")
        assert result["name"] == "word"
        assert result["params"] == ["animal"]

    def test_multiple_parameters(self):
        """Test parsing placeholder with multiple parameters."""
        result = parse_placeholder_content("number(100, 50)")
        assert result["name"] == "number"
        assert "100" in result["params"]
        assert "50" in result["params"]

    def test_with_modifier(self):
        """Test parsing placeholder with modifier."""
        result = parse_placeholder_content("word+uppercase")
        assert result["name"] == "word"
        assert len(result["modifiers"]) == 1
        assert result["modifiers"][0][0] == "uppercase"

    def test_multiple_modifiers(self):
        """Test parsing placeholder with multiple modifiers."""
        result = parse_placeholder_content("word+uppercase+reverse")
        assert result["name"] == "word"
        assert len(result["modifiers"]) == 2

    def test_with_qualifier(self):
        """Test parsing placeholder with qualifier."""
        result = parse_placeholder_content("word[50]")
        assert result["name"] == "word"
        assert result["qualifier"] == 50

    def test_modifier_with_params(self):
        """Test parsing modifier with parameters."""
        result = parse_placeholder_content('word+replace("a","b")')
        assert result["name"] == "word"
        assert len(result["modifiers"]) == 1
        mod_name, mod_params, _ = result["modifiers"][0]
        assert mod_name == "replace"
        assert "a" in mod_params
        assert "b" in mod_params

    def test_alternatives(self):
        """Test parsing alternatives."""
        result = parse_placeholder_content("a|b|c")
        assert result["alternatives"] == ["a", "b", "c"]
