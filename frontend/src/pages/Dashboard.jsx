import { useCallback, useEffect, useState } from "react";
import { getDashboardData } from "../services/dashboardService";
import { getBuilds } from "../services/buildService";

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [builds, setBuilds] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const loadDashboard = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setIsRefreshing(true);
      } else {
        setIsLoading(true);
      }

      setError(null);

      const [dashboard, buildResults] = await Promise.all([
        getDashboardData(),
        getBuilds(),
      ]);

      setDashboardData(dashboard);

      const realBuilds = Array.isArray(buildResults)
        ? buildResults
        : buildResults?.builds || [];

      setBuilds(realBuilds);
    } catch (err) {
      setError(err.message || "Unable to load dashboard data.");
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const stats = {
    totalBuilds: dashboardData?.total_builds ?? 0,
    uiIssues: dashboardData?.total_issues ?? 0,
    totalScreenshots: dashboardData?.total_screenshots ?? 0,
  };

  const latestBuild = dashboardData?.latest_build;

  const viewportOrder = ["mobile", "tablet", "desktop"];

  const viewportLabels = {
    mobile: "Mobile",
    tablet: "Tablet",
    desktop: "Desktop",
  };

  const viewportSizes = {
    mobile: "375 x 812",
    tablet: "768 x 1024",
    desktop: "1920 x 1080",
  };

  const responsiveBuilds = viewportOrder.map((viewport) => {
    const result = builds.find((build) => build.viewport === viewport);

    return {
      viewport,
      label: viewportLabels[viewport],
      size: viewportSizes[viewport],
      result,
    };
  });

  return (
    <>
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

      <section className="dashboard-content">
        <div className="section-heading">
          <div>
            <h2>Overview</h2>
            <p>Monitor your automated UI testing activity.</p>
          </div>

          <button
            type="button"
            onClick={() => loadDashboard(true)}
            disabled={isRefreshing}
          >
            {isRefreshing ? "Refreshing..." : "Refresh"}
          </button>
        </div>

        {isLoading && (
          <p role="status">
            Loading dashboard data...
          </p>
        )}

        {error && (
          <p role="alert">
            Unable to load dashboard data from the backend.
          </p>
        )}

        <div className="stats-grid">
          <article className="stat-card">
            <div className="stat-card-top">
              <div className="stat-icon" aria-hidden="true">
                {String.fromCharCode(0x25C8)}
              </div>

              <span className="stat-label">Total Builds</span>
            </div>

            <strong className="stat-value">
              {stats.totalBuilds}
            </strong>

            <span className="stat-meta">
              Automated UI audits
            </span>
          </article>

          <article className="stat-card">
            <div className="stat-card-top">
              <div className="stat-icon" aria-hidden="true">
                {String.fromCharCode(0x26A0)}
              </div>

              <span className="stat-label">
                UI Issues
              </span>
            </div>

            <strong className="stat-value">
              {stats.uiIssues}
            </strong>

            <span className="stat-meta">
              Issues detected
            </span>
          </article>

          <article className="stat-card">
            <div className="stat-card-top">
              <div className="stat-icon" aria-hidden="true">
                {String.fromCharCode(0x25A3)}
              </div>

              <span className="stat-label">
                Screenshots
              </span>
            </div>

            <strong className="stat-value">
              {stats.totalScreenshots}
            </strong>

            <span className="stat-meta">
              Captured during audits
            </span>
          </article>
        </div>

        <div className="section-heading">
          <div>
            <h2>Responsive Audit Results</h2>
            <p>
              Real browser audit results across supported viewport sizes.
            </p>
          </div>
        </div>

        <div className="build-list">
          {responsiveBuilds.map(({ viewport, label, size, result }) => (
            <article className="build-row" key={viewport}>
              <div className="build-row-info">
                <span className="latest-build-label">
                  {label.toUpperCase()}
                </span>

                <h3>{result ? "Audit completed" : "No result"}</h3>

                <p>
                  Viewport: {size}
                </p>
              </div>

              <div className="build-row-summary">
                <span
                  className={`status-badge ${
                    result ? "success" : "neutral"
                  }`}
                >
                  {result ? "Verified" : "No data"}
                </span>

                <div className="build-row-metrics">
                  <span>
                    DOM Size{" "}
                    <strong>
                      {result?.dom_size ?? "-"}
                    </strong>
                  </span>
                </div>
              </div>
            </article>
          ))}
        </div>

        <article className="latest-build">
          <div className="latest-build-header">
            <div>
              <span className="latest-build-label">
                Latest Build
              </span>

              <h3>
                {latestBuild?.job_id
                  ? `Build ${latestBuild.job_id}`
                  : "No builds yet"}
              </h3>

              <p>
                {latestBuild?.target_url || "No target URL available"}
                {" | "}
                {latestBuild?.viewport || "No viewport available"}
              </p>
            </div>

            <div className="build-status">
              <span
                className="build-status-dot"
                aria-hidden="true"
              />

              <span>
                {latestBuild ? "Verified" : "No data"}
              </span>
            </div>
          </div>

          <div className="build-divider" />

          <div className="build-metrics">
            <div className="build-metric">
              <span>DOM Size</span>

              <strong>
                {latestBuild?.dom_size ?? "-"}
              </strong>
            </div>

            <div className="build-metric success">
              <span>Audit Results</span>

              <strong>
                {builds.length || "-"}
              </strong>
            </div>

            <div className="build-metric">
              <span>UI Issues</span>

              <strong>
                {stats.uiIssues}
              </strong>
            </div>

            <div className="build-metric">
              <span>Screenshots</span>

              <strong>
                {stats.totalScreenshots}
              </strong>
            </div>
          </div>
        </article>
      </section>
    </>
  );
}

export default Dashboard;
