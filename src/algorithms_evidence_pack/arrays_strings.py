"""Arrays and strings: two pointers, sliding window, prefix sums."""

from collections import deque


def two_sum_sorted(numbers, target):
    """Two pointers on a sorted array.

    Problem: given a list sorted in non-decreasing order, find the
    indices of the two elements that add up to ``target``.
    Approach: one pointer at each end. If the current sum is too small,
    move the left pointer right; if too large, move the right pointer
    left. Each element is visited at most once.
    Complexity: O(n) time, O(1) extra space.
    Failure mode: the input must actually be sorted. On unsorted input
    the pointers can step past the only valid pair and the function
    returns None for a target that is reachable.
    Returns a tuple ``(i, j)`` of indices with ``i < j``, or None.
    """
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return (left, right)
        if total < target:
            left += 1
        else:
            right -= 1
    return None


def longest_substring_without_repeating(text):
    """Sliding window over a string.

    Problem: length of the longest substring with no repeated character.
    Approach: keep a window [left, right] and a map from character to
    its most recent index. When a character repeats inside the window,
    jump ``left`` to just after its previous occurrence. The window
    never shrinks from the right, so each character is processed once.
    Complexity: O(n) time, O(min(n, alphabet)) extra space.
    Failure mode: none structural, but the answer is a length only;
    recovering the substring itself needs the best window bounds to be
    tracked alongside, which this version deliberately does not do.
    """
    last_seen = {}
    left = 0
    best = 0
    for right, char in enumerate(text):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        best = max(best, right - left + 1)
    return best


def sliding_window_maximum(numbers, k):
    """Sliding window maximum with a monotonic deque.

    Problem: the maximum of every contiguous window of size ``k``.
    Approach: a deque of indices whose values are in decreasing order.
    The front of the deque is always the current window maximum.
    Indices that fall out of the window are dropped from the front;
    values smaller than the incoming value are dropped from the back
    because they can never be a future maximum.
    Complexity: O(n) time, O(k) extra space.
    Failure mode: ``k`` larger than the list or smaller than 1 has no
    meaningful answer, so it raises ValueError instead of guessing.
    """
    if k < 1 or k > len(numbers):
        raise ValueError("k must be between 1 and len(numbers)")
    window = deque()
    result = []
    for i, value in enumerate(numbers):
        while window and window[0] <= i - k:
            window.popleft()
        while window and numbers[window[-1]] <= value:
            window.pop()
        window.append(i)
        if i >= k - 1:
            result.append(numbers[window[0]])
    return result


class PrefixSums:
    """Prefix sums for static range-sum queries.

    Problem: answer many sum queries over ranges of a fixed list.
    Approach: precompute ``prefix[i]`` as the sum of the first ``i``
    elements. The sum over [left, right] inclusive is then
    ``prefix[right + 1] - prefix[left]`` in constant time.
    Complexity: O(n) build time and space, O(1) per query.
    Failure mode: the list is treated as immutable. Changing an element
    after construction invalidates every prefix from that point on; a
    Fenwick tree is the right structure when updates are needed.
    """

    def __init__(self, numbers):
        self._prefix = [0]
        for value in numbers:
            self._prefix.append(self._prefix[-1] + value)

    def range_sum(self, left, right):
        """Sum of elements from index ``left`` to ``right`` inclusive."""
        if left < 0 or right >= len(self._prefix) - 1 or left > right:
            raise IndexError("range out of bounds")
        return self._prefix[right + 1] - self._prefix[left]

    def total(self):
        return self._prefix[-1]
