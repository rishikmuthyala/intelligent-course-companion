/**
 * CourseCard Component
 * 
 * Displays a single course card on the dashboard.
 * Shows course information and allows navigation to the chat page.
 */

import React from 'react';

interface CourseCardProps {
  courseId: string;
  courseName: string;
  transcriptCount?: number;
  lastSynced?: string;
  onSelect?: (courseId: string) => void;
}

const CourseCard: React.FC<CourseCardProps> = ({
  courseId,
  courseName,
  transcriptCount = 0,
  lastSynced,
  onSelect
}) => {
  const handleClick = () => {
    if (onSelect) {
      onSelect(courseId);
    }
  };

  // Generate a color based on course ID for visual variety
  const getColorClass = (id: string) => {
    const colors = [
      'bg-blue-900/50 text-blue-400 border border-blue-700',
      'bg-cyan-900/50 text-cyan-400 border border-cyan-700',
      'bg-teal-900/50 text-teal-400 border border-teal-700',
      'bg-sky-900/50 text-sky-400 border border-sky-700',
      'bg-indigo-900/50 text-indigo-400 border border-indigo-700',
      'bg-blue-800/50 text-blue-300 border border-blue-600',
    ];
    const hash = id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[hash % colors.length];
  };

  const colorClass = getColorClass(courseId);

  return (
    <div
      className="bg-gray-800 rounded-lg shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:-translate-y-1 border border-gray-700"
      onClick={handleClick}
    >
      <div className="p-6">
        {/* Course Icon/Header */}
        <div className="flex items-center justify-between mb-4">
          <div className={`w-14 h-14 ${colorClass.split(' ')[0]} rounded-xl flex items-center justify-center`}>
            <svg
              className={`w-7 h-7 ${colorClass.split(' ')[1]}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
              />
            </svg>
          </div>
          <span className="text-xs text-gray-400 font-mono bg-gray-900 px-2 py-1 rounded border border-gray-700">
            {courseId}
          </span>
        </div>
        
        {/* Course Name */}
        <h3 className="text-lg font-bold text-white mb-3 line-clamp-2 min-h-[3.5rem]">
          {courseName || `Course ${courseId}`}
        </h3>
        
        {/* Course Stats */}
        <div className="space-y-2 mb-5">
          <div className="flex items-center text-sm text-gray-400">
            <svg className="w-4 h-4 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>
              {transcriptCount > 0 ? (
                <>
                  <span className="font-semibold text-white">{transcriptCount}</span>
                  {' '}transcript{transcriptCount !== 1 ? 's' : ''} available
                </>
              ) : (
                <span className="text-gray-500">No transcripts yet</span>
              )}
            </span>
          </div>
          
          {lastSynced && (
            <div className="flex items-center text-xs text-gray-500">
              <svg className="w-3 h-3 mr-1.5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Last synced: {new Date(lastSynced).toLocaleDateString()}
            </div>
          )}
        </div>
        
        {/* Action Button */}
        <button 
          className={`
            mt-auto w-full py-3 px-4 rounded-lg font-medium transition-all duration-200
            ${transcriptCount > 0 
              ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white hover:from-blue-700 hover:to-cyan-700 hover:shadow-md active:scale-95' 
              : 'bg-gray-700 text-gray-500 cursor-not-allowed'
            }
          `}
          disabled={transcriptCount === 0}
          onClick={(e) => {
            e.stopPropagation();
            handleClick();
          }}
        >
          <span className="flex items-center justify-center gap-2">
            {transcriptCount > 0 ? (
              <>
                Start Asking Questions
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </>
            ) : (
              <>
                Sync Required
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </>
            )}
          </span>
        </button>
      </div>
      
      {/* Hover effect gradient */}
      <div className="h-1 bg-gradient-to-r from-blue-500 via-cyan-500 to-blue-600 rounded-b-lg opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
    </div>
  );
};

export default CourseCard;
