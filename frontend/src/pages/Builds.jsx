import { builds } from "../data/mockData";

function Builds() {
  return (
    <>
      {/* ========================================
          Builds Header
          ======================================== */}
      <header className="dashboard-header">
        <div>
          <h1>Builds</h1>
          <p>View and monitor your automated test builds.</p>
        </div>

        <div className="environment" aria-label="Current environment: Staging">
          <span className="status-dot" aria-hidden="true" />
          <span>Staging</span>
        </div>
      </header>

      {/* ========================================
          Build History
          ======================================== */}
      <section className="dashboard-content">
        <div className="section-heading">
          <div>
            <h2>Build History</h2>
            <p>Recent OmniSight automated UI testing builds.</p>
          </div>
        </div>

        {/* ========================================
            Build List
            ======================================== */}
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
                    <span className="build-status-dot" aria-hidden="true" />

                    <span>{build.status}</span>
                  </span>

                  <div className="build-row-metrics">
                    <span>
                      Tests <strong>{build.tests}</strong>
                    </span>

                    <span>
                      Passed{" "}
                      <strong className="success-text">{build.passed}</strong>
                    </span>

                    <span>
                      Failed{" "}
                      <strong className={build.failed > 0 ? "failed-text" : ""}>
                        {build.failed}
                      </strong>
                    </span>

                    <span>
                      UI Issues{" "}
                      <strong className={build.issues > 0 ? "failed-text" : ""}>
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
