import { useEffect, useState } from "react";

import { api } from "../services/api";

function Screenshots() {
  const [screenshots, setScreenshots] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] = useState("");

  async function loadScreenshots() {
    try {
      setLoading(true);

      const data =
        await api.getScreenshots();

      setScreenshots(data);
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadScreenshots();
  }, []);

  return (
    <div className="page">
      <section className="page-heading compact">
        <div>
          <div className="eyebrow">
            VISUAL EVIDENCE
          </div>

          <h2>Screenshots</h2>

          <p>
            Screenshots captured during automated
            browser audits.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={loadScreenshots}
        >
          ↻ Refresh
        </button>
      </section>

      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}

      {loading ? (
        <div className="panel">
          <div className="empty-state">
            Loading screenshots...
          </div>
        </div>
      ) : screenshots.length === 0 ? (
        <div className="panel">
          <div className="empty-state">
            No screenshots available yet.
          </div>
        </div>
      ) : (
        <div className="screenshot-grid">
          {screenshots.map((item) => (
            <div
              className="screenshot-card"
              key={item.job_id}
            >
              <div className="screenshot-preview">
                <div className="preview-placeholder">
                  <span>▣</span>
                  <small>
                    Visual evidence
                  </small>
                </div>
              </div>

              <div className="screenshot-info">
                <span className="mono">
                  {item.job_id?.slice(0, 14)}
                </span>

                <strong>
                  {item.viewport}
                </strong>

                <span className="target-url">
                  {item.target_url}
                </span>

                <span className="screenshot-path">
                  {item.screenshot_path}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Screenshots;