/**
 * API Service
 * 
 * Handles all API calls to the backend server.
 */

import axios from 'axios';

// Base URL for the API (backend server)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Types
export interface Course {
  id: string;
  name: string;
  transcripts_downloaded?: number;
}

export interface QueryRequest {
  question: string;
}

export interface QueryResponse {
  answer: string;
  source_chunks: string[];
  course_id: string;
  question: string;
}

export interface SyncResponse {
  status: string;
  message: string;
  details?: string;
}

export interface SyncStatus {
  is_running: boolean;
  last_sync?: string;
  courses_found: number;
  transcripts_downloaded: number;
  files_processed: number;
}

export interface SummarizeRequest {
  transcript: string;
}

export interface SummarizeResponse {
  summary: string;
  detailed_notes: string;
  key_points: string[];
  topics: string[];
  important_concepts: string[];
  study_tips: string[];
  practice_questions: string[];
  session_id: string;
}

export interface FollowUpRequest {
  session_id: string;
  question: string;
}

export interface FollowUpResponse {
  answer: string;
  session_id: string;
  question: string;
}

// API Methods
export const apiService = {
  // Health check
  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await api.get('/');
    return response.data;
  },

  // Get list of available courses
  async getCourses(): Promise<{ courses: Course[]; total: number; message?: string }> {
    const response = await api.get('/courses');
    return response.data;
  },

  // Trigger sync operation
  async startSync(): Promise<SyncResponse> {
    const response = await api.post('/sync');
    return response.data;
  },

  // Get sync status
  async getSyncStatus(): Promise<SyncStatus> {
    const response = await api.get('/sync/status');
    return response.data;
  },

  // Query a course
  async queryCourse(courseId: string, question: string): Promise<QueryResponse> {
    const response = await api.post(`/query/${courseId}`, { question });
    return response.data;
  },

  // Summarize transcript
  async summarizeTranscript(transcript: string): Promise<SummarizeResponse> {
    const response = await api.post('/summarize', { transcript });
    return response.data;
  },

  // Ask follow-up question about summarized transcript
  async askFollowUp(sessionId: string, question: string): Promise<FollowUpResponse> {
    const response = await api.post('/summarize/ask', { session_id: sessionId, question });
    return response.data;
  },
};

export default apiService;
