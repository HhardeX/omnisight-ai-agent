
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

        if (isMounted) {
          setPullRequests(Array.isArray(data) ? data : []);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Unable to load pull requests.");
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
          <p>Review pull requests and their automated UI test results.</p>
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
            <h2>Recent Pull Requests</h2>
            <p>
              Monitor automated QA checks associated with your pull requests.
            </p>
          </div>
        </div>

        {isLoading && (
          <p role="status">
            Loading pull requests...
          </p>
        )}

        {error && (
          <p role="alert">
            Unable to load pull requests from the backend.
          </p>
        )}

        {!isLoading && !error && pullRequests.length === 0 && (
          <p role="status">
            No pull requests have been published yet.
          </p>
        )}

        <div className="build-list">
          {pullRequests.map((pullRequest, index) => (
            <article
              className="build-row"
              key={`${pullRequest.job_id}-${pullRequest.viewport}-${index}`}
            >
              <div className="build-row-info">
                <span className="latest-build-label">
                  PULL REQUEST
                </span>

                <h3>
                  {pullRequest.branch_name}
                </h3>

                <p>
                  Build {pullRequest.job_id} •{" "}
                  {pullRequest.viewport}
                </p>
              </div>

              <div className="build-row-summary">
                <span className="status-badge success">
                  <span
                    className="build-status-dot"
                    aria-hidden="true"
                  />
                  <span>Published</span>
                </span>

                <div className="build-row-metrics">
                  <span>
                    Commit{" "}
                    <strong>
                      {pullRequest.commit_sha
                        ? pullRequest.commit_sha.slice(0, 8)
                        : "-"}
                    </strong>
                  </span>

                  {pullRequest.pull_request_url && (
                    <a
                      href={pullRequest.pull_request_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      View PR
                    </a>
                  )}
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

export default PullRequests;
