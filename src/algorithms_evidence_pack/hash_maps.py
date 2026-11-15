"""Hash maps: constant-time lookup problems and frequency grouping."""


def two_sum(numbers, target):
    """Two-sum with a hash map.

    Problem: find indices of two elements that add to ``target`` in an
    unsorted list.
    Approach: one pass. For each value, check whether its complement
    ``target - value`` was already seen; if so, the pair is complete.
    The map stores value to index, so the check is O(1) on average.
    Complexity: O(n) average time, O(n) extra space.
    Failure mode: hash collisions degrade the average case toward
    O(n^2) in adversarial inputs crafted against the hash function.
    Python's dict is robust in practice, but the guarantee is average
    case, not worst case.
    Returns a tuple ``(i, j)`` with ``i < j``, or None.
    """
    seen = {}
    for index, value in enumerate(numbers):
        complement = target - value
        if complement in seen:
            return (seen[complement], index)
        seen[value] = index
    return None


def group_anagrams(words):
    """Group anagrams by character frequency.

    Problem: group words that are anagrams of each other.
    Approach: two words are anagrams exactly when their character
    frequency vectors match. Count the 26 lowercase letters of each
    word into a tuple and use that tuple as a dict key.
    Complexity: O(n * m) time for n words of length m, O(n * m) space
    for the groups.
    Failure mode: the frequency vector assumes lowercase ASCII letters
    a to z. Mixed case, accents, or other alphabets need normalisation
    first (for example casefolding), or words that a human would group
    together land in different buckets.
    Returns a list of groups; group order follows first appearance.
    """
    groups = {}
    for word in words:
        counts = [0] * 26
        for char in word:
            counts[ord(char) - ord("a")] += 1
        key = tuple(counts)
        groups.setdefault(key, []).append(word)
    return list(groups.values())
