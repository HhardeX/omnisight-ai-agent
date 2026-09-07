
import { useCallback, useEffect, useState } from "react";
import apiRequest from "../services/apiClient";

function HumanApprovals() {
  const [jobs, setJobs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [processingJob, setProcessingJob] = useState(null);
  const [error, setError] = useState(null);

  const loadApprovals = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setIsRefreshing(true);
      } else {
        setIsLoading(true);
      }

      setError(null);

      const allJobs = await apiRequest("/api/v1/jobs");

      setJobs(
        allJobs.filter(
          (job) => job.approval_status === "pending",
        ),
      );
    } catch (err) {
      setError(err.message || "Unable to load approval queue.");
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadApprovals();
  }, [loadApprovals]);

  async function handleDecision(jobId, decision) {
    try {
      setProcessingJob(jobId);
      setError(null);

      await apiRequest(`/api/v1/jobs/${jobId}/approval`, {
        method: "POST",
        body: JSON.stringify({ decision }),
      });

      await loadApprovals(true);
    } catch (err) {
      setError(
        err.message || `Unable to ${decision} this repair.`,
      );
    } finally {
      setProcessingJob(null);
    }
  }

  return (
    <>
      <header className="dashboard-header">
        <div>
          <h1>Human Approvals</h1>
          <p>Review low-confidence AI repair proposals.</p>
        </div>

        <button
          type="button"
          onClick={() => loadApprovals(true)}
          disabled={isRefreshing}
        >
          {isRefreshing ? "Refreshing..." : "Refresh"}
        </button>
      </header>

      <section className="dashboard-content">
        <div className="section-heading">
          <div>
            <h2>Approval Queue</h2>
            <p>
              Repairs below the AI confidence threshold require
              human review before execution.
            </p>
          </div>

          <strong>
            {jobs.length} pending
          </strong>
        </div>

        {isLoading && (
          <p role="status">
            Loading approval queue...
          </p>
        )}

        {error && (
          <p role="alert">
            {error}
          </p>
        )}

        {!isLoading && jobs.length === 0 && !error && (
          <article className="latest-build">
            <div className="latest-build-header">
              <div>
                <span className="latest-build-label">
                  Human Review
                </span>

                <h3>
                  No pending approvals
                </h3>

                <p>
                  All repair decisions are currently clear.
                </p>
              </div>
            </div>
          </article>
        )}

        {jobs.length > 0 && (
          <div className="audit-history-list">
            {jobs.map((job) => {
              const confidence =
                typeof job.approval_confidence === "number"
                  ? `${Math.round(
                      job.approval_confidence * 100,
                    )}%`
                  : "-";

              const isProcessing =
                processingJob === job.job_id;

              return (
                <article
                  className="latest-build audit-history"
                  key={job.job_id}
                >
                  <div className="latest-build-header">
                    <div>
                      <span className="latest-build-label">
                        Pending Approval
                      </span>

                      <h3>
                        {job.job_id}
                      </h3>

                      <p>
                        {job.repository}
                      </p>
                    </div>

                    <strong>
                      {confidence} confidence
                    </strong>
                  </div>

                  <div className="build-divider" />

                  <div className="build-metrics">
                    <div className="build-metric">
                      <span>Reason</span>

                      <strong>
                        {job.approval_reason || "-"}
                      </strong>
                    </div>

                    <div className="build-metric">
                      <span>Branch</span>

                      <strong>
                        {job.branch || "-"}
                      </strong>
                    </div>

                    <div className="build-metric">
                      <span>Created</span>

                      <strong>
                        {job.created_at
                          ? new Date(
                              job.created_at,
                            ).toLocaleString()
                          : "-"}
                      </strong>
                    </div>
                  </div>

                  <div className="build-divider" />

                  <div className="section-heading">
                    <div>
                      <span className="latest-build-label">
                        Decision
                      </span>

                      <p>
                        Approve to resume the existing audit
                        and repair workflow.
                      </p>
                    </div>

                    <div>
                      <button
                        type="button"
                        onClick={() =>
                          handleDecision(
                            job.job_id,
                            "reject",
                          )
                        }
                        disabled={isProcessing}
                      >
                        {isProcessing
                          ? "Processing..."
                          : "Reject"}
                      </button>

                      <button
                        type="button"
                        onClick={() =>
                          handleDecision(
                            job.job_id,
                            "approve",
                          )
                        }
                        disabled={isProcessing}
                      >
                        {isProcessing
                          ? "Processing..."
                          : "Approve"}
                      </button>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </section>
    </>
  );
}

export default HumanApprovals;
