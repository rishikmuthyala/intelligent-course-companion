# Complete Demo Flow - AI Course Companion

## 🎯 Overview
This document describes the complete end-to-end flow of the AI Course Companion application, from Canvas sync to interactive Q&A.

## 📋 Complete Flow Steps

### 1. **Landing Page** → **Canvas Sync**
- User clicks "Get Started" button
- Navigates to SyncPage component
- Real Canvas scraper (`ultra_advanced_scraper.py`) runs in background
- Shows live progress with status updates
- Polls backend `/sync/status` API every 3 seconds

### 2. **Scraping Process**
- Backend runs `ultra_advanced_scraper.py` via `/sync` endpoint
- Authenticates with Canvas using Microsoft SSO
- Navigates through courses looking for Echo360/Class Recordings
- Downloads transcript `.txt` files to `backend/transcripts/`
- Updates status in real-time

### 3. **Post-Scraping: Dashboard Display**
- **Only CS 446 course shown** with "1 lecture transcript downloaded"
- Course ID: `cs446_search_engines`
- Transcript file: `backend/transcripts/cs446_search_engines/Lecture_1_Introduction.txt`
- File was copied from your Desktop to this location

### 4. **Auto-Summarize Flow**
When user clicks on CS 446 course:
- Dashboard → `handleCourseWithTranscript()` triggered
- Navigates to TranscriptSummarizePage with `autoLoadCourse` prop
- Component auto-loads transcript via `/api/transcripts/{course_id}/{filename}`
- Automatically triggers summarization (500ms delay)
- Calls `/summarize` endpoint with full transcript text

### 5. **Summarization Process**
Backend (`main.py` `/summarize` endpoint) uses GPT-4o-mini to generate:
- **Executive Summary**: 2-3 paragraph overview
- **Detailed Notes**: Comprehensive study notes organized by topics
- **Key Points**: 7 most important takeaways
- **Topics**: Main themes covered (lowercase, comma-separated)
- **Important Concepts**: 5-8 key terms to understand
- **Study Tips**: 3-5 recommendations for mastering material
- **Practice Questions**: 5 questions to test understanding

### 6. **Notes Display**
TranscriptSummarizePage shows:
- Topics covered (as colored tags)
- Executive summary section
- Key takeaways (numbered list)
- Detailed study notes (full content)
- Concepts to master
- Study tips
- Practice questions
- Copy and download buttons

### 7. **Interactive Q&A**
Below the notes, user can:
- Ask follow-up questions about the lecture
- Backend retrieves relevant context
- GPT-4o-mini generates detailed answers based on transcript
- Questions/answers displayed in chat format
- Session-based (questions tied to specific transcript)

## 🔧 Technical Implementation

### Frontend Components Modified
1. **SyncPage.tsx**
   - Now returns only CS 446 course with `hasTranscript: true`
   - Removed multiple course fallback

2. **DashboardPage.tsx**
   - Added `onCourseWithTranscriptSelect` prop
   - Triggers auto-summarize when course with transcript is clicked

3. **App.tsx**
   - Added `handleCourseWithTranscript()` handler
   - Passes `autoLoadCourse` prop to TranscriptSummarizePage

4. **TranscriptSummarizePage.tsx**
   - Added `autoLoadCourse` prop (optional)
   - `useEffect` hook auto-loads transcript when prop is provided
   - Auto-triggers summarization button after 500ms

5. **Course Type**
   - Added optional `hasTranscript?: boolean` field

### Backend Endpoints
1. **GET `/api/transcripts/{course_id}/{filename}`** *(NEW)*
   - Serves transcript files for auto-loading
   - Returns plain text content
   - Path: `backend/transcripts/{course_id}/{filename}`

2. **POST `/summarize`**
   - Accepts transcript text
   - Returns comprehensive summary object
   - Creates session ID for Q&A

3. **POST `/followup`**
   - Accepts session ID and question
   - Returns AI-generated answer based on transcript

## 📁 File Structure
```
backend/
  transcripts/
    cs446_search_engines/
      Lecture_1_Introduction.txt  ← Your COMPSCI 446 transcript
  main.py                         ← Added /api/transcripts endpoint
  scripts/
    ultra_advanced_scraper.py     ← Canvas scraper
    rag_pipeline.py               ← Q&A processing

frontend/
  src/
    components/
      SyncPage.tsx                ← Shows only CS 446 course
      DashboardPage.tsx           ← Triggers auto-summarize
      TranscriptSummarizePage.tsx ← Auto-loads and summarizes
    App.tsx                       ← Routes to summarize page
    types/index.ts                ← Added hasTranscript field
```

## 🚀 Testing the Flow

1. **Start Backend**:
   ```bash
   cd backend
   python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Flow**:
   - Visit http://localhost:5173
   - Click "Get Started"
   - Wait for sync to complete
   - Dashboard shows: "COMPSCI 446 - Search Engines" with "1 lecture transcript downloaded"
   - Click the course card
   - Transcript auto-loads from your Desktop file
   - Summarization starts automatically
   - Full notes displayed with all sections
   - Ask questions in the Q&A section below

## 🎨 UI Theme
- **Dark theme** throughout (bg-gray-900, bg-gray-800)
- **Blue/cyan gradient** accents (from-blue-600 to-cyan-600)
- **No purple** - replaced all with blue tones
- Modern, glassmorphic design with backdrop blur effects

## 📊 API Flow Diagram
```
User clicks "Get Started"
    ↓
SyncPage → POST /sync → ultra_advanced_scraper.py runs
    ↓                                              ↓
    └─ Poll GET /sync/status ←────────────────────┘
    ↓
Complete → Dashboard (show CS 446 only)
    ↓
User clicks CS 446 course
    ↓
App.tsx → handleCourseWithTranscript()
    ↓
TranscriptSummarizePage
    ↓
GET /api/transcripts/cs446_search_engines/Lecture_1_Introduction.txt
    ↓
Auto-click summarize button
    ↓
POST /summarize (with transcript text)
    ↓
Display full notes layout
    ↓
User asks question
    ↓
POST /followup → GPT-4o-mini answer
```

## ✅ Completed Features
- [x] Canvas sync with real scraper
- [x] Show only CS 446 course on dashboard
- [x] Copy transcript from Desktop to backend
- [x] Auto-load transcript when course clicked
- [x] Auto-trigger summarization
- [x] Display comprehensive notes
- [x] Interactive Q&A with session tracking
- [x] Dark theme with blue accents throughout
- [x] Backend endpoint to serve transcript files

## 🎓 Your Transcript
- **Source**: `/Users/rishikmuthyala/Desktop/COMPSCI 446-1257-615-transcript.txt`
- **Destination**: `backend/transcripts/cs446_search_engines/Lecture_1_Introduction.txt`
- **Size**: 56KB
- **Content**: COMPSCI 446 lecture on search engines and information retrieval

## 🔮 Next Steps (Optional)
- Add more lectures from CS 446
- Support multiple courses after sync
- Real-time transcript upload during sync
- Progress indicators for summarization stages
- Save summaries to database for quick access
- Export notes as PDF

