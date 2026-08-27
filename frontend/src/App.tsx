import { Routes, Route } from "react-router-dom";

import Signup from "./pages/Signup";
import Signin from "./pages/Signin";
import Dashboard from "./pages/Dashboard";
import RoutesPage from "./pages/Routes";
import Profile from "./pages/Profile";

import DashboardLayout from "./components/DashboardLayout";

import Hero from "./components/landing/Hero";
import Explorer from "./components/landing/Explorer";
import Methodology from "./components/landing/Methodology";
import Signals from "./components/landing/Signals";
import Network from "./components/landing/Network";
import Coverage from "./components/landing/Coverage";
import CTA from "./components/landing/CTA";
import Progress from "./components/common/Progress";

export default function App() {
  return (
    <Routes>
      {/* =========================
          LANDING PAGE
      ========================== */}
      <Route
        path="/"
        element={
          <main>
            <Progress />
            <Hero />
            <Explorer />
            <Methodology />
            <Signals />
            <Network />
            <Coverage />
            <CTA />
          </main>
        }
      />

      {/* =========================
          AUTH PAGES
      ========================== */}
      <Route path="/signup" element={<Signup />} />
      <Route path="/signin" element={<Signin />} />

      {/* =========================
          DASHBOARD / APP PAGES
      ========================== */}
      <Route element={<DashboardLayout />}>
        {/* Dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />

        {/* Routes */}
        <Route path="/routes" element={<RoutesPage />} />

        {/* Profile */}
        <Route path="/profile" element={<Profile />} />
      </Route>
    </Routes>
  );
}
