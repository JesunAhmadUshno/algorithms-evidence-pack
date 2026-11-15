import random
import unittest

from algorithms_evidence_pack.binary_search import (
    binary_search,
    min_eating_speed,
    search_rotated,
)


class TestBinarySearch(unittest.TestCase):
    def test_found_and_missing(self):
        data = [1, 3, 5, 7, 9]
        for index, value in enumerate(data):
            self.assertEqual(binary_search(data, value), index)
        self.assertEqual(binary_search(data, 4), -1)
        self.assertEqual(binary_search([], 1), -1)

    def test_property_against_membership(self):
        rng = random.Random(53)
        for _ in range(200):
            data = sorted(rng.sample(range(-50, 50), rng.randint(0, 30)))
            target = rng.randint(-55, 55)
            result = binary_search(data, target)
            if target in data:
                self.assertEqual(data[result], target)
            else:
                self.assertEqual(result, -1)


class TestSearchRotated(unittest.TestCase):
    def test_known_cases(self):
        data = [4, 5, 6, 7, 0, 1, 2]
        self.assertEqual(search_rotated(data, 0), 4)
        self.assertEqual(search_rotated(data, 3), -1)
        self.assertEqual(search_rotated([1], 1), 0)
        self.assertEqual(search_rotated([1, 3], 3), 1)

    def test_property_against_linear_scan(self):
        rng = random.Random(59)
        for _ in range(200):
            base = sorted(rng.sample(range(0, 100), rng.randint(0, 25)))
            if not base:
                continue
            pivot = rng.randint(0, len(base) - 1)
            rotated = base[pivot:] + base[:pivot]
            target = rng.randint(-5, 105)
            result = search_rotated(rotated, target)
            if target in rotated:
                self.assertEqual(rotated[result], target)
            else:
                self.assertEqual(result, -1)


class TestMinEatingSpeed(unittest.TestCase):
    def test_known_cases(self):
        self.assertEqual(min_eating_speed([3, 6, 7, 11], 8), 4)
        self.assertEqual(min_eating_speed([30, 11, 23, 4, 20], 5), 30)
        self.assertEqual(min_eating_speed([30, 11, 23, 4, 20], 6), 23)

    def test_impossible_raises(self):
        with self.assertRaises(ValueError):
            min_eating_speed([1, 2, 3], 2)

    def test_property_against_brute_force(self):
        rng = random.Random(61)
        for _ in range(100):
            piles = [rng.randint(1, 30) for _ in range(rng.randint(1, 6))]
            hours = rng.randint(len(piles), len(piles) + 40)

            def hours_needed(speed):
                return sum(-(-pile // speed) for pile in piles)

            expected = next(
                speed for speed in range(1, max(piles) + 1)
                if hours_needed(speed) <= hours
            )
            result = min_eating_speed(piles, hours)
            self.assertEqual(result, expected)
            self.assertLessEqual(hours_needed(result), hours)
            if result > 1:
                self.assertGreater(hours_needed(result - 1), hours)


if __name__ == "__main__":
    unittest.main()
