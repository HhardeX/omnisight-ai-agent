import { NavLink, Outlet } from "react-router-dom";
import Logo from "./Logo";

function Layout() {
  const navigationItems = [
    {
      label: "Dashboard",
      to: "/",
      end: true,
      icon: "▦",
    },
    {
      label: "Builds",
      to: "/builds",
      icon: "◈",
    },
    {
      label: "Issues",
      to: "/issues",
      icon: "⚠",
    },
    {
      label: "Screenshots",
      to: "/screenshots",
      icon: "▣",
    },
    {
      label: "Pull Requests",
      to: "/pull-requests",
      icon: "↗",
    },
    {
      label: "Audit History",
      to: "/audit-history",
      icon: "◫",
    },
    {
      label: "Job Queue",
      to: "/job-queue",
      icon: "◌",
    },
  ];

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <Logo />

        <div className="sidebar-section-label">
          WORKSPACE
        </div>

        <nav
          className="sidebar-nav"
          aria-label="Dashboard navigation"
        >
          {navigationItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `nav-item${isActive ? " active" : ""}`
              }
            >
              <span className="nav-item-icon" aria-hidden="true">
                {item.icon}
              </span>

              <span className="nav-item-label">
                {item.label}
              </span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-section-label">
            SYSTEM
          </div>

          <button
            type="button"
            className="sidebar-bottom-item"
          >
            <span className="nav-item-icon" aria-hidden="true">
              ⚙
            </span>

            <span className="nav-item-label">
              Settings
            </span>
          </button>

          <div className="sidebar-user">
            <div className="sidebar-user-avatar">
              O
            </div>

            <div className="sidebar-user-info">
              <strong>OmniSight</strong>
              <span>Project Admin</span>
            </div>
          </div>
        </div>
      </aside>

      <main className="dashboard-main">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;