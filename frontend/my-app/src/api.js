
import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "/api";

const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Separate client prevents the refresh request from
// triggering the same response interceptor.
const authApi = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Tokens stay in memory for this learning exercise.
let accessToken = null;
let refreshToken = null;

export function setTokens(tokens) {
  accessToken = tokens.access;

  if (tokens.refresh) {
    refreshToken = tokens.refresh;
  }
}

export function clearTokens() {
  accessToken = null;
  refreshToken = null;
}

api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry ||
      !refreshToken ||
      originalRequest.url?.includes("/auth/token/")
    ) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      const response = await authApi.post(
        "/auth/token/refresh/",
        { refresh: refreshToken }
      );

      // Rotation may return a new refresh token.
      setTokens(response.data);

      originalRequest.headers =
        originalRequest.headers || {};

      originalRequest.headers.Authorization =
        `Bearer ${accessToken}`;

      return api(originalRequest);
    } catch (refreshError) {
      clearTokens();

      // Let the application handle the expired session.
      window.dispatchEvent(
        new Event("auth:session-expired")
      );

      return Promise.reject(refreshError);
    }
  }
);

export default api;
