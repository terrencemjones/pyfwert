"""Utility functions for password generation.

Ported from VB6 Main.bas.
"""

from pyfwert.random import rand


def pick_one(items, weight=1, delimiter=" "):
    """Pick a random item from a delimited string.

    Args:
        items: Space-separated string of items, or list of items.
        weight: Weighting factor for selection. Default 1.
        delimiter: Delimiter between items. Default " ".

    Returns:
        Randomly selected item (stripped of whitespace).

    Example:
        pick_one("apple banana cherry")  # Returns one fruit
        pick_one("a|b|c", delimiter="|")  # Returns 'a', 'b', or 'c'
    """
    if isinstance(items, str):
        item_list = items.split(delimiter)
    else:
        item_list = list(items)

    if len(item_list) == 0:
        return ""

    if len(item_list) == 1:
        return item_list[0].strip()

    index = rand(len(item_list) - 1, 0, weight)
    return item_list[index].strip()


def pick_character(characters, weight=0):
    """Pick a random character from a string.

    Args:
        characters: String of characters to choose from.
        weight: Weighting factor for selection. Default 0.

    Returns:
        Single randomly selected character.

    Example:
        pick_character("aeiou")  # Returns a random vowel
        pick_character("123456789", weight=2)  # Weighted toward higher digits
    """
    if not characters:
        return ""

    index = rand(len(characters), 1, weight) - 1
    return characters[index]


def sentence_case(text):
    """Capitalize the first letter, lowercase the rest.

    Args:
        text: Input string.

    Returns:
        String with first letter capitalized.

    Example:
        sentence_case("hELLO WORLD")  # Returns "Hello world"
    """
    if not text:
        return text
    return text[0].upper() + text[1:].lower()


def get_ordinal(num):
    """Return the ordinal string for a number (1st, 2nd, 3rd, etc).

    Args:
        num: Integer to convert.

    Returns:
        String with ordinal suffix.

    Example:
        get_ordinal(1)   # "1st"
        get_ordinal(2)   # "2nd"
        get_ordinal(11)  # "11th"
        get_ordinal(23)  # "23rd"
    """
    n = str(num)
    last_two = n[-2:] if len(n) >= 2 else n

    if last_two in ("11", "12", "13"):
        return n + "th"

    last_digit = n[-1]
    if last_digit == "1":
        return n + "st"
    elif last_digit == "2":
        return n + "nd"
    elif last_digit == "3":
        return n + "rd"
    else:
        return n + "th"


def get_phonetic(word, style=1):
    """Return NATO phonetic alphabet representation of a word.

    Args:
        word: String to convert.
        style: 1 for NATO alphabet, 2 for alternative alphabet.

    Returns:
        Space-separated phonetic words.

    Example:
        get_phonetic("ABC")  # "Alpha Bravo Charlie"
    """
    if style == 1 or style == 0:
        phonetic = [
            "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot",
            "Golf", "Hotel", "India", "Juliet", "Kilo", "Lima", "Mike",
            "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra",
            "Tango", "Uniform", "Victor", "Whiskey", "X-Ray", "Yankee", "Zulu"
        ]
    else:
        phonetic = [
            "Adam", "Baker", "Charles", "David", "Edward", "Frank",
            "George", "Henry", "Ida", "John", "King", "Lincoln", "Mary",
            "Nora", "Ocean", "Paul", "Queen", "Robert", "Sam",
            "Tom", "Union", "Victor", "William", "X-Ray", "Young", "Zebra"
        ]

    result = []
    for char in word.upper():
        idx = ord(char) - ord('A')
        if 0 <= idx < 26:
            result.append(phonetic[idx])

    return " ".join(result)


def to_roman(number):
    """Convert an integer to Roman numerals.

    Args:
        number: Integer to convert (1-3999).

    Returns:
        Roman numeral string.

    Example:
        to_roman(1994)  # "MCMXCIV"
        to_roman(4)     # "IV"
    """
    if not number or number <= 0:
        return ""

    result = ""
    num = int(number)

    values = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]

    for value, numeral in values:
        while num >= value:
            result += numeral
            num -= value

    return result
