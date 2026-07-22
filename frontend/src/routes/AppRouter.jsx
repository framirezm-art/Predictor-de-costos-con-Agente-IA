import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import Forecast from "../pages/Forecast";
import Chat from "../pages/Chat";

export default function AppRouter() {
  return (
    <div className="app-shell">
      <nav className="sidebar">
        <h2 className="brand">Cost Forecast</h2>
        <NavLink to="/" end className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
          Dashboard
        </NavLink>
        <NavLink to="/forecast" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
          Pronóstico
        </NavLink>
        <NavLink to="/chat" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
          Chat
        </NavLink>
      </nav>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/forecast" element={<Forecast />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </main>
    </div>
  );
}
