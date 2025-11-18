#!/usr/bin/env python3
"""
Test script for the Advanced Canvas Scraper
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent / "scripts"))

from scripts.advanced_scraper import AdvancedCanvasScraper

async def test_scraper():
    """Test the advanced scraper functionality"""
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    username = os.getenv("CANVAS_USERNAME")
    password = os.getenv("CANVAS_PASSWORD")
    
    if not username or not password:
        print("❌ Canvas credentials not found in .env file")
        print("Please ensure CANVAS_USERNAME and CANVAS_PASSWORD are set")
        return
    
    print("=" * 60)
    print("TESTING ADVANCED CANVAS SCRAPER - SCRAPE ALL COURSES")
    print("=" * 60)
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    print()
    
    try:
        print("Starting scraping process for ALL courses...")
        print("(Running with VISIBLE Chromium browser - headless=False)")
        
        # Initialize scraper and scrape all courses
        scraper = AdvancedCanvasScraper(username, password, headless=False)
        result = await scraper.scrape_all_courses()
        
        # Display results
        print("\n" + "=" * 60)
        print("SCRAPING RESULTS")
        print("=" * 60)
        
        if result:
            print(f"✅ Scraping completed successfully!")
            print(f"   Courses found: {result.get('courses_found', 0)}")
            print(f"   Transcripts downloaded: {result.get('transcripts_downloaded', 0)}")
            
            if 'courses' in result:
                print("\nCourses processed:")
                for course in result['courses']:
                    print(f"   - {course}")
        else:
            print("❌ Scraping failed or returned no results")
            
    except Exception as e:
        print(f"\n❌ Error during scraping: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_scraper())
