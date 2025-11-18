"""
Super Simple Test - Just checks if the basics work
Run this first before the full test_system.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

print("\n" + "="*60)
print("🔍 SIMPLE ENVIRONMENT CHECK")
print("="*60)

# Load .env file
load_dotenv()

# Check if .env exists
env_file = Path(".env")
if env_file.exists():
    print("✅ .env file found")
else:
    print("❌ .env file NOT found")
    print("\n💡 NEXT STEP: Create .env file")
    print("   Run: cp env.example .env")
    print("   Then edit .env and add your credentials")
    exit(1)

# Check environment variables
print("\n📝 Checking environment variables...")

openai_key = os.getenv("OPENAI_API_KEY")
canvas_user = os.getenv("CANVAS_USERNAME")
canvas_pass = os.getenv("CANVAS_PASSWORD")

if openai_key and len(openai_key) > 10:
    print(f"✅ OPENAI_API_KEY: {openai_key[:7]}...")
else:
    print("❌ OPENAI_API_KEY: Not set or invalid")

if canvas_user:
    print(f"✅ CANVAS_USERNAME: {canvas_user}")
else:
    print("❌ CANVAS_USERNAME: Not set")

if canvas_pass:
    print(f"✅ CANVAS_PASSWORD: {'*' * 8}")
else:
    print("❌ CANVAS_PASSWORD: Not set")

# Check files
print("\n📂 Checking files...")

files_to_check = [
    "requirements.txt",
    "main.py",
    "mock_transcript.txt",
    "scripts/rag_pipeline.py",
    "scripts/advanced_scraper.py",
]

all_good = True
for file in files_to_check:
    if Path(file).exists():
        print(f"✅ {file}")
    else:
        print(f"❌ {file}")
        all_good = False

# Check Python packages
print("\n📦 Checking Python packages...")

try:
    import fastapi
    print("✅ fastapi")
except:
    print("❌ fastapi - Run: pip install -r requirements.txt")
    all_good = False

try:
    import openai
    print("✅ openai")
except:
    print("❌ openai - Run: pip install -r requirements.txt")
    all_good = False

try:
    import chromadb
    print("✅ chromadb")
except:
    print("❌ chromadb - Run: pip install -r requirements.txt")
    all_good = False

try:
    from playwright.async_api import async_playwright
    print("✅ playwright")
except:
    print("❌ playwright - Run: pip install playwright && playwright install chromium")
    all_good = False

# Summary
print("\n" + "="*60)
if all_good and openai_key and canvas_user and canvas_pass:
    print("✅ EVERYTHING LOOKS GOOD!")
    print("\n🚀 Next step: Run the full test")
    print("   python test_system.py")
else:
    print("⚠️  SOME ISSUES FOUND")
    print("\n📋 TODO:")
    if not env_file.exists():
        print("   1. Create .env file: cp env.example .env")
    if not openai_key:
        print("   2. Add OPENAI_API_KEY to .env")
    if not canvas_user or not canvas_pass:
        print("   3. Add Canvas credentials to .env")
    if not all_good:
        print("   4. Install dependencies: pip install -r requirements.txt")
        print("   5. Install Playwright: playwright install chromium")

print("="*60 + "\n")

