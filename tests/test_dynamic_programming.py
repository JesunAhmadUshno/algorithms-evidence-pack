import itertools
import random
import unittest

from algorithms_evidence_pack.dynamic_programming import (
    coin_change,
    edit_distance,
    knapsack_01,
    length_of_lis,
)


def lis_quadratic(numbers):
    if not numbers:
        return 0
    dp = [1] * len(numbers)
    for i in range(len(numbers)):
        for j in range(i):
            if numbers[j] < numbers[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


class TestKnapsack(unittest.TestCase):
    def test_known_case(self):
        self.assertEqual(knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7), 9)

    def test_zero_capacity(self):
        self.assertEqual(knapsack_01([1], [10], 0), 0)

    def test_property_against_brute_force(self):
        rng = random.Random(73)
        for _ in range(100):
            n = rng.randint(0, 10)
            weights = [rng.randint(1, 8) for _ in range(n)]
            values = [rng.randint(1, 15) for _ in range(n)]
            capacity = rng.randint(0, 20)
            best = 0
            for r in range(n + 1):
                for combo in itertools.combinations(range(n), r):
                    if sum(weights[i] for i in combo) <= capacity:
                        best = max(best, sum(values[i] for i in combo))
            self.assertEqual(knapsack_01(weights, values, capacity), best)


class TestLengthOfLis(unittest.TestCase):
    def test_known_cases(self):
        self.assertEqual(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)
        self.assertEqual(length_of_lis([0, 1, 0, 3, 2, 3]), 4)
        self.assertEqual(length_of_lis([7, 7, 7]), 1)
        self.assertEqual(length_of_lis([]), 0)

    def test_property_against_quadratic(self):
        rng = random.Random(79)
        for _ in range(150):
            data = [rng.randint(0, 20) for _ in range(rng.randint(0, 25))]
            self.assertEqual(length_of_lis(data), lis_quadratic(data))


class TestCoinChange(unittest.TestCase):
    def test_known_cases(self):
        self.assertEqual(coin_change([1, 2, 5], 11), 3)
        self.assertEqual(coin_change([2], 3), -1)
        self.assertEqual(coin_change([1], 0), 0)

    def test_greedy_counterexample(self):
        # Greedy would take 4 + 1 + 1; the optimum is 3 + 3.
        self.assertEqual(coin_change([1, 3, 4], 6), 2)

    def test_property_against_bfs(self):
        rng = random.Random(83)

        def bfs_min_coins(coins, amount):
            if amount == 0:
                return 0
            seen = {0}
            frontier = [0]
            steps = 0
            while frontier:
                steps += 1
                next_frontier = []
                for total in frontier:
                    for coin in coins:
                        new_total = total + coin
                        if new_total == amount:
                            return steps
                        if new_total < amount and new_total not in seen:
                            seen.add(new_total)
                            next_frontier.append(new_total)
                frontier = next_frontier
            return -1

        for _ in range(100):
            coins = rng.sample([1, 2, 3, 5, 7, 10], rng.randint(1, 4))
            amount = rng.randint(0, 30)
            self.assertEqual(coin_change(coins, amount), bfs_min_coins(coins, amount))


class TestEditDistance(unittest.TestCase):
    def test_known_cases(self):
        self.assertEqual(edit_distance("horse", "ros"), 3)
        self.assertEqual(edit_distance("intention", "execution"), 5)
        self.assertEqual(edit_distance("kitten", "sitting"), 3)
        self.assertEqual(edit_distance("", ""), 0)
        self.assertEqual(edit_distance("abc", ""), 3)
        self.assertEqual(edit_distance("", "abc"), 3)
        self.assertEqual(edit_distance("same", "same"), 0)

    def test_symmetry_and_identity(self):
        rng = random.Random(89)
        alphabet = "abc"
        for _ in range(100):
            first = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8)))
            second = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8)))
            self.assertEqual(edit_distance(first, second), edit_distance(second, first))
            self.assertEqual(edit_distance(first, first), 0)
            # Distance is at most the longer length (substitute the
            # overlap, insert or delete the rest).
            self.assertLessEqual(
                edit_distance(first, second), max(len(first), len(second))
            )


if __name__ == "__main__":
    unittest.main()
