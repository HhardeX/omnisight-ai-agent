import { useEffect, useState } from "react";

import StatCard from "../components/StatCard";
import BuildTable from "../components/BuildTable";
import { api } from "../services/api";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [builds, setBuilds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const [dashboardData, buildsData] =
        await Promise.all([
          api.getDashboard(),
          api.getBuilds(),
        ]);

      setDashboard(dashboardData);
      setBuilds(buildsData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  return (
    <div className="dashboard-page">
      <section className="page-heading">
        <div>
          <div className="eyebrow">
            AUTONOMOUS QA
          </div>

          <h2>
            See what your application
            <span> looks like to AI.</span>
          </h2>

          <p>
            OmniSight continuously analyzes your builds,
            detects visual regressions and prepares
            self-healing fixes.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={loadDashboard}
        >
          ↻ Refresh
        </button>
      </section>

      {error && (
        <div className="error-banner">
          <strong>Backend unavailable.</strong>
          <span>{error}</span>
        </div>
      )}

      <section className="stats-grid">
        <StatCard
          label="Total Builds"
          value={dashboard?.total_builds ?? 0}
          description="Applications audited"
          icon="⌘"
          loading={loading}
        />

        <StatCard
          label="Visual Issues"
          value={dashboard?.total_issues ?? 0}
          description="Defects detected by VLM"
          icon="⚠"
          loading={loading}
        />

        <StatCard
          label="Screenshots"
          value={dashboard?.total_screenshots ?? 0}
          description="Visual states captured"
          icon="▣"
          loading={loading}
        />

        <StatCard
          label="Automation"
          value="Active"
          description="OmniSight agent status"
          icon="✦"
          loading={false}
        />
      </section>

      <section className="content-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <h3>Recent Builds</h3>
              <p>Latest automated audits</p>
            </div>

            <button
              className="ghost-button"
              onClick={loadDashboard}
            >
              Refresh
            </button>
          </div>

          <BuildTable
            builds={builds.slice(0, 8)}
            loading={loading}
          />
        </div>

        <div className="panel latest-build-panel">
          <div className="panel-header">
            <div>
              <h3>Latest Audit</h3>
              <p>Most recent analysis</p>
            </div>
          </div>

          {dashboard?.latest_build ? (
            <div className="latest-build">
              <div className="audit-ring">
                <span>AI</span>
              </div>

              <h3>
                Audit completed
              </h3>

              <p className="latest-url">
                {dashboard.latest_build.target_url}
              </p>

              <div className="audit-details">
                <div>
                  <span>Job</span>
                  <strong>
                    {dashboard.latest_build.job_id?.slice(
                      0,
                      14
                    )}
                  </strong>
                </div>

                <div>
                  <span>Viewport</span>
                  <strong>
                    {dashboard.latest_build.viewport}
                  </strong>
                </div>

                <div>
                  <span>DOM</span>
                  <strong>
                    {Number(
                      dashboard.latest_build.dom_size || 0
                    ).toLocaleString()}
                  </strong>
                </div>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              No audit has completed yet.
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

export default Dashboard;