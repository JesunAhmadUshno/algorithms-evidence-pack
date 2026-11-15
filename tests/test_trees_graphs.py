import itertools
import random
import unittest

from algorithms_evidence_pack.trees_graphs import (
    UnionFind,
    bfs,
    dfs,
    dijkstra,
    topological_sort,
)


def brute_force_distances(graph, start):
    """Bellman-Ford style reference: relax every edge V times."""
    nodes = {start} | set(graph)
    for neighbours in graph.values():
        for neighbour, _ in neighbours:
            nodes.add(neighbour)
    dist = {node: float("inf") for node in nodes}
    dist[start] = 0
    edges = [
        (u, v, w) for u, neighbours in graph.items() for v, w in neighbours
    ]
    for _ in range(len(nodes)):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return {node: d for node, d in dist.items() if d < float("inf")}


class TestTraversals(unittest.TestCase):
    def setUp(self):
        self.graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D", "E"],
            "D": [],
            "E": [],
        }

    def test_bfs_visits_level_by_level(self):
        order = bfs(self.graph, "A")
        self.assertEqual(order[0], "A")
        self.assertEqual(set(order), {"A", "B", "C", "D", "E"})
        self.assertLess(order.index("B"), order.index("D"))
        self.assertLess(order.index("C"), order.index("E"))

    def test_dfs_visits_all_reachable(self):
        order = dfs(self.graph, "A")
        self.assertEqual(order[0], "A")
        self.assertEqual(set(order), {"A", "B", "C", "D", "E"})

    def test_unreachable_nodes_not_visited(self):
        graph = {"A": ["B"], "B": [], "Z": []}
        self.assertEqual(set(bfs(graph, "A")), {"A", "B"})
        self.assertEqual(set(dfs(graph, "A")), {"A", "B"})

    def test_tree_traversal(self):
        tree = {1: [2, 3], 2: [4, 5], 3: [], 4: [], 5: []}
        self.assertEqual(bfs(tree, 1), [1, 2, 3, 4, 5])
        self.assertEqual(dfs(tree, 1), [1, 2, 4, 5, 3])


class TestDijkstra(unittest.TestCase):
    def test_known_graph(self):
        graph = {
            "A": [("B", 1), ("C", 4)],
            "B": [("C", 2), ("D", 5)],
            "C": [("D", 1)],
            "D": [],
        }
        self.assertEqual(
            dijkstra(graph, "A"),
            {"A": 0, "B": 1, "C": 3, "D": 4},
        )

    def test_property_against_brute_force(self):
        rng = random.Random(29)
        for _ in range(100):
            n = rng.randint(2, 9)
            nodes = list(range(n))
            graph = {node: [] for node in nodes}
            for u, v in itertools.permutations(nodes, 2):
                if rng.random() < 0.3:
                    graph[u].append((v, rng.randint(1, 9)))
            start = rng.choice(nodes)
            self.assertEqual(
                dijkstra(graph, start),
                brute_force_distances(graph, start),
            )


class TestTopologicalSort(unittest.TestCase):
    def test_known_dag(self):
        graph = {"cook": ["eat"], "shop": ["cook"], "eat": []}
        order = topological_sort(graph)
        self.assertLess(order.index("shop"), order.index("cook"))
        self.assertLess(order.index("cook"), order.index("eat"))

    def test_cycle_raises(self):
        graph = {"A": ["B"], "B": ["A"]}
        with self.assertRaises(ValueError):
            topological_sort(graph)

    def test_property_order_respects_every_edge(self):
        rng = random.Random(31)
        for _ in range(100):
            n = rng.randint(1, 12)
            nodes = list(range(n))
            rng.shuffle(nodes)
            graph = {node: [] for node in nodes}
            # Edges only from earlier to later in a hidden order: a DAG.
            position = {node: i for i, node in enumerate(nodes)}
            for u in nodes:
                for v in nodes:
                    if position[u] < position[v] and rng.random() < 0.25:
                        graph[u].append(v)
            order = topological_sort(graph)
            self.assertEqual(set(order), set(nodes))
            rank = {node: i for i, node in enumerate(order)}
            for u, neighbours in graph.items():
                for v in neighbours:
                    self.assertLess(rank[u], rank[v])


class TestUnionFind(unittest.TestCase):
    def test_union_and_connected(self):
        uf = UnionFind([1, 2, 3, 4])
        self.assertFalse(uf.connected(1, 2))
        self.assertTrue(uf.union(1, 2))
        self.assertTrue(uf.connected(1, 2))
        self.assertFalse(uf.union(1, 2))
        uf.union(2, 3)
        self.assertTrue(uf.connected(1, 3))
        self.assertFalse(uf.connected(1, 4))

    def test_property_against_reference_sets(self):
        rng = random.Random(37)
        elements = list(range(15))
        uf = UnionFind(elements)
        groups = [{element} for element in elements]

        def reference_connected(a, b):
            return any(a in group and b in group for group in groups)

        for _ in range(200):
            a, b = rng.choice(elements), rng.choice(elements)
            if rng.random() < 0.5:
                uf.union(a, b)
                merged = [g for g in groups if a in g or b in g]
                groups = [g for g in groups if a not in g and b not in g]
                groups.append(set().union(*merged))
            else:
                self.assertEqual(uf.connected(a, b), reference_connected(a, b))


if __name__ == "__main__":
    unittest.main()
