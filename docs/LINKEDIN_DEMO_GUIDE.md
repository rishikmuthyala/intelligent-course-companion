# 🎓 AI Course Companion - LinkedIn Demo Guide

## Overview

This demo showcases an **AI-powered course Q&A system** that uses **RAG (Retrieval-Augmented Generation)** to answer questions based on lecture transcripts.

### Tech Stack
- **Frontend:** React + TypeScript + Vite + TailwindCSS
- **Backend:** FastAPI (Python)
- **AI:** OpenAI GPT-4o-mini + LangChain
- **Vector DB:** ChromaDB
- **Scraping:** Playwright (for Canvas LMS)

---

## 🚀 Quick Demo Setup (2 minutes)

### Step 1: Setup Demo Data

```bash
cd intelligent-course-companion/backend
python3 setup_demo.py
```

This will:
- ✅ Create sample course transcripts (CS 446: Search Engines, CS 360: Operating Systems)
- ✅ Process them into a vector database
- ✅ Test the query system

### Step 2: Start Backend

```bash
python3 -m uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

### Step 3: Start Frontend (New Terminal)

```bash
cd ../frontend
npm install  # First time only
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 📸 Demo Flow for LinkedIn

### 1. Show the Landing Page
- Clean, professional interface
- Explain: "AI-powered Q&A for course materials"

### 2. Navigate to Chat
- Click "Get Started" or "Chat"
- Shows available courses:
  - CS 446 - Search Engines
  - CS 360 - Computer Systems

### 3. Select a Course and Ask Questions

**For CS 446 (Search Engines):**
- "What is PageRank and how does it work?"
- "How does web crawling work?"
- "Explain the difference between BFS and DFS in crawling"

**For CS 360 (Operating Systems):**
- "What's the difference between processes and threads?"
- "Explain deadlock and how to prevent it"
- "How does CPU scheduling work?"

### 4. Show the AI Response
- Highlight the **relevant context** found from transcripts
- Show the **AI-generated answer** (clear, accurate, sourced)
- Point out: "Answers are grounded in actual lecture content"

### 5. Show the Sync Feature (Optional)
- Click "Sync Courses"
- Explain: "In production, this scrapes Canvas LMS automatically"
- For demo: "Using pre-loaded sample transcripts"

---

## 🎬 LinkedIn Post Template

### Option 1: Technical Focus

```
🚀 Built an AI-Powered Course Companion using RAG! 

Ever struggled to review hours of lecture content before an exam? 
I built a solution using:

🔹 RAG (Retrieval-Augmented Generation) architecture
🔹 OpenAI GPT-4o-mini for answer synthesis
🔹 ChromaDB vector database for semantic search
🔹 FastAPI backend + React frontend
🔹 Automated Canvas LMS scraping

The system:
✅ Extracts lecture transcripts automatically
✅ Chunks and embeds them in a vector database
✅ Retrieves relevant context for user questions
✅ Generates accurate answers grounded in course material

[Demo video/screenshots]

Tech: Python, TypeScript, OpenAI, LangChain, ChromaDB, FastAPI, React

#AI #MachineLearning #RAG #WebDevelopment #OpenAI #Python #React
```

### Option 2: Problem-Solution Focus

```
📚 From Hours of Lecture Review to Instant Answers

Challenge: Students spend hours rewatching lectures to find specific information

Solution: AI Course Companion - Ask questions, get instant answers from your lecture transcripts!

How it works:
1️⃣ Automatically scrapes lecture transcripts from Canvas LMS
2️⃣ Processes them using vector embeddings
3️⃣ Semantic search finds relevant context
4️⃣ AI generates accurate, sourced answers

Built with: React, FastAPI, OpenAI, ChromaDB, LangChain

Try asking: "What is PageRank?" or "Explain deadlock in OS"
The AI pulls exact information from lecture transcripts! 

[Demo video/screenshots]

#EdTech #AI #StudentLife #RAG #OpenAI #WebDev
```

### Option 3: Storytelling

```
💡 Turned My Study Frustration Into an AI Solution

Last semester, I spent hours scrubbing through lecture recordings looking for one specific explanation. There had to be a better way.

So I built it. ⚡

Introducing: AI Course Companion
→ Upload/sync lecture transcripts
→ Ask questions in natural language  
→ Get instant, accurate answers with source citations

Powered by:
• RAG (Retrieval-Augmented Generation)
• OpenAI GPT-4o-mini
• ChromaDB vector database
• Custom Canvas LMS scraper

The best part? Answers are grounded in actual lecture content - no hallucinations!

[Demo screenshots showing before/after]

What problem would YOU solve with AI? 

#AI #RAG #EdTech #BuildInPublic #Python #React
```

---

## 📷 Screenshot Suggestions

### Screenshot 1: Landing Page
- Show clean, professional UI
- Highlight "Get Started" button
- Caption: "Clean, intuitive interface for students"

### Screenshot 2: Course Selection
- Show list of available courses
- Caption: "Supports multiple courses"

### Screenshot 3: Question & Answer
- Show a question like "What is PageRank?"
- Show the full AI response
- Highlight source chunks
- Caption: "AI-powered answers grounded in lecture transcripts"

### Screenshot 4: Technical Architecture (Optional)
- Create a simple diagram:
  ```
  User Query → Backend API → Vector DB Search → Context → GPT-4 → Answer
  ```

---

## 🎥 Video Demo Script (30-60 seconds)

```
[0:00-0:10] Landing page
"I built an AI assistant that helps students review course material"

[0:10-0:20] Select course
"Select a course - let's try Search Engines"

[0:20-0:30] Type question
"Ask any question - like 'What is PageRank?'"

[0:30-0:45] Show answer
"The AI searches lecture transcripts and generates accurate answers"

[0:45-0:55] Show source context
"Answers are grounded in actual lecture content - no hallucinations"

[0:55-1:00] End screen
"Built with OpenAI, LangChain, and ChromaDB. Link in bio!"
```

---

## 💡 Key Points to Emphasize

1. **Real Problem Solved**: Students struggle to review hours of lectures
2. **Technical Innovation**: RAG prevents AI hallucinations by grounding answers in real data
3. **Full-Stack**: Frontend + Backend + AI + Database + Web Scraping
4. **Production-Ready**: Automated syncing, error handling, scalable architecture
5. **Open Source Ready**: Clean code, well-documented, extensible

---

## 🔥 Demo Questions That Look Impressive

### CS 446 - Search Engines
1. "What is PageRank and how was it revolutionary?"
2. "Explain the difference between web crawling and web scraping"
3. "What is an inverted index?"
4. "How do search engines handle politeness in crawling?"

### CS 360 - Operating Systems  
1. "What's the difference between processes and threads?"
2. "Explain the four conditions required for deadlock"
3. "How does the round-robin scheduling algorithm work?"
4. "What is a context switch and why is it expensive?"

---

## 🎯 Call to Action Ideas

- "Check out the code on GitHub: [your link]"
- "Built this in 2 weeks - DM me if you want to collaborate!"
- "What would YOU build with RAG? Drop ideas below 👇"
- "Hiring? I'm open to ML Engineer / Full-Stack opportunities!"
- "Follow for more AI projects and tutorials"

---

## 📊 Metrics to Mention (If Tested)

- "Processes X lectures in Y seconds"
- "Achieves Z% accuracy on test questions"
- "Searches database of X chunks in <100ms"
- "Handles Y concurrent users"

---

## 🚀 Advanced Demo Features (If Implemented)

- Real-time sync progress
- Source citations with timestamps
- Multiple courses
- Conversation history
- Export answers

---

## 🎨 Visual Tips

- Use **dark mode** (looks more professional)
- **Record in HD** (1080p minimum)
- Use **screen recording tools** like:
  - macOS: QuickTime or Cmd+Shift+5
  - Windows: Xbox Game Bar or OBS
  - Chrome: Loom extension
- **Edit** to remove waiting/loading time
- Add **captions** for accessibility
- Use **arrows or highlights** to draw attention

---

## 📝 Alternative: Screenshot Demo

If you prefer images over video:

1. **Cover image**: Landing page with logo
2. **Image 1**: Course selection screen
3. **Image 2**: Question input + AI response  
4. **Image 3**: Source context shown
5. **Image 4**: Architecture diagram or code snippet
6. **Final image**: "Link to GitHub" or "DM for details"

---

## 🎓 Resume/Portfolio Talking Points

- "Implemented RAG architecture using OpenAI and LangChain"
- "Built automated web scraper with Playwright for Canvas LMS"
- "Designed full-stack application with React and FastAPI"
- "Integrated ChromaDB vector database for semantic search"
- "Achieved <100ms query response time"
- "Handled asynchronous operations and background tasks"

---

## 🏆 Why This Project Stands Out

1. **Real-world application** - Actually solves a problem
2. **Multiple technologies** - Full-stack + AI + DB + Scraping
3. **Production-ready** - Error handling, async, scalable
4. **Trendy tech** - RAG is hot in 2024/2025
5. **Impressive demo** - Easy to show, hard to build

---

Good luck with your demo! 🚀

Remember: The best LinkedIn posts are authentic. Share YOUR journey building this!

