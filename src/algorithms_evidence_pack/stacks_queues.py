"""Stacks and queues: matching, amortised transfer, monotonic stack."""


def is_valid_parentheses(text):
    """Valid parentheses with a stack.

    Problem: decide whether every bracket in ``text`` is closed by the
    matching type in the correct order. Brackets are (), [], {}.
    Approach: push opening brackets; on a closing bracket, the top of
    the stack must be its partner. Non-bracket characters are ignored.
    Complexity: O(n) time, O(n) worst-case space.
    Failure mode: only bracket balance is checked. The function says
    nothing about whether the text is a valid expression in any other
    sense, so "a + )" with balanced counts in the wrong shape is still
    caught, but semantic errors are out of scope by design.
    """
    partners = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in partners:
            if not stack or stack[-1] != partners[char]:
                return False
            stack.pop()
    return not stack


class QueueFromStacks:
    """A FIFO queue built from two LIFO stacks.

    Problem: implement queue operations using only stacks.
    Approach: pushes go onto the in-stack. Pops and peeks read from the
    out-stack; when the out-stack is empty, the whole in-stack is
    poured into it, which reverses the order so the oldest element
    lands on top. Each element moves stacks at most once.
    Complexity: amortised O(1) per operation, O(n) space.
    Failure mode: the amortised bound hides a worst case: the single
    pop that triggers a pour costs O(n). Latency-sensitive systems that
    need a hard per-operation bound should use a linked list or a ring
    buffer instead.
    """

    def __init__(self):
        self._in = []
        self._out = []

    def push(self, value):
        self._in.append(value)

    def _pour(self):
        while self._in:
            self._out.append(self._in.pop())

    def pop(self):
        if not self._out:
            self._pour()
        if not self._out:
            raise IndexError("pop from empty queue")
        return self._out.pop()

    def peek(self):
        if not self._out:
            self._pour()
        if not self._out:
            raise IndexError("peek from empty queue")
        return self._out[-1]

    def empty(self):
        return not self._in and not self._out

    def __len__(self):
        return len(self._in) + len(self._out)


def next_greater_elements(numbers):
    """Next greater element with a monotonic stack.

    Problem: for each element, find the first element to its right that
    is strictly greater, or -1 when there is none.
    Approach: scan left to right holding a stack of indices whose
    answers are not yet known, with values in decreasing order. When a
    new value arrives, it is the answer for every smaller value still
    waiting on the stack.
    Complexity: O(n) time, O(n) space.
    Failure mode: equal values are not "greater", so duplicates resolve
    to the next strictly larger element or -1. Callers who need
    greater-or-equal semantics must change the comparison, and the
    stack invariant changes with it.
    """
    result = [-1] * len(numbers)
    waiting = []
    for index, value in enumerate(numbers):
        while waiting and numbers[waiting[-1]] < value:
            result[waiting.pop()] = value
        waiting.append(index)
    return result
