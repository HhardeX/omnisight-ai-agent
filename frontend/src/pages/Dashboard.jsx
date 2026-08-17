import { useCallback, useEffect, useState } from "react";
import { dashboardStats, latestBuild } from "../data/mockData";
import { getDashboardData } from "../services/dashboardService";

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
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

      const data = await getDashboardData();
      setDashboardData(data);
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

  const hasBackendData = Boolean(dashboardData);

  const stats = hasBackendData
    ? {
        totalBuilds: dashboardData.total_builds ?? 0,
        uiIssues: dashboardData.total_issues ?? 0,
        totalScreenshots: dashboardData.total_screenshots ?? 0,
      }
    : {
        totalBuilds: dashboardStats.totalBuilds ?? 0,
        uiIssues: dashboardStats.uiIssues ?? 0,
        totalScreenshots: 0,
      };

  const backendBuild = dashboardData?.latest_build;

  const build = backendBuild
    ? {
        id: backendBuild.job_id,
        deployment: backendBuild.target_url,
        viewport: backendBuild.viewport,
        domSize: backendBuild.dom_size ?? 0,
      }
    : hasBackendData
      ? null
      : {
          id: latestBuild.id,
          deployment: latestBuild.deployment,
          viewport: latestBuild.time,
          domSize: 0,
        };

  const formatNumber = (value) => {
    return new Intl.NumberFormat().format(value);
  };

  const formatDomSize = (value) => {
    if (!value) {
      return "0";
    }

    return `${formatNumber(value)} chars`;
  };

  return (
    <>
      <header className="dashboard-header">
        <div>
          <h1>Dashboard</h1>
          <p>OmniSight QA overview</p>
        </div>

        <div
          className="environment"
          aria-label={
            error
              ? "Backend connection unavailable"
              : "Backend connection active"
          }
        >
          <span className="status-dot" aria-hidden="true" />
          <span>{error ? "Offline" : "Connected"}</span>
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
            disabled={isLoading || isRefreshing}
            className="refresh-button"
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
            Backend unavailable. Showing available dashboard data.
          </p>
        )}

        <div className="stats-grid">
          <article className="stat-card">
            <span className="stat-label">Total Builds</span>

            <strong className="stat-value">
              {formatNumber(stats.totalBuilds)}
            </strong>

            <span className="stat-meta">
              Automated UI audits
            </span>
          </article>

          <article className="stat-card">
            <span className="stat-label">UI Issues</span>

            <strong className="stat-value">
              {formatNumber(stats.uiIssues)}
            </strong>

            <span className="stat-meta">
              Detected visual defects
            </span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Screenshots</span>

            <strong className="stat-value">
              {formatNumber(stats.totalScreenshots)}
            </strong>

            <span className="stat-meta">
              Captured during audits
            </span>
          </article>
        </div>

        <article className="latest-build">
          <div className="latest-build-header">
            <div>
              <span className="latest-build-label">
                Latest Build
              </span>

              {build ? (
                <>
                  <h3>Build {build.id}</h3>

                  <p>
                    {build.deployment}
                    {" • "}
                    {build.viewport}
                  </p>
                </>
              ) : (
                <>
                  <h3>No builds available</h3>

                  <p>
                    Run an OmniSight audit to generate build data.
                  </p>
                </>
              )}
            </div>

            {build && (
              <div className="build-status">
                <span
                  className="build-status-dot"
                  aria-hidden="true"
                />

                <span>Audited</span>
              </div>
            )}
          </div>

          <div className="build-divider" />

          {build ? (
            <div className="build-metrics">
              <div className="build-metric">
                <span>Job ID</span>
                <strong>{build.id}</strong>
              </div>

              <div className="build-metric">
                <span>Viewport</span>
                <strong>{build.viewport}</strong>
              </div>

              <div className="build-metric">
                <span>DOM Size</span>
                <strong>{formatDomSize(build.domSize)}</strong>
              </div>

              <div className="build-metric">
                <span>UI Issues</span>
                <strong>{formatNumber(stats.uiIssues)}</strong>
              </div>
            </div>
          ) : (
            <div className="build-metrics">
              <div className="build-metric">
                <span>Status</span>
                <strong>Waiting</strong>
              </div>

              <div className="build-metric">
                <span>Builds</span>
                <strong>0</strong>
              </div>

              <div className="build-metric">
                <span>Screenshots</span>
                <strong>0</strong>
              </div>

              <div className="build-metric">
                <span>Issues</span>
                <strong>0</strong>
              </div>
            </div>
          )}
        </article>
      </section>
    </>
  );
}

export default Dashboard;