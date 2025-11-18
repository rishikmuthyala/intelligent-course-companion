# Quick Start Guide - Ultra-Advanced Canvas Scraper

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
cd "intelligent-course-companion/backend/scripts"
pip install playwright python-dotenv
playwright install chromium
```

### 2. Configure Credentials
Create a file named `.env` in the `backend` directory with your credentials:
```
CANVAS_USERNAME=your_email@umass.edu
CANVAS_PASSWORD=your_password
CANVAS_BASE_URL=https://umass.instructure.com
```

### 3. Run the Scraper
```bash
python run_ultra_scraper.py
```

Or specify a course:
```bash
python run_ultra_scraper.py "COMPSCI 446"
```

## ⚡ What Happens

1. **Browser Opens**: You'll see a browser window open automatically
2. **Login**: The scraper logs into Canvas (may need MFA - complete it manually)
3. **Navigation**: Finds and clicks on your course
4. **Echo360**: Locates class recordings/Echo360 link
5. **Download**: For each lecture, opens transcript panel and downloads .txt file
6. **Screenshots**: Takes screenshots at every step for debugging

## 📂 Output Files

- **Transcripts**: `./transcripts/*.txt` - Your downloaded transcripts
- **Screenshots**: `./debug_screenshots/*.png` - Debug screenshots
- **History**: `./debug_screenshots/navigation_history.json` - Navigation log

## 🔧 If It Fails

1. Look at the screenshots in `debug_screenshots/` folder
2. Find the last screenshot (highest number)
3. That shows where it got stuck
4. Share that screenshot if you need help

## 💡 Key Features

✅ **Exhaustive Search**: Checks everywhere on page for buttons/links
✅ **Auto-Retry**: Tries 3 times with different strategies
✅ **Smart Detection**: Finds elements by text, labels, classes
✅ **Error Recovery**: Handles pop-ups, modals, timeouts automatically
✅ **Full Logging**: Shows exactly what it's doing
✅ **Debug Screenshots**: Visual record of every step

## 🎯 Advanced Options

### Run in Background (Headless)
Edit `run_ultra_scraper.py` line 34:
```python
headless=True,  # Changed from False
```

### Process More Lectures
Edit `ultra_advanced_scraper.py` line 585:
```python
max_lectures = 20  # Change from 10
```

### Increase Timeout
Edit `ultra_advanced_scraper.py` line 34-36:
```python
BROWSER_TIMEOUT = 60000  # 60 seconds
LOGIN_TIMEOUT = 120000   # 120 seconds
```

## 📋 Common Issues

| Issue | Solution |
|-------|----------|
| Login fails | Check `.env` credentials, complete MFA if prompted |
| Can't find Echo360 | Check screenshot, link might have different name |
| No transcript button | Review video page screenshot |
| Download fails | Check transcript panel screenshot |

## 🆘 Get Help

If stuck:
1. Share the console output
2. Share the last few screenshots (highest numbers)
3. Share `navigation_history.json` file

## 📞 Need Screenshots?

Yes! If you encounter errors or the scraper gets stuck, please share:
- The console output (copy everything)
- Screenshots from `debug_screenshots/` folder (especially the last 3-4)
- The error message

This will help me understand exactly where it's failing and fix it!

---

**Read the full guide**: See `SCRAPER_GUIDE.md` for detailed documentation


