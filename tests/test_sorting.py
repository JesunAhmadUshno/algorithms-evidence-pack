import random
import unittest

from algorithms_evidence_pack.sorting import mergesort, quicksort, quicksort_inplace


class TestSorting(unittest.TestCase):
    def check_all(self, data):
        original = list(data)
        expected = sorted(data)
        self.assertEqual(quicksort(data), expected)
        self.assertEqual(mergesort(data), expected)
        copy = list(data)
        quicksort_inplace(copy)
        self.assertEqual(copy, expected)
        # quicksort and mergesort must not mutate their input.
        self.assertEqual(data, original)

    def test_known_cases(self):
        for data in [
            [],
            [1],
            [2, 1],
            [5, 2, 9, 1, 7],
            [3, 3, 3],
            [-1, -5, 0, 4],
        ]:
            self.check_all(data)

    def test_sorted_and_reversed_inputs(self):
        self.check_all(list(range(200)))
        self.check_all(list(range(200, 0, -1)))

    def test_property_against_builtin_sorted(self):
        rng = random.Random(67)
        for _ in range(150):
            data = [rng.randint(-100, 100) for _ in range(rng.randint(0, 60))]
            self.check_all(data)

    def test_large_random(self):
        rng = random.Random(71)
        data = [rng.randint(0, 10 ** 6) for _ in range(5000)]
        self.assertEqual(quicksort(data), sorted(data))
        self.assertEqual(mergesort(data), sorted(data))

    def test_mergesort_is_stable(self):
        pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
        by_key = mergesort(pairs)
        self.assertEqual(
            by_key,
            [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")],
        )


if __name__ == "__main__":
    unittest.main()
