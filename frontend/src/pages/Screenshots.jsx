import { useEffect, useState } from "react";
import { getScreenshots } from "../services/screenshotService";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

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
          setError(
            err.message || "Unable to load screenshot data.",
          );
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

  const visualIssues = screenshots.reduce(
    (total, screenshot) =>
      total + Number(screenshot.defect_count || 0),
    0,
  );

  const verified = screenshots.filter(
    (screenshot) => screenshot.status === "Verified",
  ).length;

  function getScreenshotUrl(screenshotPath) {
    if (!screenshotPath) {
      return "";
    }

    const normalizedPath = screenshotPath
      .replaceAll("\\", "/")
      .replace(/^\/+/, "");

    if (
      normalizedPath.startsWith("http://") ||
      normalizedPath.startsWith("https://")
    ) {
      return normalizedPath;
    }

    return `${API_BASE_URL}/${normalizedPath}`;
  }

  return (
    <>
      <header className="dashboard-header">
        <div>
          <h1>Screenshots</h1>
          <p>
            Review visual captures from automated UI testing.
          </p>
        </div>

        <div
          className="environment"
          aria-label="Current environment: Staging"
        >
          <span
            className="status-dot"
            aria-hidden="true"
          />
          <span>Staging</span>
        </div>
      </header>

      <section className="page-content">
        <div className="page-heading">
          <div>
            <h2>Recent Screenshots</h2>
            <p>
              Visual snapshots captured from recent OmniSight
              builds.
            </p>
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
                Run an OmniSight audit to generate screenshot
                results.
              </p>
            </div>
          </div>
        )}

        {!isLoading && !error && screenshots.length > 0 && (
          <>
            <div className="stats-grid screenshot-stats">
              <article className="stat-card">
                <span className="stat-label">
                  Total Screenshots
                </span>

                <strong className="stat-value">
                  {totalScreenshots}
                </strong>

                <span className="stat-meta">
                  Across recent builds
                </span>
              </article>

              <article className="stat-card">
                <span className="stat-label">
                  Verified
                </span>

                <strong className="stat-value">
                  {verified}
                </strong>

                <span className="stat-meta">
                  Screenshots with no detected issues
                </span>
              </article>

              <article className="stat-card">
                <span className="stat-label">
                  Visual Issues
                </span>

                <strong className="stat-value">
                  {visualIssues}
                </strong>

                <span className="stat-meta">
                  Detected by visual audits
                </span>
              </article>
            </div>

            <div className="screenshot-grid">
              {screenshots.map((screenshot) => {
                const screenshotUrl = getScreenshotUrl(
                  screenshot.screenshot_path,
                );

                const defectCount = Number(
                  screenshot.defect_count || 0,
                );

                const isVerified =
                  screenshot.status === "Verified";

                return (
                  <article
                    className="screenshot-card"
                    key={`${screenshot.job_id}-${screenshot.viewport}`}
                  >
                    <div className="screenshot-preview">
                      {screenshotUrl ? (
                        <a
                          href={screenshotUrl}
                          target="_blank"
                          rel="noreferrer"
                          aria-label={`Open ${screenshot.viewport} screenshot`}
                        >
                          <img
                            src={screenshotUrl}
                            alt={`${screenshot.viewport} screenshot of ${screenshot.target_url}`}
                            className="screenshot-image"
                          />
                        </a>
                      ) : (
                        <div className="screenshot-image-placeholder">
                          Screenshot unavailable
                        </div>
                      )}

                      <span
                        className={`screenshot-status ${
                          isVerified ? "passed" : "failed"
                        }`}
                      >
                        {isVerified
                          ? "Verified"
                          : `${defectCount} ${
                              defectCount === 1
                                ? "Issue"
                                : "Issues"
                            }`}
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
                        Screenshot captured during the
                        automated responsive browser audit.
                      </p>

                      <div className="screenshot-meta">
                        <span>
                          Viewport{" "}
                          <strong>
                            {screenshot.viewport}
                          </strong>
                        </span>

                        <span>
                          Job{" "}
                          <strong>
                            {screenshot.job_id}
                          </strong>
                        </span>

                        <span>
                          Issues{" "}
                          <strong>
                            {defectCount}
                          </strong>
                        </span>
                      </div>
                    </div>
                  </article>
                );
              })}
            </div>
          </>
        )}
      </section>
    </>
  );
}

export default Screenshots;