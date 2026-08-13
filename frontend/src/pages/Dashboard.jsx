import { dashboardStats, latestBuild } from "../data/mockData";

function Dashboard() {
  return (
    <>
      {/* ========================================
          Dashboard Header
          ======================================== */}
      <header className="dashboard-header">
        <div>
          <h1>Dashboard</h1>
          <p>OmniSight QA overview</p>
        </div>

        <div className="environment" aria-label="Current environment: Staging">
          <span className="status-dot" aria-hidden="true" />

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

            <strong className="stat-value">{dashboardStats.totalBuilds}</strong>

            <span className="stat-meta">
              +{dashboardStats.buildsThisWeek} this week
            </span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Passed Builds</span>

            <strong className="stat-value">
              {dashboardStats.passedBuilds}
            </strong>

            <span className="stat-meta">
              {dashboardStats.successRate}% success rate
            </span>
          </article>

          <article className="stat-card">
            <span className="stat-label">UI Issues</span>

            <strong className="stat-value">{dashboardStats.uiIssues}</strong>

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

              <h3>Build {latestBuild.id}</h3>

              <p>
                {latestBuild.deployment} • {latestBuild.time}
              </p>
            </div>

            <div className="build-status">
              <span className="build-status-dot" aria-hidden="true" />

              <span>{latestBuild.status}</span>
            </div>
          </div>

          <div className="build-divider" />

          {/* ========================================
              Build Metrics
              ======================================== */}
          <div className="build-metrics">
            <div className="build-metric">
              <span>Tests</span>

              <strong>{latestBuild.tests}</strong>
            </div>

            <div className="build-metric success">
              <span>Passed</span>

              <strong>{latestBuild.passed}</strong>
            </div>

            <div className="build-metric">
              <span>Failed</span>

              <strong>{latestBuild.failed}</strong>
            </div>

            <div className="build-metric">
              <span>UI Issues</span>

              <strong>{latestBuild.issues}</strong>
            </div>
          </div>
        </article>
      </section>
    </>
  );
}

export default Dashboard;
