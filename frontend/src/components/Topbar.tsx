import { Search, Bell, ChevronDown } from "lucide-react";
import { NavLink, useLocation } from "react-router-dom";
import "./Topbar.css";

export default function Topbar() {
  const location = useLocation();

  const pageInfo: Record<string, { section: string; title: string }> = {
    "/dashboard": {
      section: "Analytics",
      title: "Dashboard",
    },
    "/analytics": {
      section: "Analysis",
      title: "Analytics",
    },
    "/trends": {
      section: "Analysis",
      title: "Trends",
    },
    "/routes": {
      section: "Data",
      title: "Routes",
    },
    "/fare-data": {
      section: "Data",
      title: "Fare Data",
    },
    "/airlines": {
      section: "Data",
      title: "Airlines & Sources",
    },
    "/scraping-status": {
      section: "Monitoring",
      title: "Scraping Status",
    },
    "/cpi-comparison": {
      section: "Index",
      title: "CPI Comparison",
    },
    "/airfare-index": {
      section: "Index",
      title: "Airfare Price Index",
    },
    "/profile": {
      section: "Account",
      title: "Profile",
    },
  };

  const currentPage = pageInfo[location.pathname] || {
    section: "Analytics",
    title: "Dashboard",
  };

  return (
    <header className="topbar">
      <div className="topbar-left">
        <div className="topbar-breadcrumb">
          <span>{currentPage.section}</span>

          <span className="breadcrumb-separator">/</span>

          <strong>{currentPage.title}</strong>
        </div>
      </div>

      <div className="topbar-right">
        {/* Search */}
        <div className="topbar-search">
          <Search size={15} />

          <input type="text" placeholder="Search routes, sources..." />
        </div>

        {/* Notifications */}
        <button
          type="button"
          className="notification-button"
          aria-label="Notifications"
        >
          <Bell size={17} />
          <span className="notification-dot" />
        </button>

        {/* Profile */}
        <NavLink
          to="/profile"
          className={({ isActive }) =>
            `topbar-user ${isActive ? "profile-active" : ""}`
          }
          aria-label="Open profile"
        >
          <div className="user-avatar">AS</div>

          <div className="user-info">
            <strong>Admin</strong>
            <span>Data workspace</span>
          </div>

          <ChevronDown size={14} />
        </NavLink>
      </div>
    </header>
  );
}
