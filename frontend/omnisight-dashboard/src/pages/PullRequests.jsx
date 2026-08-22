import { useState } from "react";

const demoPullRequests = [
  {
    id: 1,
    title: "Fix checkout button mobile overflow",
    branch: "omnisight/fix-checkout-overflow",
    status: "Pending Review",
    confidence: 94,
    description:
      "AI detected that the checkout button extends beyond the mobile viewport.",
  },
  {
    id: 2,
    title: "Correct text overlap in product card",
    branch: "omnisight/fix-product-card",
    status: "Pending Review",
    confidence: 89,
    description:
      "VLM identified overlapping text caused by constrained card width.",
  },
];

function PullRequests() {
  const [requests, setRequests] =
    useState(demoPullRequests);

  function updateStatus(id, status) {
    setRequests((current) =>
      current.map((request) =>
        request.id === id
          ? { ...request, status }
          : request
      )
    );
  }

  return (
    <div className="page">
      <section className="page-heading compact">
        <div>
          <div className="eyebrow">
            SELF-HEALING ENGINE
          </div>

          <h2>Pull Requests</h2>

          <p>
            Review fixes proposed by the OmniSight
            autonomous agent.
          </p>
        </div>
      </section>

      <div className="info-banner">
        <span className="info-icon">✦</span>

        <div>
          <strong>
            AI-generated fixes require approval
          </strong>

          <p>
            Once the self-healing loop is enabled,
            OmniSight will create GitHub pull requests
            with the generated code and visual proof.
          </p>
        </div>
      </div>

      <div className="pr-list">
        {requests.map((request) => (
          <div
            className="pr-card"
            key={request.id}
          >
            <div className="pr-main">
              <div className="pr-icon">
                ⑂
              </div>

              <div>
                <div className="pr-title-row">
                  <h3>{request.title}</h3>

                  <span
                    className={
                      request.status ===
                      "Approved"
                        ? "status-badge success"
                        : request.status ===
                            "Rejected"
                          ? "status-badge danger"
                          : "status-badge warning"
                    }
                  >
                    {request.status}
                  </span>
                </div>

                <p>
                  {request.description}
                </p>

                <code>
                  {request.branch}
                </code>
              </div>
            </div>

            <div className="pr-confidence">
              <span>VLM Confidence</span>

              <strong>
                {request.confidence}%
              </strong>
            </div>

            <div className="pr-actions">
              <button
                className="danger-button"
                onClick={() =>
                  updateStatus(
                    request.id,
                    "Rejected"
                  )
                }
              >
                Reject
              </button>

              <button
                className="primary-button"
                onClick={() =>
                  updateStatus(
                    request.id,
                    "Approved"
                  )
                }
              >
                Approve Fix
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PullRequests;