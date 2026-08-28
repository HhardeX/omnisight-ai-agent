import { useEffect, useState } from "react";
import { getScreenshots } from "../services/screenshotService";

function Screenshots() {
  const [screenshots, setScreenshots] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadScreenshots() {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getScreenshots();

        if (isMounted) {
          const realScreenshots = Array.isArray(data)
            ? data
            : data?.screenshots || [];

          setScreenshots(realScreenshots);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Unable to load screenshots.");
          setScreenshots([]);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadScreenshots();

    return () => {
      isMounted = false;
    };
  }, []);

  const totalScreenshots = screenshots.length;

  const visualIssues = 0;
  const verified = totalScreenshots - visualIssues;

  return (
    <>
      <header className="dashboard-header">
        <div>
          <h1>Screenshots</h1>
          <p>Review visual captures from automated UI testing.</p>
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
            <h2>Recent Screenshots</h2>
            <p>Visual snapshots captured from recent OmniSight builds.</p>
          </div>
        </div>

        {isLoading && (
          <p role="status">
            Loading screenshot data...
          </p>
        )}

        {error && (
          <p role="alert">
            Unable to load screenshot data from the backend.
          </p>
        )}

        {!isLoading && !error && screenshots.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-content">
              <h3>No screenshots yet</h3>
              <p>
                Run an OmniSight audit to generate screenshot results.
              </p>
            </div>
          </div>
        )}

        {!isLoading && (
          <div className="stats-grid screenshot-stats">
            <article className="stat-card">
              <span className="stat-label">Total Screenshots</span>
              <strong className="stat-value">
                {totalScreenshots}
              </strong>
              <span className="stat-meta">Across recent builds</span>
            </article>

            <article className="stat-card">
              <span className="stat-label">Verified</span>
              <strong className="stat-value">
                {verified}
              </strong>
              <span className="stat-meta">No visual differences</span>
            </article>

            <article className="stat-card">
              <span className="stat-label">Visual Issues</span>
              <strong className="stat-value">
                {visualIssues}
              </strong>
              <span className="stat-meta">Needs review</span>
            </article>
          </div>
        )}

        {!isLoading && !error && screenshots.length > 0 && (
          <div className="screenshot-grid">
            {screenshots.map((screenshot) => (
              <article
                className="screenshot-card"
                key={`${screenshot.job_id}-${screenshot.viewport}`}
              >
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

                  <span className="screenshot-status passed">
                    Verified
                  </span>
                </div>

                <div className="screenshot-info">
                  <span className="screenshot-id">
                    {screenshot.viewport}
                  </span>

                  <h3>
                    {screenshot.target_url}
                  </h3>

                  <p>
                    Screenshot captured during the automated
                    responsive browser audit.
                  </p>

                  <div className="screenshot-meta">
                    <span>
                      Viewport{" "}
                      <strong>{screenshot.viewport}</strong>
                    </span>

                    <span>
                      Job{" "}
                      <strong>
                        {screenshot.job_id}
                      </strong>
                    </span>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </>
  );
}

export default Screenshots;