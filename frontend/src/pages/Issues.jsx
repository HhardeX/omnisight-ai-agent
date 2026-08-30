import { useEffect, useState } from "react";
import { getIssues } from "../services/issueService";

function Issues() {
  const [issues, setIssues] = useState([]);
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
          const realIssues = Array.isArray(data) ? data : data?.issues || [];

          setIssues(realIssues);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Unable to load issues.");
          setIssues([]);
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

  const totalIssues = issues.length;
  const openIssues = issues.filter((issue) => issue.status === "Open").length;
  const resolvedIssues = issues.filter(
    (issue) => issue.status === "Resolved",
  ).length;

  return (
    <>
      <header className="dashboard-header">
        <div>
          <h1>Issues</h1>
          <p>Review and monitor detected UI issues.</p>
        </div>

        <div className="environment" aria-label="Current environment: Staging">
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

        {isLoading && <p role="status">Loading issues...</p>}

        {error && (
          <p role="alert">Unable to load issue data from the backend.</p>
        )}

        {!isLoading && (
          <div className="stats-grid issues-stats">
            <article className="stat-card">
              <span className="stat-label">Total Issues</span>
              <strong className="stat-value">{totalIssues}</strong>
              <span className="stat-meta">Detected by automated audits</span>
            </article>

            <article className="stat-card">
              <span className="stat-label">Open Issues</span>
              <strong className="stat-value">{openIssues}</strong>
              <span className="stat-meta">Needs attention</span>
            </article>

            <article className="stat-card">
              <span className="stat-label">Resolved</span>
              <strong className="stat-value">{resolvedIssues}</strong>
              <span className="stat-meta">Successfully fixed</span>
            </article>
          </div>
        )}

        {!isLoading && !error && issues.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-content">
              <h3>No issues detected</h3>
              <p>
                OmniSight has not detected any visual UI issues in the available
                audit results.
              </p>
            </div>
          </div>
        )}

        {!isLoading && !error && issues.length > 0 && (
          <div className="issue-list">
            {issues.map((issue, index) => (
              <article
                className="issue-card"
                key={`${issue.job_id}-${issue.viewport}-${issue.element_selector}-${index}`}
              >
                <div className="issue-card-main">
                  <div className="issue-card-header">
                    <div>
                      <span className="issue-id">{issue.defect_type}</span>

                      <h3>{issue.element_selector}</h3>
                    </div>

                    <div className="issue-badges">
                      <span
                        className={`status-badge ${
                          issue.confidence_score >= 0.8
                            ? "error"
                            : issue.confidence_score >= 0.5
                              ? "warning"
                              : "neutral"
                        }`}
                      >
                        Confidence {Math.round(issue.confidence_score * 100)}%
                      </span>
                    </div>
                  </div>

                  <p className="issue-description">{issue.description}</p>

                  <div className="issue-meta">
                    <span>
                      Viewport <strong>{issue.viewport}</strong>
                    </span>

                    <span>
                      Job <strong>{issue.job_id}</strong>
                    </span>

                    <span>
                      Page <strong>{issue.target_url}</strong>
                    </span>
                  </div>

                  {issue.suggested_css && (
                    <div className="issue-meta">
                      <span>
                        Suggested CSS <strong>{issue.suggested_css}</strong>
                      </span>
                    </div>
                  )}
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </>
  );
}

export default Issues;
