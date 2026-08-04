import Dashboard from "./components/Dashboard";

export default function App() {
  return (
    <div>
      <header className="app-header">
        <div className="header-content">
          <div className="header-badge">
            <span className="header-badge-dot"></span>
            Real-time Insights
          </div>
          <h1>Job Market Analytics Platform</h1>
          <p>
            Explore in-demand skills, top hiring locations, AI career advisory, and gap analysis for tech professionals.
          </p>
        </div>
      </header>
      <main className="app-container">
        <Dashboard />
      </main>
    </div>
  );
}
