import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";
import AuditHistory from "./pages/AuditHistory";
import JobQueue from "./pages/JobQueue";

import Dashboard from "./pages/Dashboard";
import Builds from "./pages/Builds";
import Issues from "./pages/Issues";
import Screenshots from "./pages/Screenshots";
import PullRequests from "./pages/PullRequests";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/builds" element={<Builds />} />
          <Route path="/issues" element={<Issues />} />
          <Route path="/screenshots" element={<Screenshots />} />
          <Route path="/pull-requests" element={<PullRequests />} />
          <Route path="/audit-history" element={<AuditHistory />} />
          <Route path="/job-queue" element={<JobQueue />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
