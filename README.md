# Algorithms Evidence Pack

Classic data structures and algorithms, implemented from scratch in
Python, each with unit tests, a short note (problem, approach,
complexity, one failure mode, written in the module docstrings), and,
for the core set, a measured benchmark against a naive baseline or the
standard library.

This repository exists to be checked. Every claim in it can be
verified by running the tests and the benchmark script.

## Dashboard

A live dashboard is published from the `site/` folder in this
repository: [jesunahmadushno.github.io/algorithms-evidence-pack](https://jesunahmadushno.github.io/algorithms-evidence-pack/).
It carries the coverage map, the benchmark chart and table with the
losing rows kept in, a searchable implementation index, and a diagram
of the package structure. Every number on the page is generated at
build time from `RESULTS.md` and this README, and the build fails if
the page and the record drift.

## What is covered

| Area | Implementations | File |
| --- | --- | --- |
| Arrays and strings | two pointers (two-sum on sorted input), sliding window maximum, longest substring without repeats, prefix sums | `src/algorithms_evidence_pack/arrays_strings.py` |
| Hash maps | two-sum, anagram grouping by character frequency | `src/algorithms_evidence_pack/hash_maps.py` |
| Stacks and queues | valid parentheses, queue built from two stacks, monotonic stack next-greater | `src/algorithms_evidence_pack/stacks_queues.py` |
| Linked lists | reversal, cycle detection (Floyd), merge of two sorted lists, hand-written node class | `src/algorithms_evidence_pack/linked_lists.py` |
| Trees and graphs | BFS, DFS, Dijkstra shortest path, topological sort (Kahn), union-find with path compression | `src/algorithms_evidence_pack/trees_graphs.py` |
| Heaps | k largest, merge k sorted lists, median from a stream (two heaps) | `src/algorithms_evidence_pack/heaps.py` |
| Binary search | classic search, search in a rotated sorted array, search on the answer (minimum eating speed) | `src/algorithms_evidence_pack/binary_search.py` |
| Sorting | quicksort (median-of-three pivot) and mergesort, both written by hand | `src/algorithms_evidence_pack/sorting.py` |
| Dynamic programming | 0/1 knapsack, longest increasing subsequence, coin change, edit distance | `src/algorithms_evidence_pack/dynamic_programming.py` |
| Backtracking | permutations, subsets, N-queens with diagonal pruning | `src/algorithms_evidence_pack/backtracking.py` |

## Running the tests

The test suite uses only the Python standard library
(`unittest`), so there is nothing to install beyond the package
itself:

```bash
pip install -e .
python -m unittest discover -s tests
```

85 tests. Many are property-style: an implementation is compared
against an independent reference (the standard library, a brute-force
version, or a second algorithm) across hundreds of seeded random
inputs. Sorting is checked against `sorted()`, Dijkstra against a
Bellman-Ford reference, knapsack against exhaustive search, and so on.

## Running the benchmarks

```bash
PYTHONPATH=src python3 benchmarks/run_benchmarks.py
```

Eight benchmarks time implementations against naive baselines or the
standard library, taking the median of repeated runs. The script
asserts that the implementation and the baseline agree on the timed
input before timing anything. Measured results, method, machine, and
an honest reading of the numbers (including where the hand-written
sorts lose to the C implementation of `sorted()`) are in
[RESULTS.md](RESULTS.md).

## Layout

- `src/algorithms_evidence_pack/`: the implementations, one module
  per area, each function carrying its own note.
- `tests/`: one test module per implementation module.
- `benchmarks/run_benchmarks.py`: the timing harness and the naive
  baselines it compares against.
- `RESULTS.md`: the committed benchmark record.

## Claims ceiling

This is an evidence pack of fundamentals: the algorithms are written
by hand and verified by tests, and the timings are measured, not
estimated. It is not a claim about interview performance, production
system design, or anything beyond what the tests and benchmarks in
this repository actually show.

## License

Apache-2.0. See `LICENSE`.
