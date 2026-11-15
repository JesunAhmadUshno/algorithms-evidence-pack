"""Sorting implemented by hand: quicksort and mergesort."""


def _median_of_three(values, lo, mid, hi):
    """Return the index of the median of values[lo], values[mid], values[hi]."""
    a, b, c = values[lo], values[mid], values[hi]
    if a < b:
        if b < c:
            return mid
        return hi if a < c else lo
    if a < c:
        return lo
    return hi if b < c else mid


def quicksort_inplace(values):
    """Quicksort, in place, with a median-of-three pivot.

    Problem: sort a list without auxiliary storage proportional to n.
    Approach: partition around a pivot so smaller elements land left
    and larger right, then recurse on each side. The pivot is the
    median of the first, middle, and last elements, which keeps
    already-sorted and reverse-sorted inputs (the classic worst case
    for naive pivoting) on the fast path.
    Complexity: O(n log n) average time, O(n^2) worst case, O(log n)
    average stack space.
    Failure mode: an adversary who knows the pivot rule can still
    craft an input that forces the quadratic case and deep recursion.
    Production libraries defend with introsort (switching to heapsort
    past a depth limit); this teaching version does not.
    """
    def partition(lo, hi):
        pivot_index = _median_of_three(values, lo, (lo + hi) // 2, hi)
        values[pivot_index], values[hi] = values[hi], values[pivot_index]
        pivot = values[hi]
        store = lo
        for i in range(lo, hi):
            if values[i] < pivot:
                values[store], values[i] = values[i], values[store]
                store += 1
        values[store], values[hi] = values[hi], values[store]
        return store

    def sort(lo, hi):
        while lo < hi:
            pivot = partition(lo, hi)
            # Recurse into the smaller side and loop on the larger
            # side, which bounds stack depth at O(log n).
            if pivot - lo < hi - pivot:
                sort(lo, pivot - 1)
                lo = pivot + 1
            else:
                sort(pivot + 1, hi)
                hi = pivot - 1

    sort(0, len(values) - 1)
    return values


def quicksort(values):
    """Return a sorted copy of ``values`` using quicksort."""
    result = list(values)
    quicksort_inplace(result)
    return result


def mergesort(values):
    """Mergesort returning a new list.

    Problem: sort with a guaranteed n log n bound and stability.
    Approach: split the list in half, sort each half recursively, then
    merge the two sorted halves in one linear pass. Equal elements
    keep their original relative order because the merge takes from
    the left half on ties, which is what makes the sort stable.
    Complexity: O(n log n) time in all cases, O(n) extra space.
    Failure mode: the extra space is real. For very large inputs that
    nearly fill memory, the merge buffer can be the difference between
    finishing and being killed, which is why in-place algorithms win
    in memory-tight settings despite weaker guarantees.
    """
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    left = mergesort(values[:mid])
    right = mergesort(values[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
