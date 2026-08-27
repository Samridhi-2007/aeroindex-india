import { ArrowRight, Plane } from "lucide-react";

export default function CTA() {
  return (
    <section className="final">
      <div className="cta">
        <div className="cta-grid" />

        <div className="orbit a" />
        <div className="orbit b" />

        <div>
          <p className="eyebrow">The market, made visible</p>

          <h2>Ready to explore India's airfare movement in real time?</h2>

          <section>
            <a href="/dashboard" className="button white">
              Launch Dashboard <ArrowRight />
            </a>

            <a href="#methodology" className="button outline">
              View Methodology
            </a>
          </section>
        </div>
      </div>

      <footer>
        <span>
          <Plane />
          AeroIndex India
        </span>

        <p>Airfare intelligence for a more transparent market.</p>

        <small>© 2026 AeroIndex</small>
      </footer>
    </section>
  );
}
