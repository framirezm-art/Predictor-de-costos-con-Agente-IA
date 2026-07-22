import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const axiosClient = axios.create({
  baseURL,
  timeout: 300000,
  headers: { "Content-Type": "application/json" },
});

// Interceptor centralizado: normaliza el shape de error que viene del backend
// (ver app/exceptions/handlers.py -> { error, detail })
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.error ||
      error.message ||
      "Ocurrió un error inesperado al comunicarse con el servidor.";
    return Promise.reject(new Error(message));
  }
);
