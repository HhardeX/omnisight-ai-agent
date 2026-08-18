import { useEffect, useState } from "react";
import { getBuilds } from "../services/buildService";

function Builds() {
  const [builds, setBuilds] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadBuilds() {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getBuilds();

        if (!isMounted) {
          return;
        }

        const realBuilds = Array.isArray(data)
          ? data
          : data?.builds || [];

        setBuilds(realBuilds);
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Unable to load builds.");
          setBuilds([]);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadBuilds();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <>
      <header className="dashboard-header">
        <div>
          <h1>Builds</h1>
          <p>View and monitor your automated UI testing builds.</p>
        </div>

        <div
          className="environment"
          aria-label="Current environment: Staging"
        >
          <span className="status-dot" aria-hidden="true" />
          <span>Staging</span>
        </div>
      </header>

      <section className="dashboard-content">
        <div className="section-heading">
          <div>
            <h2>Build History</h2>
            <p>Recent OmniSight automated UI testing builds.</p>
          </div>
        </div>

        {isLoading && (
          <p role="status">
            Loading build data...
          </p>
        )}

        {error && (
          <p role="alert">
            Unable to load build data from the backend.
          </p>
        )}

        {!isLoading && !error && builds.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-content">
              <h3>No builds yet</h3>
              <p>
                No completed OmniSight builds are currently available.
                Run an audit to generate build results.
              </p>
            </div>
          </div>
        )}

        {!isLoading && builds.length > 0 && (
          <div className="build-list">
            {builds.map((build) => (
              <article className="build-row" key={build.job_id}>
                <div className="build-row-info">
                  <span className="latest-build-label">BUILD</span>

                  <h3>Build {build.job_id}</h3>

                  <p>
                    {build.target_url} {" • "} {build.viewport}
                  </p>
                </div>

                <div className="build-row-summary">
                  <span className="status-badge neutral">
                    Backend Result
                  </span>

                  <div className="build-row-metrics">
                    <span>
                      DOM Size <strong>{build.dom_size ?? "—"}</strong>
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

export default Builds;
