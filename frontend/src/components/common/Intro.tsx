import Reveal from "./Reveal";

export default function Intro({
  eyebrow,
  title,
  children,
  light = false,
}: {
  eyebrow: string;
  title: string;
  children: string;
  light?: boolean;
}) {
  return (
    <Reveal className={`intro ${light ? "light" : ""}`}>
      <p className="eyebrow">{eyebrow}</p>
      <h2>{title}</h2>
      <p>{children}</p>
    </Reveal>
  );
}
