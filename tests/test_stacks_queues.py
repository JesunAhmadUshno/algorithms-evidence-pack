import random
import unittest
from collections import deque

from algorithms_evidence_pack.stacks_queues import (
    QueueFromStacks,
    is_valid_parentheses,
    next_greater_elements,
)


class TestValidParentheses(unittest.TestCase):
    def test_valid(self):
        for text in ["", "()", "()[]{}", "{[()]}", "a(b)c[d]"]:
            self.assertTrue(is_valid_parentheses(text), text)

    def test_invalid(self):
        for text in ["(]", "([)]", "(", ")", "(((", "())"]:
            self.assertFalse(is_valid_parentheses(text), text)


class TestQueueFromStacks(unittest.TestCase):
    def test_fifo_order(self):
        queue = QueueFromStacks()
        for value in [1, 2, 3]:
            queue.push(value)
        self.assertEqual(queue.pop(), 1)
        queue.push(4)
        self.assertEqual(queue.peek(), 2)
        self.assertEqual([queue.pop(), queue.pop(), queue.pop()], [2, 3, 4])
        self.assertTrue(queue.empty())

    def test_empty_pop_raises(self):
        queue = QueueFromStacks()
        with self.assertRaises(IndexError):
            queue.pop()
        with self.assertRaises(IndexError):
            queue.peek()

    def test_property_against_deque(self):
        rng = random.Random(13)
        queue = QueueFromStacks()
        reference = deque()
        for _ in range(500):
            if not reference or rng.random() < 0.6:
                value = rng.randint(0, 100)
                queue.push(value)
                reference.append(value)
            else:
                self.assertEqual(queue.pop(), reference.popleft())
            self.assertEqual(len(queue), len(reference))
            self.assertEqual(queue.empty(), len(reference) == 0)


class TestNextGreaterElements(unittest.TestCase):
    def test_known_cases(self):
        self.assertEqual(next_greater_elements([2, 1, 2, 4, 3]), [4, 2, 4, -1, -1])
        self.assertEqual(next_greater_elements([5, 4, 3, 2, 1]), [-1] * 5)
        self.assertEqual(next_greater_elements([]), [])

    def test_property_against_naive(self):
        rng = random.Random(17)
        for _ in range(200):
            data = [rng.randint(0, 30) for _ in range(rng.randint(0, 20))]
            expected = []
            for i, value in enumerate(data):
                greater = -1
                for j in range(i + 1, len(data)):
                    if data[j] > value:
                        greater = data[j]
                        break
                expected.append(greater)
            self.assertEqual(next_greater_elements(data), expected)


if __name__ == "__main__":
    unittest.main()
