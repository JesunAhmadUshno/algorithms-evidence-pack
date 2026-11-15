import { useMemo, useRef, useState } from "react";
import data from "./data.json";

const REPO = "https://github.com/JesunAhmadUshno/algorithms-evidence-pack";

function clean(text) {
  return text.replace(/`/g, "");
}

function BenchmarkChart({ scale, sort }) {
  const rows = useMemo(() => {
    const list = [...data.benchmarks];
    if (sort === "speedup") list.sort((a, b) => b.speedup - a.speedup);
    if (sort === "pack") list.sort((a, b) => a.packMs - b.packMs);
    return list;
  }, [sort]);
  const maxMs = Math.max(...data.benchmarks.flatMap((b) => [b.packMs, b.baselineMs]));
  const width = (ms) => {
    if (scale === "log") {
      const lo = Math.log10(0.04);
      const hi = Math.log10(maxMs);
      return Math.max(1.5, ((Math.log10(Math.max(ms, 0.04)) - lo) / (hi - lo)) * 100);
    }
    return Math.max(1.5, (ms / maxMs) * 100);
  };
  return (
    <div className="chart">
      {rows.map((b) => {
        const loss = b.speedup < 1;
        return (
          <div className="chart-row" key={b.name}>
            <div className="chart-head">
              <span className="chart-name">{b.name}</span>
              <span className={loss ? "chip chip-loss" : "chip chip-win"}>
                {b.speedupText} {loss ? "slower" : "faster"}
              </span>
            </div>
            <p className="chart-input">input: {b.input}</p>
            <div className="bar-line">
              <span className="bar-label">this pack</span>
              <div className="bar-track">
                <div
                  className={loss ? "bar bar-loss" : "bar bar-pack"}
                  style={{ width: `${width(b.packMs)}%` }}
                />
              </div>
              <span className="bar-value num">{b.packMs} ms</span>
            </div>
            <div className="bar-line">
              <span className="bar-label">baseline</span>
              <div className="bar-track">
                <div className="bar bar-base" style={{ width: `${width(b.baselineMs)}%` }} />
              </div>
              <span className="bar-value num">{b.baselineMs} ms</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function StructureDiagram() {
  const mods = data.areas;
  const rowH = 46;
  const top = 30;
  const height = top * 2 + mods.length * rowH;
  const midY = height / 2;
  return (
    <svg
      className="diagram"
      viewBox={`0 0 980 ${height}`}
      role="img"
      aria-label="Diagram of the package structure: one Python package with ten modules, verified by the test suite and the benchmark harness"
    >
      <rect className="dg-root" x="10" y={midY - 40} width="215" height="80" rx="10" />
      <text className="dg-text" x="28" y={midY - 6}>algorithms_evidence_pack</text>
      <text className="dg-sub" x="28" y={midY + 18}>src package, Python</text>
      {mods.map((a, i) => {
        const y = top + i * rowH;
        const cy = y + 17;
        return (
          <g key={a.module}>
            <path className="dg-line" d={`M 225 ${midY} C 300 ${midY}, 300 ${cy}, 372 ${cy}`} />
            <rect className="dg-mod" x="372" y={y} width="240" height="34" rx="8" />
            <text className="dg-text-sm" x="386" y={cy + 5}>{a.module}.py</text>
            <path className="dg-line" d={`M 612 ${cy} C 680 ${cy}, 690 ${midY - 60}, 762 ${midY - 60}`} opacity={i % 3 === 0 ? 1 : 0.25} />
            <path className="dg-line" d={`M 612 ${cy} C 680 ${cy}, 690 ${midY + 60}, 762 ${midY + 60}`} opacity={i % 3 === 2 ? 1 : 0.25} />
          </g>
        );
      })}
      <rect className="dg-sink" x="762" y={midY - 92} width="208" height="64" rx="10" />
      <text className="dg-text-sm" x="778" y={midY - 62}>tests, one module each</text>
      <text className="dg-sub" x="778" y={midY - 42}>{data.testsPassing} tests passing</text>
      <rect className="dg-sink" x="762" y={midY + 28} width="208" height="64" rx="10" />
      <text className="dg-text-sm" x="778" y={midY + 58}>benchmarks harness</text>
      <text className="dg-sub" x="778" y={midY + 78}>{data.benchmarks.length} measured rows</text>
    </svg>
  );
}

export default function App() {
  const [area, setArea] = useState("All areas");
  const [query, setQuery] = useState("");
  const [scale, setScale] = useState("log");
  const [sort, setSort] = useState("record");
  const indexRef = useRef(null);

  const entries = useMemo(() => {
    const all = data.areas.flatMap((a) =>
      a.implementations.map((name) => ({ name, area: a.area, file: a.file }))
    );
    return all.filter(
      (e) =>
        (area === "All areas" || e.area === area) &&
        e.name.toLowerCase().includes(query.toLowerCase())
    );
  }, [area, query]);

  const pickArea = (name) => {
    setArea(name);
    indexRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div className="page">
      <header className="nav container">
        <span className="wordmark">Algorithms Evidence Pack</span>
        <nav className="nav-links" aria-label="Sections">
          <a href="#coverage">Coverage</a>
          <a href="#benchmarks">Benchmarks</a>
          <a href="#index">Index</a>
          <a href="#structure">Structure</a>
          <a href="#method">Method</a>
          <a className="nav-cta" href={REPO}>GitHub</a>
        </nav>
      </header>

      <main>
        <section className="hero container">
          <h1>Algorithms, verified by measurement.</h1>
          <p className="lead">
            Algorithms from scratch in Python, checked by tests and timed
            against baselines.
          </p>
          <div className="hero-actions">
            <a className="btn btn-primary" href="#benchmarks">See the benchmarks</a>
            <a className="btn btn-ghost" href={`${REPO}/blob/main/RESULTS.md`}>Read RESULTS.md</a>
          </div>
          <dl className="stats">
            <div>
              <dt>tests passing</dt>
              <dd className="num">{data.testsPassing}</dd>
            </div>
            <div>
              <dt>benchmarks measured</dt>
              <dd className="num">{data.benchmarks.length}</dd>
            </div>
            <div>
              <dt>areas covered</dt>
              <dd className="num">{data.areas.length}</dd>
            </div>
            <div>
              <dt>measured on</dt>
              <dd className="num">{data.measuredOn}</dd>
            </div>
          </dl>
        </section>

        <section id="coverage" className="section container">
          <h2>Coverage map</h2>
          <p className="section-lede">
            Ten areas, one module each. Select an area to filter the
            implementation index below.
          </p>
          <div className="coverage-grid">
            {data.areas.map((a) => (
              <button
                key={a.area}
                type="button"
                className={area === a.area ? "area-card area-card-active" : "area-card"}
                onClick={() => pickArea(a.area)}
                aria-pressed={area === a.area}
              >
                <span className="area-name">{a.area}</span>
                <span className="area-count num">
                  {a.implementations.length} listed
                </span>
                <span className="area-file">{a.module}.py</span>
              </button>
            ))}
          </div>
        </section>

        <section id="benchmarks" className="section container">
          <h2>Benchmarks, losses included</h2>
          <p className="section-lede">
            Median wall-clock times from RESULTS.md. The two hand-written sorts
            lose to the standard library, and their rows stay in the chart.
          </p>
          <div className="controls" role="group" aria-label="Chart controls">
            <div className="control-group">
              <span className="control-label" id="scale-label">scale</span>
              <div className="segmented" role="group" aria-labelledby="scale-label">
                <button type="button" className={scale === "log" ? "seg seg-active" : "seg"} onClick={() => setScale("log")} aria-pressed={scale === "log"}>log</button>
                <button type="button" className={scale === "linear" ? "seg seg-active" : "seg"} onClick={() => setScale("linear")} aria-pressed={scale === "linear"}>linear</button>
              </div>
            </div>
            <div className="control-group">
              <label className="control-label" htmlFor="sort-select">order</label>
              <select id="sort-select" className="select" value={sort} onChange={(e) => setSort(e.target.value)}>
                <option value="record">as recorded</option>
                <option value="speedup">by speedup</option>
                <option value="pack">by pack time</option>
              </select>
            </div>
          </div>
          <BenchmarkChart scale={scale} sort={sort} />
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th scope="col">benchmark</th>
                  <th scope="col">input size</th>
                  <th scope="col">this pack (ms)</th>
                  <th scope="col">baseline (ms)</th>
                  <th scope="col">speedup</th>
                </tr>
              </thead>
              <tbody>
                {data.benchmarks.map((b) => (
                  <tr key={b.name}>
                    <td>{b.name}</td>
                    <td>{b.input}</td>
                    <td className="num">{b.packMs}</td>
                    <td className="num">{b.baselineMs}</td>
                    <td className="num">{b.speedupText}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section id="index" className="section container" ref={indexRef}>
          <h2>Implementation index</h2>
          <p className="section-lede">
            Every implementation named in the README coverage table, with the
            module that holds it. Search or filter by area.
          </p>
          <div className="controls">
            <div className="control-group control-grow">
              <label className="control-label" htmlFor="search">search</label>
              <input
                id="search"
                className="search"
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="try: dijkstra, knapsack, sliding"
              />
            </div>
          </div>
          <div className="chips" role="group" aria-label="Filter by area">
            {["All areas", ...data.areas.map((a) => a.area)].map((name) => (
              <button
                key={name}
                type="button"
                className={area === name ? "chip-btn chip-btn-active" : "chip-btn"}
                onClick={() => setArea(name)}
                aria-pressed={area === name}
              >
                {name}
              </button>
            ))}
          </div>
          <p className="result-count num" role="status">
            {entries.length} of {data.areas.reduce((n, a) => n + a.implementations.length, 0)} listed implementations shown
          </p>
          <ul className="index-list">
            {entries.map((e) => (
              <li key={`${e.area}-${e.name}`} className="index-row">
                <span className="index-name">{e.name}</span>
                <span className="index-area">{e.area}</span>
                <span className="index-file">{e.file.split("/").pop()}</span>
              </li>
            ))}
          </ul>
          {entries.length === 0 && (
            <p className="empty">No implementation matches that search.</p>
          )}
        </section>

        <section id="structure" className="section container">
          <h2>How the pack is built</h2>
          <p className="section-lede">
            One package, ten modules. Each module is checked by its own test
            module, and the benchmark harness times the core set against naive
            baselines or the standard library.
          </p>
          <div className="diagram-wrap">
            <StructureDiagram />
          </div>
        </section>

        <section id="method" className="section container">
          <h2>Method and honest reading</h2>
          <div className="two-col">
            <div>
              <h3 className="col-head">Method</h3>
              <ul className="plain-list">
                {data.method.map((m) => (
                  <li key={m.slice(0, 32)}>{clean(m)}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="col-head">Reading the table honestly</h3>
              <ul className="plain-list">
                {data.honestReading.map((m) => (
                  <li key={m.slice(0, 32)}>{clean(m)}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer container">
        <p className="footer-head">Claims ceiling</p>
        <p>{clean(data.claimsCeiling)}</p>
        <p className="footer-links">
          <a href={REPO}>GitHub repository</a>
          <a href={`${REPO}/blob/main/RESULTS.md`}>RESULTS.md</a>
          <a href={`${REPO}/blob/main/README.md`}>README.md</a>
        </p>
        <p className="support">
          <a href="https://github.com/sponsors/JesunAhmadUshno">Sponsor this work</a>
          <a href="https://github.com/sponsors/JesunAhmadUshno">Donate</a>
          <a href="https://buymeacoffee.com/jesun">Buy Me a Coffee</a>
          <a href="https://calendly.com/jesunahmadushno/30min">Work with me</a>
        </p>
        <p className="footer-note">
          Every number on this page is generated at build time from RESULTS.md
          and README.md in the repository, and the build fails if the two drift.
        </p>
      </footer>
    </div>
  );
}
