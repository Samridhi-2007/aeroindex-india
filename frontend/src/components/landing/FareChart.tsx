import { motion } from "framer-motion";

import type { RouteData } from "../../data/landingData";

export default function FareChart({ d }: { d: RouteData }) {
  const w = 660;
  const h = 220;
  const pad = 34;

  const all = [...d.points, ...d.expected];

  const min = Math.min(...all) * 0.97;
  const max = Math.max(...all) * 1.03;

  const pt = (v: number, i: number) => [
    pad + (i * (w - pad * 2)) / (d.points.length - 1),
    h - pad - ((v - min) / (max - min)) * (h - pad * 2),
  ];

  const path = d.points
    .map((v, i) => `${i ? "L" : "M"} ${pt(v, i).join(" ")}`)
    .join(" ");

  const exp = d.expected
    .map((v, i) => `${i ? "L" : "M"} ${pt(v, i).join(" ")}`)
    .join(" ");

  const last = pt(d.points[d.points.length - 1], 6);

  return (
    <div className="chart">
      <div>
        <span>
          {d.from} → {d.to} / 7 observations
        </span>

        <span>Fare history · Expected range</span>
      </div>

      <svg viewBox={`0 0 ${w} ${h}`}>
        <defs>
          <linearGradient id="area" x1="0" y1="0" x2="0" y2="1">
            <stop stopColor="#3578E5" stopOpacity=".3" />
            <stop offset="1" stopColor="#3578E5" stopOpacity="0" />
          </linearGradient>
        </defs>

        {[0, 1, 2, 3].map((i) => (
          <line
            key={i}
            x1={pad}
            x2={w - pad}
            y1={pad + i * 45}
            y2={pad + i * 45}
            className="gridline"
          />
        ))}

        <motion.path
          d={`${path} L ${w - pad} ${h - pad} L ${pad} ${h - pad} Z`}
          fill="url(#area)"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        />

        <motion.path
          key={`e${d.id}`}
          d={exp}
          className="expected-line"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
        />

        <motion.path
          key={d.id}
          d={path}
          className="actual-line"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
        />

        <circle cx={last[0]} cy={last[1]} r="5" className="current-point" />
      </svg>

      <p>
        <span>7 days ago</span>
        <span>Today</span>
      </p>
    </div>
  );
}
