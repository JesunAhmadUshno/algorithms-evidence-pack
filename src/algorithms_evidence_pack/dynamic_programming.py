"""Dynamic programming: knapsack, LIS, coin change, edit distance."""

import bisect


def knapsack_01(weights, values, capacity):
    """0/1 knapsack: maximum value with each item taken at most once.

    Problem: choose a subset of items whose total weight fits the
    capacity and whose total value is maximal.
    Approach: dp[c] is the best value achievable with capacity c using
    the items considered so far. Capacities are scanned in descending
    order for each item, which guarantees the item is counted at most
    once in its own round.
    Complexity: O(n * capacity) time, O(capacity) space.
    Failure mode: the runtime is pseudo-polynomial. A capacity given
    in grams instead of kilograms multiplies the table size by 1000
    without changing the problem, so huge capacities make this
    approach infeasible even for few items.
    """
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for c in range(capacity, weight - 1, -1):
            candidate = dp[c - weight] + value
            if candidate > dp[c]:
                dp[c] = candidate
    return dp[capacity]


def length_of_lis(numbers):
    """Length of the longest strictly increasing subsequence.

    Problem: length of the longest subsequence that is strictly
    increasing (elements need not be adjacent).
    Approach: tails[i] holds the smallest possible last element of an
    increasing subsequence of length i + 1. Each new value replaces
    the first tail greater than or equal to it (found by binary
    search) or extends the list. The number of tails is the answer.
    Complexity: O(n log n) time, O(n) space.
    Failure mode: the tails array is not itself a subsequence. It
    gives the correct length but cannot be printed as the answer;
    reconstructing an actual subsequence needs parent pointers kept
    during a quadratic pass or a second algorithm.
    """
    tails = []
    for value in numbers:
        position = bisect.bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
        else:
            tails[position] = value
    return len(tails)


def coin_change(coins, amount):
    """Fewest coins to make ``amount``, or -1 if impossible.

    Problem: unlimited coins of given denominations; find the minimum
    number of coins summing exactly to ``amount``.
    Approach: dp[a] is the fewest coins for amount a. Build up from 0,
    relaxing dp[a] over every coin that fits. The sentinel amount + 1
    marks unreachable amounts, since no solution can use more coins
    than the amount itself when the smallest coin is 1, and in
    general any real solution uses at most ``amount`` coins of value
    at least 1.
    Complexity: O(amount * len(coins)) time, O(amount) space.
    Failure mode: greedy does not work here, and this function exists
    partly to make that point. For coin systems like [1, 3, 4] and
    amount 6, greedy takes 4 + 1 + 1 (three coins) while the optimum
    is 3 + 3 (two coins).
    """
    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1
    return dp[amount] if dp[amount] != unreachable else -1


def edit_distance(first, second):
    """Levenshtein edit distance between two strings.

    Problem: minimum insertions, deletions, and substitutions (each
    cost 1) turning ``first`` into ``second``.
    Approach: dp over prefixes. The distance between prefixes depends
    on the distances of the prefixes one character shorter: delete
    from the first, insert into the first, or match/substitute the
    last characters. Only two rows are kept.
    Complexity: O(len(first) * len(second)) time, O(len(second))
    space.
    Failure mode: the score treats every operation and every character
    pair as equal cost. Real applications (spell checking, DNA
    alignment) usually need weighted costs, and equal-cost distance
    can rank an implausible edit as "closest".
    """
    previous = list(range(len(second) + 1))
    for i, char_a in enumerate(first, start=1):
        current = [i]
        for j, char_b in enumerate(second, start=1):
            substitution = previous[j - 1] + (0 if char_a == char_b else 1)
            current.append(min(
                previous[j] + 1,       # delete char_a
                current[j - 1] + 1,    # insert char_b
                substitution,          # match or substitute
            ))
        previous = current
    return previous[len(second)]
