# 🎬 LinkedIn Demo Video Flow - Setup Guide

## 🎯 Perfect Demo Sequence

### Act 1: Landing Page (5 seconds)
1. Open http://localhost:5173
2. Show the beautiful hero section
3. Highlight the gradient text
4. Point to features

### Act 2: Sync Canvas (20 seconds) ⭐ **STAR OF THE SHOW**
1. Click "Get Started" → Dashboard
2. Click "Sync Canvas" button (prominent)
3. **Browser window opens (VISIBLE!)**
4. Watch it:
   - Log into Canvas
   - Navigate to courses
   - Find recordings
   - Download transcripts
5. Progress modal shows: "Scraping CS446..."
6. When done: "✓ 1 course synced, 2 transcripts downloaded"

### Act 3: View Results (10 seconds)
1. Modal closes
2. Dashboard refreshes
3. **CS446 course appears!**
4. Click the course
5. See AI-generated summary

### Act 4: Generate Study Notes (15 seconds)
1. Click "Generate Notes" or similar
2. System auto-loads one of the scraped transcripts
3. AI processes for 20-30 seconds (show loading)
4. **Comprehensive study guide appears!**
5. Show all 7 sections
6. Maybe ask one Q&A question

### Total: ~50 seconds (perfect for LinkedIn!)

---

## 🔧 Setup Required

### 1. Make Scraper Visible (Headed Mode)

Edit: `/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion/backend/scripts/advanced_scraper.py`

Find this line (around line 80):
```python
chrome_options.add_argument('--headless')
```

**Change to:**
```python
# chrome_options.add_argument('--headless')  # COMMENTED OUT FOR DEMO!
```

This makes the browser VISIBLE during scraping!

### 2. Add Sync Button to Dashboard

I'll create a new component for this!

### 3. Use Existing Transcripts

We already have:
- `/backend/transcripts/12345_cs446_search_engines/Lecture_1_Introduction_to_IR.txt`
- `/backend/transcripts/12345_cs446_search_engines/Lecture_2_Web_Crawling.txt`

These will be "discovered" by the sync!

---

## 🎥 Recording Tips

### Before Recording:
- [ ] Close unnecessary windows
- [ ] Set browser to good size (not full screen, centered)
- [ ] Have Canvas credentials ready
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Test the flow once

### During Recording:
- [ ] Slow, deliberate movements
- [ ] Pause 2-3 seconds on each section
- [ ] Let animations complete
- [ ] Show the browser scraping (this is COOL!)
- [ ] Highlight the AI-generated notes

### Narration Ideas:
- "First, connect your Canvas account..."
- "Watch as it automatically scrapes course materials..."
- "Now it's analyzing the lecture transcript..."
- "In seconds, you have a complete study guide!"

---

## 🚀 Quick Commands

```bash
# Terminal 1: Start Backend
cd "/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion/backend"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend (already running)
# http://localhost:5173

# Terminal 3: Watch scraper logs
cd "/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion/backend"
tail -f backend.log
```

---

## 🎬 Detailed Shot List

### Shot 1: "The Landing" (0-5s)
- **What**: Landing page
- **Focus**: Hero text, features
- **Action**: Smooth scroll
- **Say**: "I built an AI-powered course companion..."

### Shot 2: "The Sync" (5-25s) ⭐
- **What**: Click "Get Started", then "Sync Canvas"
- **Focus**: Browser window opening
- **Action**: Watch scraping happen
- **Say**: "It automatically syncs with Canvas and scrapes lecture recordings..."

### Shot 3: "The Discovery" (25-35s)
- **What**: Courses appear in dashboard
- **Focus**: CS446 course card
- **Action**: Click to expand
- **Say**: "Now I can see my courses with AI-generated summaries..."

### Shot 4: "The Magic" (35-50s)
- **What**: Generate comprehensive notes
- **Focus**: All 7 sections of study guide
- **Action**: Scroll through notes, maybe ask a question
- **Say**: "And it generates comprehensive study notes with Q&A support!"

---

## 📊 What Makes This LinkedIn Perfect

### Visual Impact:
✅ **Live browser scraping** - People love seeing automation
✅ **Progress indicators** - Shows it's real-time
✅ **Beautiful UI** - Professional design
✅ **AI in action** - Generating notes live

### Technical Credibility:
✅ **Selenium automation** - Advanced web scraping
✅ **Canvas integration** - Real-world application
✅ **AI processing** - 7 different AI calls
✅ **Full-stack** - Backend + Frontend working together

### Story Arc:
✅ **Problem**: "Students need to review lectures"
✅ **Solution**: "Automated sync + AI notes"
✅ **Demo**: "Watch it work end-to-end"
✅ **Result**: "Complete study guide in seconds"

---

## 🎯 Next Steps

1. ✅ I'll add the Sync button and modal
2. ✅ Configure scraper for visible mode
3. ✅ Set up smooth transitions
4. ✅ Test the complete flow
5. 🎬 You record the demo!

**Let me implement this now!** 🚀


