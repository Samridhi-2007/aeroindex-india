import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

import Change from "../common/Change";
import Count from "../common/Count";
import Spark from "../common/Spark";

import { routes } from "../../data/landingData";

export default function LiveCard() {
  const [a, setA] = useState(0);
  const d = routes[a];

  useEffect(() => {
    const id = setInterval(() => {
      setA((v) => (v + 1) % routes.length);
    }, 4400);

    return () => clearInterval(id);
  }, []);

  return (
    <aside className="hero-card">
      <div className="card-grid" />

      <div className="hero-card-head">
        <div>
          <p className="technical">LIVE INTELLIGENCE</p>

          <div>
            <strong>108.4</strong>
            <Change value={3.2} />
          </div>

          <span>India APIx</span>
        </div>

        <span className="live-pill">
          <i />
          Live
        </span>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={d.id}
          className="hero-route"
          initial={{
            opacity: 0,
            y: 6,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          exit={{
            opacity: 0,
            y: -5,
          }}
        >
          <div>
            <span>
              {d.from} → {d.to}
            </span>

            <strong>
              <Count value={d.fare} fare />
            </strong>
          </div>

          <Change value={d.change} />

          <Spark points={d.points} />
        </motion.div>
      </AnimatePresence>

      <div className="hero-card-foot">
        <span>WINDOW / T+07</span>
        <span>SYNC / 02M</span>
      </div>
    </aside>
  );
}
