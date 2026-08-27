import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Plane, Repeat2 } from "lucide-react";

import Intro from "../common/Intro";
import Reveal from "../common/Reveal";
import Segments from "../common/Segments";
import Count from "../common/Count";
import Change from "../common/Change";
import Spark from "../common/Spark";
import FareChart from "./FareChart";

import {
  airports,
  airportNames,
  routes,
  windows,
  windowCopy,
} from "../../data/landingData";

export default function Explorer() {
  const [from, setFrom] = useState("DEL");
  const [to, setTo] = useState("BOM");
  const [win, setWin] = useState("T+7");
  const [period, setPeriod] = useState("Weekly");
  const [flight, setFlight] = useState(0);

  const d = useMemo(
    () =>
      routes.find((r) => r.from === from && r.to === to) ||
      routes[
        (airports.indexOf(from) * 2 + airports.indexOf(to)) % routes.length
      ],
    [from, to],
  );

  const update = (set: (x: string) => void, x: string) => {
    set(x);
    setFlight((v) => v + 1);
  };

  const swap = () => {
    setFrom(to);
    setTo(from);
    setFlight((v) => v + 1);
  };

  return (
    <section id="explorer" className="section explorer">
      <div className="ambient-network" />

      <div className="wrap">
        <Intro
          eyebrow="Interactive explorer"
          title="Track India's Airfare Pulse"
        >
          Explore live fares, price trends, booking horizons, and market signals
          across representative Indian routes.
        </Intro>

        <Reveal>
          <div className="console">
            <div className="controls">
              <p className="technical">ROUTE CONFIGURATION</p>

              <div className="route-selects">
                <label>
                  <span>FROM</span>

                  <select
                    value={from}
                    onChange={(e) => {
                      const nextFrom = e.target.value;
                      update(setFrom, nextFrom);

                      if (nextFrom === to) {
                        const nextTo = airports.find(
                          (airport) => airport !== nextFrom,
                        );

                        if (nextTo) setTo(nextTo);
                      }
                    }}
                  >
                    {airports.map((a) => (
                      <option value={a} key={a}>
                        {airportNames[a]} ({a})
                      </option>
                    ))}
                  </select>
                </label>

                <button className="swap" onClick={swap}>
                  <Repeat2 />
                </button>

                <motion.i
                  key={flight}
                  className="flight"
                  initial={{
                    x: -12,
                    opacity: 0,
                  }}
                  animate={{
                    x: 14,
                    opacity: 1,
                  }}
                >
                  <Plane />
                </motion.i>

                <label>
                  <span>TO</span>

                  <select
                    value={to}
                    onChange={(e) => update(setTo, e.target.value)}
                  >
                    {airports
                      .filter((a) => a !== from)
                      .map((a) => (
                        <option value={a} key={a}>
                          {airportNames[a]} ({a})
                        </option>
                      ))}
                  </select>
                </label>
              </div>

              <div className="control">
                <span>BOOKING WINDOW</span>

                <Segments items={windows} active={win} set={setWin} id="win" />

                <motion.p
                  key={win}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  {windowCopy[win]}
                </motion.p>
              </div>

              <div className="control">
                <span>PERIOD</span>

                <Segments
                  items={["Daily", "Weekly", "Monthly"]}
                  active={period}
                  set={setPeriod}
                  id="period"
                />
              </div>

              <div className="refresh">
                <i />
                Market data refreshed 2 min ago
              </div>
            </div>

            <motion.div
              key={`${d.id}${win}${period}`}
              className="intel"
              initial={{ opacity: 0.7 }}
              animate={{ opacity: 1 }}
            >
              <div className="headline-metrics">
                <div>
                  <span>MEDIAN FARE</span>

                  <strong>
                    <Count value={d.fare + windows.indexOf(win) * 52} fare />
                  </strong>

                  <p>
                    <Change value={d.change} light /> vs last week
                  </p>
                </div>

                <div>
                  <span>APIx</span>
                  <strong>{d.apix}</strong>
                  <Change value={d.apixChange} light />
                </div>
              </div>

              <div className="mini-metrics">
                <div>
                  <span>Volatility</span>
                  <strong>{d.volatility}</strong>

                  <b className="bars">
                    <i />
                    <i />
                    <i />
                  </b>
                </div>

                <div>
                  <span>Confidence</span>
                  <strong>{d.confidence}%</strong>

                  <b className="confidence">
                    <i
                      style={{
                        width: `${d.confidence}%`,
                      }}
                    />
                  </b>
                </div>

                <div>
                  <span>Expected Range</span>
                  <strong>{d.range}</strong>

                  <Spark points={d.expected} dark />
                </div>
              </div>

              <FareChart d={d} />
            </motion.div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
