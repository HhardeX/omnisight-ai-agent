import { useEffect, useState } from "react";

import BuildTable from "../components/BuildTable";
import { api } from "../services/api";

function Builds() {
  const [builds, setBuilds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadBuilds() {
    try {
      setLoading(true);

      const data = await api.getBuilds();

      setBuilds(data);
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadBuilds();
  }, []);

  return (
    <div className="page">
      <section className="page-heading compact">
        <div>
          <div className="eyebrow">
            AUDIT HISTORY
          </div>

          <h2>Builds</h2>

          <p>
            Every build analyzed by the OmniSight
            browser agent.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={loadBuilds}
        >
          ↻ Refresh
        </button>
      </section>

      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}

      <div className="panel">
        <div className="panel-header">
          <div>
            <h3>All Builds</h3>
            <p>
              {builds.length} audits recorded
            </p>
          </div>
        </div>

        <BuildTable
          builds={builds}
          loading={loading}
        />
      </div>
    </div>
  );
}

export default Builds;