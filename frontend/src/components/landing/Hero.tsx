import { useEffect, useState } from "react";
import {
  AnimatePresence,
  motion,
  useMotionValueEvent,
  useScroll,
} from "framer-motion";
import { Menu, Plane, ArrowRight, X } from "lucide-react";
import { Link } from "react-router-dom";

import LiveCard from "./LiveCard";
import Ticker from "./Ticker";

export default function Hero() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [active, setActive] = useState("explorer");

  const { scrollY } = useScroll();

  const nav = [
    ["Index", "explorer"],
    ["Methodology", "methodology"],
    ["Signals", "signals"],
    ["Coverage", "coverage"],
  ];

  useMotionValueEvent(scrollY, "change", (y) => {
    setScrolled(y > 60);
  });

  useEffect(() => {
    const o = new IntersectionObserver(
      (es) => es.forEach((e) => e.isIntersecting && setActive(e.target.id)),
      {
        rootMargin: "-35% 0px -55%",
      },
    );

    nav.forEach(([, id]) => {
      const e = document.getElementById(id);

      if (e) {
        o.observe(e);
      }
    });

    return () => o.disconnect();
  }, []);

  return (
    <section id="start" className="hero">
      <video
        src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_091828_e240eb17-6edc-4129-ad9d-98678e3fd238.mp4"
        autoPlay
        muted
        loop
        playsInline
      />

      <div className="hero-overlay" />

      <header className={scrolled ? "navbar scrolled" : "navbar"}>
        <nav>
          <a href="#start" className="brand">
            <Plane />
            AeroIndex
          </a>

          <div className="nav-links">
            {nav.map(([l, id]) => (
              <a
                className={active === id ? "active" : ""}
                href={`#${id}`}
                key={id}
              >
                {l}
              </a>
            ))}
          </div>

          <Link to="/signup" className="nav-cta">
            Get Started
          </Link>

          <button onClick={() => setOpen(!open)}>
            {open ? <X /> : <Menu />}
          </button>
        </nav>

        {open && (
          <div className="mobile-menu">
            {nav.map(([l, id]) => (
              <a href={`#${id}`} key={id} onClick={() => setOpen(false)}>
                {l}
              </a>
            ))}
          </div>
        )}
      </header>

      <div className="hero-content">
        <div className="hero-copy">
          <p className="eyebrow">India's real-time airfare intelligence</p>

          <h1>
            <span>See fares.</span>
            <strong>Understand the market.</strong>
          </h1>

          <p>
            A real-time airfare price index tracking how flight prices move
            across India — across routes, airlines, and advance booking windows.
          </p>

          <div>
            <Link to="/signup" className="button primary">
              Get Started <ArrowRight />
            </Link>

            <a href="#methodology" className="button secondary">
              How It Works
            </a>
          </div>
        </div>

        <LiveCard />
      </div>

      <Ticker />
    </section>
  );
}
