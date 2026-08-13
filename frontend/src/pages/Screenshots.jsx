import { screenshots, screenshotStats } from "../data/mockData";

function Screenshots() {
  return (
    <>
      {/* ========================================
          Screenshots Header
          ======================================== */}
      <header className="dashboard-header">
        <div>
          <h1>Screenshots</h1>
          <p>Review visual captures from automated UI testing.</p>
        </div>

        <div className="environment" aria-label="Current environment: Staging">
          <span className="status-dot" aria-hidden="true" />
          <span>Staging</span>
        </div>
      </header>

      {/* ========================================
          Screenshots Content
          ======================================== */}
      <section className="page-content">
        <div className="page-heading">
          <div>
            <h2>Recent Screenshots</h2>
            <p>Visual snapshots captured from recent OmniSight builds.</p>
          </div>
        </div>

        {/* ========================================
            Screenshot Summary
            ======================================== */}
        <div className="stats-grid screenshot-stats">
          <article className="stat-card">
            <span className="stat-label">Total Screenshots</span>

            <strong className="stat-value">{screenshotStats.total}</strong>

            <span className="stat-meta">Across recent builds</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Verified</span>

            <strong className="stat-value">{screenshotStats.verified}</strong>

            <span className="stat-meta">No visual differences</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Visual Issues</span>

            <strong className="stat-value">
              {screenshotStats.visualIssues}
            </strong>

            <span className="stat-meta">Needs review</span>
          </article>
        </div>

        {/* ========================================
            Screenshot Grid
            ======================================== */}
        <div className="screenshot-grid">
          {screenshots.map((screenshot) => (
            <article className="screenshot-card" key={screenshot.id}>
              {/* Visual Preview Placeholder */}
              <div className="screenshot-preview">
                <div className="preview-browser">
                  <div className="preview-browser-bar">
                    <span />
                    <span />
                    <span />
                  </div>

                  <div className="preview-content">
                    <div className="preview-sidebar" />

                    <div className="preview-main">
                      <div className="preview-line large" />
                      <div className="preview-line" />

                      <div className="preview-box-grid">
                        <div />
                        <div />
                        <div />
                      </div>

                      <div className="preview-panel" />
                    </div>
                  </div>
                </div>

                <span
                  className={`screenshot-status ${
                    screenshot.status === "Passed" ? "passed" : "issue"
                  }`}
                >
                  {screenshot.status}
                </span>
              </div>

              {/* Screenshot Information */}
              <div className="screenshot-info">
                <span className="screenshot-id">{screenshot.id}</span>

                <h3>{screenshot.title}</h3>

                <p>{screenshot.description}</p>

                <div className="screenshot-meta">
                  <span>
                    Page <strong>{screenshot.page}</strong>
                  </span>

                  <span>
                    Build <strong>{screenshot.build}</strong>
                  </span>

                  <span>{screenshot.time}</span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

export default Screenshots;
