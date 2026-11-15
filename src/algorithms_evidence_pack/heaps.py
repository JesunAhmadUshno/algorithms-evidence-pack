"""Heaps: selection, k-way merge, and streaming median."""

import heapq


def k_largest(numbers, k):
    """The k largest elements with a bounded min-heap.

    Problem: find the k largest values without sorting everything.
    Approach: keep a min-heap of the best k values seen so far. The
    heap root is the smallest of the current winners, so a new value
    only enters when it beats that root. The heap never exceeds k.
    Complexity: O(n log k) time, O(k) space.
    Failure mode: when k is close to n this degenerates to a full
    sort's cost with worse constants. The technique pays off only
    when k is much smaller than n.
    Returns the winners sorted in descending order.
    """
    if k <= 0:
        return []
    heap = []
    for value in numbers:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)
    return sorted(heap, reverse=True)


def merge_k_sorted_lists(lists):
    """Merge k sorted lists with a heap.

    Problem: merge several sorted lists into one sorted list.
    Approach: the heap holds one frontier element per list as
    (value, list index, position). Repeatedly pop the smallest
    frontier element, emit it, and advance that list's frontier.
    Complexity: O(N log k) time for N total elements, O(k) extra
    space beyond the output.
    Failure mode: every input list must be sorted. One unsorted input
    silently produces an output that is almost sorted, which is the
    worst kind of wrong because casual checks can miss it.
    """
    heap = []
    for list_index, values in enumerate(lists):
        if values:
            heap.append((values[0], list_index, 0))
    heapq.heapify(heap)
    merged = []
    while heap:
        value, list_index, position = heapq.heappop(heap)
        merged.append(value)
        next_position = position + 1
        if next_position < len(lists[list_index]):
            heapq.heappush(
                heap,
                (lists[list_index][next_position], list_index, next_position),
            )
    return merged


class MedianFinder:
    """Median of a stream with two heaps.

    Problem: maintain the median of values that arrive one at a time.
    Approach: a max-heap (values negated, since heapq is a min-heap)
    holds the lower half and a min-heap holds the upper half. The
    heaps are kept balanced so their sizes differ by at most one, with
    the lower half holding the extra element. The median is then at
    the heap tops.
    Complexity: O(log n) per insertion, O(1) per median query, O(n)
    space.
    Failure mode: removals are not supported. Deleting an arbitrary
    value from a heap is O(n), so sliding-window medians need lazy
    deletion bookkeeping or a balanced tree instead.
    """

    def __init__(self):
        self._low = []   # max-heap via negated values
        self._high = []  # min-heap

    def add_num(self, value):
        heapq.heappush(self._low, -value)
        heapq.heappush(self._high, -heapq.heappop(self._low))
        if len(self._high) > len(self._low):
            heapq.heappush(self._low, -heapq.heappop(self._high))

    def find_median(self):
        if not self._low:
            raise ValueError("median of an empty stream")
        if len(self._low) > len(self._high):
            return float(-self._low[0])
        return (-self._low[0] + self._high[0]) / 2.0
