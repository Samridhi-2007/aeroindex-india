import { useMemo, useState } from "react";
import {
  X,
  Plane,
  SlidersHorizontal,
  ChevronRight,
  TrendingUp,
  TrendingDown,
  Activity,
  ShieldCheck,
} from "lucide-react";

import "./Routes.css";
import {
  routesData,
  type RouteData,
  type RouteStatus,
  type BookingWindow,
} from "../data/routesData";

const formatFare = (value: number) => `₹${value.toLocaleString("en-IN")}`;

const formatPercent = (value: number) =>
  `${value > 0 ? "+" : ""}${value.toFixed(1)}%`;

const statusClass = (status: RouteStatus) => {
  if (status === "Active") return "active";
  if (status === "Watch") return "watch";
  return "low";
};

const bookingWindows: BookingWindow[] = ["T+1", "T+7", "T+15", "T+30", "T+45"];

export default function RoutesPage() {
  const [origin, setOrigin] = useState("All");
  const [destination, setDestination] = useState("All");
  const [carrier, setCarrier] = useState("All");
  const [bookingWindow, setBookingWindow] = useState("All");

  const [selectedRoute, setSelectedRoute] = useState<RouteData | null>(null);

  const origins = useMemo(
    () => Array.from(new Set(routesData.map((route) => route.origin.code))),
    [],
  );

  const destinations = useMemo(
    () =>
      Array.from(new Set(routesData.map((route) => route.destination.code))),
    [],
  );

  const carriers = useMemo(
    () => Array.from(new Set(routesData.map((route) => route.carrier))),
    [],
  );

  const filteredRoutes = useMemo(() => {
    return routesData.filter((route) => {
      const originMatch = origin === "All" || route.origin.code === origin;

      const destinationMatch =
        destination === "All" || route.destination.code === destination;

      const carrierMatch = carrier === "All" || route.carrier === carrier;

      const bookingMatch =
        bookingWindow === "All" || route.bookingWindow === bookingWindow;

      return originMatch && destinationMatch && carrierMatch && bookingMatch;
    });
  }, [origin, destination, carrier, bookingWindow]);

  const clearFilters = () => {
    setOrigin("All");
    setDestination("All");
    setCarrier("All");
    setBookingWindow("All");
  };

  return (
    <main className="routes-page">
      <div className="routes-container">
        {/* PAGE HEADER */}
        <header className="routes-header">
          <div>
            <div className="routes-breadcrumb">
              DATA <span>/</span> ROUTES
            </div>

            <h1>Routes</h1>

            <p>
              Monitor route-level airfare movement, price index contribution and
              confidence across the domestic network.
            </p>
          </div>

          <div className="routes-header-meta">
            <div className="routes-live-dot" />
            <span>Demo data layer active</span>
          </div>
        </header>

        {/* FILTER CARD */}
        <section className="routes-filter-card">
          <div className="routes-filter-heading">
            <div>
              <SlidersHorizontal size={17} />
              <span>Route Filters</span>
            </div>

            <button className="routes-clear" onClick={clearFilters}>
              Clear filters
            </button>
          </div>

          <div className="routes-filters">
            <FilterSelect
              label="Origin"
              value={origin}
              options={origins}
              onChange={setOrigin}
            />

            <FilterSelect
              label="Destination"
              value={destination}
              options={destinations}
              onChange={setDestination}
            />

            <FilterSelect
              label="Carrier"
              value={carrier}
              options={carriers}
              onChange={setCarrier}
            />

            <FilterSelect
              label="Booking Window"
              value={bookingWindow}
              options={bookingWindows}
              onChange={setBookingWindow}
            />
          </div>
        </section>

        {/* TABLE */}
        <section className="routes-table-card">
          <div className="routes-table-top">
            <div>
              <h2>Route Performance</h2>
              <p>
                {filteredRoutes.length} route
                {filteredRoutes.length !== 1 ? "s" : ""} available
              </p>
            </div>

            <div className="routes-table-note">
              Select a route to view detailed index information
            </div>
          </div>

          <div className="routes-table-wrapper">
            <table className="routes-table">
              <thead>
                <tr>
                  <th>Route</th>
                  <th>Weight</th>
                  <th>Average Fare</th>
                  <th>APIx / Price Index</th>
                  <th>Weekly Change</th>
                  <th>Confidence</th>
                  <th>Status</th>
                  <th />
                </tr>
              </thead>

              <tbody>
                {filteredRoutes.map((route) => (
                  <tr
                    key={route.id}
                    onClick={() => setSelectedRoute(route)}
                    className="route-row"
                  >
                    <td>
                      <div className="route-cell">
                        <div className="route-icon">
                          <Plane size={15} />
                        </div>

                        <div>
                          <strong>
                            {route.origin.code}
                            <span>→</span>
                            {route.destination.code}
                          </strong>

                          <small>
                            {route.origin.name} → {route.destination.name}
                          </small>
                        </div>
                      </div>
                    </td>

                    <td>
                      <span className="route-number">
                        {route.weight.toFixed(1)}%
                      </span>
                    </td>

                    <td>
                      <strong className="fare-value">
                        {formatFare(route.averageFare)}
                      </strong>
                    </td>

                    <td>
                      <div className="apix-cell">
                        <strong>{route.apix.toFixed(1)}</strong>
                        <span>Index</span>
                      </div>
                    </td>

                    <td>
                      <div
                        className={`weekly-change ${
                          route.weeklyChange >= 0 ? "positive" : "negative"
                        }`}
                      >
                        {route.weeklyChange >= 0 ? (
                          <TrendingUp size={14} />
                        ) : (
                          <TrendingDown size={14} />
                        )}

                        {formatPercent(route.weeklyChange)}
                      </div>
                    </td>

                    <td>
                      <div className="confidence-cell">
                        <div className="confidence-bar">
                          <span
                            style={{
                              width: `${route.confidence}%`,
                            }}
                          />
                        </div>

                        <strong>{route.confidence}%</strong>
                      </div>
                    </td>

                    <td>
                      <span
                        className={`route-status ${statusClass(route.status)}`}
                      >
                        <i />
                        {route.status}
                      </span>
                    </td>

                    <td>
                      <ChevronRight size={17} className="route-arrow" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {filteredRoutes.length === 0 && (
              <div className="routes-empty">
                <Activity size={25} />
                <strong>No routes found</strong>
                <span>Try changing or clearing your filters.</span>
              </div>
            )}
          </div>
        </section>

        {/* FOOTER */}
        <footer className="routes-footer">
          <span>AeroIndex India · SIH26056</span>

          <span>
            <i />
            Route intelligence workspace
          </span>
        </footer>
      </div>

      {/* DRAWER */}
      {selectedRoute && (
        <RouteDrawer
          route={selectedRoute}
          onClose={() => setSelectedRoute(null)}
        />
      )}
    </main>
  );
}

/* =====================================================
   FILTER SELECT
===================================================== */

function FilterSelect({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string;
  options: readonly string[];
  onChange: (value: string) => void;
}) {
  return (
    <label className="route-filter">
      <span>{label}</span>

      <select value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="All">All</option>

        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

/* =====================================================
   ROUTE DRAWER
===================================================== */

function RouteDrawer({
  route,
  onClose,
}: {
  route: RouteData;
  onClose: () => void;
}) {
  return (
    <div className="route-drawer-overlay" onClick={onClose}>
      <aside
        className="route-drawer"
        onClick={(event) => event.stopPropagation()}
      >
        {/* DRAWER HEADER */}
        <div className="drawer-header">
          <div>
            <div className="drawer-eyebrow">ROUTE DETAIL</div>

            <h2>
              {route.origin.code}
              <span>→</span>
              {route.destination.code}
            </h2>

            <p>
              {route.origin.name} → {route.destination.name}
            </p>
          </div>

          <button
            className="drawer-close"
            onClick={onClose}
            aria-label="Close route details"
          >
            <X size={18} />
          </button>
        </div>

        {/* CURRENT FARE */}
        <section className="drawer-current-fare">
          <span>Current average fare</span>

          <strong>{formatFare(route.averageFare)}</strong>

          <div
            className={`drawer-change ${
              route.weeklyChange >= 0 ? "positive" : "negative"
            }`}
          >
            {route.weeklyChange >= 0 ? (
              <TrendingUp size={14} />
            ) : (
              <TrendingDown size={14} />
            )}

            {formatPercent(route.weeklyChange)}
            <span>vs last week</span>
          </div>
        </section>

        {/* METRICS */}
        <section className="drawer-section">
          <div className="drawer-section-title">
            <span>Index Metrics</span>
          </div>

          <div className="drawer-metrics">
            <Metric label="Base fare" value={formatFare(route.baseFare)} />

            <Metric
              label="Inflation"
              value={`+${route.inflationPercent.toFixed(1)}%`}
            />

            <Metric
              label="Route weight"
              value={`${route.weight.toFixed(1)}%`}
            />

            <Metric
              label="APIx contribution"
              value={route.apixContribution.toFixed(1)}
            />

            <Metric label="APIx / Price Index" value={route.apix.toFixed(1)} />

            <Metric
              label="Confidence score"
              value={`${route.confidence}%`}
              icon={<ShieldCheck size={14} />}
            />
          </div>
        </section>

        {/* ROUTE INFO */}
        <section className="drawer-section">
          <div className="drawer-section-title">
            <span>Route Configuration</span>
          </div>

          <div className="drawer-config">
            <div>
              <span>Carrier</span>
              <strong>{route.carrier}</strong>
            </div>

            <div>
              <span>Booking window</span>
              <strong>{route.bookingWindow}</strong>
            </div>

            <div>
              <span>Status</span>
              <strong className={`drawer-status ${statusClass(route.status)}`}>
                <i />
                {route.status}
              </strong>
            </div>
          </div>
        </section>

        {/* FORECAST */}
        <section className="drawer-section">
          <div className="drawer-section-title">
            <span>Forecast Summary</span>
            <small>Average fare outlook</small>
          </div>

          <div className="forecast-list">
            {route.forecast.map((forecast) => (
              <div className="forecast-row" key={forecast.horizon}>
                <div className="forecast-horizon">{forecast.horizon}</div>

                <div className="forecast-fare">
                  {formatFare(forecast.averageFare)}
                </div>

                <div
                  className={`forecast-change ${
                    forecast.changePercent >= 0 ? "positive" : "negative"
                  }`}
                >
                  {forecast.changePercent >= 0 ? "+" : ""}
                  {forecast.changePercent.toFixed(1)}%
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* DATA NOTE */}
        <div className="drawer-note">
          <Activity size={15} />

          <span>
            Day 1 mock data. This structure is ready to consume route-level API
            responses later.
          </span>
        </div>
      </aside>
    </div>
  );
}

/* =====================================================
   METRIC
===================================================== */

function Metric({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
  icon?: React.ReactNode;
}) {
  return (
    <div className="drawer-metric">
      <span>{label}</span>

      <strong>
        {icon}
        {value}
      </strong>
    </div>
  );
}
