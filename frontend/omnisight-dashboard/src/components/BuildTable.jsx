// import { Link } from "react-router-dom";

// function BuildTable({ builds = [], loading }) {
//   if (loading) {
//     return (
//       <div className="empty-state">
//         Loading builds...
//       </div>
//     );
//   }

//   if (!builds.length) {
//     return (
//       <div className="empty-state">
//         No builds have been audited yet.
//       </div>
//     );
//   }

//   return (
//     <div className="table-wrapper">
//       <table className="data-table">
//         <thead>
//           <tr>
//             <th>Job ID</th>
//             <th>Target</th>
//             <th>Viewport</th>
//             <th>DOM Size</th>
//             <th>Action</th>
//           </tr>
//         </thead>

//         <tbody>
//           {builds.map((build) => (
//             <tr key={build.job_id}>
//               <td>
//                 <span className="mono">
//                   {build.job_id?.slice(0, 12)}
//                 </span>
//               </td>

//               <td>
//                 <span className="target-url">
//                   {build.target_url}
//                 </span>
//               </td>

//               <td>
//                 <span className="viewport-pill">
//                   {build.viewport}
//                 </span>
//               </td>

//               <td>
//                 {Number(build.dom_size || 0).toLocaleString()}
//               </td>

//               <td>
//                 <Link
//                   className="table-link"
//                   to="/screenshots"
//                 >
//                   View
//                 </Link>
//               </td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// }

// export default BuildTable;