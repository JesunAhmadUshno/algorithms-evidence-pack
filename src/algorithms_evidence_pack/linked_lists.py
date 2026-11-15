"""Singly linked lists with hand-written node classes."""


class ListNode:
    """One node of a singly linked list."""

    __slots__ = ("value", "next")

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

    def __repr__(self):
        return f"ListNode({self.value!r})"


def build_list(values):
    """Build a linked list from an iterable, preserving order."""
    head = None
    tail = None
    for value in values:
        node = ListNode(value)
        if head is None:
            head = node
        else:
            tail.next = node
        tail = node
    return head


def list_to_pylist(head, limit=100000):
    """Convert a linked list back to a Python list.

    The ``limit`` guards the conversion: a cyclic list would otherwise
    loop forever here. Exceeding the limit raises ValueError.
    """
    values = []
    node = head
    while node is not None:
        if len(values) >= limit:
            raise ValueError("list exceeds limit (possible cycle)")
        values.append(node.value)
        node = node.next
    return values


def reverse_list(head):
    """Reverse a linked list in place.

    Problem: reverse the direction of every link.
    Approach: walk once with three pointers (previous, current, next).
    Each link is flipped to point backwards; the old tail becomes the
    new head. No new nodes are allocated.
    Complexity: O(n) time, O(1) extra space.
    Failure mode: on a cyclic list the walk never terminates. Cycle
    detection (below) is the check to run first when the input's shape
    is not trusted.
    """
    previous = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous = current
        current = following
    return previous


def has_cycle(head):
    """Detect a cycle with Floyd's tortoise and hare.

    Problem: decide whether following ``next`` pointers ever loops.
    Approach: two pointers advance at speeds 1 and 2. On a finite list
    the fast pointer reaches the end. On a cyclic list it laps the
    slow pointer inside the loop and they meet.
    Complexity: O(n) time, O(1) extra space.
    Failure mode: it answers only yes or no. It does not report where
    the cycle starts; finding the entry point needs a second phase
    (reset one pointer to the head and advance both at speed 1).
    """
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def merge_two_lists(first, second):
    """Merge two sorted linked lists into one sorted list.

    Problem: splice two ascending lists into a single ascending list.
    Approach: a dummy head removes the special case for the first
    node. Repeatedly attach the smaller of the two current heads and
    advance that list. Existing nodes are reused, not copied.
    Complexity: O(n + m) time, O(1) extra space.
    Failure mode: both inputs must already be sorted. Merging unsorted
    lists produces a list that interleaves the two orders, which looks
    plausible and is wrong; the function does not check sortedness.
    """
    dummy = ListNode(0)
    tail = dummy
    while first is not None and second is not None:
        if first.value <= second.value:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next
        tail = tail.next
    tail.next = first if first is not None else second
    return dummy.next
