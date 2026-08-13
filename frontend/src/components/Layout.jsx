import { NavLink, Outlet } from "react-router-dom";
import Logo from "./Logo";

function Layout() {
  const navigationItems = [
    {
      label: "Dashboard",
      to: "/",
      end: true,
    },
    {
      label: "Builds",
      to: "/builds",
    },
    {
      label: "Issues",
      to: "/issues",
    },
    {
      label: "Screenshots",
      to: "/screenshots",
    },
    {
      label: "Pull Requests",
      to: "/pull-requests",
    },
  ];

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <Logo />

        <nav className="sidebar-nav" aria-label="Dashboard navigation">
          {navigationItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `nav-item${isActive ? " active" : ""}`
              }
            >
              {item.label}
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
