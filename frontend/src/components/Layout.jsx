import { NavLink, Outlet } from "react-router-dom";
import Logo from "./Logo";

function Layout() {
  const navigationItems = [
    {
      label: "Dashboard",
      to: "/",
      end: true,
      icon: "\u25A6",
    },
    {
      label: "Builds",
      to: "/builds",
      icon: "\u25C8",
    },
    {
      label: "Issues",
      to: "/issues",
      icon: "\u26A0",
    },
    {
      label: "Screenshots",
      to: "/screenshots",
      icon: "\u25A3",
    },
    {
      label: "Pull Requests",
      to: "/pull-requests",
      icon: "\u2197",
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
      </aside>

      <main className="dashboard-main">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
