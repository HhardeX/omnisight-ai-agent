import { useEffect, useState } from "react";
import { getPullRequests } from "../services/pullRequestService";

function PullRequests() {
  const [pullRequests, setPullRequests] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadPullRequests() {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getPullRequests();

        if (!isMounted) {
          return;
        }

        const realPullRequests = Array.isArray(data)
          ? data
          : data?.pull_requests || [];

        setPullRequests(realPullRequests);
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Unable to load pull request data.");
          setPullRequests([]);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadPullRequests();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <>
      <header className="dashboard-header">
        <div>
          <h1>Pull Requests</h1>
          <p>Review CI/CD builds and their automated UI audit results.</p>
        </div>

        <div className="environment" aria-label="Current environment: Staging">
          <span className="status-dot" aria-hidden="true" />
          <span>Staging</span>
        </div>
      </header>

      <section className="page-content">
        <div className="page-heading">
          <div>
            <h2>Recent Builds</h2>
            <p>
              Monitor real CI/CD build events and their automated UI audit
              results.
            </p>
          </div>
        </div>

        {isLoading && <p role="status">Loading build data...</p>}

        {error && (
          <p role="alert">Unable to load build data from the backend.</p>
        )}

        {!isLoading && !error && pullRequests.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-content">
              <h3>No build events yet</h3>
              <p>
                No CI/CD build results are currently available from the
                backend.
              </p>
            </div>
          </div>
        )}

        {!isLoading && !error && pullRequests.length > 0 && (
          <div className="build-list">
            {pullRequests.map((pullRequest, index) => {
              const issueCount = Number(pullRequest.issue_count || 0);
              const viewportCount = Number(
                pullRequest.viewport_count || 0,
              );

              const statusClass =
                pullRequest.status === "Verified"
                  ? "success"
                  : pullRequest.status === "Issues Found"
                    ? "error"
                    : "warning";

              return (
                <article
                  className="build-row"
                  key={pullRequest.job_id || `build-${index}`}
                >
                  <div className="build-row-info">
                    <span className="latest-build-label">
                      CI/CD BUILD
                    </span>

                    <h3>
                      {pullRequest.repository || "Repository unavailable"}
                    </h3>

                    <p>
                      Branch: {pullRequest.branch || "Unavailable"}
                    </p>

                    <p>
                      Commit: {pullRequest.commit_sha || "Unavailable"}
                    </p>

                    <p>
                      Target: {pullRequest.target_url || "Unavailable"}
                    </p>
                  </div>

                  <div className="build-row-summary">
                    <span
                      className={`status-badge ${statusClass}`}
                    >
                      <span
                        className="build-status-dot"
                        aria-hidden="true"
                      />

                      <span>
                        {pullRequest.status || "Pending"}
                      </span>
                    </span>

                    <div className="build-row-metrics">
                      <span>
                        Viewports{" "}
                        <strong>{viewportCount}</strong>
                      </span>

                      <span>
                        UI Issues{" "}
                        <strong
                          className={
                            issueCount === 0
                              ? "success-text"
                              : "failed-text"
                          }
                        >
                          {issueCount}
                        </strong>
                      </span>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </section>
    </>
  );
}

export default PullRequests;
