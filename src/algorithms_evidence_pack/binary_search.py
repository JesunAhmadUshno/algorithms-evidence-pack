"""Binary search: classic, rotated arrays, and search on the answer."""

import math


def binary_search(numbers, target):
    """Classic binary search on a sorted list.

    Problem: locate ``target`` in a sorted list, or report absence.
    Approach: halve the candidate interval each step by comparing the
    middle element. The loop invariant is that if the target exists,
    it lies inside [lo, hi].
    Complexity: O(log n) time, O(1) space.
    Failure mode: the input must be sorted. On unsorted input the
    function returns -1 or a wrong index with no warning, because no
    local check can detect unsortedness cheaply.
    Returns the index of the target, or -1.
    """
    lo, hi = 0, len(numbers) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if numbers[mid] == target:
            return mid
        if numbers[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def search_rotated(numbers, target):
    """Search in a rotated sorted array.

    Problem: the list was sorted, then rotated at an unknown pivot.
    Find ``target`` without un-rotating the array.
    Approach: at every step, at least one half of [lo, hi] is properly
    sorted. Check whether the target lies inside the sorted half; if
    it does, search there, otherwise search the other half.
    Complexity: O(log n) time for distinct values, O(1) space.
    Failure mode: duplicates break the "one half is sorted" test when
    the endpoints and the middle are all equal, degrading the worst
    case to O(n). This implementation assumes distinct values.
    Returns the index of the target, or -1.
    """
    lo, hi = 0, len(numbers) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if numbers[mid] == target:
            return mid
        if numbers[lo] <= numbers[mid]:
            if numbers[lo] <= target < numbers[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if numbers[mid] < target <= numbers[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def min_eating_speed(piles, hours):
    """Search on the answer: minimum banana-eating speed (Koko).

    Problem: there are piles of bananas. Eating speed k means one pile
    takes ceil(pile / k) hours, one pile per hour at most. Find the
    smallest k that finishes all piles within ``hours`` hours.
    Approach: feasibility is monotone in k (if speed k works, every
    larger speed works), so binary search over k in [1, max(piles)]
    finds the smallest feasible speed without testing each one.
    Complexity: O(n log max(piles)) time, O(1) space.
    Failure mode: the pattern only works when feasibility is monotone.
    If a mid-range answer can fail while a smaller one succeeds, binary
    search on the answer silently returns a wrong "minimum".
    """
    if hours < len(piles):
        raise ValueError("cannot finish: fewer hours than piles")

    def feasible(speed):
        return sum(math.ceil(pile / speed) for pile in piles) <= hours

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
