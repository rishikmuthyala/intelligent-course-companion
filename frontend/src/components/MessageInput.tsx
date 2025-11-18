/**
 * MessageInput Component
 * 
 * Input form for users to type and submit their questions.
 * Includes send button and handles enter key submission.
 */

import React, { useState, useRef, useEffect, KeyboardEvent } from 'react';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  isDisabled?: boolean;
  placeholder?: string;
}

const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  isDisabled = false,
  placeholder = "Ask a question about your course..."
}) => {
  const [message, setMessage] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [message]);

  const handleSubmit = () => {
    if (message.trim() && !isDisabled) {
      onSendMessage(message.trim());
      setMessage('');
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  // Example questions for inspiration
  const exampleQuestions = [
    "What are the main topics covered?",
    "Explain the key concepts from lecture 1",
    "What was discussed about algorithms?",
    "Summarize the course objectives"
  ];

  const handleExampleClick = (question: string) => {
    setMessage(question);
    textareaRef.current?.focus();
  };

  return (
    <div className="border-t border-gray-200 bg-white">
      {/* Example Questions (shown when input is empty and not disabled) */}
      {!message && !isDisabled && !isFocused && (
        <div className="px-4 pt-3 pb-2 border-b border-gray-100">
          <p className="text-xs text-gray-500 mb-2">Try asking:</p>
          <div className="flex flex-wrap gap-2">
            {exampleQuestions.slice(0, 3).map((question, index) => (
              <button
                key={index}
                onClick={() => handleExampleClick(question)}
                className="text-xs px-3 py-1.5 bg-gray-50 hover:bg-gray-100 text-gray-600 hover:text-gray-800 rounded-full transition-colors border border-gray-200"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}
      
      {/* Input Area */}
      <div className="p-4">
        <div className="flex items-end gap-3 max-w-6xl mx-auto">
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              placeholder={placeholder}
              disabled={isDisabled}
              rows={1}
              className={`
                w-full px-4 py-3 pr-12 border rounded-xl resize-none transition-all duration-200
                ${isFocused 
                  ? 'border-primary-500 ring-2 ring-primary-100' 
                  : 'border-gray-300 hover:border-gray-400'
                }
                focus:outline-none disabled:bg-gray-50 disabled:cursor-not-allowed
                placeholder:text-gray-400 text-gray-900
              `}
              style={{ minHeight: '48px', maxHeight: '120px' }}
            />
            
            {/* Character count */}
            {message.length > 0 && (
              <div className="absolute bottom-3 right-3 text-xs text-gray-400">
                {message.length}/1000
              </div>
            )}
          </div>
          
          {/* Send Button */}
          <button
            onClick={handleSubmit}
            disabled={isDisabled || !message.trim() || message.length > 1000}
            className={`
              group px-4 py-3 rounded-xl font-medium transition-all duration-200 flex items-center gap-2
              ${isDisabled || !message.trim() || message.length > 1000
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                : 'bg-primary-600 text-white hover:bg-primary-700 hover:shadow-lg active:scale-95'
              }
            `}
            title={isDisabled ? "Waiting for response..." : "Send message (Enter)"}
          >
            {isDisabled ? (
              <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            ) : (
              <>
                <span className="hidden sm:inline">Send</span>
                <svg
                  className="w-5 h-5 group-hover:translate-x-0.5 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
              </>
            )}
          </button>
        </div>
        
        {/* Helper Text */}
        <div className="flex items-center justify-between mt-2 px-1">
          <p className="text-xs text-gray-500">
            {isDisabled 
              ? "Please wait for the response..." 
              : "Press Enter to send, Shift+Enter for new line"
            }
          </p>
          {message.length > 800 && (
            <p className={`text-xs ${message.length > 1000 ? 'text-red-500' : 'text-yellow-600'}`}>
              {1000 - message.length} characters remaining
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageInput;
