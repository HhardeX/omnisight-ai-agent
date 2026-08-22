import { NavLink } from "react-router-dom";

const navigation = [
  {
    label: "Dashboard",
    path: "/dashboard",
    icon: "▦",
  },
  {
    label: "Builds",
    path: "/builds",
    icon: "⌘",
  },
  {
    label: "Visual Issues",
    path: "/issues",
    icon: "⚠",
  },
  {
    label: "Screenshots",
    path: "/screenshots",
    icon: "▣",
  },
  {
    label: "Pull Requests",
    path: "/pull-requests",
    icon: "⑂",
  },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">O</div>

        <div>
          <div className="brand-name">OmniSight</div>
          <div className="brand-subtitle">AI QA Agent</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-title">MONITORING</div>

        {navigation.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <div className="agent-status">
          <span className="status-dot online" />

          <div>
            <strong>Agent Online</strong>
            <span>VLM pipeline ready</span>
          </div>
        </div>

        <div className="sidebar-version">
          OmniSight v0.1.0
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;