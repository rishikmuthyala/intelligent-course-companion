/**
 * Dashboard Page - Course overview with AI summaries
 */

import React, { useState } from 'react';
import { ArrowLeft, BookOpen, MessageSquare, FileText, Sparkles, TrendingUp, Clock } from 'lucide-react';
import CourseCard from './CourseCard';
import type { Course } from '../types';

interface DashboardPageProps {
  courses: Course[];
  onCourseSelect: (course: Course) => void;
  onBackToHome: () => void;
  onGoToSummarize?: () => void;
  onCourseWithTranscriptSelect?: (course: Course) => void;
  isLoading?: boolean;
}

const DashboardPage: React.FC<DashboardPageProps> = ({
  courses,
  onCourseSelect,
  onBackToHome,
  onGoToSummarize,
  onCourseWithTranscriptSelect,
  isLoading = false,
}) => {
  const [selectedCourseId, setSelectedCourseId] = useState<string | null>(null);

  // Debug logging
  console.log('📊 DashboardPage rendered with courses:', courses);
  console.log('📊 Number of courses:', courses?.length);
  console.log('📊 isLoading:', isLoading);

  const handleCourseClick = (courseId: string) => {
    console.log('🖱️ Course clicked:', courseId);
    setSelectedCourseId(courseId);
    // If course has transcript, trigger auto-summarize
    const course = courses.find(c => c.id === courseId);
    console.log('📚 Found course:', course);
    if (course?.hasTranscript && onCourseWithTranscriptSelect) {
      console.log('✨ Triggering auto-summarize for course with transcript');
      onCourseWithTranscriptSelect(course);
    }
  };

  const handleChatClick = (course: Course) => {
    if (course.hasTranscript && onCourseWithTranscriptSelect) {
      onCourseWithTranscriptSelect(course);
    } else {
      onCourseSelect(course);
    }
  };

  const selectedCourse = courses.find(c => c.id === selectedCourseId);

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-10 backdrop-blur-lg bg-gray-800/90">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={onBackToHome}
              className="flex items-center space-x-2 text-gray-400 hover:text-gray-200 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span className="font-medium">Home</span>
            </button>
            <div className="flex items-center space-x-2">
              <Sparkles className="w-6 h-6 text-blue-400" />
              <span className="text-xl font-bold text-white">My Courses</span>
            </div>
            {onGoToSummarize && (
              <button
                onClick={onGoToSummarize}
                className="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-medium hover:from-blue-700 hover:to-cyan-700 transition-all shadow-lg hover:shadow-xl flex items-center space-x-2"
              >
                <Sparkles className="w-4 h-4" />
                <span>Summarize Transcript</span>
              </button>
            )}
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Courses List */}
          <div className="lg:col-span-1">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <BookOpen className="w-6 h-6 mr-2 text-blue-400" />
              Your Courses
            </h2>
            <div className="space-y-4">
              {isLoading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
                  <p className="mt-4 text-gray-400">Loading courses...</p>
                </div>
              ) : courses.length === 0 ? (
                <div className="text-center py-8 bg-gray-800 rounded-2xl p-6 border-2 border-dashed border-gray-700">
                  <BookOpen className="w-12 h-12 text-gray-500 mx-auto mb-3" />
                  <p className="text-gray-300">No courses found</p>
                  <p className="text-sm text-gray-500 mt-1">Sync your Canvas account to get started</p>
                </div>
              ) : (
                courses.map((course) => (
                <div
                  key={course.id}
                  onClick={() => handleCourseClick(course.id)}
                  className={`group cursor-pointer p-5 rounded-2xl transition-all duration-200 ${
                    selectedCourseId === course.id
                      ? 'bg-gradient-to-br from-blue-600 to-cyan-600 text-white shadow-xl scale-105'
                      : 'bg-gray-800 hover:bg-gray-750 border-2 border-gray-700 hover:border-blue-500 shadow-md hover:shadow-lg'
                  }`}
                >
                  <h3 className={`font-semibold text-lg mb-1 ${
                    selectedCourseId === course.id ? 'text-white' : 'text-white'
                  }`}>
                    {course.name}
                  </h3>
                  <p className={`text-sm mb-3 ${
                    selectedCourseId === course.id ? 'text-blue-100' : 'text-gray-400'
                  }`}>
                    {course.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className={`text-xs font-medium ${
                      selectedCourseId === course.id ? 'text-blue-200' : 'text-gray-500'
                    }`}>
                      {course.professor}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleChatClick(course);
                      }}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                        selectedCourseId === course.id
                          ? 'bg-white/20 text-white hover:bg-white/30'
                          : 'bg-blue-600 text-white hover:bg-blue-700'
                      }`}
                    >
                      Chat
                    </button>
                  </div>
                </div>
                ))
              )}
            </div>
          </div>

          {/* Course Details & Summary */}
          <div className="lg:col-span-2">
            {selectedCourse ? (
              <div className="space-y-6">
                {/* Course Header */}
                <div className="bg-gradient-to-br from-blue-600 to-cyan-600 rounded-3xl p-8 text-white shadow-2xl">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h1 className="text-3xl font-bold mb-2">{selectedCourse.name}</h1>
                      <p className="text-blue-100 text-lg">{selectedCourse.description}</p>
                      <p className="text-blue-200 mt-2">{selectedCourse.professor}</p>
                    </div>
                    <button
                      onClick={() => handleChatClick(selectedCourse)}
                      className="px-6 py-3 bg-white/20 hover:bg-white/30 rounded-xl font-semibold transition-all flex items-center space-x-2 backdrop-blur-sm"
                    >
                      <MessageSquare className="w-5 h-5" />
                      <span>Start Chat</span>
                    </button>
                  </div>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-3 gap-4">
                  <StatCard
                    icon={<FileText className="w-5 h-5" />}
                    label="Lectures"
                    value="24"
                    gradient="from-blue-600 to-cyan-500"
                  />
                  <StatCard
                    icon={<Clock className="w-5 h-5" />}
                    label="Hours"
                    value="36"
                    gradient="from-cyan-500 to-blue-500"
                  />
                  <StatCard
                    icon={<TrendingUp className="w-5 h-5" />}
                    label="Progress"
                    value="78%"
                    gradient="from-teal-500 to-cyan-500"
                  />
                </div>

                {/* AI Summary */}
                <div className="bg-gray-800 rounded-3xl p-8 shadow-xl border border-gray-700">
                  <div className="flex items-center space-x-3 mb-6">
                    <div className="p-2 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-xl">
                      <Sparkles className="w-5 h-5 text-white" />
                    </div>
                    <h2 className="text-2xl font-bold text-white">AI-Generated Summary</h2>
                  </div>
                  
                  <div className="prose max-w-none">
                    <p className="text-gray-300 leading-relaxed mb-4">
                      This course provides a comprehensive introduction to computer science fundamentals, 
                      covering essential topics such as programming, algorithms, data structures, and 
                      computational thinking.
                    </p>
                    <p className="text-gray-300 leading-relaxed mb-4">
                      <strong className="text-white">Key Topics:</strong>
                    </p>
                    <ul className="space-y-2 text-gray-300">
                      <li className="flex items-start">
                        <span className="text-blue-400 mr-2">•</span>
                        <span>Programming fundamentals in Python and Java</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-blue-400 mr-2">•</span>
                        <span>Data structures: arrays, linked lists, trees, and graphs</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-blue-400 mr-2">•</span>
                        <span>Algorithm design and complexity analysis</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-blue-400 mr-2">•</span>
                        <span>Problem-solving strategies and computational thinking</span>
                      </li>
                    </ul>
                    <p className="text-gray-300 leading-relaxed mt-4">
                      <strong className="text-white">Recent Focus:</strong> The last few lectures 
                      have emphasized recursive algorithms and their applications in tree traversal and 
                      sorting algorithms.
                    </p>
                  </div>

                  <div className="mt-6 p-4 bg-blue-900/30 rounded-xl border border-blue-700">
                    <p className="text-sm text-blue-100">
                      <strong>💡 Pro Tip:</strong> Use the chat feature to ask specific questions about any topic covered in the course!
                    </p>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4">
                  <button
                    onClick={() => handleChatClick(selectedCourse)}
                    className="flex-1 px-6 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-xl font-semibold hover:from-blue-700 hover:to-cyan-700 transition-all shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
                  >
                    <MessageSquare className="w-5 h-5" />
                    <span>Ask Questions</span>
                  </button>
                  <button className="px-6 py-4 bg-gray-800 text-gray-200 rounded-xl font-semibold hover:bg-gray-700 transition-all shadow-lg border-2 border-gray-700 flex items-center justify-center space-x-2">
                    <FileText className="w-5 h-5" />
                    <span>View Materials</span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="text-center py-16">
                  <BookOpen className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-400 mb-2">
                    Select a course
                  </h3>
                  <p className="text-gray-500">
                    Choose a course from the left to view its AI-generated summary
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  gradient: string;
}

const StatCard: React.FC<StatCardProps> = ({ icon, label, value, gradient }) => {
  return (
    <div className="bg-gray-800 rounded-2xl p-5 shadow-lg border border-gray-700 hover:shadow-xl transition-all">
      <div className={`inline-flex p-2 rounded-lg bg-gradient-to-br ${gradient} text-white mb-3`}>
        {icon}
      </div>
      <div className="text-2xl font-bold text-white mb-1">{value}</div>
      <div className="text-sm text-gray-400">{label}</div>
    </div>
  );
};

export default DashboardPage;
