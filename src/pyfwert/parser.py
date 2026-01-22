"""Pattern parsing for password generation.

Ported from VB6 ParsePattern() in PafwertLib.cls.
"""

from pyfwert.constants import ESCAPE_SEQUENCES


class Placeholder:
    """Represents a placeholder in a pattern."""

    def __init__(self):
        self.original_pattern = ""
        self.normalized_pattern = ""
        self.completed_pattern = ""
        self.parent = -1
        self.start = 0
        self.index = 0


def escape_pattern(pattern):
    """Replace escape sequences with placeholder tokens.

    Args:
        pattern: Raw pattern string.

    Returns:
        Pattern with escape sequences replaced.
    """
    result = pattern
    for escape, token in ESCAPE_SEQUENCES.items():
        result = result.replace(escape, token)
    return result


def parse_pattern(pattern):
    """Parse a pattern string into a list of placeholders.

    Args:
        pattern: Pattern string (e.g., "{word}.{number}").

    Returns:
        List of Placeholder objects representing the parsed pattern.

    Raises:
        ValueError: If the pattern has mismatched braces.
    """
    pattern = pattern.strip()

    # Apply escape sequences
    escaped = escape_pattern(pattern)

    # Pad closing braces to make room for pattern ID
    escaped = escaped.replace("}", "}00")

    placeholders = []
    position_stack = []
    placeholder_count = 0
    master_pattern = ""

    i = 0
    while i < len(escaped):
        char = escaped[i]
        master_pattern += char

        if char == "{":
            position_stack.append(i)

        elif char == "}":
            if not position_stack:
                raise ValueError(f"Mismatched braces in pattern: {pattern}")

            placeholder_count += 1
            pattern_id = f"{placeholder_count:02d}"
            master_pattern += pattern_id

            # Replace the "00" padding with actual ID
            escaped = escaped[:i+1] + pattern_id + escaped[i+3:]

            # Create placeholder
            ph = Placeholder()
            ph.index = placeholder_count
            ph.start = position_stack.pop()

            if position_stack:
                ph.parent = position_stack[-1]
            else:
                ph.parent = -1

            # Extract patterns from escaped string
            ph.original_pattern = escaped[ph.start:i+3]  # Includes {, }, and ID
            ph.normalized_pattern = escaped[ph.start+1:i]  # Content between { and }

            placeholders.append(ph)

            # Skip past the pattern ID
            i += 2

        i += 1

    # Add the master placeholder (the complete pattern)
    master = Placeholder()
    master.index = placeholder_count + 1
    master.original_pattern = pattern
    master.normalized_pattern = master_pattern
    master.start = 0
    master.parent = -1
    placeholders.append(master)

    # Resolve parent references
    for ph in placeholders[:-1]:
        if ph.parent == -1:
            ph.parent = len(placeholders) - 1
        else:
            # Find the placeholder with matching start position
            for other in placeholders:
                if other.start == ph.parent:
                    ph.parent = other.index
                    break

    return placeholders


def check_pattern(pattern):
    """Check if a pattern is syntactically valid.

    Args:
        pattern: Pattern string to check.

    Returns:
        Error message string, or empty string if valid.
    """
    if not pattern:
        return "Error: Empty pattern"

    # Apply escape sequences for checking
    test_pattern = escape_pattern(pattern)

    # Count brackets, braces, and parentheses
    counts = {
        "{": 0, "}": 0,
        "[": 0, "]": 0,
        "(": 0, ")": 0,
    }

    for char in test_pattern:
        if char in counts:
            counts[char] += 1

    if counts["{"] != counts["}"]:
        return "Error: Unmatched braces in pattern"

    if counts["["] != counts["]"]:
        return "Error: Unmatched brackets in pattern"

    if counts["("] != counts[")"]:
        return "Error: Unmatched parentheses in pattern"

    try:
        parse_pattern(pattern)
    except ValueError as e:
        return f"Error: {e}"

    return ""


def parse_placeholder_content(content):
    """Parse the content of a placeholder into its components.

    Args:
        content: The content between { and }.

    Returns:
        Dict with:
            - name: The placeholder name (e.g., "word", "number")
            - params: List of parameters
            - modifiers: List of (modifier_name, params, qualifier) tuples
            - qualifier: Optional percentage qualifier
            - alternatives: List of alternatives if using | separator
    """
    result = {
        "name": "",
        "params": [],
        "modifiers": [],
        "qualifier": None,
        "alternatives": None,
    }

    # Check for alternatives (pipe separator), but not inside parentheses
    # e.g., "a|b|c" -> alternatives, but "Word(a|b)" -> NOT alternatives
    alternatives = _split_by_pipe(content)
    if len(alternatives) > 1:
        result["alternatives"] = alternatives
        return result

    # First split by + to separate base from modifiers
    # We need to be careful not to split inside parentheses
    parts = _split_by_plus(content)
    base = parts[0]
    modifier_parts = parts[1:]

    # Parse modifiers first (each can have its own qualifier)
    for mod in modifier_parts:
        mod_name = mod
        mod_params = []
        mod_qualifier = None

        # Check for qualifier in modifier [N]
        qual_start = mod.find("[")
        if qual_start != -1:
            qual_end = mod.find("]", qual_start)
            if qual_end != -1:
                try:
                    mod_qualifier = int(mod[qual_start+1:qual_end])
                except ValueError:
                    pass
                mod = mod[:qual_start] + mod[qual_end+1:]
                mod_name = mod

        # Check for parameters in modifier
        param_start = mod.find("(")
        if param_start != -1:
            param_end = mod.find(")", param_start)
            if param_end != -1:
                mod_name = mod[:param_start]
                param_str = mod[param_start+1:param_end]
                mod_params = [p.strip().strip('"') for p in param_str.split(",")]

        result["modifiers"].append((mod_name, mod_params, mod_qualifier))

    # Now parse the base (name, params, and qualifier)
    # Check for qualifier [N] on base
    qualifier_start = base.find("[")
    if qualifier_start != -1:
        qualifier_end = base.find("]", qualifier_start)
        if qualifier_end != -1:
            try:
                result["qualifier"] = int(base[qualifier_start+1:qualifier_end])
            except ValueError:
                pass
            base = base[:qualifier_start] + base[qualifier_end+1:]

    # Check for parameters (name(param1, param2))
    param_start = base.find("(")
    if param_start != -1:
        param_end = base.find(")", param_start)
        if param_end != -1:
            result["name"] = base[:param_start].strip()
            param_str = base[param_start+1:param_end]
            result["params"] = [p.strip().strip('"') for p in param_str.split(",")]
        else:
            result["name"] = base.strip()
    else:
        result["name"] = base.strip()

    return result


def _split_by_plus(content):
    """Split content by + but not inside parentheses.

    Args:
        content: String to split.

    Returns:
        List of parts.
    """
    parts = []
    current = ""
    depth = 0

    for char in content:
        if char == "(":
            depth += 1
            current += char
        elif char == ")":
            depth -= 1
            current += char
        elif char == "+" and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char

    if current:
        parts.append(current)

    return parts if parts else [content]


def _split_by_pipe(content):
    """Split content by | but not inside parentheses.

    Args:
        content: String to split.

    Returns:
        List of parts.
    """
    parts = []
    current = ""
    depth = 0

    for char in content:
        if char == "(":
            depth += 1
            current += char
        elif char == ")":
            depth -= 1
            current += char
        elif char == "|" and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char

    if current:
        parts.append(current)

    return parts if parts else [content]
