import { issues, issueStats } from "../data/mockData";

function Issues() {
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

        <div className="stats-grid issues-stats">
          <article className="stat-card">
            <span className="stat-label">Total Issues</span>
            <strong className="stat-value">{issueStats.total}</strong>
            <span className="stat-meta">Detected recently</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Open Issues</span>
            <strong className="stat-value">{issueStats.open}</strong>
            <span className="stat-meta">Needs attention</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Resolved</span>
            <strong className="stat-value">{issueStats.resolved}</strong>
            <span className="stat-meta">Successfully fixed</span>
          </article>
        </div>

        <div className="issue-list">
          {issues.map((issue) => (
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
                        issue.status === "Open" ? "warning" : "success"
                      }`}
                    >
                      {issue.status}
                    </span>
                  </div>
                </div>

                <p className="issue-description">{issue.description}</p>

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
