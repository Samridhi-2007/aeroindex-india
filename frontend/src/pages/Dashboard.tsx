import {
  RefreshCw,
  Activity,
  Database,
  Route as RouteIcon,
  TrendingUp,
  ChevronRight,
} from "lucide-react";

import {
  dashboardStats,
  trendData,
  topRoutes,
  collectionStatus,
} from "../data/dashboardData";
import "./Dashboard.css";
type StatType = "blue" | "gray" | "green" | "orange";

type Stat = {
  title: string;
  value: string;
  change: string;
  period: string;
  type: StatType;
};

type TrendItem = {
  month: string;
  value: number;
};

type RouteItem = {
  rank: string;
  route: string;
  city: string;
  fare: string;
  movement: string;
  observations: string;
};

type CollectionItem = {
  name: string;
  type: string;
  records: string;
  status: "Active" | "Warning" | "Inactive";
  initial: string;
};

const typedStats = dashboardStats as Stat[];
const typedTrendData = trendData as TrendItem[];
const typedTopRoutes = topRoutes as RouteItem[];
const typedCollectionStatus = collectionStatus as CollectionItem[];

function StatCard({ stat }: { stat: Stat }) {
  const icons = {
    blue: Activity,
    gray: TrendingUp,
    green: RouteIcon,
    orange: Database,
  };

  const Icon = icons[stat.type];

  return (
    <div className="stat-card">
      <div className={`stat-icon ${stat.type}`}>
        <Icon size={17} />
      </div>

      <div className="stat-title">{stat.title}</div>

      <div className="stat-value">{stat.value}</div>

      <div className="stat-bottom">
        <span className="stat-change">{stat.change}</span>

        <span className="stat-period">{stat.period}</span>
      </div>
    </div>
  );
}

function DemoBanner() {
  return (
    <div className="demo-banner">
      <div className="demo-left">
        <div className="demo-icon">
          <Database size={17} />
        </div>

        <div>
          <div className="demo-title">Backend connection unavailable</div>

          <div className="demo-description">
            Showing clearly labeled demo data while the API service is being
            connected.
          </div>
        </div>
      </div>

      <div className="demo-label">DEMO MODE</div>
    </div>
  );
}

function TrendChart() {
  const max = 132;
  const min = 108;

  const points = typedTrendData
    .map((item, index) => {
      const x = (index / (typedTrendData.length - 1)) * 100;

      const y = 100 - ((item.value - min) / (max - min)) * 100;

      return `${x},${y}`;
    })
    .join(" ");

  return (
    <div className="trend-card">
      <div className="section-header">
        <div>
          <h3>Airfare price index trend</h3>

          <p>Weighted domestic index · Base period: configured by backend</p>
        </div>

        <div className="range-buttons">
          <button>7D</button>
          <button className="active">30D</button>
          <button>3M</button>
          <button>6M</button>
          <button>1Y</button>
        </div>
      </div>

      <div className="chart-area">
        <div className="y-axis">
          <span>132</span>
          <span>126</span>
          <span>120</span>
          <span>114</span>
          <span>108</span>
        </div>

        <div className="dashboard-chart">
          {[1, 2, 3, 4, 5].map((line) => (
            <div key={line} className={`grid-line line-${line}`} />
          ))}

          <svg
            viewBox="0 0 100 100"
            preserveAspectRatio="none"
            className="chart-svg"
          >
            <polyline
              points={points}
              fill="none"
              stroke="#2563eb"
              strokeWidth="2"
              vectorEffect="non-scaling-stroke"
            />

            {typedTrendData.map((item, index) => {
              const x = (index / (typedTrendData.length - 1)) * 100;

              const y = 100 - ((item.value - min) / (max - min)) * 100;

              return (
                <circle
                  key={item.month}
                  cx={`${x}%`}
                  cy={`${y}%`}
                  r="2.1"
                  fill="#2563eb"
                />
              );
            })}
          </svg>

          <div className="x-axis">
            {typedTrendData.map((item) => (
              <span key={item.month}>{item.month}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="chart-footer">
        <div className="legend">
          <span className="legend-dot" />
          Index value
        </div>

        <div>
          Latest observation <strong>128.42</strong>
        </div>
      </div>
    </div>
  );
}

function CoverageSnapshot() {
  return (
    <div className="coverage-card">
      <h3>Coverage snapshot</h3>

      <div className="coverage-number">86</div>

      <div className="coverage-label">active domestic routes</div>

      <div className="coverage-progress">
        <div />
      </div>

      <div className="coverage-row">
        <span>Routes covered</span>
        <strong>86 / 110</strong>
      </div>

      <div className="coverage-row">
        <span>Sources reporting</span>
        <strong>4 / 5</strong>
      </div>

      <div className="coverage-row">
        <span>Collection success</span>
        <strong className="success">97.8%</strong>
      </div>

      <button className="monitor-link">
        View collection monitor
        <ChevronRight size={14} />
      </button>
    </div>
  );
}

function TopRoutes() {
  return (
    <div className="routes-card">
      <div className="section-header">
        <h3>Top routes by fare movement</h3>

        <button className="view-all">
          View all
          <ChevronRight size={14} />
        </button>
      </div>

      <div>
        {typedTopRoutes.map((route) => (
          <div className="route-row" key={route.rank}>
            <span className="route-rank">{route.rank}</span>

            <div className="route-info">
              <strong>{route.route}</strong>

              <span>{route.city}</span>
            </div>

            <strong className="route-fare">{route.fare}</strong>

            <span
              className={`movement ${
                route.movement.startsWith("-") ? "negative" : ""
              }`}
            >
              {route.movement}
            </span>

            <span className="observations">{route.observations}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function CollectionStatus() {
  return (
    <div className="collection-card">
      <div className="section-header">
        <h3>Collection status</h3>

        <button className="view-all">
          Monitor
          <ChevronRight size={14} />
        </button>
      </div>

      {typedCollectionStatus.map((item) => (
        <div className="collection-row" key={item.name}>
          <div className="collection-initial">{item.initial}</div>

          <div className="collection-info">
            <strong>{item.name}</strong>

            <span>
              {item.type} · {item.records}
            </span>
          </div>

          <div className={`collection-status ${item.status.toLowerCase()}`}>
            <span />
            {item.status}
          </div>
        </div>
      ))}
    </div>
  );
}

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <div className="breadcrumb">
            ANALYTICS <span>/</span> DASHBOARD
          </div>

          <h1>Airfare Price Index</h1>

          <p>
            A consolidated view of domestic airfare movement, collection
            coverage and data quality.
          </p>
        </div>

        <button className="refresh-button">
          <RefreshCw size={15} />
          Refresh data
        </button>
      </div>

      <DemoBanner />

      <div className="stats-grid">
        {typedStats.map((stat) => (
          <StatCard key={stat.title} stat={stat} />
        ))}
      </div>

      <div className="dashboard-grid">
        <TrendChart />
        <CoverageSnapshot />
      </div>

      <div className="dashboard-grid bottom-grid">
        <TopRoutes />
        <CollectionStatus />
      </div>

      <footer className="dashboard-footer">
        <span>Airfare Price Index · SIH26056</span>

        <span>● Demo data layer active · Data governance workspace</span>
      </footer>
    </div>
  );
}
