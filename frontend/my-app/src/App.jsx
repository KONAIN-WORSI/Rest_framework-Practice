import { useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate
} from "react-router-dom";

import api, { setTokens, clearTokens } from "./api";
import LoginPage from "./pages/LoginPage";
import JobsPage from "./pages/JobsPage";
import RecruiterDashboard from "./pages/RecruiterDashboard";
import ProtectedRoute from "./ProtectedRoute";
import RecruiterRoute from "./RecruiterRoute";

function AppContent() {
  const [tokens, setTokenState] = useState(null);
  const [profile, setProfile] = useState(null);
  const navigate = useNavigate();

  async function handleLogin(receivedTokens) {
  setTokens(receivedTokens);
  setTokenState(receivedTokens);

  try {
    const response = await api.get("/auth/me/");
    console.log("Logged-in profile:", response.data);

    setProfile(response.data);

    if (response.data.role === "recruiter") {
      navigate("/recruiter", { replace: true });
    } else {
      navigate("/jobs", { replace: true });
    }
  } catch (error) {
    console.error(
      "Failed to load profile:",
      error.response?.data || error.message
    );

    clearTokens();
    setTokenState(null);
    setProfile(null);
  }
 }

  function handleLogout() {
    const refresh = tokens?.refresh;

    // Clear the frontend session immediately.
    clearTokens();
    setTokenState(null);
    setProfile(null);

    // Attempt server-side refresh-token blacklisting.
    if (refresh) {
      api.post("/auth/logout/", { refresh }).catch((error) => {
        console.error("Server logout failed:", error.message);
      });
    }
  }

  useEffect(() => {
    function handleExpiredSession() {
      setTokenState(null);
      setProfile(null);
    }

    window.addEventListener(
      "auth:session-expired",
      handleExpiredSession
    );

    return () => {
      window.removeEventListener(
        "auth:session-expired",
        handleExpiredSession
      );
    };
  }, []);

  return (
    <>
      {tokens && (
        <nav>
          <button onClick={handleLogout}>Logout</button>
        </nav>
      )}

      <Routes>
        <Route
          path="/login"
          element={
            tokens
              ? <Navigate to="/jobs" replace />
              : <LoginPage onLogin={handleLogin} />
          }
        />

        <Route element={<ProtectedRoute tokens={tokens} />}>
          <Route path="/jobs" element={<JobsPage />} />

          <Route element={<RecruiterRoute profile={profile} />}>
            <Route
              path="/recruiter"
              element={<RecruiterDashboard />}
            />
          </Route>
        </Route>

        <Route
          path="/"
          element={<Navigate to="/jobs" replace />}
        />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}
