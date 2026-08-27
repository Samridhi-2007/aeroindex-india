import { useEffect, useState } from "react";
import { useReducedMotion } from "framer-motion";

const money = (n: number) => `₹${Math.round(n).toLocaleString("en-IN")}`;

export default function Count({
  value,
  fare = false,
  suffix = "",
}: {
  value: number;
  fare?: boolean;
  suffix?: string;
}) {
  const reduced = useReducedMotion();
  const [n, setN] = useState(reduced ? value : 0);

  useEffect(() => {
    if (reduced) {
      setN(value);
      return;
    }

    const from = n;
    const start = performance.now();
    let frame = 0;

    const tick = (now: number) => {
      const p = Math.min(1, (now - start) / 650);

      setN(from + (value - from) * (1 - Math.pow(1 - p, 3)));

      if (p < 1) {
        frame = requestAnimationFrame(tick);
      }
    };

    frame = requestAnimationFrame(tick);

    return () => cancelAnimationFrame(frame);
  }, [value]);

  return (
    <>
      {fare ? money(n) : Math.round(n).toLocaleString("en-IN")}
      {suffix}
    </>
  );
}
