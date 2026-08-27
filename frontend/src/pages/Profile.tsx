import {
  User,
  Mail,
  ShieldCheck,
  Database,
  Settings,
  LogOut,
} from "lucide-react";
import "./Profile.css";

export default function Profile() {
  return (
    <main className="profile-page">
      <div className="profile-container">
        {/* Breadcrumb */}
        <div className="profile-breadcrumb">
          <span>ADMINISTRATION</span>
          <span>/</span>
          <strong>PROFILE</strong>
        </div>

        {/* Header */}
        <div className="profile-header">
          <div>
            <h1>Profile</h1>
            <p>Manage your account and statistical workspace preferences.</p>
          </div>
        </div>

        <div className="profile-grid">
          {/* Profile Card */}
          <section className="profile-card profile-main-card">
            <div className="profile-card-header">
              <h2>Account Information</h2>
              <button type="button" className="profile-edit-button">
                <Settings size={14} />
                Settings
              </button>
            </div>

            <div className="profile-user">
              <div className="profile-avatar">AS</div>

              <div>
                <h3>Admin</h3>
                <p>Data workspace administrator</p>
              </div>
            </div>

            <div className="profile-info-list">
              <div className="profile-info-row">
                <div className="profile-info-icon">
                  <User size={16} />
                </div>

                <div>
                  <span>Full Name</span>
                  <strong>Admin</strong>
                </div>
              </div>

              <div className="profile-info-row">
                <div className="profile-info-icon">
                  <Mail size={16} />
                </div>

                <div>
                  <span>Email</span>
                  <strong>admin@airfareindex.gov.in</strong>
                </div>
              </div>

              <div className="profile-info-row">
                <div className="profile-info-icon">
                  <ShieldCheck size={16} />
                </div>

                <div>
                  <span>Role</span>
                  <strong>Administrator</strong>
                </div>
              </div>

              <div className="profile-info-row">
                <div className="profile-info-icon">
                  <Database size={16} />
                </div>

                <div>
                  <span>Workspace</span>
                  <strong>Statistical Workspace</strong>
                </div>
              </div>
            </div>
          </section>

          {/* Right Column */}
          <div className="profile-side">
            {/* Workspace */}
            <section className="profile-card">
              <div className="profile-card-header">
                <h2>Workspace</h2>
              </div>

              <div className="workspace-status">
                <span className="workspace-status-dot" />

                <div>
                  <strong>Workspace Active</strong>
                  <span>Secure statistical environment</span>
                </div>
              </div>

              <div className="workspace-details">
                <div>
                  <span>Workspace</span>
                  <strong>MoSPI · SIH26056</strong>
                </div>

                <div>
                  <span>Access Level</span>
                  <strong>Full Access</strong>
                </div>
              </div>
            </section>

            {/* Security */}
            <section className="profile-card">
              <div className="profile-card-header">
                <h2>Security</h2>
              </div>

              <div className="security-row">
                <ShieldCheck size={18} />

                <div>
                  <strong>Account secured</strong>
                  <span>Your workspace access is currently active.</span>
                </div>
              </div>
            </section>

            {/* Logout */}
            <button
              type="button"
              className="profile-logout-button"
              onClick={() => {
                console.log("Logout clicked");
              }}
            >
              <LogOut size={15} />
              Sign out
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
