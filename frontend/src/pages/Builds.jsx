function Builds() {
  return (
    <main className="dashboard-main">
      <header className="dashboard-header">
        <div>
          <h1>Builds</h1>
          <p>View and monitor your automated test builds.</p>
        </div>

        <div className="environment">
          <span className="status-dot"></span>
          Staging
        </div>
      </header>

      <section className="dashboard-content">
        <div className="section-heading">
          <div>
            <h2>Build History</h2>
            <p>Recent OmniSight automated UI testing builds.</p>
          </div>
        </div>

        <div className="build-list">
          <article className="build-row">
            <div className="build-row-info">
              <span className="latest-build-label">BUILD</span>

              <h3>Build #124</h3>

              <p>Staging deployment • 2 minutes ago</p>
            </div>

            <div className="build-row-summary">
              <span className="build-status">
                <span className="build-status-dot"></span>
                Passed
              </span>

              <div className="build-row-metrics">
                <span>
                  Tests <strong>18</strong>
                </span>

                <span>
                  Passed <strong className="success-text">18</strong>
                </span>

                <span>
                  Failed <strong>0</strong>
                </span>

                <span>
                  UI Issues <strong>0</strong>
                </span>
              </div>
            </div>
          </article>

          <article className="build-row">
            <div className="build-row-info">
              <span className="latest-build-label">BUILD</span>

              <h3>Build #123</h3>

              <p>Staging deployment • 28 minutes ago</p>
            </div>

            <div className="build-row-summary">
              <span className="build-status">
                <span className="build-status-dot"></span>
                Passed
              </span>

              <div className="build-row-metrics">
                <span>
                  Tests <strong>16</strong>
                </span>

                <span>
                  Passed <strong className="success-text">16</strong>
                </span>

                <span>
                  Failed <strong>0</strong>
                </span>

                <span>
                  UI Issues <strong>0</strong>
                </span>
              </div>
            </div>
          </article>

          <article className="build-row">
            <div className="build-row-info">
              <span className="latest-build-label">BUILD</span>

              <h3>Build #122</h3>

              <p>Staging deployment • 1 hour ago</p>
            </div>

            <div className="build-row-summary">
              <span className="build-status">
                <span className="build-status-dot"></span>
                Passed
              </span>

              <div className="build-row-metrics">
                <span>
                  Tests <strong>20</strong>
                </span>

                <span>
                  Passed <strong className="success-text">19</strong>
                </span>

                <span>
                  Failed <strong>1</strong>
                </span>

                <span>
                  UI Issues <strong>1</strong>
                </span>
              </div>
            </div>
          </article>
        </div>
      </section>
    </main>
  );
}

export default Builds;
