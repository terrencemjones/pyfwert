"""Number to text conversion.

Ported from VB6 NumText.bas by Frederick Rothstein.
"""

# Number word lookup table
NUMBER_TEXT = [
    "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
    "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen",
    "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty",
    "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"
]


def _hundreds_tens_units(value, use_and=False):
    """Convert a number 0-999 to words.

    Args:
        value: Integer 0-999.
        use_and: Whether to include "and" before tens/units.

    Returns:
        String representation of the number.
    """
    result = ""
    test_value = int(value)

    if test_value > 99:
        cardinal = test_value // 100
        result = NUMBER_TEXT[cardinal] + " Hundred "
        test_value = test_value - (cardinal * 100)

    if use_and:
        result += "and "

    if test_value > 20:
        cardinal = test_value // 10
        result += NUMBER_TEXT[cardinal + 18] + " "
        test_value = test_value - (cardinal * 10)

    if test_value > 0:
        result += NUMBER_TEXT[test_value] + " "

    return result


def number_as_text(number_in):
    """Convert a number to its text representation.

    Args:
        number_in: Number to convert (string or numeric).

    Returns:
        English text representation of the number.

    Example:
        number_as_text(123)     # "One Hundred Twenty Three"
        number_as_text(1000)    # "One Thousand"
        number_as_text(-42)     # "Minus Forty Two"
        number_as_text(3.14)    # "Three Point One Four"
    """
    number_str = str(number_in).strip()

    # Check for valid number
    try:
        float(number_str.replace(",", ""))
    except ValueError:
        return "Error - Number improperly formed"

    # Handle sign
    number_sign = ""
    if number_str.startswith("-"):
        number_sign = "Minus "
        number_str = number_str[1:]
    elif number_str.startswith("+"):
        number_sign = "Plus "
        number_str = number_str[1:]

    # Handle decimal point
    decimal_part = ""
    if "." in number_str:
        parts = number_str.split(".")
        whole_part = parts[0].replace(",", "")
        decimal_part = parts[1]
    else:
        whole_part = number_str.replace(",", "")

    # Handle very large numbers
    big_whole_part = ""
    if len(whole_part) > 9:
        big_whole_part = whole_part[:-9]
        whole_part = whole_part[-9:]

    if len(big_whole_part) > 9:
        return "Error - Number too large"

    result = ""

    # Very large values (billions and up)
    if big_whole_part:
        test_value = int(big_whole_part)

        if test_value > 999999:
            cardinal = test_value // 1000000
            result = _hundreds_tens_units(cardinal) + "Quadrillion "
            test_value = test_value - (cardinal * 1000000)

        if test_value > 999:
            cardinal = test_value // 1000
            result += _hundreds_tens_units(cardinal) + "Trillion "
            test_value = test_value - (cardinal * 1000)

        if test_value > 0:
            result += _hundreds_tens_units(test_value) + "Billion "

    # Regular values (up to 999,999,999)
    test_value = int(whole_part) if whole_part else 0

    if test_value == 0 and not big_whole_part:
        result = "Zero "

    if test_value > 999999:
        cardinal = test_value // 1000000
        result += _hundreds_tens_units(cardinal) + "Million "
        test_value = test_value - (cardinal * 1000000)

    if test_value > 999:
        cardinal = test_value // 1000
        result += _hundreds_tens_units(cardinal) + "Thousand "
        test_value = test_value - (cardinal * 1000)

    if test_value > 0:
        use_and = int(whole_part) >= 100 or bool(big_whole_part)
        result += _hundreds_tens_units(test_value, use_and)

    # Handle decimal portion
    if decimal_part:
        result += "Point"
        for digit in decimal_part:
            if digit.isdigit():
                result += " " + NUMBER_TEXT[int(digit)]

    return number_sign + result.strip()
