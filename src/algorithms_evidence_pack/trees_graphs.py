"""Trees and graphs: traversal, shortest paths, ordering, union-find.

Graphs are represented as dicts mapping a node to an iterable of
neighbours (unweighted) or to (neighbour, weight) pairs (weighted).
A tree is a graph with no cycles, so the same traversals apply; the
docstrings note where that matters.
"""

from collections import deque
import heapq


def bfs(graph, start):
    """Breadth-first search.

    Problem: visit every node reachable from ``start``, level by level.
    Approach: a FIFO queue holds the frontier. Nodes are marked visited
    when they are enqueued, not when they are dequeued, which prevents
    the same node entering the queue twice through different parents.
    Complexity: O(V + E) time, O(V) space.
    Failure mode: BFS order is a visit order, not a path. Reconstructing
    the actual shortest path needs a parent map recorded during the
    search, which this version does not keep.
    Returns the visit order as a list.
    """
    visited = {start}
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph.get(node, ()):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return order


def dfs(graph, start):
    """Depth-first search (iterative).

    Problem: visit every node reachable from ``start``, going deep
    before going wide.
    Approach: an explicit stack replaces recursion, so deep graphs
    cannot overflow the call stack. Neighbours are pushed in reverse
    order so the visit order matches the natural left-to-right
    recursive order for ordered adjacency lists.
    Complexity: O(V + E) time, O(V) space.
    Failure mode: iterative DFS visit order can differ from recursive
    DFS in which node is reported first among siblings if adjacency
    order is not controlled; any consumer that depends on an exact
    order must pin the adjacency order down.
    Returns the visit order as a list.
    """
    visited = {start}
    order = []
    stack = [start]
    while stack:
        node = stack.pop()
        order.append(node)
        for neighbour in reversed(list(graph.get(node, ()))):
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(neighbour)
    return order


def dijkstra(graph, start):
    """Dijkstra's shortest paths from one source.

    Problem: shortest distance from ``start`` to every reachable node
    in a weighted graph.
    Approach: a priority queue of (distance, node) candidates. The
    smallest tentative distance popped from the heap is final, because
    every edge weight is non-negative, so no later path can improve
    it. Stale heap entries are skipped by comparing against the best
    known distance.
    Complexity: O((V + E) log V) time, O(V) space.
    Failure mode: negative edge weights break the core assumption and
    the algorithm can return distances that are too large. Graphs with
    negative edges need Bellman-Ford instead.
    Returns a dict mapping node to shortest distance. Unreachable
    nodes are absent from the result.
    """
    distances = {start: 0}
    heap = [(0, start)]
    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distances.get(node, float("inf")):
            continue
        for neighbour, weight in graph.get(node, ()):
            new_dist = dist + weight
            if new_dist < distances.get(neighbour, float("inf")):
                distances[neighbour] = new_dist
                heapq.heappush(heap, (new_dist, neighbour))
    return distances


def topological_sort(graph):
    """Topological ordering of a directed acyclic graph (Kahn).

    Problem: order the nodes so every edge points from earlier to
    later in the order.
    Approach: repeatedly remove nodes with in-degree zero and reduce
    the in-degree of their neighbours. A queue holds the removable
    nodes. If nodes remain when the queue empties, they form a cycle.
    Complexity: O(V + E) time, O(V) space.
    Failure mode: a cyclic graph has no valid ordering. Rather than
    returning a partial order that looks usable, this raises
    ValueError so the caller cannot silently consume a wrong answer.
    """
    in_degree = {node: 0 for node in graph}
    for node, neighbours in graph.items():
        for neighbour in neighbours:
            in_degree.setdefault(neighbour, 0)
            in_degree[neighbour] += 1
    queue = deque(node for node, degree in in_degree.items() if degree == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph.get(node, ()):
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)
    if len(order) != len(in_degree):
        raise ValueError("graph contains a cycle")
    return order


class UnionFind:
    """Disjoint-set union with path compression and union by rank.

    Problem: maintain a partition of elements under merges, and answer
    "are these two in the same set" quickly.
    Approach: each set is a tree whose root is its representative.
    Find follows parent pointers and compresses the path so future
    lookups are nearly constant time. Union attaches the shorter tree
    under the taller one to keep trees shallow.
    Complexity: amortised near O(1) per operation (inverse Ackermann),
    O(n) space.
    Failure mode: there is no delete or split. Once two sets are
    merged they cannot be separated again, so dynamic connectivity
    with edge removals needs a different, heavier structure.
    """

    def __init__(self, elements=()):
        self._parent = {}
        self._rank = {}
        for element in elements:
            self.add(element)

    def add(self, element):
        if element not in self._parent:
            self._parent[element] = element
            self._rank[element] = 0

    def find(self, element):
        self.add(element)
        root = element
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[element] != root:
            self._parent[element], element = root, self._parent[element]
        return root

    def union(self, first, second):
        root_a = self.find(first)
        root_b = self.find(second)
        if root_a == root_b:
            return False
        if self._rank[root_a] < self._rank[root_b]:
            root_a, root_b = root_b, root_a
        self._parent[root_b] = root_a
        if self._rank[root_a] == self._rank[root_b]:
            self._rank[root_a] += 1
        return True

    def connected(self, first, second):
        return self.find(first) == self.find(second)
