# 📸 Screenshots & Demo Video Guide

This guide will help you add professional screenshots and demo video to your README.

---

## 🎬 Adding Your Demo Video

### Option 1: GitHub Video Upload (Recommended)

1. **Record your demo** (2-3 minutes showing the complete flow)
2. **Go to a GitHub issue** or pull request in your repo
3. **Drag and drop** your video file into the comment box
4. GitHub will upload it and generate a URL like:
   ```
   https://github.com/user-attachments/assets/abc123...
   ```
5. **Copy this URL** and replace the placeholder in README.md:
   ```markdown
   https://github.com/user-attachments/assets/your-video-id-here
   ```

### Option 2: YouTube

1. **Upload to YouTube** (can be unlisted)
2. **Get the share link**
3. **Embed in README**:
   ```markdown
   [![Demo Video](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)
   ```

### Option 3: Loom

1. **Record with Loom** (free)
2. **Get the share link**
3. **Add to README**:
   ```markdown
   [🎬 Watch Demo on Loom](https://www.loom.com/share/your-video-id)
   ```

---

## 📸 Adding Screenshots

### Recommended Screenshots to Capture:

1. **Landing Page** (`1-landing.png`)
   - Show the homepage with "Get Started" button
   - Capture the modern gradient design

2. **Canvas Sync** (`2-sync.png`)
   - Show the sync progress animation
   - Include the status messages

3. **Dashboard** (`3-dashboard.png`)
   - Display the CS 446 course card
   - Show statistics and course info

4. **Summarization** (`4-summarize.png`)
   - Show the transcript upload/auto-load
   - Display AI-generated summary notes

5. **Q&A Chat** (`5-chat.png`)
   - Show a conversation with the AI
   - Include both questions and answers

### How to Add Screenshots:

#### Method 1: Create `screenshots/` folder

```bash
cd intelligent-course-companion
mkdir -p .github/screenshots
```

Then add images:
```
.github/
└── screenshots/
    ├── 1-landing.png
    ├── 2-sync.png
    ├── 3-dashboard.png
    ├── 4-summarize.png
    └── 5-chat.png
```

Update README.md:
```markdown
### 🏠 Landing Page
![Landing Page](.github/screenshots/1-landing.png)

### 🔄 Canvas Sync
![Sync Page](.github/screenshots/2-sync.png)

### 📊 Dashboard
![Dashboard](.github/screenshots/3-dashboard.png)

### 📝 AI Summarization
![Summarization](.github/screenshots/4-summarize.png)

### 💬 Interactive Q&A
![Chat Interface](.github/screenshots/5-chat.png)
```

#### Method 2: Use GitHub Issues (Quick & Easy)

1. Go to any GitHub issue or PR
2. Drag and drop screenshot
3. GitHub generates a URL
4. Copy and paste into README

---

## 📹 Demo Video Script (Suggested)

**Duration: 2-3 minutes**

### 1. Introduction (0:00 - 0:15)
- "Hi, I'm [Your Name], and this is AI Course Companion"
- "An intelligent platform that transforms lecture recordings into interactive study sessions"

### 2. Landing Page (0:15 - 0:25)
- Show the landing page
- "Modern, intuitive interface with dark theme"
- Click "Get Started"

### 3. Canvas Sync (0:25 - 0:45)
- Show sync animation
- "Automatically syncs with Canvas LMS"
- "Advanced web scraping reaches Echo360 recordings"

### 4. Dashboard (0:45 - 1:00)
- Show course cards
- "Here's my CS 446 course with a lecture transcript"
- Click on the course

### 5. Auto-Summarization (1:00 - 1:30)
- Show transcript loading
- "The system automatically loads the 10,000+ word transcript"
- Show AI-generated summary appearing
- "GPT-4 with RAG generates comprehensive notes"
- Highlight key features

### 6. Q&A Demo (1:30 - 2:30)
- Scroll to Q&A section
- Ask 2-3 questions:
  - "What are the main topics covered in this lecture?"
  - "Explain information retrieval"
  - "What did the professor say about search algorithms?"
- Show AI responses

### 7. Conclusion (2:30 - 2:45)
- "Built with FastAPI, React, GPT-4, and ChromaDB"
- "Perfect for students who want to study smarter"
- "Check out the repo on GitHub!"

---

## 🎨 Screenshot Tips

### Quality
- **Resolution**: 1920x1080 or higher
- **Format**: PNG for UI, JPG for photos
- **Compression**: Use TinyPNG to reduce file size

### Capture Tools
- **Mac**: Cmd+Shift+4 (select area)
- **Windows**: Win+Shift+S (Snipping Tool)
- **Chrome**: DevTools → More tools → Screenshot

### Professional Touches
- Clean browser (close unnecessary tabs)
- Full screen capture or specific component
- Hide personal information
- Good lighting if capturing setup

### Annotations (Optional)
- Use tools like Skitch or Markup
- Add arrows pointing to key features
- Highlight important sections
- Keep it minimal and clean

---

## 🚀 After Adding Media

### Commit Changes

```bash
git add README.md .github/screenshots/
git commit -m "docs: Add demo video and screenshots"
git push origin main
```

### Test Display

1. View your GitHub repo
2. Check that images load correctly
3. Verify video plays properly
4. Test on mobile view

---

## ✅ Checklist

- [ ] Record demo video (2-3 minutes)
- [ ] Upload video to GitHub/YouTube/Loom
- [ ] Update README.md with video URL
- [ ] Capture landing page screenshot
- [ ] Capture sync page screenshot
- [ ] Capture dashboard screenshot
- [ ] Capture summarization screenshot
- [ ] Capture chat interface screenshot
- [ ] Create `.github/screenshots/` folder
- [ ] Add all screenshots
- [ ] Update README.md with image paths
- [ ] Commit and push to GitHub
- [ ] Verify everything displays correctly

---

**Need help?** Check out [GitHub's guide to images and videos](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images)

