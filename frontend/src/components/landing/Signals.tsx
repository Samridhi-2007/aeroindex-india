import { Activity, Gauge, RefreshCw, TrendingUp } from "lucide-react";

import Intro from "../common/Intro";
import Reveal from "../common/Reveal";
import Spark from "../common/Spark";

import { routes } from "../../data/landingData";

const signals = [
  [
    Activity,
    "Fare anomaly detected",
    "DEL → BLR",
    "31% above expected range",
    "₹9,240",
    "Confidence 92%",
    "anomaly",
  ],
  [
    TrendingUp,
    "Highest weekly increase",
    "DEL → BOM",
    "Up 6.8% this week",
    "₹5,842",
    "Momentum rising",
    "positive",
  ],
  [
    Gauge,
    "Most stable route",
    "BOM → BLR",
    "Variance below 3%",
    "₹4,910",
    "Stable signal",
    "stable",
  ],
  [
    RefreshCw,
    "Strongest booking-window shift",
    "MAA → DEL",
    "Demand moved forward",
    "T+15",
    "Observed today",
    "warning",
  ],
];

export default function Signals() {
  return (
    <section id="signals" className="section signals">
      <div className="signal-dots" />

      <div className="wrap">
        <Intro eyebrow="Signal layer" title="Airfare Market Signals" light>
          The movements that matter, surfaced from thousands of market
          observations.
        </Intro>

        <div className="signal-cards">
          {signals.map(([Icon, title, route, detail, value, meta, tone], i) => (
            <Reveal key={title as string} delay={i * 0.07}>
              <article className={tone as string}>
                <div>
                  <span>
                    <Icon />
                  </span>

                  <small>{meta as string}</small>
                </div>

                <p>{title as string}</p>

                <section>
                  <div>
                    <h3>{route as string}</h3>
                    <span>{detail as string}</span>
                  </div>

                  <strong>{value as string}</strong>
                </section>

                <Spark points={routes[i].points} dark />
              </article>
            </Reveal>
          ))}
        </div>

        <Reveal>
          <div className="activity-bar">
            <div className="activity-wave">
              {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
                <i key={i} />
              ))}
            </div>

            <p>
              <i />
              LIVE SIGNAL ACTIVITY
            </p>

            <div>
              <b>
                12 <small>Observations</small>
              </b>

              <b>
                7 <small>Stable Corridors</small>
              </b>

              <b>
                2 <small>Momentum Shifts</small>
              </b>

              <b>
                3 <small>Anomalies</small>
              </b>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
