
import { Navigate, Outlet } from "react-router-dom";

export default function RecruiterRoute({ profile }) {
  if (!profile) {
    return <p>Loading profile...</p>;
  }

  if (profile.role !== "recruiter") {
    return <Navigate to="/jobs" replace />;
  }

  return <Outlet />;
}
