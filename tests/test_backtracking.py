import itertools
import unittest

from algorithms_evidence_pack.backtracking import (
    permutations,
    solve_n_queens,
    subsets,
)


class TestPermutations(unittest.TestCase):
    def test_known_case(self):
        result = permutations([1, 2, 3])
        self.assertEqual(len(result), 6)
        self.assertEqual(
            sorted(tuple(p) for p in result),
            sorted(itertools.permutations([1, 2, 3])),
        )

    def test_empty_and_single(self):
        self.assertEqual(permutations([]), [[]])
        self.assertEqual(permutations([5]), [[5]])

    def test_count_is_factorial(self):
        import math

        for n in range(0, 6):
            self.assertEqual(len(permutations(list(range(n)))), math.factorial(n))


class TestSubsets(unittest.TestCase):
    def test_known_case(self):
        result = subsets([1, 2, 3])
        self.assertEqual(len(result), 8)
        self.assertIn([], result)
        self.assertIn([1, 2, 3], result)
        as_sets = sorted(tuple(sorted(s)) for s in result)
        expected = sorted(
            tuple(sorted(combo))
            for r in range(4)
            for combo in itertools.combinations([1, 2, 3], r)
        )
        self.assertEqual(as_sets, expected)

    def test_count_is_power_of_two(self):
        for n in range(0, 7):
            self.assertEqual(len(subsets(list(range(n)))), 2 ** n)


def valid_board(board):
    n = len(board)
    queens = [
        (row, board[row].index("Q")) for row in range(n)
    ]
    for (r1, c1), (r2, c2) in itertools.combinations(queens, 2):
        if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
            return False
    return True


class TestNQueens(unittest.TestCase):
    def test_known_counts(self):
        self.assertEqual(len(solve_n_queens(1)), 1)
        self.assertEqual(len(solve_n_queens(2)), 0)
        self.assertEqual(len(solve_n_queens(3)), 0)
        self.assertEqual(len(solve_n_queens(4)), 2)
        self.assertEqual(len(solve_n_queens(8)), 92)

    def test_all_returned_boards_are_valid(self):
        for n in (4, 5, 6):
            for board in solve_n_queens(n):
                self.assertEqual(len(board), n)
                self.assertTrue(valid_board(board), board)


if __name__ == "__main__":
    unittest.main()
