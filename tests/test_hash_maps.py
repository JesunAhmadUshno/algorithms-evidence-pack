import random
import unittest

from algorithms_evidence_pack.hash_maps import group_anagrams, two_sum


class TestTwoSum(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), (0, 1))

    def test_no_pair(self):
        self.assertIsNone(two_sum([1, 2, 3], 100))

    def test_same_value_twice(self):
        self.assertEqual(two_sum([3, 3], 6), (0, 1))

    def test_property_against_brute_force(self):
        rng = random.Random(5)
        for _ in range(200):
            data = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
            target = rng.randint(-30, 30)
            exists = any(
                data[i] + data[j] == target
                for i in range(len(data))
                for j in range(i + 1, len(data))
            )
            result = two_sum(data, target)
            if not exists:
                self.assertIsNone(result)
            else:
                i, j = result
                self.assertLess(i, j)
                self.assertEqual(data[i] + data[j], target)


class TestGroupAnagrams(unittest.TestCase):
    def test_known_case(self):
        groups = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        as_sets = sorted(tuple(sorted(group)) for group in groups)
        self.assertEqual(
            as_sets,
            [("ate", "eat", "tea"), ("bat",), ("nat", "tan")],
        )

    def test_empty(self):
        self.assertEqual(group_anagrams([]), [])

    def test_property_grouping_is_exact(self):
        rng = random.Random(9)
        words = []
        for _ in range(60):
            letters = [rng.choice("abcde") for _ in range(rng.randint(1, 6))]
            rng.shuffle(letters)
            words.append("".join(letters))
        groups = group_anagrams(words)
        # Every word appears exactly once across all groups.
        flat = sorted(word for group in groups for word in group)
        self.assertEqual(flat, sorted(words))
        # Words inside a group share a sorted form; words in different
        # groups do not.
        keys = []
        for group in groups:
            key = sorted(group[0])
            for word in group:
                self.assertEqual(sorted(word), key)
            keys.append(tuple(key))
        self.assertEqual(len(keys), len(set(keys)))


if __name__ == "__main__":
    unittest.main()
