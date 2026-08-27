import { ArrowRight, CheckCircle2, Plane, TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Signup() {
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
          <span>Already have an account?</span>
          <Link to="/signin" className="auth-nav-button">
            Sign In
          </Link>
        </div>
      </header>

      <div className="auth-main">
        {/* LEFT SIDE */}
        <motion.section
          className="auth-visual"
          initial={{ opacity: 0, x: -25 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7 }}
        >
          <div className="auth-visual-grid" />

          <div className="auth-visual-content">
            <p className="auth-kicker">INDIA'S AIRFARE INTELLIGENCE</p>

            <h1>
              Understand the market.
              <span>Travel smarter.</span>
            </h1>

            <p className="auth-visual-description">
              Track airfare movements, route trends, booking windows and market
              signals across India.
            </p>

            <div className="auth-stat-card">
              <div className="auth-stat-header">
                <div>
                  <span>LIVE APIx</span>
                  <strong>108.4</strong>
                </div>

                <span className="auth-live">
                  <i />
                  LIVE
                </span>
              </div>

              <div className="auth-chart">
                <svg viewBox="0 0 500 150" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="authArea" x1="0" y1="0" x2="0" y2="1">
                      <stop
                        offset="0%"
                        stopColor="#3578E5"
                        stopOpacity="0.25"
                      />
                      <stop offset="100%" stopColor="#3578E5" stopOpacity="0" />
                    </linearGradient>
                  </defs>

                  <path
                    d="M0 118 C45 108 55 105 95 112 S150 92 180 98 S235 65 265 78 S315 55 345 68 S405 40 430 51 S475 30 500 35 L500 150 L0 150 Z"
                    fill="url(#authArea)"
                  />

                  <path
                    d="M0 118 C45 108 55 105 95 112 S150 92 180 98 S235 65 265 78 S315 55 345 68 S405 40 430 51 S475 30 500 35"
                    fill="none"
                    stroke="#3578E5"
                    strokeWidth="3"
                  />

                  <circle cx="500" cy="35" r="5" fill="#F3A94D" />
                </svg>
              </div>

              <div className="auth-stat-footer">
                <span>DEL → BOM</span>
                <strong>₹5,842</strong>
                <b>↑ 6.8%</b>
              </div>
            </div>

            <div className="auth-benefits">
              <div>
                <CheckCircle2 />
                <span>Real-time airfare signals</span>
              </div>

              <div>
                <CheckCircle2 />
                <span>Booking-window intelligence</span>
              </div>

              <div>
                <CheckCircle2 />
                <span>Route-level market trends</span>
              </div>
            </div>
          </div>

          <div className="auth-coordinate">
            COORD / IN-AIRSPACE · DATA / LIVE
          </div>
        </motion.section>

        {/* RIGHT SIDE */}
        <motion.section
          className="auth-form-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.1 }}
        >
          <div className="auth-form-card">
            <div className="auth-form-heading">
              <p>GET STARTED</p>

              <h2>Create your account</h2>

              <span>
                Join AeroIndex and start exploring India's airfare intelligence.
              </span>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
              }}
            >
              <div className="auth-field-row">
                <label className="auth-field">
                  <span>FIRST NAME</span>
                  <input type="text" placeholder="Samridhi" />
                </label>

                <label className="auth-field">
                  <span>LAST NAME</span>
                  <input type="text" placeholder="Prakash" />
                </label>
              </div>

              <label className="auth-field">
                <span>EMAIL ADDRESS</span>
                <input type="email" placeholder="you@example.com" />
              </label>

              <label className="auth-field">
                <span>PASSWORD</span>
                <input type="password" placeholder="Create a password" />
              </label>

              <label className="auth-field">
                <span>CONFIRM PASSWORD</span>
                <input type="password" placeholder="Confirm your password" />
              </label>

              <label className="auth-checkbox">
                <input type="checkbox" />
                <span>
                  I agree to the <a href="#terms">Terms of Service</a> and{" "}
                  <a href="#privacy">Privacy Policy</a>.
                </span>
              </label>

              <button type="submit" className="auth-submit">
                Create Account
                <ArrowRight />
              </button>
            </form>

            <div className="auth-or">
              <span />
              <small>OR</small>
              <span />
            </div>

            <div className="auth-signin-text">
              Already have an account?
              <Link to="/signin"> Sign in</Link>
            </div>

            <div className="auth-security">
              <TrendingUp />
              <span>Your data stays secure and private.</span>
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
