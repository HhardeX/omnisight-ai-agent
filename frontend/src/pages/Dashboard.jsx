import { useCallback, useEffect, useState } from "react";
import { getDashboardData } from "../services/dashboardService";
import { getBuilds } from "../services/buildService";
import apiRequest from "../services/apiClient";

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [buildHistory, setBuildHistory] = useState([]);
  const [jobs, setJobs] = useState([]);
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

      const [dashboard, builds, jobHistory] = await Promise.all([
        getDashboardData(),
        getBuilds(),
        apiRequest("/api/v1/jobs"),
      ]);

      setDashboardData(dashboard);
      setBuildHistory(builds);
      setJobs(jobHistory);
    } catch (err) {
      setError(err.message || "Unable to load dashboard data.");
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    let isMounted = true;

    async function loadInitialDashboard() {
      try {
        setIsLoading(true);
        setError(null);

        const [dashboard, builds, jobHistory] = await Promise.all([
          getDashboardData(),
          getBuilds(),
          apiRequest("/api/v1/jobs"),
        ]);

        if (isMounted) {
          setDashboardData(dashboard);
          setBuildHistory(builds);
          setJobs(jobHistory);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Unable to load dashboard data.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadInitialDashboard();

    return () => {
      isMounted = false;
    };
  }, []);

  const stats = {
    totalBuilds: dashboardData?.total_builds ?? 0,
    uiIssues: dashboardData?.total_issues ?? 0,
    totalScreenshots: dashboardData?.total_screenshots ?? 0,
  };

  const backendBuild = dashboardData?.latest_build;

  const build = backendBuild
    ? {
        id: backendBuild.job_id,
        deployment: backendBuild.target_url,
        viewport: backendBuild.viewport,
        domSize: backendBuild.dom_size,
        status: "Completed",
        issues: stats.uiIssues,
      }
    : null;

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
                ▪
              </div>

              <span className="stat-label">
                Total Builds
              </span>
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
                !
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
                ▫
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

        <article className="latest-build">
          <div className="latest-build-header">
            <div>
              <span className="latest-build-label">
                Latest Build
              </span>

              <h3>
                {build?.id
                  ? `Build ${build.id}`
                  : "No builds yet"}
              </h3>

              <p>
                {build?.deployment || "No target URL available"}{" "}
                •{" "}
                {build?.viewport || "No viewport available"}
              </p>
            </div>

            <div className="build-status">
              <span
                className="build-status-dot"
                aria-hidden="true"
              />

              <span>
                {build?.status || "No build"}
              </span>
            </div>
          </div>

          <div className="build-divider" />

          <div className="build-metrics">
            <div className="build-metric">
              <span>DOM Size</span>

              <strong>
                {build?.domSize ?? "-"}
              </strong>
            </div>

            <div className="build-metric">
              <span>Viewport</span>

              <strong>
                {build?.viewport || "-"}
              </strong>
            </div>

            <div className="build-metric">
              <span>UI Issues</span>

              <strong>
                {build?.issues ?? 0}
              </strong>
            </div>
          </div>
        </article>

        <article className="latest-build audit-history">
          <div className="latest-build-header">
            <div>
              <span className="latest-build-label">
                Audit History
              </span>

              <h3>
                Previous Builds
              </h3>

              <p>
                Persisted OmniSight audit results
              </p>
            </div>

            <strong>
              {buildHistory.length} audits
            </strong>
          </div>

          <div className="build-divider" />

          {buildHistory.length === 0 ? (
            <p>
              No audit history available.
            </p>
          ) : (
            <div className="audit-history-list">
              {buildHistory.map((historyItem) => (
                <div
                  className="audit-history-item"
                  key={`${historyItem.job_id}-${historyItem.viewport}`}
                >
                  <div>
                    <strong>
                      {historyItem.job_id}
                    </strong>

                    <p>
                      {historyItem.target_url}
                    </p>
                  </div>

                  <div className="build-metric">
                    <span>Viewport</span>

                    <strong>
                      {historyItem.viewport}
                    </strong>
                  </div>

                  <div className="build-metric">
                    <span>DOM Size</span>

                    <strong>
                      {historyItem.dom_size}
                    </strong>
                  </div>
                </div>
              ))}
            </div>
          )}
        </article>

        <article className="latest-build audit-history">
          <div className="latest-build-header">
            <div>
              <span className="latest-build-label">
                Job Queue
              </span>

              <h3>
                Audit Jobs
              </h3>

              <p>
                Persistent OmniSight job lifecycle
              </p>
            </div>

            <strong>
              {jobs.length} jobs
            </strong>
          </div>

          <div className="build-divider" />

          {jobs.length === 0 ? (
            <p>
              No jobs available.
            </p>
          ) : (
            <div className="audit-history-list">
              {jobs.map((job) => (
                <div
                  className="audit-history-item"
                  key={job.job_id}
                >
                  <div>
                    <strong>
                      {job.job_id}
                    </strong>

                    <p>
                      {job.repository}
                    </p>
                  </div>

                  <div className="build-metric">
                    <span>Status</span>

                    <strong>
                      {job.status}
                    </strong>
                  </div>

                  <div className="build-metric">
                    <span>Branch</span>

                    <strong>
                      {job.branch}
                    </strong>
                  </div>

                  <div className="build-metric">
                    <span>Created</span>

                    <strong>
                      {new Date(job.created_at).toLocaleString()}
                    </strong>
                  </div>

                  <div className="build-metric">
                    <span>Completed</span>

                    <strong>
                      {job.completed_at
                        ? new Date(job.completed_at).toLocaleString()
                        : "-"}
                    </strong>
                  </div>
                </div>
              ))}
            </div>
          )}
        </article>
      </section>
    </>
  );
}

export default Dashboard;