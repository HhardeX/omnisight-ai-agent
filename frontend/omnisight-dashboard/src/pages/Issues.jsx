import { useEffect, useState } from "react";

import IssueCard from "../components/IssueCard";
import { api } from "../services/api";

function Issues() {
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadIssues() {
    try {
      setLoading(true);

      const data = await api.getIssues();

      setIssues(data);
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadIssues();
  }, []);

  return (
    <div className="page">
      <section className="page-heading compact">
        <div>
          <div className="eyebrow">
            VISION ENGINE
          </div>

          <h2>Visual Issues</h2>

          <p>
            Defects identified through screenshot and
            DOM reasoning.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={loadIssues}
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
            Analyzing visual results...
          </div>
        </div>
      ) : issues.length === 0 ? (
        <div className="panel">
          <div className="success-state">
            <div className="success-icon">✓</div>

            <h3>No visual defects detected</h3>

            <p>
              OmniSight has not found any issues in the
              completed audits.
            </p>
          </div>
        </div>
      ) : (
        <div className="issues-list">
          {issues.map((issue, index) => (
            <IssueCard
              key={`${issue.job_id}-${index}`}
              issue={issue}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default Issues;