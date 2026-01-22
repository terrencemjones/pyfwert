# Pyfwert

A pattern-based password generator that creates strong, memorable passwords.

Pyfwert is a Python port of the [Pafwert](https://github.com/xato/pafwert) VB6 password generator. Unlike random generators that produce strings like "KBYd4ie*2", Pyfwert generates passwords like "bone.horse.berner" or "Miss. Undercarriage" using pattern templates and extensive wordlists.

## Installation

```bash
pip install pyfwert
```

## Quick Start

```python
from pyfwert import generate_password

# Generate a simple password
password = generate_password("{word}.{word}.{word}")
# Example output: "bone.horse.berner"

# Generate with numbers and symbols
password = generate_password("{word}{number(99)}{symbol}")
# Example output: "dragon42!"

# Generate with modifiers
password = generate_password("{word+uppercase}-{word+obscure}")
# Example output: "THUNDER-h0rs3"
```

## Advanced Usage

```python
from pyfwert import PasswordGenerator

# Create a generator with custom wordlist directory
gen = PasswordGenerator(wordlist_dir="/path/to/wordlists")

# Generate with various patterns
password = gen.generate("{word(animal)+propercase} {word(color)}")
# Example output: "Horse blue"

# Use backreferences
password = gen.generate("{number(9)}{$W1}{$W1}")
# Example output: "777"
```

## Pattern Syntax

Patterns use placeholders enclosed in curly braces `{...}`:

### Basic Placeholders

- `{word}` - Random word from default wordlist
- `{word(animal)}` - Random word from specific wordlist
- `{number}` - Random digit (0-9)
- `{number(99)}` - Random number (0-99)
- `{number(100,999)}` - Random number in range
- `{symbol}` - Random symbol
- `{letter}` - Random letter
- `{vowel}` - Random vowel
- `{consonant}` - Random consonant
- `{pronounceable}` - Fake pronounceable word
- `{sequence(5)}` - Keyboard sequence of length 5

### Modifiers

Add modifiers with `+`:

- `+uppercase` / `+ucase` - Convert to uppercase
- `+lowercase` / `+lcase` - Convert to lowercase
- `+propercase` - Capitalize first letter
- `+randomcase` - Random capitalization
- `+obscure` - L33t-speak substitutions
- `+reverse` - Reverse the text
- `+bracket` - Wrap in brackets
- `+piglatin` - Convert to pig latin
- `+scramble` - Scramble letters
- `+num2words` - Convert number to words

### Selection Groups

Use `|` for random selection:

```python
"{word|number|symbol}"  # Randomly picks word, number, or symbol
"{Mr.|Mrs.|Ms.}"        # Randomly picks a title
```

### Qualifiers

Use `[N]` for percentage chance:

```python
"{word[50]}"  # 50% chance of including a word
"{symbol[25]}"  # 25% chance of including a symbol
```

### Backreferences

Use `$W1`, `$W2`, etc. to reference previous placeholders:

```python
"{number(9)}{$W1}{$W1}"  # Repeats the same digit: "777"
```

### Escape Characters

- `\\` - Literal backslash
- `\{` - Literal opening brace
- `\}` - Literal closing brace
- `\+` - Literal plus sign

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

## Credits

Original Pafwert by Mark Burnett (2001-2013).
Python port created in 2026.
