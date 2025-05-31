"use client";

import React, { useState, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";
import { ChatMessage, ChatState } from "@/types/chat";
import { ChatAPI } from "@/services/api";
import MessageHistory from "./MessageHistory";
import MessageInput from "./MessageInput";

const ChatInterface: React.FC = () => {
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    conversationId: null,
    isLoading: false,
    error: null,
  });

  const addMessage = useCallback(
    (role: "user" | "assistant", message: string) => {
      const newMessage: ChatMessage = {
        id: uuidv4(),
        role,
        message,
        timestamp: new Date(),
      };

      setChatState((prev) => ({
        ...prev,
        messages: [...prev.messages, newMessage],
      }));

      return newMessage;
    },
    []
  );

  const handleSendMessage = useCallback(
    async (message: string) => {
      try {
        // Clear any previous errors
        setChatState((prev) => ({ ...prev, error: null, isLoading: true }));

        // Add user message
        addMessage("user", message);

        // Send message to API
        const response = await ChatAPI.sendMessage({
          message,
          conversation_id: chatState.conversationId || undefined,
        });

        // Update conversation ID if it's a new conversation
        setChatState((prev) => ({
          ...prev,
          conversationId: response.conversation_id,
          isLoading: false,
        }));

        // Add AI response
        addMessage("assistant", response.response);
      } catch (error) {
        console.error("Error sending message:", error);

        const errorMessage =
          error instanceof Error ? error.message : "Failed to send message";

        setChatState((prev) => ({
          ...prev,
          error: errorMessage,
          isLoading: false,
        }));

        // Add error message to chat
        addMessage(
          "assistant",
          `Sorry, I encountered an error: ${errorMessage}. Please try again.`
        );
      }
    },
    [chatState.conversationId, addMessage]
  );

  const clearChat = useCallback(() => {
    setChatState({
      messages: [],
      conversationId: null,
      isLoading: false,
      error: null,
    });
  }, []);

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold">AI Assistant</h1>
            <p className="text-blue-100 text-sm">
              {chatState.conversationId
                ? "Conversation in progress"
                : "Start a new conversation"}
            </p>
          </div>
          {chatState.messages.length > 0 && (
            <button
              onClick={clearChat}
              className="px-3 py-1 bg-blue-700 hover:bg-blue-800 rounded text-sm transition-colors"
            >
              Clear Chat
            </button>
          )}
        </div>
      </div>

      {/* Error Banner */}
      {chatState.error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-red-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">
                <strong>Error:</strong> {chatState.error}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Chat Messages */}
      <MessageHistory
        messages={chatState.messages}
        isLoading={chatState.isLoading}
      />

      {/* Message Input */}
      <MessageInput
        onSendMessage={handleSendMessage}
        isLoading={chatState.isLoading}
        disabled={!!chatState.error}
      />

      {/* Status Bar */}
      <div className="bg-gray-50 px-4 py-2 text-xs text-gray-500 border-t">
        <div className="flex items-center justify-between">
          <span>
            {chatState.messages.length > 0 &&
              `${chatState.messages.length} messages`}
          </span>
          <span>
            {chatState.conversationId &&
              `ID: ${chatState.conversationId.substring(0, 8)}...`}
          </span>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
