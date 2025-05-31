"use client";

import React from "react";

interface LoadingIndicatorProps {
  size?: "small" | "medium" | "large";
  color?: string;
  text?: string;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({
  size = "medium",
  color = "#3b82f6",
  text,
}) => {
  const sizeClasses = {
    small: "w-4 h-4",
    medium: "w-6 h-6",
    large: "w-8 h-8",
  };

  return (
    <div className="flex items-center justify-center space-x-2">
      <div
        className={`${sizeClasses[size]} animate-spin rounded-full border-2 border-gray-300 border-t-current`}
        style={{ borderTopColor: color }}
      />
      {text && (
        <span className="text-sm text-gray-600 animate-pulse">{text}</span>
      )}
    </div>
  );
};

export default LoadingIndicator;
