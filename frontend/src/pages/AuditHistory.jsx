import { useCallback, useEffect, useState } from "react";
import { getBuilds } from "../services/buildService";

function AuditHistory() {
  const [buildHistory, setBuildHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadHistory = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const builds = await getBuilds();
      setBuildHistory(builds);
    } catch (err) {
      setError(err.message || "Unable to load audit history.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  return (
    <>
      <header className="dashboard-header">
        <div>
          <span className="dashboard-eyebrow">Feature 1</span>
          <h1>Audit History</h1>
          <p>Persisted OmniSight visual audit results.</p>
        </div>

        <button
          type="button"
          className="dashboard-refresh-button"
          onClick={loadHistory}
          disabled={isLoading}
        >
          {isLoading ? "Loading..." : "Refresh"}
        </button>
      </header>

      <section className="dashboard-content">
        <div className="section-heading">
          <div>
            <h2>Previous Builds</h2>
            <p>
              Historical browser audits stored in the OmniSight database.
            </p>
          </div>

          <strong>{buildHistory.length} audits</strong>
        </div>

        {error && (
          <div className="dashboard-error" role="alert">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="latest-build">
            <p>Loading audit history...</p>
          </div>
        ) : buildHistory.length === 0 ? (
          <div className="latest-build">
            <p>No audit history available.</p>
          </div>
        ) : (
          <div className="audit-history-list">
            {buildHistory.map((historyItem) => (
              <article
                className="latest-build audit-history-item"
                key={`${historyItem.job_id}-${historyItem.viewport}`}
              >
                <div>
                  <span className="latest-build-label">Audit</span>
                  <h3>{historyItem.job_id}</h3>
                  <p>{historyItem.target_url}</p>
                </div>

                <div className="build-metric">
                  <span>Viewport</span>
                  <strong>{historyItem.viewport}</strong>
                </div>

                <div className="build-metric">
                  <span>DOM Size</span>
                  <strong>{historyItem.dom_size}</strong>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </>
  );
}

export default AuditHistory;