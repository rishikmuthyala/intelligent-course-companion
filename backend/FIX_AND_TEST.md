# Fix and Test Guide 🔧

## Current Issues Found

1. ❌ **No `.env` file** - Need to create one with credentials
2. ❌ **PDF instead of text** - `scripts/transcripts/Syllabus-Computer Science 360.txt` is a PDF, not text
3. ✅ **Mock data exists** - `mock_transcript.txt` is ready for testing

---

## Quick Fix (5 minutes)

### Step 1: Create .env file

```bash
cd /Users/rishikmuthyala/Desktop/AI\ Course\ Companion/intelligent-course-companion/backend

# Copy the example
cp env.example .env

# Edit with your credentials
nano .env  # or use any text editor
```

Add your actual credentials:
```env
CANVAS_BASE_URL="https://umass.instructure.com"
CANVAS_USERNAME="your_email@umass.edu"
CANVAS_PASSWORD="your_actual_password"
OPENAI_API_KEY="sk-proj-your_actual_key"
```

### Step 2: Run Simple Check

```bash
python simple_test.py
```

This checks if everything is set up correctly.

### Step 3: Run Full Test

```bash
python test_system.py
```

This will:
- ✅ Verify environment variables
- ✅ Test RAG pipeline with mock data
- ✅ Test OpenAI integration
- ✅ Create a test vector database
- ✅ Run a sample query

---

## Testing the Application

### Option A: Test Backend Only

```bash
# Start the FastAPI server
python -m uvicorn main:app --reload
```

Open http://localhost:8000 in your browser - you should see:
```json
{"status":"healthy","service":"Intelligent Course Companion API"}
```

### Option B: Test Full Stack (Backend + Frontend)

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd ../frontend
npm install  # first time only
npm run dev
```

Open http://localhost:5173

---

## Testing the Scraper

### Remove the Bad PDF File First

```bash
rm scripts/transcripts/Syllabus-Computer\ Science\ 360.txt
```

### Run the Ultra Advanced Scraper

```bash
cd scripts
python ultra_advanced_scraper.py
```

This will:
1. Open a browser window (you can watch it work)
2. Log into Canvas
3. Find your courses
4. Navigate to Echo360
5. Download actual text transcripts

**Note:** It saves screenshots to `debug_screenshots/` if you need to debug.

---

## Understanding the Files

### Key Files:

```
backend/
├── main.py                     # FastAPI server
├── .env                        # YOUR CREDENTIALS (create this!)
├── mock_transcript.txt         # Sample data for testing
├── test_system.py             # Full system test
├── simple_test.py             # Quick environment check
├── requirements.txt           # Python dependencies
│
├── scripts/
│   ├── rag_pipeline.py        # RAG: chunks + vector DB
│   ├── advanced_scraper.py    # Basic Canvas scraper
│   ├── ultra_advanced_scraper.py  # Advanced scraper (use this!)
│   └── transcripts/           # Downloaded transcripts go here
│
├── chroma_db/                 # Vector database
└── transcripts/               # Also stores transcripts
```

---

## What Each Test Does

### `simple_test.py`
- Checks if `.env` exists
- Verifies environment variables are set
- Checks if required files exist
- Checks if Python packages are installed

### `test_system.py`
- Runs all checks from `simple_test.py`
- Creates a test course with mock data
- Processes transcripts into vector database
- Runs a sample query: "What is PageRank?"
- Tests OpenAI connection

---

## Expected Results

### ✅ All Tests Pass

You should see:
```
🎉 ALL TESTS PASSED! Your system is ready to use.

TEST SUMMARY
   ✅ PASS: Environment
   ✅ PASS: Mock Transcript
   ✅ PASS: Scraper Files
   ✅ PASS: RAG Pipeline
   ✅ PASS: API Query
```

Then you can:
1. Start the backend: `python -m uvicorn main:app --reload`
2. Start the frontend: `cd ../frontend && npm run dev`
3. Use the app at http://localhost:5173

### ⚠️ Some Tests Fail

Check the error messages and:
1. Verify `.env` file has correct credentials
2. Check OpenAI API key is valid and has credits
3. Run `pip install -r requirements.txt`
4. Run `playwright install chromium`

---

## Common Issues

### "No module named 'playwright'"
```bash
pip install playwright
playwright install chromium
```

### "OpenAI API Error: Invalid API Key"
- Check your key at https://platform.openai.com/api-keys
- Make sure it's in `.env` as: `OPENAI_API_KEY="sk-proj-..."`

### "Scraper downloads PDFs instead of text"
- The scraper is finding syllabus PDFs instead of Echo360 transcripts
- Make sure Echo360 is enabled for your courses
- Use `ultra_advanced_scraper.py` which has better detection

### "No courses found"
- Verify Canvas credentials in `.env`
- Make sure you're enrolled in courses
- Run with `headless=False` to see what's happening

---

## Next Steps After Tests Pass

1. **Run the scraper to get real transcripts:**
   ```bash
   cd scripts
   python ultra_advanced_scraper.py
   ```

2. **Start the backend:**
   ```bash
   python -m uvicorn main:app --reload
   ```

3. **Start the frontend:**
   ```bash
   cd ../frontend
   npm run dev
   ```

4. **Use the app:**
   - Go to http://localhost:5173
   - Click "Sync Courses"
   - Select a course
   - Ask questions!

---

## Debug Tips

- **Check screenshots:** `scripts/debug_screenshots/` shows what the scraper sees
- **Check logs:** The scraper prints detailed logs as it runs
- **Run visible:** Set `headless=False` in scrapers to watch them work
- **Check transcripts:** Look in `scripts/transcripts/` and `transcripts/` for downloaded files
- **Test queries:** Use the `/query/{course_id}` API endpoint directly

---

## Quick Commands Summary

```bash
# Setup
cp env.example .env
nano .env  # Add your credentials
pip install -r requirements.txt
playwright install chromium

# Test
python simple_test.py      # Quick check
python test_system.py      # Full test

# Run Application
python -m uvicorn main:app --reload  # Backend
cd ../frontend && npm run dev         # Frontend

# Run Scraper
cd scripts
python ultra_advanced_scraper.py     # Get transcripts
```

---

Good luck! 🚀

