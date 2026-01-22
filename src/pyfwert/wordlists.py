"""Wordlist loading and caching.

Provides efficient random word selection from wordlist files.
"""

import os
from pathlib import Path

from pyfwert.random import rand


# Module-level cache for loaded wordlists
_wordlist_cache = {}

# Default wordlist directory (relative to this module)
_default_wordlist_dir = None


def get_default_wordlist_dir():
    """Get the default wordlist directory path.

    Returns:
        Path to the data/wordlists directory.
    """
    global _default_wordlist_dir
    if _default_wordlist_dir is None:
        _default_wordlist_dir = Path(__file__).parent / "data" / "wordlists"
    return _default_wordlist_dir


def set_wordlist_dir(path):
    """Set a custom wordlist directory.

    Args:
        path: Path to directory containing wordlist files.
    """
    global _default_wordlist_dir
    _default_wordlist_dir = Path(path)


def get_wordlist_path(name, wordlist_dir=None):
    """Get the full path to a wordlist file.

    Args:
        name: Wordlist name (with or without .txt extension).
        wordlist_dir: Optional custom wordlist directory.

    Returns:
        Path object to the wordlist file.

    Raises:
        FileNotFoundError: If the wordlist file doesn't exist.
    """
    if wordlist_dir is None:
        wordlist_dir = get_default_wordlist_dir()
    else:
        wordlist_dir = Path(wordlist_dir)

    # Add .txt extension if not present
    if not name.lower().endswith(".txt"):
        name = name + ".txt"

    filepath = wordlist_dir / name

    if not filepath.exists():
        raise FileNotFoundError(f"Wordlist file not found: {filepath}")

    return filepath


def load_wordlist(name, wordlist_dir=None):
    """Load a wordlist file into memory.

    Args:
        name: Wordlist name (e.g., "animal", "color").
        wordlist_dir: Optional custom wordlist directory.

    Returns:
        List of words from the wordlist.

    Results are cached for performance.
    """
    if wordlist_dir is None:
        wordlist_dir = get_default_wordlist_dir()

    cache_key = f"{wordlist_dir}:{name.lower()}"

    if cache_key in _wordlist_cache:
        return _wordlist_cache[cache_key]

    filepath = get_wordlist_path(name, wordlist_dir)

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        words = [line.strip() for line in f if line.strip()]

    _wordlist_cache[cache_key] = words
    return words


def random_word(name, wordlist_dir=None):
    """Get a random word from a wordlist.

    Args:
        name: Wordlist name (e.g., "animal", "color").
        wordlist_dir: Optional custom wordlist directory.

    Returns:
        A random word from the wordlist.

    This function uses efficient file seeking for large files
    or loads smaller files into memory.
    """
    if wordlist_dir is None:
        wordlist_dir = get_default_wordlist_dir()

    filepath = get_wordlist_path(name, wordlist_dir)
    file_size = os.path.getsize(filepath)

    # For small files, load into memory (cached)
    if file_size < 100000:  # 100KB threshold
        words = load_wordlist(name, wordlist_dir)
        if not words:
            return ""
        return words[rand(len(words) - 1, 0)]

    # For large files, use random seeking (like the VB6 version)
    buffer_size = 128

    with open(filepath, "rb") as f:
        max_retries = 5
        for _ in range(max_retries):
            # Seek to random position
            seek_pos = rand(file_size - buffer_size, 1)
            f.seek(seek_pos)

            # Read a buffer
            buffer = f.read(buffer_size).decode("utf-8", errors="ignore")

            # Find the next complete line
            lines = buffer.split("\n")
            if len(lines) >= 3:
                # Return the second complete line (first may be partial)
                word = lines[1].strip()
                if word:
                    return word

    # Fallback: load entire file
    words = load_wordlist(name, wordlist_dir)
    if not words:
        return ""
    return words[rand(len(words) - 1, 0)]


def count_words(name, wordlist_dir=None):
    """Count the number of words in a wordlist.

    Args:
        name: Wordlist name.
        wordlist_dir: Optional custom wordlist directory.

    Returns:
        Number of words in the wordlist.
    """
    words = load_wordlist(name, wordlist_dir)
    return len(words)


def load_patterns(wordlist_dir=None):
    """Load and parse the patterns.cfg file.

    Args:
        wordlist_dir: Optional custom wordlist directory.

    Returns:
        List of tuples (name, pattern) for each pattern.
    """
    if wordlist_dir is None:
        wordlist_dir = get_default_wordlist_dir()

    filepath = Path(wordlist_dir) / "patterns.cfg"

    if not filepath.exists():
        raise FileNotFoundError(f"Patterns file not found: {filepath}")

    patterns = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Split on first colon
            if ":" in line:
                name, pattern = line.split(":", 1)
                patterns.append((name.strip(), pattern.strip()))
            else:
                patterns.append(("", line))

    return patterns


def get_random_pattern(wordlist_dir=None):
    """Get a random pattern from patterns.cfg.

    Args:
        wordlist_dir: Optional custom wordlist directory.

    Returns:
        A random pattern string.
    """
    patterns = load_patterns(wordlist_dir)
    if not patterns:
        raise ValueError("No patterns found in patterns.cfg")

    index = rand(len(patterns) - 1, 0)
    return patterns[index][1]


def clear_cache():
    """Clear the wordlist cache."""
    global _wordlist_cache
    _wordlist_cache = {}
