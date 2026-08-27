import { motion } from "framer-motion";
import type { ReactNode } from "react";

const reveal = {
  initial: {
    opacity: 0,
    y: 20,
  },
  whileInView: {
    opacity: 1,
    y: 0,
  },
  viewport: {
    once: true,
    amount: 0.18,
  },
  transition: {
    duration: 0.65,
    ease: [0.22, 1, 0.36, 1],
  },
};

export default function Reveal({
  children,
  className = "",
  delay = 0,
}: {
  children: ReactNode;
  className?: string;
  delay?: number;
}) {
  return (
    <motion.div
      className={className}
      {...reveal}
      transition={{
        ...reveal.transition,
        delay,
      }}
    >
      {children}
    </motion.div>
  );
}
