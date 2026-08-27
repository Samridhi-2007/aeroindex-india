import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

import Intro from "../common/Intro";
import Reveal from "../common/Reveal";
import Count from "../common/Count";
import Change from "../common/Change";
import Spark from "../common/Spark";

import { routes } from "../../data/landingData";

export default function Network() {
  const [a, setA] = useState(0);
  const d = routes[a];

  const nodes = [
    { c: "DEL", x: 51, y: 14 },
    { c: "BOM", x: 28, y: 52 },
    { c: "BLR", x: 50, y: 80 },
    { c: "HYD", x: 56, y: 60 },
    { c: "MAA", x: 64, y: 84 },
    { c: "CCU", x: 80, y: 38 },
  ];

  const links = [
    [0, 1],
    [0, 2],
    [1, 2],
    [2, 3],
    [4, 0],
    [0, 5],
  ];

  return (
    <section className="section network">
      <div className="wrap">
        <Intro eyebrow="Network view" title="India Route Intelligence">
          An artistic pulse of the corridors shaping India's airfare market.
        </Intro>

        <Reveal>
          <div className="network-shell">
            <div className="map">
              <div className="scan" />

              <span className="technical">
                COORD / IN-AIRSPACE · OBS / LIVE
              </span>

              <svg viewBox="0 0 100 100">
                {links.map(([x, y], i) => (
                  <g
                    key={i}
                    className={a === i ? "link active" : "link"}
                    onClick={() => setA(i)}
                  >
                    <line
                      x1={nodes[x].x}
                      y1={nodes[x].y}
                      x2={nodes[y].x}
                      y2={nodes[y].y}
                    />

                    {a === i && (
                      <circle r=".9" className="particle">
                        <animateMotion
                          dur="3.8s"
                          repeatCount="indefinite"
                          path={`M${nodes[x].x},${nodes[x].y} L${nodes[y].x},${nodes[y].y}`}
                        />
                      </circle>
                    )}
                  </g>
                ))}

                {nodes.map((n, i) => (
                  <g
                    key={n.c}
                    className={links[a].includes(i) ? "node selected" : "node"}
                  >
                    <circle className="ring" cx={n.x} cy={n.y} r="4" />

                    <circle cx={n.x} cy={n.y} r="1.6" />

                    <text x={n.x + 3} y={n.y + 1}>
                      {n.c}
                    </text>
                  </g>
                ))}
              </svg>

              <em>Select an airport or corridor</em>
            </div>

            <AnimatePresence mode="wait">
              <motion.aside
                key={d.id}
                initial={{
                  opacity: 0,
                  x: 10,
                }}
                animate={{
                  opacity: 1,
                  x: 0,
                }}
                exit={{
                  opacity: 0,
                }}
              >
                <p className="technical">SELECTED CORRIDOR</p>

                <h3>
                  {d.from} <span>→</span> {d.to}
                </h3>

                <strong>
                  <Count value={d.fare} fare />
                </strong>

                <p>
                  <Change value={d.change} /> this week
                </p>

                <Spark points={d.points} />

                <dl>
                  <div>
                    <dt>APIx</dt>
                    <dd>{d.apix}</dd>
                  </div>

                  <div>
                    <dt>Volatility</dt>
                    <dd>{d.volatility}</dd>
                  </div>

                  <div>
                    <dt>Expected Range</dt>
                    <dd>{d.range}</dd>
                  </div>

                  <div>
                    <dt>Last Refresh</dt>
                    <dd>2 min ago</dd>
                  </div>
                </dl>
              </motion.aside>
            </AnimatePresence>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
