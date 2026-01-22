"""Placeholder resolution for password generation.

Ported from VB6 GetWord() in PafwertLib.cls.
"""

from pyfwert.random import rand, chance
from pyfwert.utils import pick_one, pick_character, get_ordinal, get_phonetic
from pyfwert.pronounceable import pronounceable_word
from pyfwert.wordlists import random_word
from pyfwert import constants


def resolve_placeholder(name, params=None, wordlist_dir=None, keywords=None):
    """Resolve a placeholder to its value.

    Args:
        name: Placeholder name (e.g., "word", "number", "symbol").
        params: Optional list of parameters.
        wordlist_dir: Optional custom wordlist directory.
        keywords: Optional keywords for word selection.

    Returns:
        The resolved value as a string.
    """
    if params is None:
        params = ["", "", "", ""]
    else:
        params = list(params) + ["", "", "", ""]
        params = params[:4]

    placeholder = name.lower().strip()

    # Word from wordlist
    if placeholder == "word":
        wordlist = params[0] if params[0] else "4-letter"
        # Handle alternatives in wordlist parameter (e.g., "Verb|babysound")
        if "|" in wordlist:
            wordlist = pick_one(wordlist.split("|"), delimiter="|")
        return random_word(wordlist, wordlist_dir)

    # Space
    if placeholder in ("sp", "space"):
        return " "

    # Vowel
    if placeholder == "vowel":
        count = int(params[0]) if params[0] else 1
        return "".join(pick_character(constants.VOWELS) for _ in range(count))

    # Consonant
    if placeholder == "consonant":
        count = int(params[0]) if params[0] else 1
        return "".join(pick_character(constants.CONSONANTS) for _ in range(count))

    # Symbol
    if placeholder == "symbol":
        return pick_one(constants.SYMBOLS)

    # End punctuation
    if placeholder == "endpunctuation":
        return pick_one(constants.END_PUNCTUATION)

    # Sentence punctuation
    if placeholder == "sentencepunctuation":
        return pick_character(constants.SENTENCE_PUNCTUATION)

    # Number
    if placeholder == "number":
        max_val = int(params[0]) if params[0] else 9
        min_val = int(params[1]) if params[1] else 0
        weight = int(params[2]) if params[2] else 1
        decimal_places = int(params[3]) if params[3] else 0
        return str(rand(max_val, min_val, weight, decimal_places))

    # Letter
    if placeholder == "letter":
        count = int(params[0]) if params[0] else 1
        if count < 0:
            count = abs(count)
        return "".join(pick_character(constants.LETTERS) for _ in range(count))

    # Smiley
    if placeholder == "smiley":
        return pick_one(constants.SMILEYS)

    # Keyboard character
    if placeholder == "keyboard":
        return pick_character(constants.KEYBOARD)

    # Number row
    if placeholder == "numrow":
        return pick_character(constants.NUMROW)

    if placeholder == "numrowfull":
        return pick_character(constants.NUMROW_FULL)

    # Keyboard rows
    if placeholder == "row1":
        return pick_character(constants.ROW1)

    if placeholder == "row1full":
        return pick_character(constants.ROW1_FULL)

    if placeholder == "row2":
        return pick_character(constants.ROW2)

    if placeholder == "row2full":
        return pick_character(constants.ROW2_FULL)

    if placeholder == "row3":
        return pick_character(constants.ROW3)

    if placeholder == "row3full":
        return pick_character(constants.ROW3_FULL)

    # Hand positions
    if placeholder == "lefthand":
        return pick_character(constants.LEFT_HAND)

    if placeholder == "righthand":
        return pick_character(constants.RIGHT_HAND)

    # Sequence
    if placeholder == "sequence":
        length = int(params[0]) if params[0] else 3
        return get_sequence(length)

    # Ordinal
    if placeholder == "ordinal":
        num = int(params[0]) if params[0] else rand(99, 1)
        return get_ordinal(num)

    # Phonetic
    if placeholder == "phonetic":
        word = params[0] if params[0] else pick_character(constants.LETTERS)
        style = int(params[1]) if params[1] else 1
        return get_phonetic(word, style)

    # Pronounceable fake word
    if placeholder == "pronounceable":
        return pronounceable_word()

    # Number pattern
    if placeholder == "numberpattern":
        length = int(params[0]) if params[0] else 3
        return get_number_pattern(length)

    # ASCII code
    if placeholder == "asc":
        if params[0]:
            return str(ord(params[0][0]))
        return str(rand(255, 32))

    # Character from ASCII code
    if placeholder == "chr":
        if params[0]:
            try:
                code = int(params[0])
                if 32 <= code <= 126:
                    return chr(code)
            except ValueError:
                pass
        return ""

    # Long month name
    if placeholder == "longmonth":
        return pick_one(constants.LONG_MONTHS)

    # Short month name
    if placeholder == "shortmonth":
        return pick_one(constants.SHORT_MONTHS)

    # Long day name
    if placeholder == "longday":
        return pick_one(constants.LONG_DAYS)

    # Short day name
    if placeholder == "shortday":
        return pick_one(constants.SHORT_DAYS)

    # Number code (formatted number pattern)
    if placeholder == "numbercode":
        return number_code()

    # If not recognized, treat it as a wordlist name or literal
    try:
        return random_word(placeholder, wordlist_dir)
    except FileNotFoundError:
        # Return the placeholder name as literal text
        return name


def get_sequence(length=3):
    """Generate a keyboard sequence.

    Args:
        length: Length of sequence.

    Returns:
        A keyboard sequence string.
    """
    letters = "abcdefghijklmnopqrstuvwxyz"
    numbers = "1234567890"
    key1 = "qwertyuiop"
    key2 = "asdfghjkl"
    key3 = "zxcvbnm"
    key4 = "poiuytrewq"
    key5 = "lkjhgfdsa"
    key6 = "mnbvcxz"

    if length <= 0:
        length = 3

    choice = rand(19)
    seq = ""

    if choice == 1:
        start = rand(len(letters) - length, 0)
        seq = letters[start:start + length]

    elif choice == 2:
        start = rand(len(numbers) - length, 0)
        seq = numbers[start:start + length]

    elif choice == 3:
        start = rand(len(key1) - length, 0)
        seq = key1[start:start + length]

    elif choice == 4:
        start = rand(len(key2) - length, 0)
        seq = key2[start:start + length]

    elif choice == 5:
        start = rand(len(key3) - length, 0)
        seq = key3[start:start + length]

    elif choice == 6:
        start = rand(len(key4) - length, 0)
        seq = key4[start:start + length]

    elif choice == 7:
        start = rand(len(key5) - length, 0)
        seq = key5[start:start + length]

    elif choice == 8:
        start = rand(len(key6) - length, 0)
        seq = key6[start:start + length]

    elif choice == 9:
        i = rand(7, 1)
        n = length // 3
        seq = key1[i:i+n] + key2[i:i+n] + key3[i:i+n]

    elif choice == 10:
        i = rand(7, 1)
        n = length // 3
        seq = key3[i:i+n] + key2[i:i+n] + key1[i:i+n]

    elif choice in (11, 12, 13):
        i = rand(min(8, len(key1) - 1, len(key2) - 1), 1)
        while len(seq) < length:
            if i < len(key1) and i < len(key2):
                seq += key1[i] + key2[i]
            i = (i + 1) % min(len(key1), len(key2))

    elif choice == 14:
        i = rand(9, 1)
        while len(seq) < length:
            if i < len(key1) and i < len(numbers):
                seq += key1[i] + numbers[i]
            i = (i + 1) % min(len(key1), len(numbers))

    elif choice in (15, 16):
        i = rand(min(8, len(key4) - 1, len(key5) - 1), 1)
        while len(seq) < length:
            if i < len(key4) and i < len(key5):
                seq += key4[i] + key5[i]
            i = (i + 1) % min(len(key4), len(key5))

    elif choice == 17:
        i = rand(9, 1)
        while len(seq) < length and i < len(key1):
            j = len(key1) - i - 1
            if j >= 0 and j < len(key1):
                seq += key1[i] + key1[j]
            i += 1

    elif choice == 18:
        i = rand(8, 1)
        while len(seq) < length and i < len(key2):
            j = len(key2) - i - 1
            if j >= 0 and j < len(key2):
                seq += key2[i] + key2[j]
            i += 1

    else:
        i = rand(6, 1)
        while len(seq) < length and i < len(key3):
            j = len(key3) - i - 1
            if j >= 0 and j < len(key3):
                seq += key3[i] + key3[j]
            i += 1

    return seq[:length]


def get_number_pattern(length=3):
    """Generate a patterned number sequence.

    Args:
        length: Length of pattern.

    Returns:
        A patterned number string.
    """
    if length <= 0:
        length = 3

    digits = [""] * (length + 1)
    digits[1] = str(rand(9))

    for i in range(2, length + 1):
        choice = rand(3, 0)

        if choice == 0:
            digits[i] = str(rand(9))
        elif choice == 1:
            digits[i] = digits[rand(i - 1, 1)]
        elif choice == 2:
            prev = int(digits[i - 1]) if digits[i - 1] else 0
            if prev > 1:
                digits[i] = str(prev - 1)
            else:
                digits[i] = str(rand(9))
        else:
            prev = int(digits[i - 1]) if digits[i - 1] else 0
            if prev < 9:
                digits[i] = str(prev + 1)
            else:
                digits[i] = str(rand(9))

    result = "".join(digits[1:])
    return result.zfill(length)


def number_code():
    """Generate a number code with delimiters.

    Returns:
        A formatted number code string.
    """
    repeat_digit = str(rand(9, 0))
    delim = pick_one("- - - - - - - - . . . , / \\ :")

    code = ""
    while True:
        x = str(rand(9, 0))

        while True:
            code += x

            if chance(30):
                code += repeat_digit
            elif chance(40):
                code += delim

            if len(code) > 2:
                break

            if not chance(30):
                break

        if len(code) > rand(4, 3):
            break

        if chance(10):
            from pyfwert.modifiers import bracket
            code = bracket(code)

        if chance(15) and len(code) > 2:
            break

    # Remove trailing non-numeric character
    if code and not code[-1].isdigit():
        code = code[:-1]

    return code
