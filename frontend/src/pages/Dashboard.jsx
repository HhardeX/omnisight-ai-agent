import Logo from "../components/Logo";

function Dashboard() {
  return (
    <div className="dashboard">
      {/* ========================================
          Sidebar
          ======================================== */}
      <aside className="sidebar">
        <Logo />

        <nav className="sidebar-nav" aria-label="Dashboard navigation">
          <button className="nav-item active" type="button">
            Dashboard
          </button>

          <button className="nav-item" type="button">
            Builds
          </button>

          <button className="nav-item" type="button">
            Issues
          </button>

          <button className="nav-item" type="button">
            Screenshots
          </button>

          <button className="nav-item" type="button">
            Pull Requests
          </button>
        </nav>
      </aside>

      {/* ========================================
          Main Dashboard
          ======================================== */}
      <main className="dashboard-main">
        {/* Dashboard Header */}
        <header className="dashboard-header">
          <div>
            <h1>Dashboard</h1>
            <p>OmniSight QA overview</p>
          </div>

          <div className="environment">
            <span className="status-dot" />
            <span>Staging</span>
          </div>
        </header>

        {/* ========================================
            Dashboard Overview
            ======================================== */}
        <section className="dashboard-content">
          <div className="section-heading">
            <div>
              <h2>Overview</h2>
              <p>Monitor your automated UI testing activity.</p>
            </div>
          </div>

          {/* ========================================
              Statistics
              ======================================== */}
          <div className="stats-grid">
            <article className="stat-card">
              <span className="stat-label">Total Builds</span>

              <strong className="stat-value">12</strong>

              <span className="stat-meta">+3 this week</span>
            </article>

            <article className="stat-card">
              <span className="stat-label">Passed Builds</span>

              <strong className="stat-value">10</strong>

              <span className="stat-meta">83% success rate</span>
            </article>

            <article className="stat-card">
              <span className="stat-label">UI Issues</span>

              <strong className="stat-value">2</strong>

              <span className="stat-meta">Needs review</span>
            </article>
          </div>

          {/* ========================================
              Latest Build
              ======================================== */}
          <article className="latest-build">
            <div className="latest-build-header">
              <div>
                <span className="latest-build-label">Latest Build</span>

                <h3>Build #124</h3>

                <p>Staging deployment • 2 minutes ago</p>
              </div>

              <div className="build-status">
                <span className="build-status-dot" />
                <span>Passed</span>
              </div>
            </div>

            <div className="build-divider" />

            {/* Build Metrics */}
            <div className="build-metrics">
              <div className="build-metric">
                <span>Tests</span>
                <strong>18</strong>
              </div>

              <div className="build-metric success">
                <span>Passed</span>
                <strong>18</strong>
              </div>

              <div className="build-metric">
                <span>Failed</span>
                <strong>0</strong>
              </div>

              <div className="build-metric">
                <span>UI Issues</span>
                <strong>0</strong>
              </div>
            </div>
          </article>
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
