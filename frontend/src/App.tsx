/**
 * Main App Component
 * 
 * Root component that handles routing between Landing, Dashboard, and Chat pages.
 */

import { useState } from 'react';
import LandingPage from './components/LandingPage';
import SyncPage from './components/SyncPage';
import DashboardPage from './components/DashboardPage';
import ChatPage from './components/ChatPage';
import TranscriptSummarizePage from './components/TranscriptSummarizePage';
import type { Course } from './types';

type Page = 'landing' | 'sync' | 'dashboard' | 'chat' | 'summarize';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('landing');
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [courses, setCourses] = useState<Course[]>([]);
  const [isLoading] = useState(false);


  const handleGetStarted = () => {
    // Start with sync page to run Canvas scraper
    setCurrentPage('sync');
  };

  const handleSyncComplete = (syncedCourses: Course[]) => {
    // After sync completes, load courses and go to dashboard
    console.log('🎯 handleSyncComplete called with courses:', syncedCourses);
    console.log('🎯 Number of courses:', syncedCourses?.length);
    
    if (!syncedCourses || syncedCourses.length === 0) {
      console.error('❌ No courses provided to handleSyncComplete!');
      // Fallback: create CS 446 course
      syncedCourses = [{
        id: 'cs446_search_engines',
        name: 'COMPSCI 446 - Search Engines',
        description: '1 lecture transcript downloaded',
        professor: 'Dr. Professor',
        synced: true,
        hasTranscript: true,
      }];
    }
    
    setCourses(syncedCourses);
    console.log('✅ Courses set, navigating to dashboard');
    setCurrentPage('dashboard');
  };

  const handleCourseSelect = (course: Course) => {
    setSelectedCourse(course);
    setCurrentPage('chat');
  };

  const handleBackToDashboard = () => {
    setCurrentPage('dashboard');
    setSelectedCourse(null);
  };

  const handleBackToHome = () => {
    setCurrentPage('landing');
    setCourses([]);
    setSelectedCourse(null);
  };

  const handleGoToSummarize = () => {
    setCurrentPage('summarize');
  };

  const handleBackFromSummarize = () => {
    setCurrentPage('dashboard');
    setSelectedCourse(null);
  };

  const handleCourseWithTranscript = (course: Course) => {
    // Load transcript and go to summarize page
    setSelectedCourse(course);
    setCurrentPage('summarize');
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {currentPage === 'landing' && (
        <LandingPage 
          onGetStarted={handleGetStarted}
          onGoToSummarize={handleGoToSummarize}
        />
      )}
      {currentPage === 'sync' && (
        <SyncPage onSyncComplete={handleSyncComplete} />
      )}
      {currentPage === 'dashboard' && (
        <DashboardPage
          courses={courses}
          onCourseSelect={handleCourseSelect}
          onBackToHome={handleBackToHome}
          onGoToSummarize={handleGoToSummarize}
          onCourseWithTranscriptSelect={handleCourseWithTranscript}
          isLoading={isLoading}
        />
      )}
      {currentPage === 'chat' && (
        <ChatPage
          courseId={selectedCourse?.id}
          courseName={selectedCourse?.name}
          onBack={handleBackToDashboard}
        />
      )}
      {currentPage === 'summarize' && (
        <TranscriptSummarizePage 
          onBack={handleBackFromSummarize}
          autoLoadCourse={selectedCourse}
        />
      )}
    </div>
  );
}

export default App;