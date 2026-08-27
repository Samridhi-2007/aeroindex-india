export default function Spark({
  points,
  dark = false,
}: {
  points: number[];
  dark?: boolean;
}) {
  const min = Math.min(...points);
  const max = Math.max(...points);

  const p = points
    .map(
      (v, i) =>
        `${i * (120 / (points.length - 1))},${
          38 - ((v - min) / Math.max(1, max - min)) * 28
        }`,
    )
    .join(" ");

  const last = p.split(" ");

  return (
    <svg className="spark" viewBox="0 0 120 44">
      <polyline
        points={p}
        fill="none"
        stroke={dark ? "#77A7F7" : "#3578E5"}
        strokeWidth="2"
        strokeLinecap="round"
      />

      <circle
        cx="120"
        cy={last[last.length - 1].split(",")[1]}
        r="3"
        fill="#F3A94D"
      />
    </svg>
  );
}
