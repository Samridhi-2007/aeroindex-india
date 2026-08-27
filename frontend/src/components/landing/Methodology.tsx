import { BarChart3, Database, ShieldCheck, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

import Intro from "../common/Intro";
import Reveal from "../common/Reveal";

const stages = [
  [
    Database,
    "Data Collection",
    "Airlines and OTAs are tracked across major Indian city pairs.",
  ],
  [
    ShieldCheck,
    "Normalization",
    "Fare quotes are cleaned and standardized for true comparability.",
  ],
  [
    BarChart3,
    "Index Computation",
    "Daily, weekly, and monthly signals are aggregated into APIx.",
  ],
  [
    Sparkles,
    "Insight Layer",
    "Trends, anomalies, volatility, and booking-window movement surface.",
  ],
];

export default function Methodology() {
  return (
    <section id="methodology" className="section methodology">
      <div className="wrap">
        <Intro eyebrow="Methodology" title="How the Index Works">
          A disciplined intelligence layer turns fragmented airfare observations
          into one comparable market signal.
        </Intro>

        <div className="pipeline">
          <motion.div
            className="pipeline-line"
            initial={{ scaleX: 0 }}
            whileInView={{ scaleX: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 1.2 }}
          />

          {stages.map(([Icon, title, text], i) => (
            <Reveal key={title as string} delay={i * 0.1}>
              <article>
                <div>
                  <span>
                    <Icon />
                    <i />
                  </span>

                  <b>0{i + 1}</b>
                </div>

                <h3>{title as string}</h3>
                <p>{text as string}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
