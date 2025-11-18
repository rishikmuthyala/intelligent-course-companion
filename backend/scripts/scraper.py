"""
Canvas/Echo360 transcript scraper using Playwright.

This module handles:
- Canvas authentication
- Course discovery
- Echo360 lecture transcript downloading
"""

import os
import asyncio
import time
import re
from pathlib import Path
from typing import List, Dict, Optional, Any
from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeoutError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL", "https://umass.instructure.com")
BROWSER_TIMEOUT = 30000  # 30 seconds default timeout
LOGIN_TIMEOUT = 60000  # 60 seconds for login (in case of MFA)


async def download_all_transcripts(username: str, password: str) -> Dict[str, Any]:
    """
    Main function to download all available transcripts from Canvas/Echo360.
    
    Args:
        username: Canvas username
        password: Canvas password
    
    Returns:
        Dictionary containing download statistics and any errors
    """
    print("=" * 60)
    print("Starting Canvas Transcript Scraper")
    print("=" * 60)
    
    result = {
        "success": False,
        "courses_found": 0,
        "courses": [],
        "transcripts_downloaded": 0,
        "errors": []
    }
    
    async with async_playwright() as p:
        # Launch browser with visible UI for debugging
        print("\n[1/4] Launching browser...")
        browser = await p.chromium.launch(
            headless=False,  # Set to True for production
            args=['--disable-blink-features=AutomationControlled']
        )
        
        try:
            # Create a new browser context with viewport settings
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # Create a new page
            page = await context.new_page()
            page.set_default_timeout(BROWSER_TIMEOUT)
            
            # Step 1: Login to Canvas
            print(f"\n[2/4] Navigating to Canvas: {CANVAS_BASE_URL}")
            login_success = await login_to_canvas(page, username, password)
            
            if not login_success:
                print("\n❌ Login failed. Please check your credentials.")
                result["errors"].append("Login failed")
                return result
            
            print("\n✅ Successfully logged in to Canvas!")
            result["success"] = True
            
            # Step 2: Discover courses
            courses = await discover_courses(page)
            
            if not courses:
                print("\n⚠️ No courses found. Please check if you have active courses.")
                result["errors"].append("No courses found")
                return result
            
            result["courses_found"] = len(courses)
            result["courses"] = courses  # Store course details in result
            
            # Step 3: Download transcripts for each course
            print("\n[4/4] Downloading transcripts from Echo360...")
            print(f"   → Processing {len(courses)} course(s)...")
            
            total_transcripts = 0
            for course_idx, course in enumerate(courses, 1):
                print(f"\n   Course {course_idx}/{len(courses)}:")
                transcripts = await download_transcripts_for_course(page, course)
                total_transcripts += transcripts
                
                # Add transcript count to course info
                course['transcripts_downloaded'] = transcripts
            
            result["transcripts_downloaded"] = total_transcripts
            
            if total_transcripts > 0:
                print(f"\n✅ Successfully downloaded {total_transcripts} transcript(s) total!")
            else:
                print("\n⚠️ No transcripts were downloaded. This could mean:")
                print("   - Courses don't have Echo360 recordings")
                print("   - Transcripts aren't available for the recordings")
                print("   - The Echo360 interface has changed")
            
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            result["errors"].append(f"Unexpected error: {str(e)}")
        
        finally:
            # Keep browser open for a moment to see the result
            print("\nClosing browser in 5 seconds...")
            await asyncio.sleep(5)
            await browser.close()
    
    print("\n" + "=" * 60)
    print("Scraper completed")
    print(f"Result: {result}")
    print("=" * 60)
    
    return result


async def login_to_canvas(page: Page, username: str, password: str) -> bool:
    """
    Handle Canvas login including potential MFA.
    
    Args:
        page: Playwright page object
        username: Canvas username
        password: Canvas password
    
    Returns:
        True if login successful, False otherwise
    """
    try:
        # First try direct login page
        print(f"   → Navigating to {CANVAS_BASE_URL}/login")
        await page.goto(f"{CANVAS_BASE_URL}/login", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        # Check if we're on the UMass IT landing page
        if "umass.edu/it" in page.url.lower():
            print("   → Detected UMass IT landing page, clicking LOG INTO CANVAS button...")
            # Look for the LOG INTO CANVAS button
            login_button_selectors = [
                'a:has-text("LOG INTO CANVAS")',
                'a.button:has-text("LOG INTO CANVAS")',
                'a[href*="canvas"]',
                'a[href*="instructure"]',
                '.button:has-text("LOG")'
            ]
            
            for selector in login_button_selectors:
                try:
                    login_btn = await page.query_selector(selector)
                    if login_btn:
                        await login_btn.click()
                        await page.wait_for_load_state("networkidle")
                        await asyncio.sleep(2)
                        break
                except:
                    continue
        
        # Wait for the login form to be visible
        print("   → Waiting for login form...")
        
        # Try multiple possible selectors for username field
        username_selectors = [
            'input[name="pseudonym_session[unique_id]"]',
            'input#pseudonym_session_unique_id',
            'input[type="text"][name*="username"]',
            'input[type="email"]',
            'input[type="text"]',  # Generic text input
            'input[name="username"]',  # Simple username
            'input[name="email"]',  # Email field
            'input[id*="username"]',  # Any ID containing username
            'input[id*="email"]',  # Any ID containing email
            'input[placeholder*="Username"]',  # Placeholder text
            'input[placeholder*="Email"]'  # Email placeholder
        ]
        
        username_field = None
        for selector in username_selectors:
            try:
                username_field = await page.wait_for_selector(selector, timeout=5000)
                if username_field:
                    print(f"   → Found username field with selector: {selector}")
                    break
            except:
                continue
        
        if not username_field:
            print("   ❌ Could not find username field")
            return False
        
        # Fill in username
        print(f"   → Entering username: {username[:3]}***")
        await username_field.fill(username)
        
        # Find and fill password field
        password_selectors = [
            'input[name="pseudonym_session[password]"]',
            'input#pseudonym_session_password',
            'input[type="password"]'
        ]
        
        password_field = None
        for selector in password_selectors:
            try:
                password_field = await page.wait_for_selector(selector, timeout=5000)
                if password_field:
                    print(f"   → Found password field with selector: {selector}")
                    break
            except:
                continue
        
        if not password_field:
            print("   ❌ Could not find password field")
            return False
        
        print("   → Entering password: ********")
        await password_field.fill(password)
        
        # Find and click login button
        login_button_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Log In")',
            'button:has-text("Sign In")',
            '.Button--login'
        ]
        
        login_button = None
        for selector in login_button_selectors:
            try:
                login_button = await page.wait_for_selector(selector, timeout=5000)
                if login_button:
                    print(f"   → Found login button with selector: {selector}")
                    break
            except:
                continue
        
        if not login_button:
            print("   ❌ Could not find login button")
            return False
        
        # Click login button and wait for navigation
        print("   → Clicking login button...")
        await login_button.click()
        
        # Wait for either successful login or error message
        print("   → Waiting for login response...")
        
        # Check for MFA prompt
        try:
            mfa_prompt = await page.wait_for_selector(
                'text=/duo|two.factor|verification|authenticate/i',
                timeout=5000
            )
            if mfa_prompt:
                print("\n   ⚠️  Multi-factor authentication detected!")
                print("   → Please complete MFA in the browser window...")
                print("   → Waiting up to 60 seconds for MFA completion...")
                
                # Wait for dashboard or courses page after MFA
                await page.wait_for_selector(
                    'a[href*="/courses"], #dashboard, .ic-DashboardCard',
                    timeout=LOGIN_TIMEOUT
                )
        except:
            # No MFA detected, continue
            pass
        
        # Verify successful login by checking for dashboard elements
        try:
            await page.wait_for_selector(
                'a[href*="/courses"], #dashboard, .ic-DashboardCard, #global_nav_courses_link',
                timeout=10000
            )
            
            # Additional verification - check URL
            current_url = page.url
            if "/login" not in current_url.lower():
                print(f"   → Successfully logged in! Current page: {current_url}")
                return True
            else:
                print(f"   ❌ Still on login page: {current_url}")
                
                # Check for error messages
                error_element = await page.query_selector('.error_text, .ic-flash-error, .alert')
                if error_element:
                    error_text = await error_element.text_content()
                    print(f"   → Login error: {error_text}")
                
                return False
                
        except PlaywrightTimeoutError:
            print("   ❌ Login timeout - could not verify successful login")
            
            # Check for error messages
            error_element = await page.query_selector('.error_text, .ic-flash-error, .alert')
            if error_element:
                error_text = await error_element.text_content()
                print(f"   → Login error: {error_text}")
            
            return False
        
    except Exception as e:
        print(f"   ❌ Login exception: {str(e)}")
        return False


async def discover_courses(page: Page) -> List[Dict[str, str]]:
    """
    Extract all active courses from Canvas dashboard.
    
    Args:
        page: Authenticated Playwright page (should be on dashboard)
    
    Returns:
        List of course dictionaries with name and url
    """
    print("\n[3/4] Discovering courses...")
    courses = []
    
    try:
        # Wait for dashboard to fully load
        print("   → Waiting for dashboard to load...")
        
        # Try multiple possible selectors for course cards
        course_selectors = [
            'a.ic-DashboardCard__link',  # Primary selector for course card links
            'div[class*="ic-DashboardCard"] a[href*="/courses/"]',  # UMass: any link in dashboard card
            'a[href*="/courses/"][class*="Card"]',  # Generic card link
            'div.ic-DashboardCard__header a',  # Header links in dashboard cards
            'a[data-testid="course-card-link"]',  # Possible test ID selector
            'div[id*="dashboard"] a[href*="/courses/"]',  # Any dashboard course link
            'a[href*="/courses/"]',  # Fallback: any course link on page
        ]
        
        course_elements = None
        selector_used = None
        
        for selector in course_selectors:
            try:
                # Wait for at least one course card to appear
                await page.wait_for_selector(selector, timeout=10000)
                course_elements = await page.query_selector_all(selector)
                if course_elements and len(course_elements) > 0:
                    selector_used = selector
                    print(f"   → Found course cards using selector: {selector}")
                    break
            except:
                continue
        
        if not course_elements:
            print("   ⚠️  No course cards found on dashboard")
            
            # Try to navigate to courses page as fallback
            print("   → Attempting to navigate to courses page...")
            courses_link = await page.query_selector('a[href="/courses"], #global_nav_courses_link')
            if courses_link:
                await courses_link.click()
                await page.wait_for_load_state('networkidle')
                
                # Try to find courses on the courses page
                course_elements = await page.query_selector_all('a[href*="/courses/"]:has-text("")')
        
        if course_elements:
            print(f"   → Processing {len(course_elements)} course(s)...")
            
            for element in course_elements:
                try:
                    # Extract course name (text content)
                    course_name = await element.text_content()
                    if course_name:
                        course_name = course_name.strip()
                    
                    # Extract course URL (href attribute)
                    course_url = await element.get_attribute('href')
                    
                    # Skip if no name or URL
                    if not course_name or not course_url:
                        continue
                    
                    # Make URL absolute if it's relative
                    if course_url.startswith('/'):
                        course_url = f"{CANVAS_BASE_URL}{course_url}"
                    
                    # Extract course ID from URL (format: /courses/12345)
                    course_id = None
                    if '/courses/' in course_url:
                        parts = course_url.split('/courses/')
                        if len(parts) > 1:
                            course_id = parts[1].split('/')[0].split('?')[0]
                    
                    # Skip if no valid course ID (must be numeric)
                    if not course_id or not course_id.isdigit():
                        continue
                    
                    # Skip very short course names (likely not real courses)
                    if len(course_name) < 3:
                        continue
                    
                    # Add to courses list
                    course_info = {
                        'name': course_name,
                        'url': course_url,
                        'id': course_id  # Adding ID for future use
                    }
                    
                    # Avoid duplicates (check by course_id to be more precise)
                    if course_id not in [c['id'] for c in courses]:
                        courses.append(course_info)
                        print(f"      ✓ Found course: {course_name} (ID: {course_id})")
                
                except Exception as e:
                    print(f"      ⚠️ Error processing course element: {str(e)}")
                    continue
            
            # Sort courses by name for consistent ordering
            courses.sort(key=lambda x: x['name'])
            
            print(f"\n   ✅ Found {len(courses)} course(s) total")
            
            # Display summary
            if courses:
                print("\n   📚 Discovered Courses:")
                for i, course in enumerate(courses, 1):
                    print(f"      {i}. {course['name']}")
                    print(f"         URL: {course['url']}")
        else:
            print("   ❌ Could not find any courses")
    
    except Exception as e:
        print(f"   ❌ Error during course discovery: {str(e)}")
    
    return courses


async def get_active_courses(page: Page) -> List[Dict[str, str]]:
    """
    Legacy function name - redirects to discover_courses.
    
    Args:
        page: Authenticated Playwright page
    
    Returns:
        List of course dictionaries with id and name
    """
    return await discover_courses(page)


async def download_transcripts_for_course(page: Page, course: Dict[str, str]) -> int:
    """
    Download all Echo360 transcripts for a specific course.
    
    Args:
        page: Authenticated Playwright page
        course: Dictionary with 'name', 'url', and 'id' keys
    
    Returns:
        Number of transcripts successfully downloaded
    """
    transcripts_downloaded = 0
    course_name = course['name']
    course_url = course['url']
    course_id = course['id']
    
    print(f"\n   📚 Processing course: {course_name}")
    
    try:
        # Step 1: Navigate to the course homepage
        print(f"      → Navigating to {course_name}...")
        await page.goto(course_url, wait_until='networkidle')
        
        # Step 2: Find and click Echo360 link in course navigation
        print("      → Looking for Echo360 link...")
        
        # Try multiple selectors for Echo360 link
        echo360_selectors = [
            'a:has-text("Echo360")',
            'a:has-text("echo360")',
            'a:has-text("Lecture Recordings")',
            'a:has-text("Recordings")',
            'a.context_external_tool_link[href*="echo360"]',
            'a[class*="external_tool"][href*="echo"]',
            'li.section a[href*="/external_tools/"]'
        ]
        
        echo360_link = None
        for selector in echo360_selectors:
            try:
                elements = await page.query_selector_all(selector)
                for element in elements:
                    text = await element.text_content()
                    if text and any(keyword in text.lower() for keyword in ['echo', 'recording', 'lecture']):
                        echo360_link = element
                        print(f"      → Found Echo360 link: '{text.strip()}'")
                        break
                if echo360_link:
                    break
            except:
                continue
        
        if not echo360_link:
            print(f"      ⚠️  No Echo360 link found for {course_name}")
            return 0
        
        # Click the Echo360 link
        await echo360_link.click()
        
        # Step 3: Wait for Echo360 content to load (might be in iframe)
        print("      → Waiting for Echo360 content to load...")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)  # Extra wait for dynamic content
        
        # Check if Echo360 is in an iframe
        iframe = await page.query_selector('iframe[src*="echo360"], iframe[id*="tool"], iframe[title*="Echo"]')
        if iframe:
            print("      → Echo360 content detected in iframe, switching context...")
            frame = await iframe.content_frame()
            if frame:
                page = frame  # Switch context to iframe
        
        # Step 4: Find all lecture links
        print("      → Searching for lecture recordings...")
        
        # Try multiple selectors for lecture list items
        lecture_selectors = [
            'a[href*="/media/"][href*="/view"]',  # Direct media links
            '.class-row a',  # Class row links
            '.echoes-list a.echo-name',  # Echo list items
            'div[role="row"] a[href*="/media/"]',  # Table row links
            'a.menu-thumb-link',  # Thumbnail links
            '.class-item a',  # Class items
            'tr td:first-child a',  # UMass: First link in table row
            'tbody tr a',  # Any link in table body rows
            'a[href*="echo360"]',  # Any Echo360 link
            '.available-list a',  # Available lectures list
            'div.echo-class-item a'  # Echo class item links
        ]
        
        lecture_links = []
        for selector in lecture_selectors:
            elements = await page.query_selector_all(selector)
            if elements:
                print(f"      → Found {len(elements)} potential lecture(s) with selector: {selector}")
                lecture_links.extend(elements)
                break
        
        if not lecture_links:
            print(f"      ⚠️  No lecture recordings found for {course_name}")
            return 0
        
        print(f"      → Found {len(lecture_links)} lecture recording(s)")
        
        # Create transcript directory for this course
        transcript_dir = ensure_transcript_directory(course_id)
        print(f"      → Transcript directory: {transcript_dir}")
        
        # Step 5: Process each lecture
        for idx, lecture_link in enumerate(lecture_links, 1):
            try:
                # Get lecture title
                lecture_title = await lecture_link.text_content()
                if not lecture_title:
                    lecture_title = f"Lecture_{idx}"
                else:
                    lecture_title = lecture_title.strip()
                
                # Clean filename (remove special characters)
                clean_title = re.sub(r'[^\w\s-]', '', lecture_title)
                clean_title = re.sub(r'[-\s]+', '_', clean_title)
                
                print(f"\n      [{idx}/{len(lecture_links)}] Processing: {lecture_title}")
                
                # Click on the lecture link
                await lecture_link.click()
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)  # Wait for video page to load
                
                # Look for transcript download button/link
                print("         → Looking for transcript download option...")
                
                transcript_selectors = [
                    'button:has-text("Transcript")',
                    'a:has-text("Download transcript")',
                    'button[aria-label*="transcript"]',
                    'a[href*="transcript"][href$=".txt"]',
                    'button.transcript-btn',
                    '[data-tooltip*="transcript"]',
                    'button:has-text("CC")',  # Closed captions might have transcript
                    '.more-menu button',  # Check in more/options menu
                    'button[title*="Download"]',  # Download button
                    'a[title*="Download"]',  # Download link
                    'button:has-text("Download")',  # Download text
                    '[aria-label*="Download"]',  # Download aria label
                    '.download-btn',  # Download class
                    'button.download',  # Download button class
                ]
                
                transcript_element = None
                
                # First, check if we need to open a menu
                menu_button = await page.query_selector('.more-menu button, button[aria-label="More options"], button[aria-label="Settings"]')
                if menu_button:
                    await menu_button.click()
                    await asyncio.sleep(1)
                
                # Now look for transcript option
                for selector in transcript_selectors:
                    transcript_element = await page.query_selector(selector)
                    if transcript_element:
                        print(f"         → Found transcript option with selector: {selector}")
                        break
                
                if transcript_element:
                    # Click the download button
                    await transcript_element.click()
                    await asyncio.sleep(1)  # Wait for popup/modal
                    
                    # Look for TXT download option in the popup
                    txt_selectors = [
                        'button:has-text("TXT")',
                        'a:has-text("TXT")',
                        'button:has-text(".txt")',
                        'a[href$=".txt"]',
                        '[data-format="txt"]',
                        'label:has-text("TXT")',
                        'input[value="TXT"] + label',
                        '.download-option:has-text("TXT")'
                    ]
                    
                    txt_option = None
                    for txt_sel in txt_selectors:
                        txt_option = await page.query_selector(txt_sel)
                        if txt_option:
                            print(f"         → Found TXT option")
                            break
                    
                    if txt_option:
                        # Set up download handling
                        download_path = transcript_dir / f"{clean_title}.txt"
                        
                        # Start waiting for download before clicking
                        async with page.expect_download() as download_info:
                            await txt_option.click()
                            download = await download_info.value
                            
                            # Save the file to our structured location
                            await download.save_as(download_path)
                            print(f"         ✓ Downloaded transcript: {download_path.name}")
                            transcripts_downloaded += 1
                    else:
                        print(f"         ⚠️  Could not find TXT download option")
                else:
                    print(f"         ⚠️  No transcript available for: {lecture_title}")
                
                # Navigate back to lecture list
                await page.go_back()
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"         ❌ Error processing lecture {idx}: {str(e)}")
                # Try to recover by going back
                try:
                    await page.go_back()
                    await asyncio.sleep(2)
                except:
                    pass
                continue
        
        print(f"\n      ✅ Downloaded {transcripts_downloaded} transcript(s) for {course_name}")
        
    except Exception as e:
        print(f"      ❌ Error processing course {course_name}: {str(e)}")
    
    return transcripts_downloaded


async def download_course_transcripts(page: Page, course_id: str, course_name: str) -> int:
    """
    Legacy function - redirects to download_transcripts_for_course.
    
    Args:
        page: Authenticated Playwright page
        course_id: Canvas course ID
        course_name: Human-readable course name
    
    Returns:
        Number of transcripts downloaded
    """
    course = {'id': course_id, 'name': course_name, 'url': f"{CANVAS_BASE_URL}/courses/{course_id}"}
    return await download_transcripts_for_course(page, course)


def ensure_transcript_directory(course_id: str) -> Path:
    """
    Create transcript directory for a course if it doesn't exist.
    
    Args:
        course_id: Canvas course ID
    
    Returns:
        Path object for the transcript directory
    """
    transcript_dir = Path(f"./transcripts/{course_id}")
    transcript_dir.mkdir(parents=True, exist_ok=True)
    return transcript_dir


if __name__ == "__main__":
    # Test the scraper independently
    canvas_username = os.getenv("CANVAS_USERNAME", "")
    canvas_password = os.getenv("CANVAS_PASSWORD", "")
    
    if not canvas_username or not canvas_password:
        print("Error: Canvas credentials not found in environment variables")
        exit(1)
    
    # Run the async scraper
    asyncio.run(download_all_transcripts(canvas_username, canvas_password))
