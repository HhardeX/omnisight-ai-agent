
import { useEffect, useState } from "react";
import { getIssues } from "../services/issueService";

function getSeverity(confidenceScore) {
  if (confidenceScore >= 0.9) {
    return "High";
  }

  if (confidenceScore >= 0.75) {
    return "Medium";
  }

  return "Low";
}

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
          setIssues(Array.isArray(data) ? data : []);
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
  const openIssues = issues.length;
  const resolvedIssues = 0;

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
            Unable to load issues from the backend.
          </p>
        )}

        {!isLoading && !error && issues.length === 0 && (
          <p role="status">
            No UI issues have been detected.
          </p>
        )}

        <div className="stats-grid issues-stats">
          <article className="stat-card">
            <span className="stat-label">Total Issues</span>
            <strong className="stat-value">{totalIssues}</strong>
            <span className="stat-meta">Detected by OmniSight</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Open Issues</span>
            <strong className="stat-value">{openIssues}</strong>
            <span className="stat-meta">Requires attention</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Resolved</span>
            <strong className="stat-value">{resolvedIssues}</strong>
            <span className="stat-meta">Published fixes</span>
          </article>
        </div>

        <div className="issue-list">
          {issues.map((issue, index) => {
            const severity = getSeverity(issue.confidence_score);

            return (
              <article
                className="issue-card"
                key={`${issue.job_id}-${issue.viewport}-${issue.element_selector}-${index}`}
              >
                <div className="issue-card-main">
                  <div className="issue-card-header">
                    <div>
                      <span className="issue-id">
                        {issue.job_id}
                      </span>

                      <h3>
                        {issue.defect_type || "UI issue"}
                      </h3>
                    </div>

                    <div className="issue-badges">
                      <span
                        className={`status-badge ${
                          severity === "High"
                            ? "error"
                            : severity === "Medium"
                              ? "warning"
                              : "neutral"
                        }`}
                      >
                        {severity}
                      </span>

                      <span className="status-badge warning">
                        Open
                      </span>
                    </div>
                  </div>

                  <p className="issue-description">
                    {issue.description || "No description provided."}
                  </p>

                  <div className="issue-meta">
                    <span>
                      Element{" "}
                      <strong>
                        {issue.element_selector || "-"}
                      </strong>
                    </span>

                    <span>
                      Viewport{" "}
                      <strong>
                        {issue.viewport || "-"}
                      </strong>
                    </span>

                    <span>
                      Confidence{" "}
                      <strong>
                        {typeof issue.confidence_score === "number"
                          ? `${Math.round(issue.confidence_score * 100)}%`
                          : "-"}
                      </strong>
                    </span>
                  </div>

                  <div className="issue-meta">
                    <span>
                      Page{" "}
                      <strong>
                        {issue.target_url || "-"}
                      </strong>
                    </span>

                    <span>
                      Suggested CSS{" "}
                      <strong>
                        {issue.suggested_css || "-"}
                      </strong>
                    </span>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      </section>
    </>
  );
}

export default Issues;
