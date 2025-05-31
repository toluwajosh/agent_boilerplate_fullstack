import axios, { AxiosResponse } from "axios";
import { ChatRequest, ChatResponse, ErrorResponse } from "@/types/chat";

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  timeout: 30000, // 30 seconds timeout
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log("API Request:", {
      method: config.method?.toUpperCase(),
      url: config.url,
      data: config.data,
    });
    return config;
  },
  (error) => {
    console.error("API Request Error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log("API Response:", {
      status: response.status,
      data: response.data,
    });
    return response;
  },
  (error) => {
    console.error("API Response Error:", {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
    });

    // Transform error response
    if (error.response?.data) {
      throw new Error(
        error.response.data.error ||
          error.response.data.detail ||
          "An error occurred"
      );
    }

    throw new Error(error.message || "Network error occurred");
  }
);

export class ChatAPI {
  /**
   * Send a message to the chat endpoint
   */
  static async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response: AxiosResponse<ChatResponse> = await api.post(
        "/chat",
        request
      );
      return response.data;
    } catch (error) {
      console.error("Error sending message:", error);
      throw error;
    }
  }

  /**
   * Health check for the API
   */
  static async healthCheck(): Promise<{ status: string; service: string }> {
    try {
      const response = await api.get("/health");
      return response.data;
    } catch (error) {
      console.error("Health check failed:", error);
      throw error;
    }
  }

  /**
   * Get API status and information
   */
  static async getApiInfo(): Promise<any> {
    try {
      const response = await api.get("/");
      return response.data;
    } catch (error) {
      console.error("Error getting API info:", error);
      throw error;
    }
  }
}

export default api;
