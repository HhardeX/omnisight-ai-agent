import { useEffect, useState } from "react";
import { dashboardStats, latestBuild } from "../data/mockData";
import { getDashboardData } from "../services/dashboardService";

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadDashboard() {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getDashboardData();

        if (isMounted) {
          setDashboardData(data);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      isMounted = false;
    };
  }, []);

  const stats = dashboardData?.stats || dashboardStats;
  const build = dashboardData?.latestBuild || latestBuild;

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

        <div
          className="environment"
          aria-label="Current environment: Staging"
        >
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
            API Status
            ======================================== */}
        {isLoading && (
          <p role="status">
            Loading dashboard data...
          </p>
        )}

        {error && (
          <p role="alert">
            Backend unavailable. Showing mock dashboard data.
          </p>
        )}

        {/* ========================================
            Statistics
            ======================================== */}
        <div className="stats-grid">
          <article className="stat-card">
            <span className="stat-label">Total Builds</span>

            <strong className="stat-value">
              {stats.totalBuilds}
            </strong>

            <span className="stat-meta">
              +{stats.buildsThisWeek} this week
            </span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Passed Builds</span>

            <strong className="stat-value">
              {stats.passedBuilds}
            </strong>

            <span className="stat-meta">
              {stats.successRate}% success rate
            </span>
          </article>

          <article className="stat-card">
            <span className="stat-label">UI Issues</span>

            <strong className="stat-value">
              {stats.uiIssues}
            </strong>

            <span className="stat-meta">
              Needs review
            </span>
          </article>
        </div>

        {/* ========================================
            Latest Build
            ======================================== */}
        <article className="latest-build">
          <div className="latest-build-header">
            <div>
              <span className="latest-build-label">
                Latest Build
              </span>

              <h3>Build {build.id}</h3>

              <p>
                {build.deployment} • {build.time}
              </p>
            </div>

            <div className="build-status">
              <span
                className="build-status-dot"
                aria-hidden="true"
              />

              <span>{build.status}</span>
            </div>
          </div>

          <div className="build-divider" />

          {/* ========================================
              Build Metrics
              ======================================== */}
          <div className="build-metrics">
            <div className="build-metric">
              <span>Tests</span>
              <strong>{build.tests}</strong>
            </div>

            <div className="build-metric success">
              <span>Passed</span>
              <strong>{build.passed}</strong>
            </div>

            <div className="build-metric">
              <span>Failed</span>
              <strong>{build.failed}</strong>
            </div>

            <div className="build-metric">
              <span>UI Issues</span>
              <strong>{build.issues}</strong>
            </div>
          </div>
        </article>
      </section>
    </>
  );
}

export default Dashboard;

