import { useEffect, useState } from "react";
import { issues as mockIssues, issueStats as mockIssueStats } from "../data/mockData";
import { getIssues } from "../services/issueService";

function Issues() {
  const [issueData, setIssueData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadIssues() {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getIssues();

        if (isMounted) {
          setIssueData(data);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Unable to load issues");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadIssues();

    return () => {
      isMounted = false;
    };
  }, []);

  const apiIssues = Array.isArray(issueData)
    ? issueData
    : issueData?.issues;

  const displayedIssues = apiIssues || mockIssues;
  const stats = issueData?.stats || mockIssueStats;

  return (
    <>
      <header className="dashboard-header">
        <div>
          <h1>Issues</h1>
          <p>Review and monitor detected UI issues.</p>
        </div>

        <div
          className="environment"
          aria-label="Current environment: Staging"
        >
          <span className="status-dot" aria-hidden="true" />
          <span>Staging</span>
        </div>
      </header>

      <section className="page-content">
        <div className="page-heading">
          <div>
            <h2>Detected Issues</h2>
            <p>UI issues discovered by OmniSight automated testing.</p>
          </div>
        </div>

        {isLoading && (
          <p role="status">
            Loading issues...
          </p>
        )}

        {error && (
          <p role="alert">
            Backend unavailable. Showing mock issue data.
          </p>
        )}

        <div className="stats-grid issues-stats">
          <article className="stat-card">
            <span className="stat-label">Total Issues</span>
            <strong className="stat-value">{stats.total}</strong>
            <span className="stat-meta">Detected recently</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Open Issues</span>
            <strong className="stat-value">{stats.open}</strong>
            <span className="stat-meta">Needs attention</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Resolved</span>
            <strong className="stat-value">{stats.resolved}</strong>
            <span className="stat-meta">Successfully fixed</span>
          </article>
        </div>

        <div className="issue-list">
          {displayedIssues.map((issue) => (
            <article className="issue-card" key={issue.id}>
              <div className="issue-card-main">
                <div className="issue-card-header">
                  <div>
                    <span className="issue-id">{issue.id}</span>
                    <h3>{issue.title}</h3>
                  </div>

                  <div className="issue-badges">
                    <span
                      className={`status-badge ${
                        issue.severity === "High"
                          ? "error"
                          : issue.severity === "Medium"
                            ? "warning"
                            : "neutral"
                      }`}
                    >
                      {issue.severity}
                    </span>

                    <span
                      className={`status-badge ${
                        issue.status === "Open"
                          ? "warning"
                          : "success"
                      }`}
                    >
                      {issue.status}
                    </span>
                  </div>
                </div>

                <p className="issue-description">
                  {issue.description}
                </p>

                <div className="issue-meta">
                  <span>
                    Page <strong>{issue.page}</strong>
                  </span>

                  <span>
                    Build <strong>{issue.build}</strong>
                  </span>

                  <span>
                    Detected <strong>{issue.detected}</strong>
                  </span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

export default Issues;
