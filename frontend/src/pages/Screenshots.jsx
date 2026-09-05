
import { useEffect, useState } from "react";
import { getScreenshots } from "../services/screenshotService";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function getScreenshotUrl(screenshotPath) {
  if (!screenshotPath) {
    return null;
  }

  const normalizedPath = screenshotPath.replaceAll("\\", "/");
  const artifactsIndex = normalizedPath.indexOf("/artifacts/");

  if (artifactsIndex >= 0) {
    return `${API_BASE_URL}${normalizedPath.slice(artifactsIndex)}`;
  }

  if (normalizedPath.startsWith("artifacts/")) {
    return `${API_BASE_URL}/${normalizedPath}`;
  }

  return null;
}

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
          setScreenshots(Array.isArray(data) ? data : []);
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
            Unable to load screenshots from the backend.
          </p>
        )}

        {!isLoading && !error && screenshots.length === 0 && (
          <p role="status">
            No screenshots have been captured yet.
          </p>
        )}

        <div className="stats-grid screenshot-stats">
          <article className="stat-card">
            <span className="stat-label">Total Screenshots</span>
            <strong className="stat-value">{totalScreenshots}</strong>
            <span className="stat-meta">Captured during audits</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Available</span>
            <strong className="stat-value">{totalScreenshots}</strong>
            <span className="stat-meta">Ready for review</span>
          </article>

          <article className="stat-card">
            <span className="stat-label">Viewports</span>
            <strong className="stat-value">
              {new Set(screenshots.map((screenshot) => screenshot.viewport)).size}
            </strong>
            <span className="stat-meta">Responsive captures</span>
          </article>
        </div>

        <div className="screenshot-grid">
          {screenshots.map((screenshot, index) => {
            const imageUrl = getScreenshotUrl(
              screenshot.screenshot_path,
            );

            return (
              <article
                className="screenshot-card"
                key={`${screenshot.job_id}-${screenshot.viewport}-${index}`}
              >
                <div className="screenshot-preview">
                  {imageUrl ? (
                    <img
                      src={imageUrl}
                      alt={`OmniSight ${screenshot.viewport} screenshot for ${screenshot.target_url}`}
                      loading="lazy"
                    />
                  ) : (
                    <p role="status">
                      Screenshot image unavailable.
                    </p>
                  )}

                  <span className="screenshot-status passed">
                    Captured
                  </span>
                </div>

                <div className="screenshot-info">
                  <span className="screenshot-id">
                    {screenshot.job_id}
                  </span>

                  <h3>
                    {screenshot.viewport} viewport
                  </h3>

                  <p>
                    Real Playwright screenshot captured by OmniSight.
                  </p>

                  <div className="screenshot-meta">
                    <span>
                      Page <strong>{screenshot.target_url}</strong>
                    </span>

                    <span>
                      Viewport <strong>{screenshot.viewport}</strong>
                    </span>
                  </div>

                  <div className="screenshot-meta">
                    <span>
                      Path{" "}
                      <strong>
                        {screenshot.screenshot_path}
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

export default Screenshots;
