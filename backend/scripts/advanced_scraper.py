"""
Advanced Canvas/Echo360 Transcript Scraper
Handles dynamic pop-ups, course navigation, and transcript downloads
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
POPUP_WAIT_TIME = 10000  # 10 seconds to wait for pop-ups


class AdvancedCanvasScraper:
    """Advanced scraper for Canvas LMS with Echo360 integration"""
    
    def __init__(self, username: str, password: str, headless: bool = False):
        self.username = username
        self.password = password
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.download_dir = Path("./transcripts")
        self.download_dir.mkdir(exist_ok=True)
        
    async def initialize_browser(self):
        """Initialize Playwright browser with optimal settings"""
        print("🌐 Initializing browser...")
        playwright = await async_playwright().start()
        
        # Launch browser with anti-detection measures
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )
        
        # Create context with realistic viewport and user agent
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            accept_downloads=True,
            ignore_https_errors=True
        )
        
        # Set download behavior
        self.page = await self.context.new_page()
        self.page.set_default_timeout(BROWSER_TIMEOUT)
        
        print("✅ Browser initialized successfully")
        
    async def phase1_login_and_dashboard(self) -> bool:
        """Phase 1: Handle login and dashboard access with pop-up management"""
        print("\n" + "="*60)
        print("PHASE 1: LOGIN AND DASHBOARD ACCESS")
        print("="*60)
        
        try:
            # Step 1: Navigate to Canvas
            print(f"\n📍 Navigating to {CANVAS_BASE_URL}")
            await self.page.goto(CANVAS_BASE_URL, wait_until="domcontentloaded")
            await asyncio.sleep(2)
            
            # Check if we need to click through a landing page
            current_url = self.page.url
            if "umass.edu/it" in current_url.lower() or "/canvas" in current_url.lower():
                print("   → Detected landing page, looking for Canvas login button...")
                login_buttons = [
                    'a:has-text("LOG INTO CANVAS")',
                    'a:has-text("Login to Canvas")',
                    'a:has-text("Canvas Login")',
                    'button:has-text("Login")',
                    'a.button[href*="canvas"]',
                    'a[href*="instructure.com"]'
                ]
                
                for selector in login_buttons:
                    try:
                        btn = await self.page.wait_for_selector(selector, timeout=3000)
                        if btn:
                            print(f"   → Found login button, clicking...")
                            await btn.click()
                            await self.page.wait_for_load_state("networkidle")
                            break
                    except:
                        continue
            
            # Step 2: Handle login form
            print("\n🔐 Handling login form...")
            
            # Check if already at login page or need to navigate
            if "/login" not in self.page.url:
                await self.page.goto(f"{CANVAS_BASE_URL}/login", wait_until="networkidle")
            
            # Check if we're on Microsoft SSO login
            if "login.microsoftonline.com" in self.page.url:
                print("   → Detected Microsoft SSO login")
                
                # Microsoft SSO username field
                username_field = await self.page.wait_for_selector('input[name="loginfmt"]', timeout=5000)
                if username_field:
                    print(f"   → Entering email: {self.username[:3]}***")
                    await username_field.fill(self.username)
                    
                    # Click Next button
                    next_btn = await self.page.query_selector('input#idSIButton9')
                    if next_btn:
                        await next_btn.click()
                        await asyncio.sleep(2)
                    
                    # Wait for password field to appear
                    password_field = await self.page.wait_for_selector('input[name="passwd"]', timeout=5000)
                    if password_field:
                        print("   → Entering password")
                        await password_field.fill(self.password)
                        
                        # Click Sign In button
                        signin_btn = await self.page.query_selector('input#idSIButton9')
                        if signin_btn:
                            print("   → Signing in...")
                            await signin_btn.click()
                            await self.page.wait_for_load_state("networkidle")
                            await asyncio.sleep(2)
                            
                            # Handle "Stay signed in?" prompt if it appears
                            try:
                                stay_signed = await self.page.wait_for_selector('input#idBtn_Back', timeout=3000)
                                if stay_signed:
                                    print("   → Clicking 'No' on stay signed in prompt")
                                    await stay_signed.click()
                                    await asyncio.sleep(2)
                            except:
                                pass
                            
                            # Handle confirmation page - "Continue to Canvas" or similar
                            print("   → Looking for confirmation/continue button...")
                            confirm_selectors = [
                                'button:has-text("Yes")',
                                'button:has-text("Continue")',
                                'button:has-text("Accept")',
                                'button:has-text("Allow")',
                                'input[type="submit"][value="Yes"]',
                                'input[type="submit"][value="Continue"]',
                                'button#idSIButton9',  # Microsoft's common submit button
                                'input#idSIButton9',
                                'button.btn-primary',
                                'button[type="submit"]',
                                'input[type="submit"]'
                            ]
                            
                            for selector in confirm_selectors:
                                try:
                                    confirm_btn = await self.page.wait_for_selector(selector, timeout=2000)
                                    if confirm_btn:
                                        # Check if button text contains positive confirmation
                                        btn_text = await confirm_btn.text_content() if await confirm_btn.get_attribute('type') != 'submit' else await confirm_btn.get_attribute('value')
                                        if btn_text and any(word in btn_text.lower() for word in ['yes', 'continue', 'accept', 'allow', 'sign']):
                                            print(f"   → Clicking confirmation: '{btn_text}'")
                                            await confirm_btn.click()
                                            await self.page.wait_for_load_state("networkidle")
                                            await asyncio.sleep(3)
                                            
                                            # After confirmation, handle the welcome pop-up that appears
                                            print("   → Checking for welcome/hello pop-up after confirmation...")
                                            try:
                                                # Look specifically for the X button on the welcome pop-up
                                                close_selectors = [
                                                    'button:has-text("×")',  # X symbol
                                                    'button:has-text("X")',   # Letter X
                                                    'button.close',
                                                    'button[aria-label="Close"]',
                                                    '.modal-close',
                                                    'a.close',
                                                    'span.close',
                                                    '[role="button"]:has-text("×")',
                                                    '[role="button"]:has-text("X")'
                                                ]
                                                
                                                for close_sel in close_selectors:
                                                    try:
                                                        close_btn = await self.page.wait_for_selector(close_sel, timeout=1500)
                                                        if close_btn:
                                                            print("   → Found and clicking X button on welcome pop-up")
                                                            await close_btn.click()
                                                            await asyncio.sleep(1)
                                                            break
                                                    except:
                                                        continue
                                            except:
                                                pass
                                            
                                            break
                                except:
                                    continue
            else:
                # Standard Canvas login
                username_selectors = [
                    'input[name="pseudonym_session[unique_id]"]',
                    'input#pseudonym_session_unique_id',
                    'input[type="text"][name*="username"]',
                    'input[type="email"]',
                    'input[placeholder*="Username"]',
                    'input[placeholder*="Email"]',
                    'input[type="text"]'
                ]
                
                username_field = None
                for selector in username_selectors:
                    try:
                        username_field = await self.page.wait_for_selector(selector, timeout=3000)
                        if username_field:
                            print(f"   → Found username field")
                            await username_field.fill(self.username)
                            break
                    except:
                        continue
                
                if not username_field:
                    print("   ❌ Could not find username field")
                    return False
                
                # Find and fill password field
                password_selectors = [
                    'input[name="pseudonym_session[password]"]',
                    'input#pseudonym_session_password',
                    'input[type="password"]'
                ]
                
                password_field = None
                for selector in password_selectors:
                    try:
                        password_field = await self.page.query_selector(selector)
                        if password_field:
                            print(f"   → Found password field")
                            await password_field.fill(self.password)
                            break
                    except:
                        continue
                
                # Submit login form
                submit_selectors = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("Log In")',
                    'button:has-text("Login")',
                    'button.Button--login'
                ]
                
                for selector in submit_selectors:
                    try:
                        submit_btn = await self.page.query_selector(selector)
                        if submit_btn:
                            print("   → Submitting login form...")
                            await submit_btn.click()
                            break
                    except:
                        continue
            
            # Wait for navigation after login
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(3)
            
            # Check for MFA
            if "duo" in self.page.url.lower() or "mfa" in self.page.url.lower():
                print("   ⏳ MFA detected. Please complete authentication...")
                await self.page.wait_for_url("**/dashboard**", timeout=120000)
            
            print("   ✅ Login successful!")
            
            # Step 3: Handle post-login pop-up
            print("\n🔍 Checking for welcome tour/feature pop-up...")
            
            # Wait for potential pop-up to appear
            popup_dismissed = False
            popup_selectors = [
                # Common Canvas tour/modal selectors
                'button:has-text("Done")',
                'button:has-text("Skip")',
                'button:has-text("Skip Tour")',
                'button:has-text("End Tour")',
                'button:has-text("Exit")',
                'button:has-text("Close")',
                'button:has-text("Got it")',
                'button:has-text("Dismiss")',
                'button[aria-label="Close"]',
                'button.close',
                'button.modal-close',
                'a:has-text("Skip")',
                '[data-testid="close-button"]',
                '.ui-dialog-titlebar-close',
                '.tour-close-button',
                '.introjs-skipbutton',
                'button.introjs-skipbutton'
            ]
            
            # Try to find and dismiss pop-up
            for selector in popup_selectors:
                try:
                    popup_close = await self.page.wait_for_selector(selector, timeout=2000)
                    if popup_close:
                        print(f"   → Found pop-up dismissal button: {selector}")
                        await popup_close.click()
                        popup_dismissed = True
                        await asyncio.sleep(1)
                        print("   ✅ Pop-up dismissed successfully")
                        break
                except:
                    continue
            
            if not popup_dismissed:
                print("   → No pop-up detected or already dismissed")
            
            # Verify we're on the dashboard - look for course cards specifically
            try:
                # Wait for dashboard to load with course cards
                await self.page.wait_for_selector('div.ic-DashboardCard, a.ic-DashboardCard__link, div[class*="dashboard"]', timeout=10000)
                print("\n✅ Successfully reached Canvas dashboard!")
            except:
                try:
                    # Fallback - just check we have some course links
                    await self.page.wait_for_selector('a[href*="/courses/"]', timeout=5000)
                    print("\n✅ Successfully reached Canvas dashboard!")
                except:
                    # Final fallback - just check we're logged in
                    print("\n✅ Successfully logged in and ready to navigate!")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Phase 1 Error: {str(e)}")
            return False
    
    async def phase2_course_navigation(self, course_name: str) -> bool:
        """Phase 2: Navigate to specific course and explore tabs"""
        print("\n" + "="*60)
        print("PHASE 2: COURSE NAVIGATION")
        print("="*60)
        
        try:
            # Find and click on the target course
            print(f"\n🎯 Looking for course: {course_name}")
            
            # Wait for dashboard to fully load
            await asyncio.sleep(2)
            
            # First try exact selectors
            course_selectors = [
                f'a:has-text("{course_name}")',
                f'div.ic-DashboardCard__header:has-text("{course_name}") a',
                f'h3:has-text("{course_name}") a',
                f'a[title*="{course_name}"]'
            ]
            
            
            course_found = False
            for selector in course_selectors:
                try:
                    course_link = await self.page.wait_for_selector(selector, timeout=2000)
                    if course_link:
                        print(f"   → Found course: {course_name}")
                        await course_link.click()
                        await self.page.wait_for_load_state("networkidle")
                        course_found = True
                        break
                except:
                    continue
            
            if not course_found:
                # Try finding any course card or link
                print("   → Searching all course cards...")
                
                # Look for course cards
                course_cards = await self.page.query_selector_all('div.ic-DashboardCard, div[class*="card"], a.ic-DashboardCard__link')
                print(f"   → Found {len(course_cards)} course card(s)")
                
                for card in course_cards:
                    try:
                        # Get text from the card
                        card_text = await card.text_content()
                        if card_text:
                            # Check if course name matches (partial match)
                            if any(part.lower() in card_text.lower() for part in course_name.split()):
                                print(f"   → Found matching course card: {card_text[:50]}...")
                                
                                # Find clickable element in card
                                link = await card.query_selector('a')
                                if link:
                                    await link.click()
                                else:
                                    await card.click()
                                
                                await self.page.wait_for_load_state("networkidle")
                                course_found = True
                                break
                    except:
                        continue
                
                if not course_found:
                    # Final attempt: look for any course links
                    all_links = await self.page.query_selector_all('a[href*="/courses/"]')
                    print(f"   → Found {len(all_links)} course link(s)")
                    
                    for link in all_links:
                        text = await link.text_content()
                        if text and any(part.lower() in text.lower() for part in course_name.split()):
                            print(f"   → Found course (partial match): {text[:50]}...")
                            await link.click()
                            await self.page.wait_for_load_state("networkidle")
                            course_found = True
                            break
            
            if not course_found:
                print(f"   ❌ Could not find course: {course_name}")
                return False
            
            print("   ✅ Entered course successfully")
            
            # Explore course tabs to ensure everything loads
            print("\n📑 Exploring course tabs...")
            
            tabs_to_visit = [
                ("Modules", ["a:has-text('Modules')", "a[href*='/modules']"]),
                ("Announcements", ["a:has-text('Announcements')", "a[href*='/announcements']"]),
                ("Assignments", ["a:has-text('Assignments')", "a[href*='/assignments']"])
            ]
            
            for tab_name, selectors in tabs_to_visit:
                for selector in selectors:
                    try:
                        tab_link = await self.page.query_selector(selector)
                        if tab_link:
                            print(f"   → Clicking {tab_name} tab...")
                            await tab_link.click()
                            await self.page.wait_for_load_state("networkidle")
                            await asyncio.sleep(1)
                            break
                    except:
                        continue
            
            print("   ✅ Course navigation complete")
            return True
            
        except Exception as e:
            print(f"\n❌ Phase 2 Error: {str(e)}")
            return False
    
    async def phase3_echo360_transcript_download(self) -> bool:
        """Phase 3: Access Echo360 and download transcript"""
        print("\n" + "="*60)
        print("PHASE 3: ECHO360 ACCESS AND TRANSCRIPT DOWNLOAD")
        print("="*60)
        
        try:
            # Navigate to Echo360
            print("\n🎬 Looking for Echo360/Class Recordings...")
            
            # First check the navigation menu for Echo360 links
            print("   → Checking navigation menu...")
            nav_selectors = [
                'nav a:has-text("Echo360")',
                'nav a:has-text("echo360")', 
                'nav a:has-text("Class Recordings")',
                'nav a:has-text("Lecture Recordings")',
                'nav a:has-text("Recordings")',
                '.navigation a:has-text("Echo360")',
                '.navigation a:has-text("Recordings")',
                'ul.section-tabs a:has-text("Echo360")',
                'ul.section-tabs a:has-text("Recordings")'
            ]
            
            echo360_found = False
            
            # Try navigation menu first
            for selector in nav_selectors:
                try:
                    nav_link = await self.page.query_selector(selector)
                    if nav_link:
                        link_text = await nav_link.text_content()
                        print(f"   → Found in navigation: '{link_text.strip()}'")
                        await nav_link.click()
                        await asyncio.sleep(5)
                        echo360_found = True
                        break
                except:
                    continue
            
            # If not found in navigation, check main content area
            if not echo360_found:
                print("   → Checking main content area...")
                echo360_selectors = [
                    'a:has-text("Echo360")',
                    'a:has-text("echo360")',
                    'a:has-text("Class Recordings")',
                    'a:has-text("Lecture Recordings")',
                    'a:has-text("Recordings")',
                    'a[href*="echo360"]',
                    'a.context_external_tool[href*="echo"]',
                    'a[title*="Echo360"]',
                    'a[title*="Recording"]'
                ]
                
                for selector in echo360_selectors:
                    try:
                        echo_links = await self.page.query_selector_all(selector)
                        for echo_link in echo_links:
                            try:
                                link_text = await echo_link.text_content()
                                if link_text and any(word in link_text.lower() for word in ['echo', 'recording', 'lecture', 'class recording']):
                                    print(f"   → Found Echo360 link: '{link_text.strip()}'")
                                    
                                    # Try JavaScript click if regular click fails
                                    try:
                                        # First try regular click
                                        await echo_link.click(timeout=2000)
                                    except:
                                        # Fallback to JavaScript click
                                        print("   → Using JavaScript click...")
                                        await self.page.evaluate('(element) => element.click()', echo_link)
                                    
                                    for i in range(10):
                                        await asyncio.sleep(1)
                                        
                                    print("   → Clicked Echo360 link, waiting for it to load...")
                                    await asyncio.sleep(5)  # Wait for Echo360 to load
                                    
                                    # Check if we navigated or if iframe loaded
                                    current_url = self.page.url
                                    if 'echo360' in current_url.lower():
                                        print("   → Navigated to Echo360")
                                        echo360_found = True
                                        break                        
                                    
                                    # Check for iframe
                                    iframes = await self.page.query_selector_all('iframe')
                                    if iframes:
                                        print("   → Echo360 loaded in iframe")
                                        echo360_found = True
                                        break
                                    
                            except Exception as e:
                                print(f"   → Error: {str(e)[:100]}")
                                continue
                        if echo360_found:
                            break
                    except:
                        continue
            
            if not echo360_found:
                print("   ❌ Could not find Echo360 link")
                return False
            
            print("   ✅ Accessed Echo360 successfully")
            
            # Check for iframe (Echo360 often loads in iframe)
            iframe = await self.page.query_selector('iframe[src*="echo360"], iframe[id*="tool"], iframe[title*="Echo"]')
            if iframe:
                print("   → Switching to Echo360 iframe...")
                frame = await iframe.content_frame()
                if frame:
                    self.page = frame  # Switch context to iframe
            
            # Find and click on first available lecture
            print("\n📹 Looking for lecture recordings...")
            
            # Wait for the lecture list to load (longer wait for dynamic content)
            print("   → Waiting for lecture list to load...")
            await asyncio.sleep(5)
            
            # Debug: Check what's visible in the iframe
            try:
                page_title = await self.page.title()
                print(f"   → Current page title: {page_title}")
                
                # Check if Echo360 link is not yet activated or there are no recordings
                if "Link Not Yet Activated" in page_title:
                    print("   ❌ Echo360 link not yet activated for this course")
                    return False
                
                # Check page content for no recordings message
                body = await self.page.query_selector('body')
                if body:
                    body_text = await body.text_content()
                    if body_text:
                        if any(msg in body_text for msg in [
                            "Link Not Yet Activated",
                            "No recordings available",
                            "No lectures found",
                            "No classes scheduled",
                            "There are no recordings"
                        ]):
                            print("   ❌ No recordings available in this course")
                            return False
                        
                        # Show preview for debugging
                        preview = body_text[:200].replace('\n', ' ')
                        print(f"   → Page preview: {preview}...")
                
                # Check if there are any tables (lectures are usually in tables)
                tables = await self.page.query_selector_all('table')
                print(f"   → Found {len(tables)} table(s) on page")
                
                # Check for rows that might contain lectures
                rows = await self.page.query_selector_all('tr')
                print(f"   → Found {len(rows)} row(s) on page")
                
                # If no tables or very few rows, likely no recordings
                if len(tables) == 0 or len(rows) < 2:  # Less than 2 rows means no data rows
                    print("   ❌ No lecture recordings found (no data tables)")
                    return False
                    
            except Exception as e:
                print(f"   → Debug error: {str(e)}")
            
            # Look for lecture rows - they typically have "COMPSCI 446-1257-61515" text
            lecture_selectors = [
                'tr:has-text("COMPSCI")',  # Table rows with COMPSCI text
                'tr:has-text("446")',  # Rows with course number
                'tbody tr',  # Table body rows
                'tr',  # Any table row
                'tr[role="row"]',  # Generic table rows
                'table tr',  # Rows in any table
                'a[href*="/media/"]',  # Media links
                '.class-row',  # Class rows
                'div.echo-class',  # Echo class divs
                # More specific Echo360 selectors
                '[data-testid*="lecture"]',
                '[class*="lecture-row"]',
                '[class*="class-row"]'
            ]
            
            lecture_found = False
            for selector in lecture_selectors:
                try:
                    lectures = await self.page.query_selector_all(selector)
                    if lectures and len(lectures) > 0:
                        print(f"   → Found {len(lectures)} potential lecture element(s)")
                        
                        # Filter to find actual lecture rows (skip headers, etc.)
                        for i, lecture in enumerate(lectures[:5]):  # Try first 5
                            try:
                                lecture_text = await lecture.text_content()
                                if lecture_text and ('compsci' in lecture_text.lower() or 
                                                    '446' in lecture_text or 
                                                    'september' in lecture_text.lower() or
                                                    'october' in lecture_text.lower() or
                                                    '2025' in lecture_text):
                                    print(f"   → Clicking on lecture: {lecture_text[:50]}...")
                                    
                                    # Try JavaScript click for reliability
                                    try:
                                        await self.page.evaluate('(element) => element.click()', lecture)
                                    except:
                                        # Fallback to regular click
                                        await lecture.click()
                                    
                                    print("   → Clicked lecture, waiting for video page...")
                                    await asyncio.sleep(5)  # Wait for navigation/video load
                                    
                                    # Check if we navigated to a video page
                                    current_url = self.page.url
                                    if '/media/' in current_url or 'presentation' in current_url:
                                        print("   → Successfully opened lecture video")
                                        lecture_found = True
                                        break
                                    
                                    # Check if video player appeared
                                    video_elements = await self.page.query_selector_all('video, [class*="video"], [class*="player"]')
                                    if video_elements:
                                        print("   → Video player detected")
                                        lecture_found = True
                                        break
                            except Exception as e:
                                print(f"   → Could not click lecture {i+1}: {str(e)[:50]}")
                                continue
                        
                        if lecture_found:
                            break
                except Exception as e:
                    print(f"   → Error with selector {selector}: {str(e)[:50]}")
                    continue
            
            if not lecture_found:
                print("   ❌ No lectures found")
                return False
            
            print("   ✅ Opened lecture recording")
            
            # Step 1: Click the Transcript button on the video player
            print("\n📝 Looking for Transcript button on video player...")
            
            # Wait a bit for video player controls to load
            await asyncio.sleep(3)
            
            # Debug: Check what buttons are available
            try:
                all_buttons = await self.page.query_selector_all('button')
                print(f"   → Found {len(all_buttons)} button(s) on page")
                
                # Check first few buttons for their text/aria-label
                for i, btn in enumerate(all_buttons[:10]):
                    try:
                        btn_text = await btn.text_content()
                        aria_label = await btn.get_attribute('aria-label')
                        title = await btn.get_attribute('title')
                        if btn_text or aria_label or title:
                            print(f"   → Button {i+1}: text='{btn_text}', aria='{aria_label}', title='{title}'")
                    except:
                        pass
            except:
                pass
            
            # Look for transcript button - usually in top right area of video player
            transcript_button_selectors = [
                'button:has-text("Transcript")',
                'button:has-text("Transcripts")',
                'button[aria-label*="Transcript"]',
                'button[title*="Transcript"]',
                'button:has-text("CC")',
                'button[aria-label*="Captions"]',
                'button[aria-label*="Subtitles"]',
                '[data-tooltip*="Transcript"]',
                'button.transcript-btn',
                'div.controls button:has-text("Transcript")',
                # Echo360 specific selectors
                '.echo-transcript-button',
                '.transcript-toggle',
                'button[class*="transcript"]',
                '[class*="transcript-button"]',
                '[class*="cc-button"]',
                '[class*="caption"]',
                # More generic button selectors
                'button[type="button"]',
                '[role="button"]',
                'div.controls button',
                '.player-controls button',
                # Icon-based buttons
                'button svg',
                'button i'
            ]
            
            transcript_found = False
            for selector in transcript_button_selectors:
                try:
                    transcript_btn = await self.page.wait_for_selector(selector, timeout=2000)
                    if transcript_btn:
                        print("   → Found Transcript button, clicking...")
                        await transcript_btn.click()
                        await asyncio.sleep(2)  # Wait for transcript panel to open
                        transcript_found = True
                        break
                except:
                    continue
            
            if not transcript_found:
                print("   ❌ Could not find Transcript button")
                return False
            
            print("   ✅ Opened transcript panel")
            
            # Step 2: Look for Download button in the transcript panel
            print("\n📥 Looking for Download button in transcript panel...")
            
            download_button_selectors = [
                'button:has-text("Download")',
                'a:has-text("Download")',
                'button[aria-label*="Download"]',
                'button[title*="Download"]',
                'a[title*="Download"]',
                '[aria-label*="Download transcript"]',
                'button.download-btn',
                'a.download-link',
                # Icon-based selectors
                'button svg[class*="download"]',
                'button i[class*="download"]',
                '[role="button"]:has-text("Download")',
                # Echo360 specific
                '.transcript-download',
                '.download-transcript-button'
            ]
            
            download_found = False
            for selector in download_button_selectors:
                try:
                    download_btn = await self.page.wait_for_selector(selector, timeout=2000)
                    if download_btn:
                        print("   → Found Download button")
                        
                        # Set up download handler before clicking
                        try:
                            async with self.page.expect_download() as download_info:
                                await download_btn.click()
                                print("   → Clicked Download, waiting for file...")
                                download = await download_info.value
                                
                                # Save the .txt file
                                filename = download.suggested_filename
                                if not filename.endswith('.txt'):
                                    filename = filename.rsplit('.', 1)[0] + '.txt'
                                
                                save_path = self.download_dir / filename
                                await download.save_as(save_path)
                                print(f"   ✅ Transcript downloaded: {save_path.name}")
                                print(f"   📁 Saved to: {save_path}")
                                return True
                        except Exception as e:
                            print(f"   → Download error: {str(e)}")
                            
                            # Alternative: Check if it opens a modal/popup for download options
                            print("   → Checking for download format options...")
                            await asyncio.sleep(1)
                            
                            # Look for TXT option if there's a format selection
                            txt_selectors = [
                                'button:has-text("TXT")',
                                'a:has-text("TXT")',
                                'button:has-text(".txt")',
                                'a:has-text(".txt")',
                                'label:has-text("TXT")',
                                'input[value="TXT"]',
                                'a[href$=".txt"]'
                            ]
                            
                            for txt_sel in txt_selectors:
                                try:
                                    txt_option = await self.page.wait_for_selector(txt_sel, timeout=1500)
                                    if txt_option:
                                        print("   → Found TXT option, downloading...")
                                        
                                        async with self.page.expect_download() as download_info:
                                            await txt_option.click()
                                            download = await download_info.value
                                            
                                            save_path = self.download_dir / download.suggested_filename
                                            await download.save_as(save_path)
                                            print(f"   ✅ Transcript downloaded: {save_path.name}")
                                            return True
                                except:
                                    continue
                        
                        download_found = True
                        break
                except:
                    continue
            
            if not download_found:
                print("   ❌ Could not find Download button")
            
            return False
            
        except Exception as e:
            print(f"\n❌ Phase 3 Error: {str(e)}")
            return False
    
    async def get_all_courses(self) -> List[Dict[str, str]]:
        """
        Get a list of all available courses from the dashboard
        
        Returns:
            List of dictionaries with course info (name and href)
        """
        courses = []
        
        try:
            # Wait for dashboard to fully load with multiple strategies
            print("   → Waiting for dashboard content to load...")
            await asyncio.sleep(3)
            
            # Wait for network to be idle
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
            # Try multiple selectors for course cards/links
            course_selectors = [
                'div.ic-DashboardCard a',  # Dashboard card links
                'a.ic-DashboardCard__link',  # Specific card links
                'div[class*="DashboardCard"] a',  # Any dashboard card variant
                'a[href*="/courses/"][class*="Card"]',  # Card-style links
                'a[href*="/courses/"]',  # Any course link
            ]
            
            all_links = []
            for selector in course_selectors:
                try:
                    links = await self.page.query_selector_all(selector)
                    if links:
                        print(f"   → Found {len(links)} links using selector: {selector[:50]}...")
                        all_links.extend(links)
                        break
                except:
                    continue
            
            if not all_links:
                # Fallback: try to get all links and filter
                print("   → Using fallback method to find course links...")
                all_page_links = await self.page.query_selector_all('a')
                all_links = [link for link in all_page_links 
                           if '/courses/' in (await link.get_attribute('href') or '')]
            
            print(f"   → Total course links found: {len(all_links)}")
            
            # Process each link
            for link in all_links:
                try:
                    href = await link.get_attribute('href')
                    # Try to get only the direct text, not all child text
                    try:
                        # Use innerText to avoid duplicates
                        text = await self.page.evaluate('(el) => el.innerText', link)
                    except:
                        text = await link.text_content()
                    
                    if text and text.strip() and href and '/courses/' in href:
                        # Extract course ID from href
                        parts = href.split('/courses/')
                        if len(parts) > 1:
                            course_id = parts[1].split('/')[0].split('?')[0]
                            
                            # Skip if not a valid course ID (should be numeric)
                            if not course_id.isdigit():
                                continue
                            
                            # Skip duplicates
                            if not any(c['id'] == course_id for c in courses):
                                # Clean up course name - remove duplicates and extra whitespace
                                course_name = text.strip()
                                # Remove duplicate patterns (e.g., "COMPSCI 360COMPSCI 360" -> "COMPSCI 360")
                                lines = course_name.split('\n')
                                if lines:
                                    # Take the first non-empty line as the course name
                                    course_name = lines[0].strip()
                                
                                # Skip if text is too short or looks like a button
                                if len(course_name) > 2 and not course_name.lower() in ['view', 'edit', 'settings']:
                                    courses.append({
                                        'id': course_id,
                                        'name': course_name,
                                        'href': href if href.startswith('http') else f"https://umamherst.instructure.com{href}"
                                    })
                                    print(f"      • {course_name} (ID: {course_id})")
                except Exception as e:
                    # Silently skip problematic links
                    continue
            
        except Exception as e:
            print(f"   ❌ Error getting courses: {str(e)}")
        
        return courses
    
    async def scrape_all_courses(self) -> Dict[str, Any]:
        """
        Scrape transcripts from all available courses
        
        Returns:
            Dictionary with overall scraping results
        """
        result = {
            "success": False,
            "courses_found": 0,
            "transcripts_downloaded": 0,
            "courses": [],
            "errors": []
        }
        
        try:
            # Initialize browser
            await self.initialize_browser()
            
            # Phase 1: Login and Dashboard
            if not await self.phase1_login_and_dashboard():
                result["errors"].append("Failed to login")
                return result
            
            print("\n✅ Successfully reached Canvas dashboard!")
            
            # Get all available courses
            print("\n📚 Getting list of all courses...")
            courses = await self.get_all_courses()
            result["courses_found"] = len(courses)
            result["courses"] = [{"id": c['id'], "name": c['name']} for c in courses]
            
            if not courses:
                print("   ⚠️  No courses found on dashboard")
                return result
            
            print(f"\n🎯 Found {len(courses)} courses. Starting to scrape transcripts...")
            
            # Sort courses to prioritize CS 446 (Search Engines) for testing
            sorted_courses = []
            cs446_course = None
            other_courses = []
            
            for course in courses:
                if '446' in course['name'] or 'Search Engines' in course['name']:
                    cs446_course = course
                else:
                    other_courses.append(course)
            
            # Put CS 446 first if found
            if cs446_course:
                sorted_courses = [cs446_course] + other_courses
                print(f"   📌 Prioritizing CS 446 (Search Engines) for testing")
            else:
                sorted_courses = courses
            
            # Track visited courses
            visited_courses = set()
            
            # Try to scrape each course
            for i, course in enumerate(sorted_courses, 1):
                # Skip if already visited
                if course['id'] in visited_courses:
                    continue
                    
                visited_courses.add(course['id'])
                print(f"\n[{i}/{len(sorted_courses)}] Processing: {course['name']}")
                
                try:
                    # Check if browser is still alive
                    try:
                        await self.page.evaluate('() => true')
                    except:
                        print("   ⚠️  Browser crashed, reinitializing...")
                        await self.initialize_browser()
                        # Re-login after browser restart
                        print("   → Re-authenticating...")
                        if not await self.phase1_login_and_dashboard():
                            print("   ❌ Failed to re-login after browser crash")
                            continue
                    
                    # Navigate back to dashboard with timeout handling
                    print("   → Returning to dashboard...")
                    try:
                        await self.page.goto("https://umamherst.instructure.com/", wait_until="networkidle", timeout=30000)
                    except:
                        # If navigation fails, try with reduced wait
                        print("   → Navigation timeout, retrying with reduced wait...")
                        try:
                            await self.page.goto("https://umamherst.instructure.com/", wait_until="domcontentloaded", timeout=15000)
                        except:
                            print("   → Skipping course due to navigation issues")
                            continue
                    
                    await asyncio.sleep(2)
                    
                    # Navigate to course and try to download transcript
                    if await self.phase2_course_navigation(course['name']):
                        echo360_result = await self.phase3_echo360_transcript_download()
                        if echo360_result:
                            result["transcripts_downloaded"] += 1
                            print(f"   ✅ Successfully downloaded transcript for {course['name']}")
                            # For testing, you might want to stop after first successful download
                            # Uncomment the next line to stop after first success:
                            # break
                        else:
                            print(f"   ⚠️  No Echo360/transcripts found for {course['name']}")
                            print(f"   → Moving to next unvisited course...")
                    else:
                        print(f"   ⚠️  Could not navigate to {course['name']}")
                        
                except Exception as e:
                    error_msg = f"Error processing {course['name']}: {str(e)}"
                    print(f"   ❌ {error_msg}")
                    result["errors"].append(error_msg)
            
            result["success"] = result["transcripts_downloaded"] > 0
            
        except Exception as e:
            result["errors"].append(str(e))
            print(f"\n❌ Overall error: {str(e)}")
        
        finally:
            # Clean up
            if self.browser:
                await self.browser.close()
        
        return result
    
    async def run(self, course_name: str) -> Dict[str, Any]:
        """Execute the complete scraping workflow"""
        result = {
            "success": False,
            "phases_completed": [],
            "transcript_downloaded": False,
            "errors": []
        }
        
        try:
            # Initialize browser
            await self.initialize_browser()
            
            # Phase 1: Login and Dashboard
            if await self.phase1_login_and_dashboard():
                result["phases_completed"].append("login_dashboard")
                
                # Phase 2: Course Navigation
                if await self.phase2_course_navigation(course_name):
                    result["phases_completed"].append("course_navigation")
                    
                    # Phase 3: Echo360 and Download
                    if await self.phase3_echo360_transcript_download():
                        result["phases_completed"].append("transcript_download")
                        result["transcript_downloaded"] = True
                        result["success"] = True
                    else:
                        result["errors"].append("Failed to download transcript")
                else:
                    result["errors"].append("Failed to navigate to course")
            else:
                result["errors"].append("Failed to login")
            
        except Exception as e:
            result["errors"].append(str(e))
        
        finally:
            # Clean up
            if self.browser:
                await self.browser.close()
        
        return result
    
    async def __aenter__(self):
        await self.initialize_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()


# Main execution function
async def scrape_canvas_transcripts(username: str, password: str, course_name: str, headless: bool = False):
    """
    Main function to scrape Canvas transcripts
    
    Args:
        username: Canvas username
        password: Canvas password
        course_name: Name of the course to access
        headless: Whether to run browser in headless mode
    
    Returns:
        Dictionary with scraping results
    """
    scraper = AdvancedCanvasScraper(username, password, headless)
    return await scraper.run(course_name)


# Example usage
if __name__ == "__main__":
    import sys
    
    # Load credentials from environment
    load_dotenv()
    
    username = os.getenv("CANVAS_USERNAME")
    password = os.getenv("CANVAS_PASSWORD")
    
    if not username or not password:
        print("❌ Please set CANVAS_USERNAME and CANVAS_PASSWORD in .env file")
        sys.exit(1)
    
    # Get course name from command line or use default
    course_name = sys.argv[1] if len(sys.argv) > 1 else "COMPSCI 446"
    
    print(f"🚀 Starting Canvas transcript scraper for course: {course_name}")
    print(f"   Username: {username[:3]}***")
    print(f"   Headless: False (browser will be visible)")
    print()
    
    # Run the scraper
    result = asyncio.run(scrape_canvas_transcripts(
        username=username,
        password=password,
        course_name=course_name,
        headless=False  # Set to True for production
    ))
    
    # Print results
    print("\n" + "="*60)
    print("SCRAPING RESULTS")
    print("="*60)
    print(f"Success: {result['success']}")
    print(f"Phases Completed: {', '.join(result['phases_completed'])}")
    print(f"Transcript Downloaded: {result['transcript_downloaded']}")
    if result['errors']:
        print(f"Errors: {', '.join(result['errors'])}")
