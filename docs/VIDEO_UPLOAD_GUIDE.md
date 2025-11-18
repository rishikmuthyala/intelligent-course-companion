# 📹 Video Upload Guide - Git LFS Setup Complete!

## ✅ Git LFS is Configured!

Your repository is now set up to handle large video files using Git Large File Storage (LFS).

---

## 🎬 How to Add Your Demo Video

### Step 1: Copy Your Video File

Copy your demo video to the demo directory and rename it to `demo.mp4` (or keep your preferred format):

```bash
# Navigate to the demo directory
cd "/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion/.github/demo"

# Copy your video here
# For example, if your video is on Desktop:
cp ~/Desktop/your-video-name.mp4 ./demo.mp4

# Or drag and drop your video file into:
# /Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion/.github/demo/
```

**Supported formats:**
- ✅ `.mp4` (recommended - best compatibility)
- ✅ `.mov`
- ✅ `.avi`
- ✅ `.mkv`

**Important:** Rename your video to `demo.mp4` for consistency with the README.

---

### Step 2: Add and Commit the Video

```bash
cd "/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion"

# Add your video to Git
git add .github/demo/demo.mp4

# Commit the video
git commit -m "docs: Add demo video via Git LFS"

# Check that LFS is tracking it
git lfs ls-files
```

You should see output like:
```
3a162f2 * .github/demo/demo.mp4
```

The `*` indicates the file is tracked by Git LFS!

---

### Step 3: Update README with Your GitHub Username

Before pushing, update the video URL in README.md:

Find this line:
```markdown
https://github.com/YOUR_USERNAME/ai-course-companion/raw/main/.github/demo/demo.mp4
```

Replace `YOUR_USERNAME` with your actual GitHub username:
```markdown
https://github.com/rishikmuthyala/ai-course-companion/raw/main/.github/demo/demo.mp4
```

Then commit:
```bash
git add README.md
git commit -m "docs: Update video URL with GitHub username"
```

---

### Step 4: Push to GitHub

If this is your first push:

```bash
# Create repo on GitHub first: https://github.com/new
# Name: ai-course-companion
# Then:

git remote add origin https://github.com/YOUR_USERNAME/ai-course-companion.git
git push -u origin main
```

If you've already pushed before:

```bash
git push origin main
```

**Note:** Git LFS will upload the video file separately. This may take a few minutes depending on your video size and internet speed.

---

## 🎥 Alternative: Embed Video in README (Better Display)

GitHub won't directly play videos in the README. For a better experience, you can:

### Option 1: Use GitHub's Video Embed (Recommended)

1. Go to any GitHub issue in your repo
2. Drag and drop your video into the comment box
3. GitHub uploads it and generates an embed code like:

```
https://github.com/user-attachments/assets/abc123-def456-video.mp4
```

4. Copy this URL and use it in your README instead

### Option 2: Create a Video Thumbnail with Link

Add this to your README:

```markdown
## 🎬 Demo Video

[![AI Course Companion Demo](https://img.shields.io/badge/▶️-Watch%20Demo-blue?style=for-the-badge)](.github/demo/demo.mp4)

<video width="100%" controls>
  <source src=".github/demo/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

> **📹 Watch the full demo** showing the complete flow: Canvas sync → Web scraping → Auto-summarization → Interactive Q&A
```

### Option 3: YouTube/Loom (Best for Recruiters)

Upload to YouTube (unlisted) or Loom and embed:

**YouTube:**
```markdown
[![Demo Video](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)
```

**Loom:**
```markdown
[![Watch the demo](https://img.shields.io/badge/▶️-Watch%20on%20Loom-625DF5?style=for-the-badge&logo=loom)](https://www.loom.com/share/YOUR_VIDEO_ID)
```

---

## ✅ Current Setup

- ✅ Git LFS installed
- ✅ Video formats configured: `.mp4`, `.mov`, `.avi`, `.mkv`
- ✅ Demo directory created: `.github/demo/`
- ✅ README updated with video path
- ✅ `.gitattributes` file created

---

## 📊 Check Your Setup

```bash
cd "/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion"

# Verify Git LFS is working
git lfs env

# Check which files are tracked by LFS
git lfs ls-files

# See what file patterns are tracked
cat .gitattributes
```

---

## 🚨 Troubleshooting

### "This exceeds GitHub's file size limit of 100 MB"

If your video is over 100 MB:

1. **Compress the video:**
   ```bash
   # Using ffmpeg (install with: brew install ffmpeg)
   ffmpeg -i demo.mp4 -vcodec h264 -acodec aac -b:v 2M demo-compressed.mp4
   ```

2. **Or use external hosting:**
   - YouTube (unlisted)
   - Loom
   - Vimeo
   - Google Drive with public link

### "Git LFS bandwidth quota exceeded"

GitHub LFS free tier includes:
- **1 GB storage**
- **1 GB bandwidth per month**

If exceeded, consider:
- Use YouTube/Loom instead
- Upgrade to GitHub Pro (free for students)
- Compress video to reduce size

---

## 💡 Best Practices

1. **Keep videos under 50 MB** for faster loading
2. **Use .mp4 format** for best compatibility
3. **Aim for 2-3 minutes** demo length
4. **1080p or 720p resolution** is sufficient
5. **Add captions** if possible (helps recruiters)

---

## 📝 Quick Command Reference

```bash
# Add your video
cd "/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion"
cp ~/Desktop/your-video.mp4 .github/demo/demo.mp4

# Commit and push
git add .github/demo/demo.mp4
git commit -m "docs: Add demo video"
git push origin main

# Check LFS status
git lfs ls-files
```

---

## 🎉 You're Ready!

Once you add your video and push to GitHub:

1. Go to your repo: `https://github.com/YOUR_USERNAME/ai-course-companion`
2. Click on `.github/demo/demo.mp4` to view it
3. Recruiters can click the link in your README to watch

**Your demo video will showcase your full-stack AI application! 🚀**

---

*Need help? Check the [Git LFS documentation](https://git-lfs.github.com/)*

