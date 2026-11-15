"""Backtracking: permutations, subsets, and N-queens with pruning."""


def permutations(numbers):
    """All permutations of a list of distinct values.

    Problem: enumerate every ordering of the input.
    Approach: build the answer one position at a time. At each step,
    try every value not yet used, recurse, then undo the choice
    (backtrack) so the next candidate starts from the same state.
    Complexity: O(n * n!) time, since there are n! permutations and
    copying each costs O(n). O(n) working space beyond the output.
    Failure mode: duplicate values produce duplicate permutations,
    because positions are treated as distinct even when values are
    not. Deduplication needs sorting plus skipping used equal values,
    which this version deliberately leaves out and documents instead.
    """
    result = []
    current = []
    used = [False] * len(numbers)

    def backtrack():
        if len(current) == len(numbers):
            result.append(list(current))
            return
        for index, value in enumerate(numbers):
            if used[index]:
                continue
            used[index] = True
            current.append(value)
            backtrack()
            current.pop()
            used[index] = False

    backtrack()
    return result


def subsets(numbers):
    """All subsets (the power set) of a list.

    Problem: enumerate every subset, including the empty set.
    Approach: at each index, branch twice: take the element or skip
    it. The recursion depth is the list length and each leaf is one
    subset.
    Complexity: O(n * 2^n) time, O(n) working space beyond the output.
    Failure mode: the output itself is exponentially large, so beyond
    roughly 25 elements the enumeration cannot finish in reasonable
    time or memory no matter how efficient the code is. The limit is
    the problem, not the implementation.
    """
    result = []
    current = []

    def backtrack(index):
        if index == len(numbers):
            result.append(list(current))
            return
        backtrack(index + 1)          # skip numbers[index]
        current.append(numbers[index])
        backtrack(index + 1)          # take numbers[index]
        current.pop()

    backtrack(0)
    return result


def solve_n_queens(n):
    """All ways to place n non-attacking queens on an n by n board.

    Problem: place n queens so no two share a row, column, or
    diagonal, and enumerate every solution.
    Approach: place one queen per row, top to bottom. Three sets
    track attacked columns and both diagonal families (row - col and
    row + col are constant along each diagonal). A candidate square
    is pruned immediately if any set contains its key, which is what
    keeps the search far smaller than n! raw placements.
    Complexity: exponential worst case but heavily pruned; the number
    of solutions peaks at 724 for n = 10 and 92 for n = 8. O(n)
    working space beyond the output.
    Failure mode: beyond about n = 12 the enumeration becomes a
    serious computation (14 million solutions at n = 14). Counting
    solutions without storing them, or symmetry reduction, is needed
    at that scale.
    Returns each solution as a list of strings, one per row, with
    "Q" for a queen and "." for an empty square.
    """
    solutions = []
    columns = set()
    diag_down = set()   # constant row - col
    diag_up = set()     # constant row + col
    board = []

    def backtrack(row):
        if row == n:
            solutions.append(list(board))
            return
        for col in range(n):
            if col in columns or (row - col) in diag_down or (row + col) in diag_up:
                continue
            columns.add(col)
            diag_down.add(row - col)
            diag_up.add(row + col)
            board.append("." * col + "Q" + "." * (n - col - 1))
            backtrack(row + 1)
            board.pop()
            columns.remove(col)
            diag_down.remove(row - col)
            diag_up.remove(row + col)

    backtrack(0)
    return solutions
