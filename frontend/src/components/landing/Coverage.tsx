import {
  CheckCircle2,
  Gauge,
  Plane,
  RefreshCw,
  Route as RouteIcon,
  Search,
} from "lucide-react";

import Intro from "../common/Intro";
import Reveal from "../common/Reveal";
import Count from "../common/Count";

const chips = [
  [Plane, "Airlines", "Scheduled airline observations"],
  [Search, "OTAs", "Representative market quotes"],
  [RouteIcon, "Route Basket", "Major Indian corridors"],
  [Gauge, "Booking Windows", "T+1 through T+45"],
  [RefreshCw, "Daily Refresh", "Continuously refreshed signals"],
  [
    CheckCircle2,
    "Quality Validation",
    "Cross-source consistency and anomaly checks",
  ],
];

function Status() {
  return (
    <div className="status">
      <div className="radar">
        <i />
        <i />
        <i />
      </div>

      <p className="technical">SYSTEM STATUS</p>

      <h3>
        <i />
        Sources Healthy
      </h3>

      <div>
        <span>
          <strong>94%</strong>
          Coverage
        </span>

        <span>
          <strong>18,420</strong>
          Observations
        </span>

        <span>
          <strong>2 min</strong>
          Last update
        </span>

        <span>
          <strong>0</strong>
          Critical failures
        </span>
      </div>
    </div>
  );
}

export default function Coverage() {
  return (
    <section id="coverage" className="section coverage">
      <div className="wrap">
        <Intro
          eyebrow="Trust & coverage"
          title="Built on Broad Market Coverage"
        >
          A representative, quality-controlled view designed for defensible
          market insight.
        </Intro>

        <div className="coverage-layout">
          <Reveal>
            <div className="counters">
              <div>
                <strong>
                  <Count value={20} suffix="+" />
                </strong>
                <span>Representative Routes</span>
              </div>

              <div>
                <strong>
                  <Count value={5} />
                </strong>
                <span>Booking Windows</span>
              </div>

              <div>
                <strong>
                  <Count value={3} />
                </strong>
                <span>Index Frequencies</span>
              </div>

              <div>
                <strong>Multi-source</strong>
                <span>Fare Validation</span>
              </div>
            </div>

            <div className="chips">
              {chips.map(([Icon, l, t]) => (
                <div tabIndex={0} key={l as string}>
                  <Icon />
                  <span>{l as string}</span>
                  <em>{t as string}</em>
                </div>
              ))}
            </div>
          </Reveal>

          <Reveal delay={0.1}>
            <Status />
          </Reveal>
        </div>
      </div>
    </section>
  );
}
