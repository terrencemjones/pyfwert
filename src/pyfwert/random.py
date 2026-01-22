"""Cryptographic random number generation with optional weighting.

Uses Python's secrets module for cryptographically secure randomness.
Ported from VB6 Rand() function in Main.bas.
"""

import secrets


def rand(max_val=9, min_val=0, weight=1, decimal_places=0):
    """Generate a random number with optional weighting.

    Args:
        max_val: Maximum value (inclusive). Default 9.
        min_val: Minimum value (inclusive). Default 0.
        weight: Weighting factor. Positive weights toward max, negative toward min.
                Absolute value determines iterations. Default 1.
        decimal_places: Number of decimal places. Default 0 (integer).

    Returns:
        Random number as int (if decimal_places=0) or float.

    The weighting works by applying multiple random selections:
    - weight > 0: Results tend toward max_val
    - weight < 0: Results tend toward min_val
    - weight = 0: Treated as 1

    Example:
        rand(100)  # Random 0-100
        rand(100, 50)  # Random 50-100
        rand(100, 0, 3)  # Weighted toward 100
        rand(100, 0, -3)  # Weighted toward 0
    """
    if max_val == 0:
        max_val = 9

    if weight == 0:
        weight = 1

    ceiling = float(max_val)

    for _ in range(abs(weight)):
        # Generate random float between 0 and 1
        rnd = secrets.randbelow(256) / 255.0
        ceiling = (rnd * (ceiling - min_val)) + min_val

    # Apply weight direction
    if weight > 0:
        ceiling = max_val - (ceiling - min_val)

    if decimal_places > 0:
        factor = 10 ** decimal_places
        return round(ceiling * factor) / factor
    else:
        return int(round(ceiling))


def chance(percent_chance, weight=1):
    """Return True if the percentage chance randomly occurs.

    Args:
        percent_chance: Probability from 0-100.
        weight: Weighting factor for the random check. Default 1.

    Returns:
        True if the random value is <= percent_chance.

    Example:
        if chance(50):  # 50% chance
            print("Heads!")
    """
    return rand(100, 1, weight) <= percent_chance


def randbelow(n):
    """Return a random int in the range [0, n).

    This is a simple wrapper around secrets.randbelow for consistency.

    Args:
        n: Upper bound (exclusive).

    Returns:
        Random integer from 0 to n-1.
    """
    if n <= 0:
        return 0
    return secrets.randbelow(n)
