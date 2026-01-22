"""Text modifiers for password generation.

Ported from VB6 ModifyWord() in PafwertLib.cls.
"""

from pyfwert.random import rand, chance
from pyfwert.utils import pick_one, sentence_case, to_roman
from pyfwert.number_text import number_as_text


def apply_modifier(word, modifier_name, params=None):
    """Apply a modifier to a word.

    Args:
        word: The word to modify.
        modifier_name: Name of the modifier.
        params: Optional list of parameters for the modifier.

    Returns:
        Modified word.

    Raises:
        ValueError: If the modifier is not recognized.
    """
    if not word:
        return word

    if params is None:
        params = ["", "", "", ""]
    else:
        # Ensure we have at least 4 parameters
        params = list(params) + ["", "", "", ""]
        params = params[:4]

    modifier = modifier_name.lower().strip()

    # Article "a" or "an"
    if modifier == "a":
        if word[0].lower() in "aeiou":
            return "an " + word
        return "a " + word

    # Bracket with various bracket types
    if modifier == "bracket":
        return bracket(word, params[0])

    # Number to words
    if modifier in ("num2word", "num2words"):
        return sentence_case(number_as_text(word))

    # Reverse string
    if modifier == "reverse":
        return word[::-1]

    # Uppercase
    if modifier in ("ucase", "uppercase"):
        return word.upper()

    # Lowercase
    if modifier in ("lcase", "lowercase"):
        return word.lower()

    # Proper case (capitalize each word)
    if modifier == "propercase":
        return word.title()

    # Sentence case
    if modifier == "sentencecase":
        return sentence_case(word)

    # Obscure (leet speak)
    if modifier == "obscure":
        return obscure(word)

    # Replace
    if modifier == "replace":
        return word.replace(params[0], params[1])

    # Random case
    if modifier == "randomcase":
        return random_case(word)

    # Scramble letters
    if modifier == "scramble":
        times = int(params[0]) if params[0] else 1
        return scramble_word(word, times)

    # Pig latin
    if modifier == "piglatin":
        return pig_latin(word)

    # Repeat
    if modifier == "repeat":
        times = int(params[0]) if params[0] else 1
        return word * (times + 1)

    # Right substring
    if modifier == "right":
        length = int(params[0]) if params[0] else len(word)
        return word[-length:]

    # Left substring
    if modifier == "left":
        length = int(params[0]) if params[0] else len(word)
        return word[:length]

    # Trim whitespace
    if modifier == "trim":
        return word.strip()

    # Format (for numbers)
    if modifier == "format":
        try:
            fmt = params[0] if params[0] else "0"
            # Convert VB format to Python (basic support)
            if "0" in fmt:
                width = fmt.count("0")
                return word.zfill(width)
            return word
        except Exception:
            return word

    # Mid substring
    if modifier == "mid":
        start = int(params[0]) if params[0] else 1
        length = int(params[1]) if params[1] else 1
        return word[start-1:start-1+length]

    # Swap first letters of two words
    if modifier == "swap":
        return swap_initials(word)

    # Roman numeral
    if modifier == "romannumeral":
        try:
            return to_roman(int(word))
        except ValueError:
            return word

    # Hide (return empty string)
    if modifier == "hide":
        return ""

    # Quote
    if modifier == "quote":
        return '"' + word + '"'

    # Stutter
    if modifier == "stutter":
        return stutter(word)

    # Random modifier
    if modifier == "random":
        random_mod = pick_one("bracket num2words randomcase reverse obscure piglatin scramble swap")
        return apply_modifier(word, random_mod, params)

    # Unknown modifier - return word unchanged (or raise error)
    raise ValueError(f"Unknown modifier: {modifier}")


def bracket(word, bracket_list=""):
    """Wrap a word in random brackets.

    Args:
        word: Word to bracket.
        bracket_list: Optional custom bracket pairs (space-separated).

    Returns:
        Bracketed word.
    """
    if not bracket_list:
        bracket_list = "[ ] < > ( ) ( ) ( ) ( ) ( ) ( ) ( ) ( ) [ ] [ ] | | \\ / * * [ ] { } / / \\ / / \\ \\ \\ <- -> -> <-"

    brackets = bracket_list.split(" ")
    if len(brackets) < 2:
        return word

    x = int(rand(len(brackets) // 2 - 1, 0)) * 2
    return brackets[x] + word + brackets[x + 1]


def obscure(word):
    """Apply leet-speak style substitutions to a word.

    Args:
        word: Word to obscure.

    Returns:
        Obscured word.
    """
    result = word

    # Substitution rules: (pattern, replacement, case_number)
    rules = [
        ("ate", "8"), ("for", "4"), ("e", "3"), ("l", "1"), ("s", "z"),
        ("o", "0"), ("a", "@"), ("s", "$"), ("l", "|"), ("ait", "8"),
        ("a", ""), ("e", ""), ("ou", "u"), ("cc", "x"), ("oo", "ew"),
        ("and", "&"), ("are", "r"), ("ks", "x"), ("f", "ph"), ("ph", "f"),
        ("won", "1"), ("l", "r"), ("ee", "eee"), ("000", "k"), ("er", "r"),
        ("ex", "x"), ("ecs", "x"), ("m", "mm"), ("cke", "x0"), ("qu", "kw"),
        ("a", "'"), ("u", "'"), ("ei", "ee"), ("one", "own"), ("oi", "oy"),
        ("om", "um"), ("a", "aa"), ("ew", "u"), ("us", "is"), ("y", "ee"),
        ("sh", "ch"), ("to", "2"), ("s", "th"), ("ck", "q"), ("ci", "si"),
        ("ie", "iye"), ("tion", "shun"), ("r", "w"), ("come", "cum"),
        ("cks", "x"), ("ight", "ite"), ("ing", "'n"), ("th", "f"),
        ("too", "2"), ("why", "y"), ("your", "yor"), ("sc", "sh"),
        ("sh", "th"), ("ly", "lee"), ("er", "uh"), ("er", "a"),
        ("the", "da"), ("it is", "'tis"), ("you", "ya"), ("l", "w"),
        ("th", "d"), ("a", "u"), ("th", "'"), ("your", "yer"),
        ("ned", "nt"), ("e", "_"), ("t", "+"), ("e", "="), ("can", "kin"),
        ("t", "'"), ("ng", "n'"), ("red", "hed"), ("he", "eh"), ("h", ""),
        ("f", "v"), ("ha", "o"), ("v", "f"), ("v", "b"), ("N", "|\\|"),
        ("ll", "dd"), ("ll", "tt"), ("dd", "tt"), ("h", "'"), ("o", "a"),
        ("e", "a"), ("a", "uh"), ("a", "u"), ("oo", "u"), ("i", "ih"),
        ("a ", "ah"), ("s", "ss"), ("t", "tt"), ("d", "dd"), ("at", "@"),
        (" ", ""), ("with", "w/"), ("t", "d"), ("t", "dd"), ("d", "t"),
        ("d", "tt"), ("cks", "x"), ("er", "ah"),
    ]

    # Apply 2-20 random substitutions
    max_attempts = rand(20, 2, 2)
    for i in range(max_attempts):
        rule_index = rand(len(rules) - 1, 0)
        old, new = rules[rule_index]

        if old in result:
            result = result.replace(old, new, 1)

        # If we've made changes, maybe exit early
        if i >= 2 and result != word and chance(75):
            break

    return result


def random_case(word):
    """Apply random capitalization to a word.

    Args:
        word: Word to transform.

    Returns:
        Word with random case.
    """
    from pyfwert.constants import VOWELS, CONSONANTS

    choice = rand(14, 0)

    if choice == 0:
        # Do nothing
        return word

    elif choice == 1:
        # All upper
        return word.upper()

    elif choice == 2:
        # All lower
        return word.lower()

    elif choice == 3:
        # Title case
        return word.title()

    elif choice == 4:
        # Pick one letter and uppercase all occurrences
        letter = word[rand(len(word) - 1, 0)]
        return word.replace(letter, letter.upper())

    elif choice == 5:
        # Totally random
        return "".join(c.upper() if rand(1) else c for c in word)

    elif choice in (6, 7):
        # Uppercase one random character
        i = rand(len(word) - 1, 0)
        return word[:i] + word[i].upper() + word[i+1:]

    elif choice == 8:
        # Vowels uppercase
        return "".join(c.upper() if c.lower() in VOWELS else c for c in word)

    elif choice == 9:
        # Consonants uppercase
        return "".join(c.upper() if c.lower() in CONSONANTS else c for c in word)

    elif choice == 10:
        # Two consecutive letters uppercase
        i = rand(len(word) - 2, 0)
        return word[:i] + word[i:i+2].upper() + word[i+2:]

    elif choice == 11:
        # Last letter uppercase
        return word[:-1] + word[-1].upper()

    elif choice == 12:
        # First and last letters uppercase
        if len(word) >= 2:
            return word[0].upper() + word[1:-1] + word[-1].upper()
        return word.upper()

    elif choice == 13:
        # First x letters uppercase
        x = rand(len(word), 1, 2)
        return word[:x].upper() + word[x:]

    else:  # choice == 14
        # Every other letter uppercase
        return "".join(c.upper() if i % 2 == 0 else c for i, c in enumerate(word))


def scramble_word(word, times=1):
    """Randomly swap characters in a word.

    Args:
        word: Word to scramble.
        times: Number of swaps to perform.

    Returns:
        Scrambled word.
    """
    if len(word) < 2:
        return word

    chars = list(word)
    for _ in range(times):
        x1 = rand(len(chars) - 1, 0)
        x2 = rand(len(chars) - 1, 0)
        chars[x1], chars[x2] = chars[x2], chars[x1]

    return "".join(chars)


def pig_latin(text):
    """Convert text to pig latin.

    Args:
        text: Text to convert.

    Returns:
        Pig latin version.
    """
    words = text.split(" ")
    result = []

    for word in words:
        if not word:
            result.append(word)
            continue

        first_char = word[0].lower()

        if first_char in "aeiou":
            converted = word + "yay"
        else:
            converted = word[1:] + word[0] + "ay"

        # Preserve original capitalization
        if word[0].isupper():
            converted = converted[0].upper() + converted[1:].lower()

        result.append(converted)

    return " ".join(result)


def swap_initials(text):
    """Swap the first letters of two words in a phrase.

    Args:
        text: Text containing multiple words.

    Returns:
        Text with first letters swapped.
    """
    words = text.split(" ")
    if len(words) < 2:
        return text

    # Swap first letters of first two words
    word1 = list(words[0])
    word2 = list(words[1])

    if word1 and word2:
        word1[0], word2[0] = word2[0], word1[0]
        words[0] = "".join(word1)
        words[1] = "".join(word2)

    return " ".join(words)


def stutter(word):
    """Add a stutter effect to a word.

    Args:
        word: Word to stutter.

    Returns:
        Stuttered word.
    """
    syllable_marker = "aeiou" if rand(100) > 20 else "hywrtnaeiou"

    for i, char in enumerate(word):
        if char.lower() in syllable_marker:
            first_part = word[:i+1]
            stuttered = word

            # Maybe add ellipsis
            if rand(100) < 5:
                first_part += "..."
            # Maybe add space
            if rand(100) < 10:
                first_part += " "

            # Repeat 1-4 times
            for _ in range(rand(4, 1, -2)):
                stuttered = first_part + stuttered

            return stuttered

    return word
