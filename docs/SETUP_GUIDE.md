# 🚀 Intelligent Course Companion - Complete Setup Guide

## 📋 Prerequisites

Before running the application, you need to gather the following information and install required software:

### Required Accounts & Credentials

1. **Canvas Account** (REQUIRED)
   - Your Canvas username (email)
   - Your Canvas password
   - Access to courses with Echo360 recordings

2. **OpenAI API Key** (REQUIRED)
   - Sign up at https://platform.openai.com/signup
   - Create an API key at https://platform.openai.com/api-keys
   - You'll need billing enabled (costs ~$0.01-0.05 per query)

### Required Software

1. **Python 3.11+**
   - Download from https://www.python.org/downloads/
   - Verify: `python --version`

2. **Node.js 18+**
   - Download from https://nodejs.org/
   - Verify: `node --version`

3. **Git** (optional but recommended)
   - Download from https://git-scm.com/downloads/

---

## 🔧 Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd intelligent-course-companion/backend
```

### Step 2: Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it:
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browser
```bash
# This downloads Chromium for web scraping
playwright install chromium
```

### Step 5: Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
# Copy the example file
cp env.example .env
```

Edit `.env` with your actual values:

```env
# Canvas Configuration
CANVAS_BASE_URL="https://umass.instructure.com"  # Change if different institution
CANVAS_USERNAME="your-email@umass.edu"           # ← YOUR CANVAS EMAIL
CANVAS_PASSWORD="your-canvas-password"           # ← YOUR CANVAS PASSWORD

# OpenAI Configuration
OPENAI_API_KEY="sk-..."                         # ← YOUR OPENAI API KEY

# ChromaDB Configuration (keep default)
CHROMA_PERSIST_DIRECTORY="./chroma_db"

# Application Configuration (keep defaults)
DEBUG_MODE=true
LOG_LEVEL="INFO"
```

⚠️ **IMPORTANT SECURITY NOTES:**
- Never commit the `.env` file to version control
- Keep your API keys secret
- The `.gitignore` file already excludes `.env`

### Step 6: Test Backend Server
```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Test the API by visiting: http://localhost:8000/docs

---

## 🎨 Frontend Setup

### Step 1: Open New Terminal & Navigate to Frontend
```bash
cd intelligent-course-companion/frontend
```

### Step 2: Install Node Dependencies
```bash
npm install
```

### Step 3: Configure Environment Variables

Create a `.env` file in the frontend directory:

```bash
# Copy the example file
cp env.example .env
```

Edit `.env` if needed (default should work):

```env
# Backend API URL
VITE_API_URL=http://localhost:8000  # Change only if backend runs on different port
```

### Step 4: Start Development Server
```bash
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## 🚀 Running the Complete Application

### Start Both Servers:

**Terminal 1 - Backend:**
```bash
cd intelligent-course-companion/backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd intelligent-course-companion/frontend
npm run dev
```

### Access the Application:

Open your browser and navigate to: **http://localhost:5173**

---

## 📝 First Time Usage Guide

### 1. Initial Sync
1. Open the application at http://localhost:5173
2. Click the **"Sync with Canvas"** button
3. The browser will open and log into Canvas automatically
4. **If Multi-Factor Authentication (MFA) is enabled:**
   - Complete the MFA process in the browser window
   - The script will wait for you
5. The sync will download all transcripts (may take 5-30 minutes)
6. The page will auto-refresh when complete

### 2. Ask Questions
1. Click on any course card
2. Type your question in the chat interface
3. Press Enter or click Send
4. The AI will respond using ONLY course materials
5. Click "Show Source Excerpts" to verify the answer

---

## 🔍 Troubleshooting

### Common Issues & Solutions

#### 1. "Canvas credentials not found"
**Solution:** Make sure your `.env` file in `/backend` has:
- `CANVAS_USERNAME="your-email@university.edu"`
- `CANVAS_PASSWORD="your-password"`

#### 2. "OpenAI API key not found"
**Solution:** Add your OpenAI API key to `/backend/.env`:
- `OPENAI_API_KEY="sk-..."`

#### 3. "Failed to load courses"
**Solution:** Check if backend is running:
- Backend should be on http://localhost:8000
- Frontend should be on http://localhost:5173

#### 4. Canvas login fails
**Solution:** 
- Verify credentials are correct
- Check if Canvas URL matches your institution
- Try logging in manually first to check for issues

#### 5. No transcripts found
**Solution:**
- Ensure your courses have Echo360 recordings
- Check if Echo360 link is visible in Canvas course
- Transcripts must be available (not all recordings have them)

#### 6. Port already in use
**Solution:**
- Backend: Change port in `main.py` last line
- Frontend: Change port in `vite.config.ts`

---

## 📁 Project Structure Overview

```
intelligent-course-companion/
│
├── backend/
│   ├── .env                    ← YOUR CREDENTIALS HERE
│   ├── main.py                 # FastAPI server
│   ├── requirements.txt        # Python dependencies
│   └── scripts/
│       ├── scraper.py          # Canvas/Echo360 scraper
│       └── rag_pipeline.py     # AI processing pipeline
│
├── frontend/
│   ├── .env                    ← API URL CONFIG (usually default)
│   ├── package.json            # Node dependencies
│   └── src/
│       ├── components/         # React components
│       ├── services/api.ts     # API client
│       └── App.tsx             # Main app
│
├── transcripts/                # Downloaded transcripts (auto-created)
│   └── [course_id]/
│       └── *.txt
│
└── chroma_db/                  # Vector database (auto-created)
    └── [embeddings]
```

---

## 🔒 Security Checklist

- [ ] Never share your `.env` files
- [ ] Don't commit credentials to Git
- [ ] Keep your OpenAI API key secret
- [ ] Use strong Canvas password
- [ ] Monitor OpenAI usage/costs at https://platform.openai.com/usage

---

## 💰 Cost Estimates

**OpenAI API Costs:**
- GPT-4o-mini: ~$0.00015 per 1K tokens
- Embeddings: ~$0.00002 per 1K tokens
- **Typical usage:** $0.01-0.05 per question
- **Monthly estimate:** $5-20 for moderate use

---

## 📞 Support

If you encounter issues:

1. Check the console logs in both terminals
2. Verify all credentials in `.env` files
3. Ensure both servers are running
4. Check browser console for frontend errors (F12)
5. Review API logs at http://localhost:8000/docs

---

## ✅ Configuration Summary

Here's everything you need to provide:

### Backend `.env` File:
```env
CANVAS_BASE_URL="https://umass.instructure.com"  # Your Canvas URL
CANVAS_USERNAME="your-email@university.edu"      # Your Canvas email
CANVAS_PASSWORD="your-password"                  # Your Canvas password
OPENAI_API_KEY="sk-..."                         # Your OpenAI API key
CHROMA_PERSIST_DIRECTORY="./chroma_db"          # Keep default
DEBUG_MODE=true                                  # Keep default
LOG_LEVEL="INFO"                                # Keep default
```

### Frontend `.env` File:
```env
VITE_API_URL=http://localhost:8000              # Keep default
```

---

## 🎉 Ready to Go!

Once configured, your application will:
1. ✅ Automatically log into Canvas
2. ✅ Download all course transcripts
3. ✅ Process them with AI
4. ✅ Let you ask questions
5. ✅ Provide course-specific answers

Enjoy your Intelligent Course Companion! 🚀
