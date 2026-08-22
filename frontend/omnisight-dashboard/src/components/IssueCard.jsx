function IssueCard({ issue }) {
  return (
    <div className="issue-card">
      <div className="issue-card-header">
        <div>
          <span className="issue-type">
            {issue.defect_type || "Visual defect"}
          </span>

          <h3>
            {issue.description || "No description provided"}
          </h3>
        </div>

        <div className="confidence">
          {issue.confidence_score != null
            ? `${Math.round(issue.confidence_score * 100)}%`
            : "—"}
        </div>
      </div>

      <div className="issue-meta">
        <span>
          Selector:{" "}
          <code>
            {issue.element_selector || "unknown"}
          </code>
        </span>

        <span>
          Viewport: {issue.viewport || "unknown"}
        </span>
      </div>

      {issue.suggested_css && (
        <div className="suggestion-box">
          <div className="suggestion-title">
            AI Suggested Fix
          </div>

          <pre>{issue.suggested_css}</pre>
        </div>
      )}
    </div>
  );
}

export default IssueCard;