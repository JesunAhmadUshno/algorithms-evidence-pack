import random
import statistics
import unittest

from algorithms_evidence_pack.heaps import (
    MedianFinder,
    k_largest,
    merge_k_sorted_lists,
)


class TestKLargest(unittest.TestCase):
    def test_known_cases(self):
        self.assertEqual(k_largest([3, 2, 1, 5, 6, 4], 2), [6, 5])
        self.assertEqual(k_largest([1], 1), [1])
        self.assertEqual(k_largest([1, 2], 0), [])

    def test_property_against_sorted(self):
        rng = random.Random(41)
        for _ in range(100):
            data = [rng.randint(-30, 30) for _ in range(rng.randint(0, 30))]
            k = rng.randint(0, len(data) + 2)
            expected = sorted(data, reverse=True)[:k]
            self.assertEqual(k_largest(data, k), expected)


class TestMergeKSortedLists(unittest.TestCase):
    def test_known_case(self):
        self.assertEqual(
            merge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]]),
            [1, 1, 2, 3, 4, 4, 5, 6],
        )

    def test_empty_inputs(self):
        self.assertEqual(merge_k_sorted_lists([]), [])
        self.assertEqual(merge_k_sorted_lists([[], []]), [])
        self.assertEqual(merge_k_sorted_lists([[], [1], []]), [1])

    def test_property_against_sorted_flatten(self):
        rng = random.Random(43)
        for _ in range(100):
            lists = [
                sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 10)))
                for _ in range(rng.randint(0, 6))
            ]
            flat = [value for values in lists for value in values]
            self.assertEqual(merge_k_sorted_lists(lists), sorted(flat))


class TestMedianFinder(unittest.TestCase):
    def test_known_sequence(self):
        finder = MedianFinder()
        finder.add_num(5)
        self.assertEqual(finder.find_median(), 5.0)
        finder.add_num(15)
        self.assertEqual(finder.find_median(), 10.0)
        finder.add_num(1)
        self.assertEqual(finder.find_median(), 5.0)
        finder.add_num(3)
        self.assertEqual(finder.find_median(), 4.0)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            MedianFinder().find_median()

    def test_property_against_statistics_median(self):
        rng = random.Random(47)
        finder = MedianFinder()
        seen = []
        for _ in range(200):
            value = rng.randint(-100, 100)
            finder.add_num(value)
            seen.append(value)
            self.assertEqual(finder.find_median(), float(statistics.median(seen)))


if __name__ == "__main__":
    unittest.main()
