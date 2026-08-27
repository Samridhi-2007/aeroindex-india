import { motion } from "framer-motion";

export default function Segments({
  items,
  active,
  set,
  id,
}: {
  items: string[];
  active: string;
  set: (x: string) => void;
  id: string;
}) {
  return (
    <div className="segments">
      {items.map((x) => (
        <button key={x} onClick={() => set(x)}>
          {active === x && <motion.i layoutId={id} />}
          <span>{x}</span>
        </button>
      ))}
    </div>
  );
}
