# 📹 How to Embed Video Directly in README

Your demo video is currently linked in the README. To make it **auto-play inline** in your GitHub README, follow these steps:

---

## ✅ Best Method: GitHub Issue Upload (Recommended)

This makes your video auto-play directly in the README!

### Step 1: Upload Video via GitHub Issue

1. **Push your repo to GitHub first** (if you haven't already)
   ```bash
   cd "/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion"
   git remote add origin https://github.com/rishikmuthyala/ai-course-companion.git
   git push -u origin main
   ```

2. **Go to your repo** on GitHub:
   ```
   https://github.com/rishikmuthyala/ai-course-companion
   ```

3. **Click "Issues" tab** → **"New Issue"**

4. **Title**: "Demo Video" (or anything)

5. **In the comment box**: 
   - Drag and drop your `demo.mp4` file
   - OR click the attachment area to browse and upload
   - GitHub will upload it and show something like:
     ```
     Uploading demo.mp4…
     ```
   - Wait for it to complete

6. **GitHub generates a URL** that looks like:
   ```
   https://github.com/user-attachments/assets/a1b2c3d4-e5f6-7890-abcd-ef1234567890/demo.mp4
   ```
   
7. **Copy this entire URL** (including the video filename)

8. **You can close/cancel the issue** (don't need to create it)

---

### Step 2: Update README with the GitHub URL

Replace the video section in `README.md`:

**Current:**
```markdown
https://github.com/rishikmuthyala/ai-course-companion/assets/demo.mp4
```

**Replace with the URL from step 6:**
```markdown
https://github.com/user-attachments/assets/YOUR-UNIQUE-ID-HERE/demo.mp4
```

**Full example:**
```markdown
## 🎬 Demo Video

<div align="center">

### 📹 Watch the Full Demo

https://github.com/user-attachments/assets/a1b2c3d4-e5f6-7890-abcd-ef1234567890/demo.mp4

**See the complete flow:** Canvas Sync → Web Scraping → Auto-Summarization → Interactive Q&A

</div>
```

---

### Step 3: Commit and Push

```bash
cd "/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion"
git add README.md
git commit -m "docs: Update README with embedded demo video"
git push origin main
```

---

## 🎥 Result

Your video will now **auto-play** directly in the README! 

Visitors will see:
- ▶️ Play button overlay
- Video player embedded inline
- No need to download
- Professional presentation

---

## 🔄 Alternative: Keep Current Setup

Your current setup works great too! It provides:
- ✅ Direct download link
- ✅ Git LFS efficiency
- ✅ Clear call-to-action
- ✅ No GitHub bandwidth limits

**Current video URL:**
```
https://github.com/rishikmuthyala/ai-course-companion/raw/main/.github/demo/demo.mp4
```

This is perfectly fine for recruiters - they can click to download and watch!

---

## 💡 Pro Tips

### Option 1: Both Methods
Use BOTH approaches:
```markdown
## 🎬 Demo Video

<!-- Embedded video (auto-plays) -->
https://github.com/user-attachments/assets/YOUR-ID/demo.mp4

[⬇️ Download Full Quality](https://github.com/rishikmuthyala/ai-course-companion/raw/main/.github/demo/demo.mp4)
```

### Option 2: YouTube/Loom (Best for recruiters)
Upload to YouTube (unlisted) or Loom:

```markdown
## 🎬 Demo Video

[![Watch Demo](https://img.shields.io/badge/▶️_Watch_Demo-YouTube-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

<div align="center">
  <a href="https://www.youtube.com/watch?v=YOUR_VIDEO_ID">
    <img src="https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg" alt="Demo Video" width="80%">
  </a>
</div>
```

Benefits:
- ✅ Better video player
- ✅ Plays on mobile
- ✅ No file size concerns
- ✅ Professional thumbnail
- ✅ Can add captions/chapters

### Option 3: Animated GIF Preview
Create a GIF of key moments:

```markdown
## 🎬 Demo Video

![Demo Preview](https://github.com/rishikmuthyala/ai-course-companion/raw/main/.github/demo/preview.gif)

[📹 Watch Full Demo (30MB)](https://github.com/rishikmuthyala/ai-course-companion/raw/main/.github/demo/demo.mp4)
```

---

## 🎯 Recommendation

**For your portfolio:**

1. **Immediate:** Keep current setup (works great!)
2. **After push:** Try the GitHub Issue upload method for inline playback
3. **Optional:** Also upload to YouTube for maximum compatibility

**All three approaches are professional and recruiter-friendly!** ✅

---

## ❓ FAQ

**Q: Will the Git LFS video play in README?**
A: Not directly. GitHub requires videos to be uploaded via Issues/PRs to get an embed URL that auto-plays.

**Q: Should I use both Git LFS and Issue upload?**
A: Yes! Keep LFS for version control, use Issue upload URL for README embedding.

**Q: What about file size?**
A: GitHub Issue uploads support up to 100MB. Your 30MB video is perfect!

**Q: Can I delete the issue after getting the URL?**
A: Yes! The video remains hosted by GitHub even if you close/delete the issue.

---

## ✅ Summary

**Current setup (no changes needed):**
- ✅ Video link in README works
- ✅ Recruiters can download and watch
- ✅ Professional presentation

**To make it auto-play inline:**
- Upload via GitHub Issue → Get embed URL → Update README

**Both are great!** Choose based on preference. 🎉

