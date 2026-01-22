"""Pyfwert - Pattern-based password generator.

A Python port of the Pafwert VB6 password generator.
Generates strong, memorable passwords using pattern templates.

Example usage:
    from pyfwert import generate_password

    # Simple usage
    password = generate_password("{word}.{word}.{word}")

    # With modifiers
    password = generate_password("{word+uppercase}-{number(99)}")

    # Using the class
    from pyfwert import PasswordGenerator
    gen = PasswordGenerator(wordlist_dir="/custom/path")
    password = gen.generate("{word(animal)} {word(color)}")
"""

__version__ = "0.1.0"
__author__ = "Mark Burnett"
__license__ = "Apache-2.0"

from pyfwert.generator import PasswordGenerator, generate_password
from pyfwert.wordlists import (
    set_wordlist_dir,
    get_default_wordlist_dir,
    random_word,
    load_patterns,
    get_random_pattern,
)
from pyfwert.pronounceable import pronounceable_word, fakeword

__all__ = [
    # Main API
    "PasswordGenerator",
    "generate_password",
    # Wordlist functions
    "set_wordlist_dir",
    "get_default_wordlist_dir",
    "random_word",
    "load_patterns",
    "get_random_pattern",
    # Word generation
    "pronounceable_word",
    "fakeword",
    # Version info
    "__version__",
]
