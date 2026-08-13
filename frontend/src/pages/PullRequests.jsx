import { pullRequests } from "../data/mockData";

function PullRequests() {
  return (
    <>
      {/* ========================================
          Pull Requests Header
          ======================================== */}
      <header className="dashboard-header">
        <div>
          <h1>Pull Requests</h1>
          <p>Review pull requests and their automated UI test results.</p>
        </div>

        <div className="environment" aria-label="Current environment: Staging">
          <span className="status-dot" aria-hidden="true" />
          <span>Staging</span>
        </div>
      </header>

      {/* ========================================
          Pull Request Content
          ======================================== */}
      <section className="page-content">
        <div className="page-heading">
          <div>
            <h2>Recent Pull Requests</h2>
            <p>
              Monitor automated QA checks associated with your pull requests.
            </p>
          </div>
        </div>

        {/* ========================================
            Pull Request List
            ======================================== */}
        <div className="build-list">
          {pullRequests.map((pullRequest) => (
            <article className="build-row" key={pullRequest.id}>
              {/* Pull Request Information */}
              <div className="build-row-info">
                <span className="latest-build-label">PULL REQUEST</span>

                <h3>
                  {pullRequest.id} — {pullRequest.title}
                </h3>

                <p>
                  {pullRequest.branch} • {pullRequest.author} •{" "}
                  {pullRequest.time}
                </p>
              </div>

              {/* Pull Request Summary */}
              <div className="build-row-summary">
                <span
                  className={`status-badge ${
                    pullRequest.status === "Passed" ? "success" : "warning"
                  }`}
                >
                  <span className="build-status-dot" aria-hidden="true" />

                  <span>{pullRequest.status}</span>
                </span>

                <div className="build-row-metrics">
                  <span>
                    Checks <strong>{pullRequest.checks}</strong>
                  </span>

                  <span>
                    UI Issues{" "}
                    <strong
                      className={
                        pullRequest.issues === 0
                          ? "success-text"
                          : "failed-text"
                      }
                    >
                      {pullRequest.issues}
                    </strong>
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

export default PullRequests;
