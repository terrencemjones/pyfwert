"""Main password generator class.

Ported from VB6 PafwertLib.cls.
"""

import re

from pyfwert.parser import parse_placeholder_content
from pyfwert.placeholders import resolve_placeholder
from pyfwert.modifiers import apply_modifier
from pyfwert.wordlists import get_random_pattern, get_default_wordlist_dir
from pyfwert.random import rand, chance
from pyfwert.utils import pick_one, pick_character
from pyfwert.constants import (
    VOWELS2, CONSONANTS2, THREE_LETTER_WORDS,
    UNESCAPE_SEQUENCES, ESCAPE_SEQUENCES
)


class PasswordGenerator:
    """Pattern-based password generator.

    Generates strong, memorable passwords using pattern templates
    and extensive wordlists.
    """

    def __init__(self, wordlist_dir=None):
        """Initialize the password generator.

        Args:
            wordlist_dir: Optional custom wordlist directory.
                          If None, uses the bundled wordlists.
        """
        self.wordlist_dir = wordlist_dir
        self.keywords = ""
        self.last_pattern = ""
        self.last_password = ""
        self._backrefs = {}

    def generate(self, pattern=None, keywords=None):
        """Generate a password using a pattern.

        Args:
            pattern: Pattern string (e.g., "{word}.{number}").
                     If None, uses a random pattern from patterns.cfg.
            keywords: Optional keywords for word selection.

        Returns:
            Generated password string.

        Example patterns:
            - "{word}.{word}.{word}" -> "bone.horse.berner"
            - "{word+uppercase}{number(99)}" -> "DRAGON42"
            - "{word(animal)} {number}" -> "horse 7"
        """
        max_retries = 10

        for attempt in range(max_retries):
            try:
                if pattern:
                    result = self._generate_from_pattern(pattern, keywords)
                else:
                    random_pattern = get_random_pattern(self.wordlist_dir)
                    result = self._generate_from_pattern(random_pattern, keywords)

                self.last_password = result
                return result

            except Exception as e:
                if attempt == max_retries - 1:
                    # Failsafe: generate something rather than fail
                    return self._generate_failsafe()
                continue

        return self._generate_failsafe()

    def _generate_from_pattern(self, pattern, keywords=None):
        """Generate password from a specific pattern.

        Args:
            pattern: Pattern string.
            keywords: Optional keywords.

        Returns:
            Generated password.
        """
        self.last_pattern = pattern
        self._backrefs = {}
        self._backref_counter = 0

        # Apply escape sequences
        escaped = self._escape_pattern(pattern)

        # Process placeholders recursively
        result = self._process_pattern(escaped, keywords)

        # Unescape
        result = self._unescape(result)

        # Clean up double spaces
        while "  " in result:
            result = result.replace("  ", " ")

        return result.strip()

    def _escape_pattern(self, pattern):
        """Apply escape sequences to pattern."""
        result = pattern
        for escape, token in ESCAPE_SEQUENCES.items():
            result = result.replace(escape, token)
        return result

    def _process_pattern(self, pattern, keywords=None):
        """Process a pattern, resolving all placeholders.

        Uses a recursive approach to handle nested placeholders.
        """
        result = ""
        i = 0
        while i < len(pattern):
            if pattern[i] == "{":
                # Find matching closing brace
                depth = 1
                j = i + 1
                while j < len(pattern) and depth > 0:
                    if pattern[j] == "{":
                        depth += 1
                    elif pattern[j] == "}":
                        depth -= 1
                    j += 1

                if depth == 0:
                    # Extract placeholder content
                    content = pattern[i+1:j-1]

                    # Process any nested placeholders first
                    processed_content = self._process_pattern(content, keywords)

                    # Resolve this placeholder
                    value = self._resolve_placeholder_content(processed_content, keywords)

                    # Check for qualifier after closing brace (e.g., }[50])
                    if j < len(pattern) and pattern[j] == "[":
                        qual_end = pattern.find("]", j)
                        if qual_end != -1:
                            try:
                                qualifier = int(pattern[j+1:qual_end])
                                if rand(99, 0) >= qualifier:
                                    value = ""
                            except ValueError:
                                pass
                            j = qual_end + 1

                    # Check for modifiers after the closing brace (e.g., }+propercase)
                    while j < len(pattern) and pattern[j] == "+":
                        # Parse the modifier
                        mod_end = j + 1
                        paren_depth = 0
                        # Find end of modifier - stop at +, {, space, or . (but not inside parens)
                        while mod_end < len(pattern):
                            c = pattern[mod_end]
                            if c == "(":
                                paren_depth += 1
                            elif c == ")":
                                paren_depth -= 1
                            elif paren_depth == 0 and c in "+{ \t.":
                                break
                            mod_end += 1

                        mod_str = pattern[j+1:mod_end]
                        if mod_str:
                            # Parse modifier name, params, and qualifier
                            mod_name, mod_params, mod_qualifier = self._parse_modifier_string(mod_str)

                            # Process any placeholders in modifier parameters
                            mod_params = [self._process_pattern(p, keywords) if "{" in p else p
                                          for p in mod_params]

                            # Check qualifier
                            if mod_qualifier is None or rand(99, 0) < mod_qualifier:
                                try:
                                    # Unescape value, apply modifier, re-escape
                                    unescaped = self._unescape(value)
                                    # Also unescape modifier params
                                    mod_params = [self._unescape(p) for p in mod_params]
                                    modified = apply_modifier(unescaped, mod_name, mod_params)
                                    value = self._escape_value(modified)
                                except ValueError:
                                    pass

                        j = mod_end

                    result += value
                    i = j
                else:
                    # Unmatched brace, treat as literal
                    result += pattern[i]
                    i += 1
            else:
                result += pattern[i]
                i += 1

        return result

    def _parse_modifier_string(self, mod_str):
        """Parse a modifier string like 'propercase[25]' or 'replace(" ","-")'.

        Returns:
            Tuple of (modifier_name, params_list, qualifier_int_or_none)
        """
        mod_name = mod_str
        mod_params = []
        mod_qualifier = None

        # Check for qualifier [N]
        qual_start = mod_str.find("[")
        if qual_start != -1:
            qual_end = mod_str.find("]", qual_start)
            if qual_end != -1:
                try:
                    mod_qualifier = int(mod_str[qual_start+1:qual_end])
                except ValueError:
                    pass
                mod_str = mod_str[:qual_start] + mod_str[qual_end+1:]
                mod_name = mod_str

        # Check for parameters (name(param1, param2))
        param_start = mod_str.find("(")
        if param_start != -1:
            param_end = mod_str.find(")", param_start)
            if param_end != -1:
                mod_name = mod_str[:param_start]
                param_str = mod_str[param_start+1:param_end]
                mod_params = [p.strip().strip('"') for p in param_str.split(",")]

        return mod_name, mod_params, mod_qualifier

    def _resolve_placeholder_content(self, content, keywords=None):
        """Resolve placeholder content to a value.

        Args:
            content: The content between { and }.
            keywords: Optional keywords.

        Returns:
            Resolved value.
        """
        # Check for backreference first
        if content.startswith("$W"):
            try:
                ref_num = int(content[2:])
                if ref_num in self._backrefs:
                    return self._backrefs[ref_num]
                return ""
            except ValueError:
                return ""

        # Parse the placeholder content
        parsed = parse_placeholder_content(content)

        # Handle alternatives (pipe separator)
        if parsed["alternatives"]:
            # Pick one of the alternatives
            choice = pick_one(parsed["alternatives"], delimiter="|")
            # If the choice contains braces, it has sub-placeholders to process
            if "{" in choice:
                return self._process_pattern(choice, keywords)
            # Otherwise, return the choice as literal text
            return choice

        # Check qualifier
        if parsed["qualifier"] is not None:
            if rand(99, 0) >= parsed["qualifier"]:
                return ""

        # Get the base value
        name = parsed["name"]
        params = parsed["params"]

        # If the name is empty or starts with space, it's likely a grouping construct
        # like { {Word(something)}} where the inner placeholder was already processed
        # In this case, return the content as literal text (but respect the qualifier)
        if not name or (content and content[0] in " \t"):
            # Remove any qualifier that was already parsed
            result_content = content
            # The parsed qualifier should still apply
            if parsed["qualifier"] is not None:
                # Qualifier was already checked above, so we passed - just clean up content
                # Remove [N] from content if present
                import re
                result_content = re.sub(r'\[\d+\]', '', content)

            # Store for backreference (the processed content)
            self._backref_counter += 1
            self._backrefs[self._backref_counter] = result_content
            return result_content

        value = resolve_placeholder(
            name, params,
            wordlist_dir=self.wordlist_dir,
            keywords=keywords
        )

        # Apply modifiers
        for mod_name, mod_params, mod_qualifier in parsed["modifiers"]:
            # Check modifier qualifier
            if mod_qualifier is not None:
                if rand(99, 0) >= mod_qualifier:
                    continue

            # Process any placeholders in modifier parameters
            processed_params = []
            for p in mod_params:
                if "{" in p:
                    processed_params.append(self._unescape(self._process_pattern(p, keywords)))
                else:
                    processed_params.append(p)

            try:
                value = apply_modifier(value, mod_name, processed_params)
            except ValueError:
                # Unknown modifier, skip
                pass

        # Escape special characters in the value
        value = self._escape_value(value)

        # Store escaped value for backreference
        self._backref_counter += 1
        self._backrefs[self._backref_counter] = value

        return value

    def _escape_value(self, value):
        """Escape special characters in a resolved value.

        Args:
            value: The resolved value.

        Returns:
            Escaped value.
        """
        # Escape characters that have special meaning in patterns
        replacements = [
            ("\\", "#sla#"),
            ("+", "#pls#"),
            ("{", "#lbr#"),
            ("}", "#rbr#"),
            ("[", "#lba#"),
            ("]", "#rba#"),
            ("(", "#lpa#"),
            (")", "#rpa#"),
            ("|", "#pip#"),
        ]
        for old, new in replacements:
            value = value.replace(old, new)
        return value

    def _unescape(self, text):
        """Convert escape tokens back to actual characters.

        Args:
            text: Text with escape tokens.

        Returns:
            Text with actual characters.
        """
        for token, char in UNESCAPE_SEQUENCES.items():
            text = text.replace(token, char)
        return text

    def _generate_failsafe(self):
        """Generate a failsafe password when normal generation fails.

        Returns:
            A simple generated password.
        """
        parts = []
        for _ in range(7):
            parts.append(pick_one(
                VOWELS2 + " ! @ # % $ ^ & * : ' / ` ~ * - < > + = . . , , ; ; ? ? " +
                CONSONANTS2 + " " + THREE_LETTER_WORDS +
                " 1 2 3 4 5 6 7 8 9 0"
            ))
        return "".join(parts)


def generate_password(pattern=None, wordlist_dir=None, keywords=None):
    """Convenience function to generate a password.

    Args:
        pattern: Pattern string (optional, uses random if not provided).
        wordlist_dir: Optional custom wordlist directory.
        keywords: Optional keywords for word selection.

    Returns:
        Generated password string.

    Example:
        password = generate_password("{word}.{word}.{number}")
    """
    gen = PasswordGenerator(wordlist_dir=wordlist_dir)
    return gen.generate(pattern, keywords)
