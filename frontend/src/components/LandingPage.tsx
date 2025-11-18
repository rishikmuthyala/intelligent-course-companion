/**
 * Landing Page - Dark, minimal, modern design
 */

import React from 'react';
import { Brain, Sparkles, ArrowRight } from 'lucide-react';

interface LandingPageProps {
  onGetStarted: () => void;
  onGoToSummarize?: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted, onGoToSummarize }) => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-900">
      {/* Simple Header */}
      <nav className="p-6 bg-gray-900/50 backdrop-blur-sm border-b border-gray-800">
        <div className="container mx-auto flex items-center space-x-2">
          <Brain className="w-6 h-6 text-blue-400" />
          <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            AI Course Companion
          </span>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="flex-1 flex items-center justify-center px-4 bg-gray-900">
        <div className="max-w-4xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center px-4 py-2 glass-dark rounded-full text-blue-300 text-sm font-medium mb-8 animate-fade-in">
            <Sparkles className="w-4 h-4 mr-2" />
            Powered by AI
          </div>
          
          {/* Main Heading */}
          <h1 className="text-6xl md:text-8xl font-bold mb-6 leading-tight animate-slide-up text-white">
            Learn
            <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-500 bg-clip-text text-transparent"> Smarter</span>
          </h1>
          
          {/* Subheading */}
          <p className="text-xl md:text-2xl text-gray-400 mb-12 max-w-2xl mx-auto leading-relaxed animate-slide-up" style={{ animationDelay: '0.1s' }}>
            Sync Canvas, generate AI study notes, and chat with your course content
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <button
              onClick={onGetStarted}
              className="group px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white rounded-xl font-semibold text-lg shadow-2xl shadow-blue-900/50 hover:shadow-blue-900/70 hover:scale-105 transition-all flex items-center justify-center"
            >
              Get Started
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
            
            {onGoToSummarize && (
              <button 
                onClick={onGoToSummarize}
                className="px-8 py-4 glass-dark hover:bg-white/10 text-white rounded-xl font-semibold text-lg transition-all flex items-center justify-center border border-gray-700"
              >
                <Sparkles className="mr-2 w-5 h-5" />
                Summarize Transcript
              </button>
            )}
          </div>

          {/* Simple Feature List */}
          <div className="mt-20 grid md:grid-cols-3 gap-6 max-w-3xl mx-auto">
            <Feature 
              title="Auto Sync"
              description="Connect your Canvas account"
            />
            <Feature 
              title="AI Notes"
              description="Get comprehensive study guides"
            />
            <Feature 
              title="Smart Chat"
              description="Ask questions about lectures"
            />
          </div>
        </div>
      </div>

      {/* Simple Footer */}
      <footer className="py-6 text-center text-gray-500 text-sm bg-gray-900 border-t border-gray-800">
        Built with AI for smarter learning
      </footer>
    </div>
  );
};

interface FeatureProps {
  title: string;
  description: string;
}

const Feature: React.FC<FeatureProps> = ({ title, description }) => {
  return (
    <div className="p-6 glass-dark rounded-2xl hover:bg-white/10 transition-all group border border-gray-800">
      <h3 className="text-lg font-bold text-white mb-2 group-hover:text-blue-400 transition-colors">{title}</h3>
      <p className="text-gray-400 text-sm">{description}</p>
    </div>
  );
};

export default LandingPage;
