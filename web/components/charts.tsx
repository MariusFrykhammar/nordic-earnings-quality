"use client";
// Hand-built SVG charts: one y-axis, 2px lines, direct labels, recessive grid, hover tooltips.
import { useState } from "react";
import { money } from "@/lib/format";

export type Pt = { year: number; np: number | null; ocf: number | null };

function niceTicks(min: number, max: number, n = 4): number[] {
  if (min === max) { min -= 1; max += 1; }
  const span = max - min;
  const step0 = span / n;
  const mag = Math.pow(10, Math.floor(Math.log10(step0)));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= step0) ?? 10 * mag;
  const out: number[] = [];
  const end = Math.ceil(max / step - 1e-9) * step;
  for (let v = Math.floor(min / step + 1e-9) * step; v <= end + step * 0.001; v += step) out.push(Number(v.toFixed(10)));
  return out;
}

const axis = (v: number) => {
  const a = Math.abs(v);
  return new Intl.NumberFormat("en-GB", { maximumFractionDigits: a >= 10 || v === 0 ? 0 : a >= 1 ? 1 : 2 }).format(v).replace("-", "−");
};

/** Net profit vs operating cash flow. The gap is shaded where profit runs ahead of cash. */
export function DivergenceChart({ data, currency, height = 300, width = 640 }: { data: Pt[]; currency: string; height?: number; width?: number }) {
  const [hover, setHover] = useState<number | null>(null);
  const W = width, H = height, L = 56, R = 132, T = 14, B = 30;
  const pts = data.filter((d) => d.np !== null || d.ocf !== null);
  if (pts.length < 2) return <p className="muted small">Not enough years reported to draw the chart.</p>;
  const vals = pts.flatMap((d) => [d.np, d.ocf]).filter((v): v is number => v !== null);
  const ticks = niceTicks(Math.min(0, ...vals), Math.max(0, ...vals));
  const y0 = ticks[0], y1 = ticks[ticks.length - 1];
  const x = (i: number) => L + (i * (W - L - R)) / (pts.length - 1);
  const y = (v: number) => T + ((y1 - v) * (H - T - B)) / (y1 - y0);

  const line = (k: "np" | "ocf") =>
    pts.map((d, i) => (d[k] === null ? null : `${x(i)},${y(d[k] as number)}`)).filter(Boolean).join(" L ");

  // shaded gap: polygons over each segment where both values exist and profit > cash
  const gaps: string[] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const a = pts[i], b = pts[i + 1];
    if (a.np === null || a.ocf === null || b.np === null || b.ocf === null) continue;
    const da = a.np - a.ocf, db = b.np - b.ocf;
    if (da <= 0 && db <= 0) continue;
    if (da > 0 && db > 0) {
      gaps.push(`${x(i)},${y(a.np)} ${x(i + 1)},${y(b.np)} ${x(i + 1)},${y(b.ocf)} ${x(i)},${y(a.ocf)}`);
    } else {
      const t = da / (da - db); // crossing point
      const xc = x(i) + t * (x(i + 1) - x(i));
      const yc = y(a.np + t * (b.np - a.np));
      gaps.push(da > 0
        ? `${x(i)},${y(a.np)} ${xc},${yc} ${x(i)},${y(a.ocf)}`
        : `${xc},${yc} ${x(i + 1)},${y(b.np)} ${x(i + 1)},${y(b.ocf)}`);
    }
  }
  const last = pts[pts.length - 1];
  const labY = (v: number | null, other: number | null) => {
    if (v === null) return 0;
    let yy = y(v);
    if (other !== null && Math.abs(y(v) - y(other)) < 16) yy += v >= other ? -8 : 8;
    return yy;
  };
  const hp = hover === null ? null : pts[hover];

  return (
    <div className="chart-wrap">
      <svg
        className="chart"
        viewBox={`0 0 ${W} ${H}`}
        role="img"
        aria-label={`Net profit and operating cash flow, ${currency} millions, ${pts[0].year} to ${last.year}`}
        onMouseLeave={() => setHover(null)}
      >
        {ticks.map((t) => (
          <g key={t}>
            <line x1={L} x2={W - R} y1={y(t)} y2={y(t)} className={t === 0 ? "zero" : "grid"} strokeWidth={1} />
            <text x={L - 8} y={y(t) + 4} textAnchor="end">{axis(t)}</text>
          </g>
        ))}
        {gaps.map((p, i) => <polygon key={i} points={p} className="gapfill" />)}
        <path d={`M ${line("ocf")}`} fill="none" className="l-cash" strokeWidth={2} strokeLinejoin="round" />
        <path d={`M ${line("np")}`} fill="none" className="l-profit" strokeWidth={2} strokeLinejoin="round" />
        {pts.map((d, i) => (
          <text key={d.year} x={x(i)} y={H - 8} textAnchor="middle">{d.year}</text>
        ))}
        {last.np !== null && <text className="lab" x={W - R + 8} y={labY(last.np, last.ocf) + 4} >Net profit</text>}
        {last.ocf !== null && <text className="lab" x={W - R + 8} y={labY(last.ocf, last.np) + 4} >Operating cash flow</text>}
        {hp && (
          <g>
            <line x1={x(hover!)} x2={x(hover!)} y1={T} y2={H - B} className="cross" />
            {hp.np !== null && <circle cx={x(hover!)} cy={y(hp.np)} r={4.5} className="d-profit" strokeWidth={2} />}
            {hp.ocf !== null && <circle cx={x(hover!)} cy={y(hp.ocf)} r={4.5} className="d-cash" strokeWidth={2} />}
          </g>
        )}
        {pts.map((d, i) => (
          <rect key={"h" + d.year} x={x(i) - (W - L - R) / (2 * (pts.length - 1))} y={T} width={(W - L - R) / (pts.length - 1)} height={H - T - B}
            fill="transparent" onMouseEnter={() => setHover(i)} onFocus={() => setHover(i)} tabIndex={-1} />
        ))}
      </svg>
      {hp && (
        <div className="tip" style={{ left: `${(x(hover!) / W) * 100}%`, top: `${(Math.min(y(hp.np ?? 0), y(hp.ocf ?? 0)) / H) * 100}%` }}>
          <span><b>FY{hp.year}</b>, {currency} millions</span>
          <span>Net profit {money(hp.np)}</span>
          <span>Operating cash flow {money(hp.ocf)}</span>
        </div>
      )}
    </div>
  );
}

/** Tiny profit-vs-cash pair for table rows. */
export function Spark({ data }: { data: Pt[] }) {
  const W = 112, H = 30, P = 3;
  const pts = data.filter((d) => d.np !== null || d.ocf !== null);
  if (pts.length < 2) return <span className="muted small">–</span>;
  const vals = pts.flatMap((d) => [d.np, d.ocf]).filter((v): v is number => v !== null);
  const lo = Math.min(...vals), hi = Math.max(...vals);
  const x = (i: number) => P + (i * (W - 2 * P)) / (pts.length - 1);
  const y = (v: number) => (hi === lo ? H / 2 : P + ((hi - v) * (H - 2 * P)) / (hi - lo));
  const path = (k: "np" | "ocf") =>
    "M " + pts.map((d, i) => (d[k] === null ? null : `${x(i)},${y(d[k] as number)}`)).filter(Boolean).join(" L ");
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} aria-hidden="true" style={{ display: "block" }}>
      {lo < 0 && hi > 0 && <line x1={0} x2={W} y1={y(0)} y2={y(0)} stroke="#1d2938" />}
      <path d={path("ocf")} fill="none" stroke="#d9690c" strokeWidth={2} strokeLinejoin="round" />
      <path d={path("np")} fill="none" stroke="#5b8bff" strokeWidth={2} strokeLinejoin="round" />
    </svg>
  );
}

const pctTick = (t: number) => {
  const v = Math.round(t * 1000) / 10;
  return (Number.isInteger(v) ? v.toFixed(0) : v.toFixed(1)).replace("-", "−") + "%";
};

export type Bubble = { lei: string; name: string; x: number; y: number; size: number };

/** Revenue growth (x) vs EBIT margin (y), area = revenue in EUR. Direct labels, no legend needed. */
export function BubbleChart({ data }: { data: Bubble[] }) {
  const [hover, setHover] = useState<string | null>(null);
  const W = 680, H = 380, L = 56, R = 24, T = 16, B = 42;
  if (!data.length) return null;
  const xs = data.map((d) => d.x), ys = data.map((d) => d.y);
  const xt = niceTicks(Math.min(0, ...xs), Math.max(0, ...xs));
  const yt = niceTicks(Math.min(0, ...ys), Math.max(0, ...ys));
  const x = (v: number) => L + ((v - xt[0]) * (W - L - R)) / (xt[xt.length - 1] - xt[0]);
  const y = (v: number) => T + ((yt[yt.length - 1] - v) * (H - T - B)) / (yt[yt.length - 1] - yt[0]);
  const maxS = Math.max(...data.map((d) => d.size), 1);
  const r = (s: number) => 6 + 26 * Math.sqrt(Math.max(s, 0) / maxS);
  const h = data.find((d) => d.lei === hover);
  // greedy label placement: above the circle, else below, else to the right
  const boxes: { x0: number; x1: number; y0: number; y1: number }[] = [];
  const labels = [...data].sort((a, b) => y(a.y) - y(b.y)).map((d) => {
    const w = d.name.length * 7.2, cx = x(d.x), cy = y(d.y), rr = r(d.size);
    const cands = [
      { x: cx, y: cy - rr - 6 },
      { x: cx, y: cy + rr + 15 },
      { x: cx + rr + 6 + w / 2, y: cy + 4 },
      { x: cx - rr - 6 - w / 2, y: cy + 4 },
    ];
    const fits = (c: { x: number; y: number }) => {
      const b = { x0: c.x - w / 2, x1: c.x + w / 2, y0: c.y - 12, y1: c.y + 3 };
      return !boxes.some((o) => b.x0 < o.x1 && b.x1 > o.x0 && b.y0 < o.y1 && b.y1 > o.y0) &&
        !data.some((o) => o.lei !== d.lei && Math.hypot(Math.max(b.x0 - x(o.x), 0, x(o.x) - b.x1), Math.max(b.y0 - y(o.y), 0, y(o.y) - b.y1)) < r(o.size) - 2);
    };
    const c = cands.find(fits) ?? cands[0];
    boxes.push({ x0: c.x - w / 2, x1: c.x + w / 2, y0: c.y - 12, y1: c.y + 3 });
    return { lei: d.lei, name: d.name, x: c.x, y: c.y };
  });
  return (
    <div className="chart-wrap" style={{ maxWidth: 820 }}>
      <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Revenue growth against EBIT margin; circle area shows revenue">
        {yt.map((t) => (
          <g key={"y" + t}>
            <line x1={L} x2={W - R} y1={y(t)} y2={y(t)} className={t === 0 ? "zero" : "grid"} />
            <text x={L - 8} y={y(t) + 4} textAnchor="end">{pctTick(t)}</text>
          </g>
        ))}
        {xt.map((t) => (
          <g key={"x" + t}>
            <line x1={x(t)} x2={x(t)} y1={T} y2={H - B} className={t === 0 ? "zero" : "grid"} />
            <text x={x(t)} y={H - B + 18} textAnchor="middle">{pctTick(t)}</text>
          </g>
        ))}
        <text x={(L + W - R) / 2} y={H - 4} textAnchor="middle">Revenue growth, latest year</text>
        <text x={14} y={(T + H - B) / 2} textAnchor="middle" transform={`rotate(-90 14 ${(T + H - B) / 2})`}>EBIT margin</text>
        {[...data].sort((a, b) => b.size - a.size).map((d) => (
          <circle key={d.lei} cx={x(d.x)} cy={y(d.y)} r={r(d.size)} className="bubble" strokeWidth={2}
            onMouseEnter={() => setHover(d.lei)} onMouseLeave={() => setHover(null)} />
        ))}
        {labels.map((l) => (
          <text key={"l" + l.lei} className="lab" x={l.x} y={l.y} textAnchor="middle" style={{ pointerEvents: "none" }}>{l.name}</text>
        ))}
      </svg>
      {h && (
        <div className="tip" style={{ left: `${(x(h.x) / W) * 100}%`, top: `${((y(h.y) - r(h.size)) / H) * 100}%` }}>
          <span><b>{h.name}</b></span>
          <span>Revenue growth {(h.x * 100).toFixed(1)}%</span>
          <span>EBIT margin {(h.y * 100).toFixed(1)}%</span>
          <span>Revenue €{Math.round(h.size).toLocaleString("en-GB")}m</span>
        </div>
      )}
    </div>
  );
}
