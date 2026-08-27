import { ArrowRight, LockKeyhole, Plane, TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Signin() {
  return (
    <main className="auth-page">
      <header className="auth-navbar">
        <Link to="/" className="auth-logo">
          <span className="auth-logo-icon">
            <Plane />
          </span>
          <span>AeroIndex</span>
        </Link>

        <div className="auth-nav-right">
          <span>New to AeroIndex?</span>
          <Link to="/signup" className="auth-nav-button">
            Get Started
          </Link>
        </div>
      </header>

      <div className="auth-main">
        {/* LEFT */}
        <motion.section
          className="auth-visual signin-visual"
          initial={{ opacity: 0, x: -25 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7 }}
        >
          <div className="auth-visual-grid" />

          <div className="auth-visual-content">
            <p className="auth-kicker">WELCOME BACK</p>

            <h1>
              Your market view.
              <span>Always in motion.</span>
            </h1>

            <p className="auth-visual-description">
              Pick up where you left off and continue monitoring India's airfare
              market.
            </p>

            <div className="signin-preview">
              <div className="preview-top">
                <div>
                  <span>MARKET PULSE</span>
                  <strong>108.4</strong>
                </div>

                <div className="preview-badge">
                  <i />
                  Stable
                </div>
              </div>

              <div className="preview-routes">
                <div>
                  <span>DEL → BOM</span>
                  <strong>₹5,842</strong>
                  <b>↑ 6.8%</b>
                </div>

                <div>
                  <span>DEL → BLR</span>
                  <strong>₹6,930</strong>
                  <em>↓ 2.1%</em>
                </div>

                <div>
                  <span>BOM → BLR</span>
                  <strong>₹4,910</strong>
                  <b>↑ 1.7%</b>
                </div>
              </div>
            </div>

            <div className="auth-security-points">
              <div>
                <span>01</span>
                <p>Monitor route-level fare movement</p>
              </div>

              <div>
                <span>02</span>
                <p>Identify booking-window changes</p>
              </div>

              <div>
                <span>03</span>
                <p>Follow market signals in real time</p>
              </div>
            </div>
          </div>

          <div className="auth-coordinate">SYSTEM / SECURE · APIx / ONLINE</div>
        </motion.section>

        {/* RIGHT */}
        <motion.section
          className="auth-form-section signin-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.1 }}
        >
          <div className="auth-form-card signin-card">
            <div className="auth-form-heading">
              <div className="signin-icon">
                <LockKeyhole />
              </div>

              <p>SECURE ACCESS</p>

              <h2>Welcome back</h2>

              <span>
                Sign in to access your AeroIndex intelligence dashboard.
              </span>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
              }}
            >
              <label className="auth-field">
                <span>EMAIL ADDRESS</span>
                <input type="email" placeholder="you@example.com" />
              </label>

              <label className="auth-field">
                <div className="password-label">
                  <span>PASSWORD</span>

                  <button type="button">Forgot password?</button>
                </div>

                <input type="password" placeholder="Enter your password" />
              </label>

              <label className="auth-checkbox remember">
                <input type="checkbox" />
                <span>Keep me signed in</span>
              </label>

              <button type="submit" className="auth-submit">
                Sign In
                <ArrowRight />
              </button>
            </form>

            <div className="auth-or">
              <span />
              <small>OR</small>
              <span />
            </div>

            <div className="auth-signin-text">
              Don't have an account?
              <Link to="/signup"> Create one</Link>
            </div>

            <div className="auth-security">
              <TrendingUp />
              <span>Secure access to your market intelligence.</span>
            </div>
          </div>

          <p className="auth-copyright">
            © 2026 AeroIndex India · Airfare intelligence
          </p>
        </motion.section>
      </div>
    </main>
  );
}
