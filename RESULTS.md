# Results

Measured on 2026-11-15. Every number below comes from running
`benchmarks/run_benchmarks.py` in this repository; nothing is
estimated. Before any timing starts, the script asserts that the
implementation and the baseline return identical results on the timed
input, so a fast but wrong implementation cannot produce a good row.

## Method

- Timer: `time.perf_counter`, median of 5 repetitions (3 for the LIS
  row, whose baseline is slow), same fixed-seed input for every
  repetition.
- Machine: shared cloud VM, AMD EPYC 9D64 (4 vCPUs visible), Linux,
  Python 3.12.3. Absolute times move between runs on a shared
  machine; the ordering of implementations and the rough size of each
  gap were stable across repeated runs.

## Correctness

85 unit tests pass (`python -m unittest discover -s tests`), covering
every implementation in the pack. Many are property-style: outputs
are compared against an independent reference (the standard library,
a brute-force version, or a second algorithm) on hundreds of seeded
random inputs. Examples: both hand-written sorts against `sorted()`,
Dijkstra against Bellman-Ford on random graphs, knapsack against
exhaustive subset search, the streaming median against
`statistics.median` at every prefix.

## Benchmarks

| Benchmark | Input size | This pack (ms) | Baseline (ms) | Speedup |
| --- | --- | --- | --- | --- |
| quicksort vs sorted() | n = 20,000 random ints | 55.72 | 5.52 | 0.1x |
| mergesort vs sorted() | n = 20,000 random ints | 73.42 | 4.69 | 0.1x |
| sliding window maximum (deque) vs naive max per window | n = 20,000, k = 100 | 8.70 | 50.27 | 5.8x |
| two-sum (hash map) vs brute force, no-pair worst case | n = 2,000 | 0.38 | 217.45 | 571.7x |
| next greater element (monotonic stack) vs naive scan | n = 4,000 | 1.33 | 4.10 | 3.1x |
| Dijkstra (heap) vs Bellman-Ford | 300 nodes, about 1,800 edges | 1.29 | 1.66 | 1.3x |
| longest increasing subsequence (binary search) vs quadratic DP | n = 2,000 | 0.39 | 513.08 | 1299.7x |
| k largest (bounded heap) vs full sort | n = 50,000, k = 10 | 3.03 | 16.61 | 5.5x |

## Reading the table honestly

- The two hand-written sorts lose to `sorted()`, by a lot. That is
  expected: `sorted()` is Timsort implemented in C, and a pure-Python
  quicksort or mergesort pays interpreter costs on every comparison.
  The sorts are in the pack because implementing them correctly is
  the skill being evidenced, not because they beat the standard
  library. Their rows are reported anyway, because a results file
  that only shows wins is not a results file.
- Against naive baselines written in the same language, the
  algorithmic improvements show up clearly: the hash map turns a
  217 ms quadratic scan into 0.38 ms, and the binary-search LIS turns
  roughly half a second of quadratic DP into 0.39 ms.
- The Dijkstra margin over Bellman-Ford is small at this graph size
  (300 nodes). Bellman-Ford with early exit is competitive on small,
  sparse graphs; the heap-based algorithm's advantage grows with
  graph size, which this single size does not demonstrate.
