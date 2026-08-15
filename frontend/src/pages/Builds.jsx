import { useEffect, useState } from "react";
import { builds as mockBuilds } from "../data/mockData";
import { getBuilds } from "../services/buildService";

function Builds() {
  const [builds, setBuilds] = useState(mockBuilds);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadBuilds() {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getBuilds();

        if (isMounted) {
          const realBuilds = Array.isArray(data)
            ? data
            : data?.builds || [];

          setBuilds(realBuilds.length > 0 ? realBuilds : mockBuilds);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Unable to load builds.");
          setBuilds(mockBuilds);
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
          <p>View and monitor your automated test builds.</p>
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
            Backend unavailable. Showing mock build data.
          </p>
        )}

        <div className="build-list">
          {builds.map((build) => {
            const isFailed = build.status === "Failed";

            return (
              <article className="build-row" key={build.id}>
                <div className="build-row-info">
                  <span className="latest-build-label">BUILD</span>

                  <h3>Build {build.id}</h3>

                  <p>
                    {build.deployment} • {build.time}
                  </p>
                </div>

                <div className="build-row-summary">
                  <span
                    className={`build-status ${
                      isFailed ? "build-status-failed" : ""
                    }`}
                    aria-label={`Build status: ${build.status}`}
                  >
                    <span
                      className="build-status-dot"
                      aria-hidden="true"
                    />

                    <span>{build.status}</span>
                  </span>

                  <div className="build-row-metrics">
                    <span>
                      Tests <strong>{build.tests}</strong>
                    </span>

                    <span>
                      Passed{" "}
                      <strong className="success-text">
                        {build.passed}
                      </strong>
                    </span>

                    <span>
                      Failed{" "}
                      <strong
                        className={
                          build.failed > 0 ? "failed-text" : ""
                        }
                      >
                        {build.failed}
                      </strong>
                    </span>

                    <span>
                      UI Issues{" "}
                      <strong
                        className={
                          build.issues > 0 ? "failed-text" : ""
                        }
                      >
                        {build.issues}
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

export default Builds;
