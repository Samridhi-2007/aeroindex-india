import { motion, useScroll, useSpring } from "framer-motion";

export default function Progress() {
  const { scrollYProgress } = useScroll();

  const x = useSpring(scrollYProgress, {
    stiffness: 120,
    damping: 30,
  });

  return <motion.div className="scroll-progress" style={{ scaleX: x }} />;
}
