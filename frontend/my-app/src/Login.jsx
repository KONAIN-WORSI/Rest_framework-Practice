import { useState } from "react";
import api, {setTokens} from "./api";


export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/auth/token/", {
        email,
        password,
      });

      // Keep the tokens in memory for this learning exercise.
      setTokens(response.data)
      onLogin(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Login failed. Check your credentials and API."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>

      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        autoComplete="email"
        required
      />

      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        autoComplete="current-password"
        required
      />

      <button disabled={loading}>
        {loading ? "Logging in..." : "Login"}
      </button>

      {error && <p role="alert">{error}</p>}
    </form>
  );
}
