// Generates src/data.json by parsing the committed record files
// (RESULTS.md and README.md at the repository root). No number on the
// site is hand-typed here: every figure is parsed from those files,
// and tools/check.mjs re-parses them independently and fails the
// build if the generated data drifts from the record.
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..", "..");
const results = readFileSync(join(root, "RESULTS.md"), "utf-8");
const readme = readFileSync(join(root, "README.md"), "utf-8");

function section(md, heading) {
  const start = md.indexOf(heading);
  if (start < 0) throw new Error(`section not found: ${heading}`);
  const rest = md.slice(start + heading.length);
  const next = rest.indexOf("\n## ");
  return next < 0 ? rest : rest.slice(0, next);
}

function bullets(text) {
  const out = [];
  let current = null;
  for (const line of text.split("\n")) {
    if (line.startsWith("- ")) {
      if (current !== null) out.push(current);
      current = line.slice(2);
    } else if (current !== null && line.trim() && !line.startsWith("#")) {
      current += " " + line.trim();
    } else if (current !== null && !line.trim()) {
      out.push(current);
      current = null;
    }
  }
  if (current !== null) out.push(current);
  return out.map((b) => b.replace(/\s+/g, " ").trim());
}

// Benchmarks table from RESULTS.md
const benchSection = section(results, "## Benchmarks");
const benchmarks = [];
for (const line of benchSection.split("\n")) {
  if (!line.startsWith("|")) continue;
  const cells = line.split("|").slice(1, -1).map((c) => c.trim());
  if (cells.length !== 5) continue;
  if (cells[0] === "Benchmark" || /^-+$/.test(cells[0].replace(/[: ]/g, ""))) continue;
  benchmarks.push({
    name: cells[0],
    input: cells[1],
    packMs: parseFloat(cells[2]),
    baselineMs: parseFloat(cells[3]),
    speedup: parseFloat(cells[4].replace(/x$/, "")),
    speedupText: cells[4],
  });
}
if (benchmarks.length === 0) throw new Error("no benchmark rows parsed from RESULTS.md");

// Coverage table from README.md
const coverageSection = section(readme, "## What is covered");
const areas = [];
for (const line of coverageSection.split("\n")) {
  if (!line.startsWith("|")) continue;
  const cells = line.split("|").slice(1, -1).map((c) => c.trim());
  if (cells.length !== 3) continue;
  if (cells[0] === "Area" || /^-+$/.test(cells[0].replace(/[: ]/g, ""))) continue;
  const file = cells[2].replace(/`/g, "");
  areas.push({
    area: cells[0],
    implementations: cells[1].split(",").map((s) => s.trim()).filter(Boolean),
    file,
    module: file.split("/").pop().replace(/\.py$/, ""),
  });
}
if (areas.length === 0) throw new Error("no coverage rows parsed from README.md");

const measuredMatch = results.match(/Measured on (\d{4}-\d{2}-\d{2})/);
const testsMatch = results.match(/(\d+) unit tests pass/);
const claims = section(readme, "## Claims ceiling")
  .split("\n")
  .filter((l) => l.trim() && !l.startsWith("##"))
  .join(" ")
  .replace(/\s+/g, " ")
  .trim();

const data = {
  measuredOn: measuredMatch ? measuredMatch[1] : null,
  testsPassing: testsMatch ? parseInt(testsMatch[1], 10) : null,
  method: bullets(section(results, "## Method")),
  honestReading: bullets(section(results, "## Reading the table honestly")),
  benchmarks,
  areas,
  claimsCeiling: claims,
};

writeFileSync(join(here, "..", "src", "data.json"), JSON.stringify(data, null, 2));
console.log(
  `data.json written: ${benchmarks.length} benchmarks, ${areas.length} areas, ` +
    `${areas.reduce((n, a) => n + a.implementations.length, 0)} listed implementations`
);
