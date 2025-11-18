#!/bin/bash

# ==============================================================================
# PUSH AI COURSE COMPANION TO GITHUB
# ==============================================================================
# 
# BEFORE RUNNING THIS SCRIPT:
# 1. Create the repository on GitHub:
#    → Go to: https://github.com/new
#    → Repository name: ai-course-companion
#    → Visibility: Public
#    → Do NOT check "Initialize with README"
#    → Click: Create repository
#
# 2. Then run this script:
#    chmod +x PUSH_TO_GITHUB.sh
#    ./PUSH_TO_GITHUB.sh
# ==============================================================================

echo "🚀 Pushing AI Course Companion to GitHub..."
echo ""

# Navigate to repository directory
cd "/Users/rishikmuthyala/Desktop/AI Course Companion/intelligent-course-companion"

# Add GitHub remote
echo "📡 Adding GitHub remote..."
git remote add origin https://github.com/rishikmuthyala/ai-course-companion.git

# Verify remote was added
echo ""
echo "✅ Remote added:"
git remote -v

# Push to GitHub
echo ""
echo "⬆️  Pushing to GitHub (this may take a few minutes for the 30MB video)..."
git push -u origin main

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║              ✅ SUCCESSFULLY PUSHED TO GITHUB! ✅              ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Your repository is now live at:"
echo "   https://github.com/rishikmuthyala/ai-course-companion"
echo ""
echo "📹 Demo video URL:"
echo "   https://github.com/rishikmuthyala/ai-course-companion/raw/main/.github/demo/demo.mp4"
echo ""
echo "📋 NEXT STEPS:"
echo "   1. Visit your repo and verify everything looks good"
echo "   2. Add topics/tags in repo settings (ai, gpt-4, education, etc.)"
echo "   3. Pin the repo to your GitHub profile"
echo "   4. Share on LinkedIn!"
echo ""

