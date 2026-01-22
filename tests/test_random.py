"""Tests for random number generation."""

import pytest
from pyfwert.random import rand, chance, randbelow


class TestRand:
    """Test the rand function."""

    def test_default_range(self):
        """Test default range is 0-9."""
        for _ in range(100):
            result = rand()
            assert 0 <= result <= 9

    def test_custom_max(self):
        """Test custom maximum."""
        for _ in range(100):
            result = rand(100)
            assert 0 <= result <= 100

    def test_custom_range(self):
        """Test custom min and max."""
        for _ in range(100):
            result = rand(100, 50)
            assert 50 <= result <= 100

    def test_distribution(self):
        """Test that values are distributed across range."""
        results = [rand(10) for _ in range(1000)]
        unique = set(results)
        # Should hit most values in 1000 tries
        assert len(unique) >= 8

    def test_positive_weight(self):
        """Test positive weight biases toward max."""
        results = [rand(100, 0, 5) for _ in range(1000)]
        avg = sum(results) / len(results)
        # With weight 5, should be biased toward 100
        assert avg > 50

    def test_negative_weight(self):
        """Test negative weight biases toward min."""
        results = [rand(100, 0, -5) for _ in range(1000)]
        avg = sum(results) / len(results)
        # With weight -5, should be biased toward 0
        assert avg < 50

    def test_decimal_places(self):
        """Test decimal places."""
        result = rand(100, 0, 1, 2)
        # Should be a float
        assert isinstance(result, float)

    def test_zero_max_defaults_to_nine(self):
        """Test that max=0 defaults to 9."""
        for _ in range(20):
            result = rand(0)
            assert 0 <= result <= 9

    def test_zero_weight_treated_as_one(self):
        """Test that weight=0 is treated as 1."""
        # Should not crash
        result = rand(100, 0, 0)
        assert 0 <= result <= 100


class TestChance:
    """Test the chance function."""

    def test_always(self):
        """Test 100% chance always returns True."""
        for _ in range(100):
            assert chance(100) is True

    def test_never(self):
        """Test 0% chance always returns False."""
        for _ in range(100):
            assert chance(0) is False

    def test_fifty_percent(self):
        """Test 50% chance returns mix of True/False."""
        results = [chance(50) for _ in range(1000)]
        true_count = sum(results)
        # Should be roughly 50%, allow 35-65% range
        assert 350 < true_count < 650

    def test_low_percent(self):
        """Test low percentage is mostly False."""
        results = [chance(10) for _ in range(1000)]
        true_count = sum(results)
        # Should be roughly 10%, allow 5-15% range
        assert 50 < true_count < 150

    def test_high_percent(self):
        """Test high percentage is mostly True."""
        results = [chance(90) for _ in range(1000)]
        true_count = sum(results)
        # Should be roughly 90%, allow 85-95% range
        assert 850 < true_count < 950


class TestRandbelow:
    """Test the randbelow function."""

    def test_range(self):
        """Test that result is in range [0, n)."""
        for _ in range(100):
            result = randbelow(10)
            assert 0 <= result < 10

    def test_distribution(self):
        """Test that values are distributed."""
        results = [randbelow(10) for _ in range(1000)]
        unique = set(results)
        # Should hit all values in 1000 tries
        assert len(unique) == 10

    def test_zero(self):
        """Test that n=0 returns 0."""
        assert randbelow(0) == 0

    def test_negative(self):
        """Test that negative n returns 0."""
        assert randbelow(-5) == 0

    def test_one(self):
        """Test that n=1 always returns 0."""
        for _ in range(20):
            assert randbelow(1) == 0
