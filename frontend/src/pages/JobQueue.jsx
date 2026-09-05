import { useCallback, useEffect, useState } from "react";
import apiRequest from "../services/apiClient";

function JobQueue() {
  const [jobs, setJobs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadJobs = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const jobHistory = await apiRequest("/api/v1/jobs");
      setJobs(jobHistory);
    } catch (err) {
      setError(err.message || "Unable to load job queue.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  return (
    <>
      <header className="dashboard-header">
        <div>
          <span className="dashboard-eyebrow">Feature 2</span>
          <h1>Job Queue</h1>
          <p>Monitor persistent OmniSight audit job lifecycle.</p>
        </div>

        <button
          type="button"
          className="dashboard-refresh-button"
          onClick={loadJobs}
          disabled={isLoading}
        >
          {isLoading ? "Loading..." : "Refresh"}
        </button>
      </header>

      <section className="dashboard-content">
        <div className="section-heading">
          <div>
            <h2>Audit Jobs</h2>
            <p>
              Persistent jobs processed through the OmniSight background worker.
            </p>
          </div>

          <strong>{jobs.length} jobs</strong>
        </div>

        {error && (
          <div className="dashboard-error" role="alert">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="latest-build">
            <p>Loading job queue...</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="latest-build">
            <p>No jobs available.</p>
          </div>
        ) : (
          <div className="audit-history-list">
            {jobs.map((job) => (
              <article
                className="latest-build audit-history-item"
                key={job.job_id}
              >
                <div>
                  <span className="latest-build-label">Job</span>
                  <h3>{job.job_id}</h3>
                  <p>{job.repository}</p>
                </div>

                <div className="build-metric">
                  <span>Status</span>
                  <strong>{job.status}</strong>
                </div>

                <div className="build-metric">
                  <span>Branch</span>
                  <strong>{job.branch || "-"}</strong>
                </div>

                <div className="build-metric">
                  <span>Created</span>
                  <strong>
                    {job.created_at
                      ? new Date(job.created_at).toLocaleString()
                      : "-"}
                  </strong>
                </div>

                <div className="build-metric">
                  <span>Completed</span>
                  <strong>
                    {job.completed_at
                      ? new Date(job.completed_at).toLocaleString()
                      : "-"}
                  </strong>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </>
  );
}

export default JobQueue;
