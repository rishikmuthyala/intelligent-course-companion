/**
 * TypeScript type definitions for the application
 */

export interface Course {
  id: string;
  name: string;
  description: string;
  professor?: string;
  synced?: boolean;
  hasTranscript?: boolean;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface ChatResponse {
  message: string;
  sources?: string[];
}
