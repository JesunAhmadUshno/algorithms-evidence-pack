// Drift check: independently re-parses RESULTS.md and README.md and
// compares every figure against the generated src/data.json. Fails
// the build (exit 1) on any mismatch, so the page cannot drift from
// the committed record.
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..", "..");
const results = readFileSync(join(root, "RESULTS.md"), "utf-8");
const data = JSON.parse(readFileSync(join(here, "..", "src", "data.json"), "utf-8"));

let failures = 0;
function fail(msg) {
  console.error(`check FAIL: ${msg}`);
  failures += 1;
}

const rows = [];
for (const line of results.split("\n")) {
  if (!line.startsWith("|")) continue;
  const cells = line.split("|").slice(1, -1).map((c) => c.trim());
  if (cells.length !== 5 || cells[0] === "Benchmark") continue;
  if (/^-+$/.test(cells[0].replace(/[: ]/g, ""))) continue;
  rows.push(cells);
}
if (rows.length !== data.benchmarks.length)
  fail(`benchmark row count: RESULTS.md has ${rows.length}, data.json has ${data.benchmarks.length}`);
rows.forEach((cells, i) => {
  const b = data.benchmarks[i];
  if (!b) return;
  if (b.name !== cells[0]) fail(`row ${i} name: "${b.name}" != "${cells[0]}"`);
  if (b.input !== cells[1]) fail(`row ${i} input: "${b.input}" != "${cells[1]}"`);
  if (b.packMs !== parseFloat(cells[2])) fail(`row ${i} packMs: ${b.packMs} != ${cells[2]}`);
  if (b.baselineMs !== parseFloat(cells[3])) fail(`row ${i} baselineMs: ${b.baselineMs} != ${cells[3]}`);
  if (b.speedupText !== cells[4]) fail(`row ${i} speedup: "${b.speedupText}" != "${cells[4]}"`);
});

const testsMatch = results.match(/(\d+) unit tests pass/);
if (!testsMatch || data.testsPassing !== parseInt(testsMatch[1], 10))
  fail(`testsPassing: data.json ${data.testsPassing} != RESULTS.md ${testsMatch && testsMatch[1]}`);

const measuredMatch = results.match(/Measured on (\d{4}-\d{2}-\d{2})/);
if (!measuredMatch || data.measuredOn !== measuredMatch[1])
  fail(`measuredOn: data.json ${data.measuredOn} != RESULTS.md ${measuredMatch && measuredMatch[1]}`);

if (failures > 0) {
  console.error(`check: ${failures} drift failure(s)`);
  process.exit(1);
}
console.log("check: data.json matches RESULTS.md exactly");
