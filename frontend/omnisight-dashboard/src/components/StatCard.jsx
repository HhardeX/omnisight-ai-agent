function StatCard({ label, value, description, icon, loading }) {
  return (
    <div className="stat-card">
      <div className="stat-card-top">
        <span className="stat-label">{label}</span>

        <div className="stat-icon">{icon}</div>
      </div>

      <div className="stat-value">
        {loading ? "—" : value}
      </div>

      <div className="stat-description">
        {description}
      </div>
    </div>
  );
}

export default StatCard;