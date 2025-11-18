#!/usr/bin/env python3
"""
Simple script to run the ultra-advanced Canvas scraper
Usage: python run_ultra_scraper.py [course_name]
"""

import sys
import asyncio
from ultra_advanced_scraper import UltraAdvancedCanvasScraper
from dotenv import load_dotenv
import os

async def main():
    # Load environment variables
    load_dotenv()
    
    username = os.getenv("CANVAS_USERNAME")
    password = os.getenv("CANVAS_PASSWORD")
    
    if not username or not password:
        print("❌ ERROR: Please set CANVAS_USERNAME and CANVAS_PASSWORD in .env file")
        print("\nCreate a .env file in the backend directory with:")
        print("CANVAS_USERNAME=your_email@umass.edu")
        print("CANVAS_PASSWORD=your_password")
        print("CANVAS_BASE_URL=https://umass.instructure.com")
        return
    
    # Get course name from command line or use default
    course_name = sys.argv[1] if len(sys.argv) > 1 else "COMPSCI 446"
    
    print("🚀 " + "="*60)
    print("   ULTRA-ADVANCED CANVAS TRANSCRIPT SCRAPER")
    print("="*60)
    print(f"\n📋 Configuration:")
    print(f"   • Username: {username[:3]}***@{username.split('@')[1] if '@' in username else '***'}")
    print(f"   • Course: {course_name}")
    print(f"   • Debug Mode: ENABLED")
    print(f"   • Screenshots: ./debug_screenshots/")
    print(f"   • Transcripts: ./transcripts/")
    print(f"   • Headless: NO (browser will be visible)")
    print()
    print("💡 Features:")
    print("   ✓ Intelligent error recovery with retry mechanisms")
    print("   ✓ Exhaustive element searching (scans entire page)")
    print("   ✓ Screenshot capture at each step for debugging")
    print("   ✓ Multiple fallback strategies for every action")
    print("   ✓ Visual element detection and smart navigation")
    print("   ✓ Automatic pop-up and modal handling")
    print("   ✓ Detailed logging and navigation history")
    print()
    print("⏳ Starting scraper... Please wait, this may take several minutes.")
    print()
    
    # Create scraper instance
    scraper = UltraAdvancedCanvasScraper(
        username=username,
        password=password,
        headless=False,  # Set to True for production/background mode
        debug=True       # Keep True for detailed logging
    )
    
    try:
        # Run the scraper
        result = await scraper.run_ultra_advanced(course_name)
        
        # Print results
        print("\n" + "="*60)
        print("   FINAL RESULTS")
        print("="*60)
        
        if result['success']:
            print("\n🎉 SUCCESS!")
            print(f"   • Transcripts Downloaded: {result['transcripts_downloaded']}")
            print(f"   • Phases Completed: {', '.join(result['phases_completed'])}")
            print(f"\n📁 Check the ./transcripts/ folder for downloaded files")
        else:
            print("\n⚠️  PARTIAL SUCCESS or FAILURE")
            print(f"   • Phases Completed: {', '.join(result['phases_completed']) if result['phases_completed'] else 'None'}")
            print(f"   • Transcripts Downloaded: {result['transcripts_downloaded']}")
            
            if result['errors']:
                print(f"\n❌ Errors encountered:")
                for i, error in enumerate(result['errors'], 1):
                    print(f"   {i}. {error}")
        
        print(f"\n📸 Debug Information:")
        print(f"   • Screenshots saved in: ./debug_screenshots/")
        print(f"   • Navigation history: ./debug_screenshots/navigation_history.json")
        print(f"   • Review screenshots to understand what happened at each step")
        
        print("\n💡 Tip: If scraping failed, review the screenshots to see where it got stuck")
        print("   and share them if you need help debugging.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        print("   Check the screenshots for more details")
    
    print("\n" + "="*60)
    print("   SCRAPING COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())


