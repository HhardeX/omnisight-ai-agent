// import { useLocation } from "react-router-dom";

// const titles = {
//   "/dashboard": ["Dashboard", "AI-powered QA overview"],
//   "/builds": ["Builds", "Monitor automated application audits"],
//   "/issues": ["Visual Issues", "Review defects detected by OmniSight"],
//   "/screenshots": ["Screenshots", "Visual evidence captured by the agent"],
//   "/pull-requests": [
//     "Pull Requests",
//     "Review AI-generated self-healing changes",
//   ],
// };

// function Header() {
//   const location = useLocation();

//   const [title, subtitle] =
//     titles[location.pathname] || titles["/dashboard"];

//   return (
//     <header className="topbar">
//       <div>
//         <h1>{title}</h1>
//         <p>{subtitle}</p>
//       </div>

//       <div className="topbar-actions">
//         <div className="system-status">
//           <span className="status-dot online" />
//           Backend connected
//         </div>

//         <button className="avatar">A</button>
//       </div>
//     </header>
//   );
// }

// export default Header;