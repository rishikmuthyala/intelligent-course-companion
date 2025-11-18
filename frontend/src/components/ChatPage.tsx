/**
 * Chat Page - Interactive Q&A with course content
 */

import React, { useState, useRef, useEffect } from 'react';
import { ArrowLeft, Send, Sparkles, Bot, User, Loader2 } from 'lucide-react';
import { apiService } from '../services/api';

interface ChatPageProps {
  courseId?: string;
  courseName?: string;
  onBack: () => void;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatPage: React.FC<ChatPageProps> = ({ courseId, courseName, onBack }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: `Hi! I'm your AI assistant for **${courseName}**. I can help you with:\n\n- Explaining course concepts\n- Summarizing lectures\n- Answering questions about assignments\n- Clarifying difficult topics\n\nWhat would you like to know?`,
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      if (!courseId) {
        throw new Error('No course selected');
      }

      // Call the actual API
      const response = await apiService.queryCourse(courseId, content);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Fallback response if API fails
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I apologize, but I'm having trouble connecting to the course materials right now. This could be because:\n\n• The course data hasn't been synced yet\n• There's a connection issue with the backend\n• The course ID is invalid\n\nPlease try syncing your courses or contact support if the issue persists.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const suggestedQuestions = [
    "What were the main topics in the last lecture?",
    "Can you explain the key concepts from Chapter 3?",
    "What should I focus on for the upcoming exam?",
    "Summarize this week's assignments",
  ];

  return (
    <div className="min-h-screen flex flex-col bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-10 backdrop-blur-lg bg-gray-800/90 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={onBack}
              className="flex items-center space-x-2 text-gray-400 hover:text-gray-200 transition-colors group"
            >
              <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
              <span className="font-medium">Back</span>
            </button>
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-xl">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-white">{courseName}</h1>
                <p className="text-sm text-gray-400">AI Assistant</p>
              </div>
            </div>
            <div className="w-20" /> {/* Spacer */}
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto bg-gray-900">
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <div className="space-y-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
              >
                <div
                  className={`max-w-[80%] ${
                    message.role === 'user'
                      ? 'bg-gradient-to-br from-blue-600 to-cyan-600 text-white rounded-2xl rounded-tr-sm'
                      : 'bg-gray-800 text-gray-100 rounded-2xl rounded-tl-sm shadow-md border border-gray-700'
                  } p-5`}
                >
                  <div className="flex items-start space-x-3">
                    {message.role === 'assistant' && (
                      <div className="flex-shrink-0 p-1.5 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-lg">
                        <Sparkles className="w-4 h-4 text-white" />
                      </div>
                    )}
                    <div className="flex-1">
                      <div
                        className={`prose prose-sm max-w-none ${
                          message.role === 'user' ? 'text-white prose-invert' : 'text-gray-100'
                        }`}
                        dangerouslySetInnerHTML={{
                          __html: message.content
                            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                            .replace(/\n/g, '<br />'),
                        }}
                      />
                      <p
                        className={`text-xs mt-2 ${
                          message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                        }`}
                      >
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                    {message.role === 'user' && (
                      <div className="flex-shrink-0 p-1.5 bg-white/20 rounded-lg">
                        <User className="w-4 h-4" />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start animate-slide-up">
                <div className="bg-gray-800 text-gray-100 rounded-2xl rounded-tl-sm shadow-md border border-gray-700 p-5">
                  <div className="flex items-center space-x-3">
                    <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
                    <span className="text-gray-300">Thinking...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Suggested Questions */}
          {messages.length === 1 && !isLoading && (
            <div className="mt-8 animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <p className="text-sm font-medium text-gray-400 mb-3">Suggested questions:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {suggestedQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleSendMessage(question)}
                    className="text-left p-4 bg-gray-800 rounded-xl border-2 border-gray-700 hover:border-blue-500 hover:shadow-lg transition-all group"
                  >
                    <p className="text-sm text-gray-300 group-hover:text-blue-400 transition-colors">
                      {question}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-gray-700 bg-gray-800 shadow-lg">
        <div className="container mx-auto px-4 py-4 max-w-4xl">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const input = e.currentTarget.elements.namedItem('message') as HTMLInputElement;
              if (input.value.trim() && !isLoading) {
                handleSendMessage(input.value.trim());
                input.value = '';
              }
            }}
            className="flex items-end space-x-3"
          >
            <div className="flex-1">
              <textarea
                name="message"
                rows={1}
                placeholder="Ask anything about your course..."
                className="w-full px-4 py-3 bg-gray-700 border-2 border-gray-600 text-white placeholder-gray-400 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 resize-none transition-all"
                disabled={isLoading}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    e.currentTarget.form?.requestSubmit();
                  }
                }}
              />
            </div>
            <button
              type="submit"
              disabled={isLoading}
              className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-xl font-semibold hover:from-blue-700 hover:to-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center space-x-2"
            >
              <Send className="w-5 h-5" />
              <span>Send</span>
            </button>
          </form>
          <p className="text-xs text-gray-500 mt-2 text-center">
            AI responses are generated from your course materials
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
