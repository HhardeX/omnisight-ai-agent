function StatusBadge({ status = "unknown" }) {
  const normalized = String(status).toLowerCase();

  let className = "status-badge neutral";

  if (
    normalized === "passed" ||
    normalized === "success" ||
    normalized === "approved"
  ) {
    className = "status-badge success";
  }

  if (
    normalized === "failed" ||
    normalized === "error" ||
    normalized === "critical"
  ) {
    className = "status-badge danger";
  }

  if (
    normalized === "pending" ||
    normalized === "running" ||
    normalized === "open"
  ) {
    className = "status-badge warning";
  }

  return (
    <span className={className}>
      {status}
    </span>
  );
}

export default StatusBadge;