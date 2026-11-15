import random
import unittest

from algorithms_evidence_pack.linked_lists import (
    build_list,
    has_cycle,
    list_to_pylist,
    merge_two_lists,
    reverse_list,
)


class TestBuildAndConvert(unittest.TestCase):
    def test_round_trip(self):
        self.assertEqual(list_to_pylist(build_list([1, 2, 3])), [1, 2, 3])
        self.assertIsNone(build_list([]))
        self.assertEqual(list_to_pylist(None), [])


class TestReverseList(unittest.TestCase):
    def test_reverse(self):
        head = build_list([1, 2, 3, 4])
        self.assertEqual(list_to_pylist(reverse_list(head)), [4, 3, 2, 1])

    def test_empty_and_single(self):
        self.assertIsNone(reverse_list(None))
        self.assertEqual(list_to_pylist(reverse_list(build_list([7]))), [7])

    def test_property_double_reverse_is_identity(self):
        rng = random.Random(19)
        for _ in range(100):
            data = [rng.randint(0, 50) for _ in range(rng.randint(0, 15))]
            head = reverse_list(reverse_list(build_list(data)))
            self.assertEqual(list_to_pylist(head), data)


class TestHasCycle(unittest.TestCase):
    def test_acyclic(self):
        self.assertFalse(has_cycle(build_list([1, 2, 3])))
        self.assertFalse(has_cycle(None))

    def test_cycle_back_to_head(self):
        head = build_list([1, 2, 3])
        tail = head.next.next
        tail.next = head
        self.assertTrue(has_cycle(head))

    def test_cycle_in_middle(self):
        head = build_list([1, 2, 3, 4])
        head.next.next.next.next = head.next
        self.assertTrue(has_cycle(head))

    def test_self_loop(self):
        head = build_list([1])
        head.next = head
        self.assertTrue(has_cycle(head))


class TestMergeTwoLists(unittest.TestCase):
    def test_merge(self):
        merged = merge_two_lists(build_list([1, 3, 5]), build_list([2, 4, 6]))
        self.assertEqual(list_to_pylist(merged), [1, 2, 3, 4, 5, 6])

    def test_merge_with_empty(self):
        self.assertEqual(list_to_pylist(merge_two_lists(None, build_list([1]))), [1])
        self.assertEqual(list_to_pylist(merge_two_lists(build_list([1]), None)), [1])

    def test_property_against_sorted(self):
        rng = random.Random(23)
        for _ in range(100):
            first = sorted(rng.randint(0, 40) for _ in range(rng.randint(0, 10)))
            second = sorted(rng.randint(0, 40) for _ in range(rng.randint(0, 10)))
            merged = merge_two_lists(build_list(first), build_list(second))
            self.assertEqual(list_to_pylist(merged), sorted(first + second))


if __name__ == "__main__":
    unittest.main()
