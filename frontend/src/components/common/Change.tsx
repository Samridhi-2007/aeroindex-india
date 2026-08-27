import { ArrowDownRight, ArrowUpRight } from "lucide-react";

export default function Change({
  value,
  light = false,
}: {
  value: number;
  light?: boolean;
}) {
  const up = value >= 0;

  return (
    <span className={`change ${up ? "up" : "down"} ${light ? "light" : ""}`}>
      {up ? <ArrowUpRight /> : <ArrowDownRight />}
      {Math.abs(value)}%
    </span>
  );
}
