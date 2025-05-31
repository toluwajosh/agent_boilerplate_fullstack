export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  message: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}

export interface ChatState {
  messages: ChatMessage[];
  conversationId: string | null;
  isLoading: boolean;
  error: string | null;
}
