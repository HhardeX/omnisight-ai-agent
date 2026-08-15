import { useEffect, useState } from "react";
import {
  screenshots as mockScreenshots,
  screenshotStats as mockScreenshotStats,
} from "../data/mockData";
import { getScreenshots } from "../services/screenshotService";

function Screenshots() {
  const [screenshotData, setScreenshotData] = useState(null);
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
          setScreenshotData(data);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Unable to load screenshots.");
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

  const apiScreenshots = Array.isArray(screenshotData)
    ? screenshotData
    : screenshotData?.screenshots;

  const displayedScreenshots = apiScreenshots || mockScreenshots;
  const stats = screenshotData?.stats || mockScreenshotStats;

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
            Backend unavailable. Showing mock screenshot data.
          </p>
        )}

        <div className="stats-grid screenshot-stats">
          <article className="stat-card">
            <span className="stat-label">Total Screenshots</span>
            <strong className="stat-value">{stats.total}</strong>
            <span className="stat-meta">Across recent builds</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Verified</span>
            <strong className="stat-value">{stats.verified}</strong>
            <span className="stat-meta">No visual differences</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Visual Issues</span>
            <strong className="stat-value">{stats.visualIssues}</strong>
            <span className="stat-meta">Needs review</span>
          </article>
        </div>

        <div className="screenshot-grid">
          {displayedScreenshots.map((screenshot) => (
            <article className="screenshot-card" key={screenshot.id}>
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
