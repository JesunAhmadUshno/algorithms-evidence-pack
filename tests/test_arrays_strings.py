import random
import unittest

from algorithms_evidence_pack.arrays_strings import (
    PrefixSums,
    longest_substring_without_repeating,
    sliding_window_maximum,
    two_sum_sorted,
)


class TestTwoSumSorted(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(two_sum_sorted([2, 7, 11, 15], 9), (0, 1))

    def test_no_pair(self):
        self.assertIsNone(two_sum_sorted([1, 2, 3], 100))

    def test_property_against_brute_force(self):
        rng = random.Random(42)
        for _ in range(200):
            data = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 12)))
            target = rng.randint(-30, 30)
            expected = None
            for i in range(len(data)):
                for j in range(i + 1, len(data)):
                    if data[i] + data[j] == target:
                        expected = (i, j)
                        break
                if expected is not None:
                    break
            result = two_sum_sorted(data, target)
            if expected is None:
                self.assertIsNone(result)
            else:
                self.assertIsNotNone(result)
                i, j = result
                self.assertEqual(data[i] + data[j], target)


class TestLongestSubstring(unittest.TestCase):
    def test_known_cases(self):
        self.assertEqual(longest_substring_without_repeating("abcabcbb"), 3)
        self.assertEqual(longest_substring_without_repeating("bbbbb"), 1)
        self.assertEqual(longest_substring_without_repeating("pwwkew"), 3)
        self.assertEqual(longest_substring_without_repeating(""), 0)

    def test_property_against_brute_force(self):
        rng = random.Random(7)
        alphabet = "abcd"
        for _ in range(200):
            text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 14)))
            best = 0
            for i in range(len(text)):
                seen = set()
                for j in range(i, len(text)):
                    if text[j] in seen:
                        break
                    seen.add(text[j])
                    best = max(best, j - i + 1)
            self.assertEqual(longest_substring_without_repeating(text), best)


class TestSlidingWindowMaximum(unittest.TestCase):
    def test_known_case(self):
        self.assertEqual(
            sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3),
            [3, 3, 5, 5, 6, 7],
        )

    def test_k_one_and_k_n(self):
        data = [4, 2, 9, 1]
        self.assertEqual(sliding_window_maximum(data, 1), data)
        self.assertEqual(sliding_window_maximum(data, 4), [9])

    def test_invalid_k(self):
        with self.assertRaises(ValueError):
            sliding_window_maximum([1, 2], 3)
        with self.assertRaises(ValueError):
            sliding_window_maximum([1, 2], 0)

    def test_property_against_naive(self):
        rng = random.Random(11)
        for _ in range(200):
            data = [rng.randint(-50, 50) for _ in range(rng.randint(1, 25))]
            k = rng.randint(1, len(data))
            expected = [max(data[i:i + k]) for i in range(len(data) - k + 1)]
            self.assertEqual(sliding_window_maximum(data, k), expected)


class TestPrefixSums(unittest.TestCase):
    def test_range_sums(self):
        prefix = PrefixSums([3, 1, 4, 1, 5])
        self.assertEqual(prefix.range_sum(0, 4), 14)
        self.assertEqual(prefix.range_sum(1, 3), 6)
        self.assertEqual(prefix.range_sum(2, 2), 4)
        self.assertEqual(prefix.total(), 14)

    def test_out_of_bounds(self):
        prefix = PrefixSums([1, 2])
        with self.assertRaises(IndexError):
            prefix.range_sum(0, 2)
        with self.assertRaises(IndexError):
            prefix.range_sum(1, 0)

    def test_property_against_builtin_sum(self):
        rng = random.Random(3)
        data = [rng.randint(-10, 10) for _ in range(30)]
        prefix = PrefixSums(data)
        for _ in range(100):
            left = rng.randint(0, 29)
            right = rng.randint(left, 29)
            self.assertEqual(prefix.range_sum(left, right), sum(data[left:right + 1]))


if __name__ == "__main__":
    unittest.main()
