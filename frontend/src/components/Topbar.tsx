import { Search, Bell, ChevronDown } from "lucide-react";

export default function Topbar() {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <div className="topbar-breadcrumb">
          <span>Analytics</span>
          <span className="breadcrumb-separator">/</span>
          <strong>Dashboard</strong>
        </div>
      </div>

      <div className="topbar-right">
        <div className="topbar-search">
          <Search size={15} />

          <input type="text" placeholder="Search routes, sources..." />
        </div>

        <button
          type="button"
          className="notification-button"
          aria-label="Notifications"
        >
          <Bell size={17} />
          <span className="notification-dot" />
        </button>

        <div className="topbar-user">
          <div className="user-avatar">AS</div>

          <div className="user-info">
            <strong>Admin</strong>
            <span>Data workspace</span>
          </div>

          <ChevronDown size={14} />
        </div>
      </div>
    </header>
  );
}
