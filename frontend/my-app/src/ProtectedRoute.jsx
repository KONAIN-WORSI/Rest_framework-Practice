
import { Navigate, Outlet } from "react-router-dom";

export default function ProtectedRoute({ tokens }) {
  if (!tokens?.access) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
