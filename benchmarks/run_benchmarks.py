"""Benchmarks: implementations vs naive baselines or the stdlib.

Run from the repository root:

    PYTHONPATH=src python3 benchmarks/run_benchmarks.py

Each benchmark reports the median wall-clock time over several
repetitions, measured with time.perf_counter. Inputs are generated
once per benchmark with a fixed seed, so every repetition times the
same data. Correctness of the timed functions is covered by the unit
tests; the benchmark also asserts that the implementation and the
baseline agree on the timed input before timing starts.
"""

import random
import statistics
import sys
import time

sys.path.insert(0, "src")

from algorithms_evidence_pack.arrays_strings import sliding_window_maximum
from algorithms_evidence_pack.dynamic_programming import length_of_lis
from algorithms_evidence_pack.hash_maps import two_sum
from algorithms_evidence_pack.heaps import k_largest
from algorithms_evidence_pack.sorting import mergesort, quicksort
from algorithms_evidence_pack.stacks_queues import next_greater_elements
from algorithms_evidence_pack.trees_graphs import dijkstra


# ---------- naive baselines ----------

def sliding_window_maximum_naive(numbers, k):
    return [max(numbers[i:i + k]) for i in range(len(numbers) - k + 1)]


def two_sum_brute(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return (i, j)
    return None


def next_greater_naive(numbers):
    result = []
    for i, value in enumerate(numbers):
        greater = -1
        for j in range(i + 1, len(numbers)):
            if numbers[j] > value:
                greater = numbers[j]
                break
        result.append(greater)
    return result


def bellman_ford(graph, start):
    nodes = {start} | set(graph)
    for neighbours in graph.values():
        for neighbour, _ in neighbours:
            nodes.add(neighbour)
    dist = {node: float("inf") for node in nodes}
    dist[start] = 0
    edges = [(u, v, w) for u, ns in graph.items() for v, w in ns]
    for _ in range(len(nodes) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return {node: d for node, d in dist.items() if d < float("inf")}


def lis_quadratic(numbers):
    if not numbers:
        return 0
    dp = [1] * len(numbers)
    for i in range(len(numbers)):
        for j in range(i):
            if numbers[j] < numbers[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


# ---------- timing helper ----------

def median_ms(func, reps):
    times = []
    for _ in range(reps):
        start = time.perf_counter()
        func()
        times.append((time.perf_counter() - start) * 1000.0)
    return statistics.median(times)


def run_benchmark(name, size_label, impl, baseline, check, reps=5):
    assert check(), f"implementation and baseline disagree: {name}"
    impl_ms = median_ms(impl, reps)
    base_ms = median_ms(baseline, reps)
    speedup = base_ms / impl_ms if impl_ms > 0 else float("inf")
    print(
        f"| {name} | {size_label} | {impl_ms:.2f} | {base_ms:.2f} | {speedup:.1f}x |"
    )
    return impl_ms, base_ms


def main():
    rng = random.Random(20261115)
    print("| Benchmark | Input size | This pack (ms) | Baseline (ms) | Speedup |")
    print("| --- | --- | --- | --- | --- |")

    data = [rng.randint(0, 10 ** 6) for _ in range(20000)]
    run_benchmark(
        "quicksort vs sorted()",
        "n = 20,000 random ints",
        lambda: quicksort(data),
        lambda: sorted(data),
        lambda: quicksort(data) == sorted(data),
    )
    run_benchmark(
        "mergesort vs sorted()",
        "n = 20,000 random ints",
        lambda: mergesort(data),
        lambda: sorted(data),
        lambda: mergesort(data) == sorted(data),
    )

    window_data = [rng.randint(0, 1000) for _ in range(20000)]
    run_benchmark(
        "sliding window maximum (deque) vs naive max per window",
        "n = 20,000, k = 100",
        lambda: sliding_window_maximum(window_data, 100),
        lambda: sliding_window_maximum_naive(window_data, 100),
        lambda: sliding_window_maximum(window_data, 100)
        == sliding_window_maximum_naive(window_data, 100),
    )

    pair_data = [rng.randint(0, 5000) for _ in range(2000)]
    absent_target = 10 ** 9  # forces both to scan everything
    run_benchmark(
        "two-sum (hash map) vs brute force, no-pair worst case",
        "n = 2,000",
        lambda: two_sum(pair_data, absent_target),
        lambda: two_sum_brute(pair_data, absent_target),
        lambda: two_sum(pair_data, absent_target)
        == two_sum_brute(pair_data, absent_target),
    )

    greater_data = [rng.randint(0, 10000) for _ in range(4000)]
    run_benchmark(
        "next greater element (monotonic stack) vs naive scan",
        "n = 4,000",
        lambda: next_greater_elements(greater_data),
        lambda: next_greater_naive(greater_data),
        lambda: next_greater_elements(greater_data)
        == next_greater_naive(greater_data),
    )

    node_count = 300
    graph = {node: [] for node in range(node_count)}
    for u in range(node_count):
        for v in range(node_count):
            if u != v and rng.random() < 0.02:
                graph[u].append((v, rng.randint(1, 20)))
    run_benchmark(
        "Dijkstra (heap) vs Bellman-Ford",
        "300 nodes, about 1,800 edges",
        lambda: dijkstra(graph, 0),
        lambda: bellman_ford(graph, 0),
        lambda: dijkstra(graph, 0) == bellman_ford(graph, 0),
    )

    lis_data = [rng.randint(0, 5000) for _ in range(2000)]
    run_benchmark(
        "longest increasing subsequence (binary search) vs quadratic DP",
        "n = 2,000",
        lambda: length_of_lis(lis_data),
        lambda: lis_quadratic(lis_data),
        lambda: length_of_lis(lis_data) == lis_quadratic(lis_data),
        reps=3,
    )

    big = [rng.randint(0, 10 ** 7) for _ in range(50000)]
    run_benchmark(
        "k largest (bounded heap) vs full sort",
        "n = 50,000, k = 10",
        lambda: k_largest(big, 10),
        lambda: sorted(big, reverse=True)[:10],
        lambda: k_largest(big, 10) == sorted(big, reverse=True)[:10],
    )


if __name__ == "__main__":
    main()
