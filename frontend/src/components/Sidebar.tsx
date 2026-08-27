import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  TrendingUp,
  BarChart3,
  Database,
  Plane,
  Building2,
  Activity,
  LineChart,
  FileText,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

type SidebarProps = {
  collapsed: boolean;
  onToggle: () => void;
};

const menuSections = [
  {
    title: "OVERVIEW",
    items: [
      {
        label: "Dashboard",
        path: "/dashboard",
        icon: LayoutDashboard,
      },
    ],
  },
  {
    title: "INDEX",
    items: [
      {
        label: "Airfare Price Index",
        path: "/airfare-price-index",
        icon: TrendingUp,
      },
      {
        label: "CPI Comparison",
        path: "/cpi-comparison",
        icon: BarChart3,
      },
    ],
  },
  {
    title: "DATA",
    items: [
      {
        label: "Fare Data",
        path: "/fare-data",
        icon: Database,
      },
      {
        label: "Routes",
        path: "/routes",
        icon: Plane,
      },
      {
        label: "Airlines & Sources",
        path: "/airlines-sources",
        icon: Building2,
      },
    ],
  },
  {
    title: "MONITORING",
    items: [
      {
        label: "Data Collection",
        path: "/data-collection",
        icon: Database,
      },
      {
        label: "Scraping Status",
        path: "/scraping-status",
        icon: Activity,
      },
    ],
  },
  {
    title: "ANALYSIS",
    items: [
      {
        label: "Analytics",
        path: "/analytics",
        icon: LineChart,
      },
      {
        label: "Trends",
        path: "/trends",
        icon: TrendingUp,
      },
    ],
  },
  {
    title: "REPORTS",
    items: [
      {
        label: "Reports & Exports",
        path: "/reports-exports",
        icon: FileText,
      },
    ],
  },
];

export default function Sidebar({ collapsed, onToggle }: SidebarProps) {
  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      <div className="sidebar-brand">
        <div className="brand-icon">
          <Plane size={20} />
        </div>

        {!collapsed && (
          <div className="brand-text">
            <div className="brand-name">AirfareIndex</div>
            <div className="brand-subtitle">MoSPI · SIH26056</div>
          </div>
        )}
      </div>

      <button
        type="button"
        className="sidebar-toggle"
        onClick={onToggle}
        aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
      >
        {collapsed ? <ChevronRight size={15} /> : <ChevronLeft size={15} />}
      </button>

      <nav className="sidebar-menu">
        {menuSections.map((section) => (
          <div className="menu-section" key={section.title}>
            {!collapsed && <div className="section-title">{section.title}</div>}

            {section.items.map((item) => {
              const Icon = item.icon;

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `sidebar-link ${isActive ? "active" : ""}`
                  }
                  title={collapsed ? item.label : undefined}
                >
                  <span className="sidebar-icon">
                    <Icon size={16} strokeWidth={1.8} />
                  </span>

                  {!collapsed && (
                    <span className="sidebar-label">{item.label}</span>
                  )}

                  {item.label === "Dashboard" && !collapsed && (
                    <span className="status-dot" />
                  )}
                </NavLink>
              );
            })}
          </div>
        ))}
      </nav>

      <div className="sidebar-footer">
        {!collapsed ? (
          <>
            <div className="workspace-title">
              <Activity size={12} />
              Statistical workspace
            </div>

            <div className="secure-text">Secure statistical workspace</div>
          </>
        ) : (
          <Activity size={15} />
        )}
      </div>
    </aside>
  );
}
