# Quick Test Guide - AI Course Companion

## 🚀 Quick Start (5 minutes)

### Step 1: Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd intelligent-course-companion/backend
cp .env.template .env
```

Then edit `.env` and add:
- Your **Canvas username** (UMass email)
- Your **Canvas password**
- Your **OpenAI API key** (get from https://platform.openai.com/api-keys)

### Step 2: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers (for scraping)
playwright install chromium
```

### Step 3: Run the Test

```bash
cd intelligent-course-companion/backend
python test_system.py
```

This will:
✅ Check your environment variables
✅ Test the RAG pipeline with mock data
✅ Verify OpenAI connection
✅ Create a test vector database

---

## 📝 Testing the Full Application

### Test 1: Backend API Only

```bash
cd intelligent-course-companion/backend
python -m uvicorn main:app --reload
```

Then open http://localhost:8000 - you should see:
```json
{"status":"healthy","service":"Intelligent Course Companion API"}
```

### Test 2: Backend + Frontend

**Terminal 1 (Backend):**
```bash
cd intelligent-course-companion/backend
python -m uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd intelligent-course-companion/frontend
npm install  # First time only
npm run dev
```

Then open http://localhost:5173 in your browser.

---

## 🔍 Testing the Scraper

### Option 1: Test with Ultra Advanced Scraper (Recommended)

```bash
cd intelligent-course-companion/backend/scripts
python ultra_advanced_scraper.py
```

This will:
1. Open a browser (you can see what's happening)
2. Log into Canvas
3. Navigate through courses
4. Download transcripts from Echo360

### Option 2: Test with Basic Scraper

```bash
cd intelligent-course-companion/backend
python -m scripts.advanced_scraper
```

---

## 🐛 Troubleshooting

### Issue: "PDF downloaded instead of text transcript"

**Problem:** The scraper is downloading PDF syllabuses instead of Echo360 transcripts.

**Solution:** 
1. Make sure Echo360 is enabled for your course
2. Check that lectures have been recorded and transcripts are available
3. The ultra_advanced_scraper.py has better Echo360 detection

### Issue: "No courses found"

**Solution:**
1. Verify Canvas credentials in `.env`
2. Make sure you're enrolled in courses
3. Try running with `headless=False` to see what's happening

### Issue: "OpenAI API error"

**Solution:**
1. Check your API key is correct
2. Verify you have credits: https://platform.openai.com/account/usage
3. Make sure the key starts with `sk-proj-...` or `sk-...`

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
pip install -r requirements.txt
playwright install chromium
```

---

## ✅ What Should Work Now

After running `test_system.py` successfully:

1. ✅ **RAG Pipeline:** Can chunk and store documents in ChromaDB
2. ✅ **Vector Search:** Can find relevant context for queries
3. ✅ **OpenAI Integration:** Can generate answers from context
4. ✅ **Backend API:** FastAPI server can handle requests

---

## 🎯 Next Steps

1. **Run the test:** `python test_system.py`
2. **If all pass:** Start the full app (backend + frontend)
3. **If scraper needed:** Run `ultra_advanced_scraper.py` to get real transcripts
4. **Test queries:** Use the frontend to ask questions about your courses

---

## 📊 Known Issues & Fixes

### Current Transcript File is a PDF

The file at `backend/scripts/transcripts/Syllabus-Computer Science 360.txt` is actually a PDF, not text.

**To fix:**
1. Delete it: `rm backend/scripts/transcripts/Syllabus-Computer\ Science\ 360.txt`
2. Run the scraper to get real transcripts
3. Or use the mock_transcript.txt for testing

### Scraper Gets Stuck

If the scraper hangs:
1. Press `Ctrl+C` to stop
2. Check the debug screenshots: `backend/scripts/debug_screenshots/`
3. Run with `headless=False` to watch what's happening
4. Use `ultra_advanced_scraper.py` which has better error recovery

---

## 💡 Tips

- Start with `test_system.py` to verify basic functionality
- Use mock_transcript.txt for testing without scraping
- Check debug screenshots if scraper fails
- Run scrapers with `headless=False` to see what's happening
- Use the `/sync/status` API endpoint to monitor scraping progress

---

Need help? Check:
- `backend/README.md`
- `backend/scripts/SCRAPER_GUIDE.md`
- Debug screenshots in `backend/scripts/debug_screenshots/`

