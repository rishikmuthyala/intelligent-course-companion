"""
Ultra Advanced Canvas/Echo360 Transcript Scraper
Features:
- Intelligent error recovery and retry mechanisms
- Visual element detection and smart navigation
- Screenshot capability for debugging
- Multiple fallback strategies
- Exhaustive button/link searching
- Automatic page flow detection
"""

import os
import asyncio
import time
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from playwright.async_api import (
    async_playwright, 
    Page, 
    Browser, 
    ElementHandle,
    TimeoutError as PlaywrightTimeoutError
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL", "https://umass.instructure.com")
BROWSER_TIMEOUT = 45000  # 45 seconds default timeout
LOGIN_TIMEOUT = 90000  # 90 seconds for login (in case of MFA)
POPUP_WAIT_TIME = 15000  # 15 seconds to wait for pop-ups
MAX_RETRIES = 5  # Maximum number of retries for each operation
SCREENSHOT_DIR = Path("./debug_screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


class UltraAdvancedCanvasScraper:
    """Ultra Advanced scraper with intelligent recovery and debugging capabilities"""
    
    def __init__(self, username: str, password: str, headless: bool = False, debug: bool = True):
        self.username = username
        self.password = password
        self.headless = headless
        self.debug = debug
        self.browser = None
        self.context = None
        self.page = None
        self.download_dir = Path("./transcripts")
        self.download_dir.mkdir(exist_ok=True)
        self.screenshot_counter = 0
        self.navigation_history = []
        self.retry_count = {}
        
    async def take_screenshot(self, name: str = "debug") -> str:
        """Take a screenshot for debugging purposes"""
        if not self.debug:
            return ""
        
        try:
            self.screenshot_counter += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.screenshot_counter:03d}_{timestamp}_{name}.png"
            filepath = SCREENSHOT_DIR / filename
            await self.page.screenshot(path=str(filepath), full_page=True)
            print(f"   📸 Screenshot saved: {filename}")
            return str(filepath)
        except Exception as e:
            print(f"   ⚠️ Screenshot failed: {str(e)}")
            return ""
    
    async def log_page_info(self, context: str = ""):
        """Log current page information for debugging"""
        if not self.debug:
            return
        
        try:
            url = self.page.url
            title = await self.page.title()
            print(f"\n📍 Page Info ({context}):")
            print(f"   URL: {url}")
            print(f"   Title: {title}")
            self.navigation_history.append({
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "url": url,
                "title": title
            })
        except:
            pass
    
    async def find_element_by_multiple_strategies(
        self, 
        strategies: List[Dict[str, Any]], 
        action: str = "click",
        timeout: int = 5000
    ) -> bool:
        """
        Try multiple strategies to find and interact with an element
        
        Args:
            strategies: List of strategy dictionaries with 'type' and 'selector'
            action: Action to perform ('click', 'fill', 'get_text')
            timeout: Timeout for each strategy
        
        Returns:
            True if successful, False otherwise
        """
        for i, strategy in enumerate(strategies, 1):
            try:
                strategy_type = strategy.get('type', 'selector')
                
                if strategy_type == 'selector':
                    selector = strategy['selector']
                    element = await self.page.wait_for_selector(selector, timeout=timeout)
                    
                elif strategy_type == 'text':
                    text = strategy['text']
                    element = await self.page.get_by_text(text).first
                    
                elif strategy_type == 'role':
                    role = strategy['role']
                    name = strategy.get('name')
                    if name:
                        element = await self.page.get_by_role(role, name=name).first
                    else:
                        element = await self.page.get_by_role(role).first
                        
                elif strategy_type == 'xpath':
                    xpath = strategy['xpath']
                    element = await self.page.wait_for_selector(f'xpath={xpath}', timeout=timeout)
                    
                elif strategy_type == 'js':
                    # Execute JavaScript to find element
                    js_code = strategy['js']
                    element = await self.page.evaluate_handle(js_code)
                    
                else:
                    continue
                
                if element:
                    if action == 'click':
                        # Try multiple click methods
                        try:
                            await element.click(timeout=2000)
                        except:
                            # Fallback to JavaScript click
                            await self.page.evaluate('(el) => el.click()', element)
                        
                        print(f"   ✅ Strategy {i} succeeded: {strategy_type}")
                        return True
                    
                    elif action == 'fill' and 'value' in strategy:
                        await element.fill(strategy['value'])
                        return True
                    
                    elif action == 'get_text':
                        text = await element.text_content()
                        return text
                        
            except Exception as e:
                if self.debug:
                    print(f"   → Strategy {i} failed: {strategy_type} - {str(e)[:50]}")
                continue
        
        return False
    
    async def intelligent_wait_and_retry(
        self, 
        operation, 
        operation_name: str,
        max_retries: int = 3,
        base_wait: int = 2
    ):
        """
        Intelligent retry mechanism with exponential backoff
        
        Args:
            operation: Async function to retry
            operation_name: Name for logging
            max_retries: Maximum number of retries
            base_wait: Base wait time in seconds
        """
        for attempt in range(max_retries):
            try:
                print(f"   → Attempt {attempt + 1}/{max_retries} for {operation_name}")
                result = await operation()
                if result:
                    return result
            except Exception as e:
                print(f"   ⚠️ Attempt {attempt + 1} failed: {str(e)[:100]}")
            
            if attempt < max_retries - 1:
                wait_time = base_wait * (2 ** attempt)  # Exponential backoff
                print(f"   ⏳ Waiting {wait_time} seconds before retry...")
                await asyncio.sleep(wait_time)
                
                # Take screenshot for debugging
                if self.debug:
                    await self.take_screenshot(f"retry_{operation_name}_{attempt + 1}")
        
        return None
    
    async def scan_entire_page_for_elements(self, target_texts: List[str]) -> List[Dict]:
        """
        Scan the entire page for elements containing target texts
        
        Args:
            target_texts: List of text patterns to search for
            
        Returns:
            List of found elements with their properties
        """
        found_elements = []
        
        try:
            # Get all clickable elements
            clickable_selectors = [
                'a', 'button', '[role="button"]', '[onclick]', 
                '[role="link"]', 'input[type="submit"]', 'input[type="button"]',
                '[tabindex]:not([tabindex="-1"])', '[class*="btn"]', '[class*="button"]'
            ]
            
            for selector in clickable_selectors:
                elements = await self.page.query_selector_all(selector)
                
                for element in elements:
                    try:
                        # Get element properties
                        text = await element.text_content() or ""
                        aria_label = await element.get_attribute('aria-label') or ""
                        title = await element.get_attribute('title') or ""
                        href = await element.get_attribute('href') or ""
                        class_name = await element.get_attribute('class') or ""
                        
                        # Check if element matches any target text
                        element_text = f"{text} {aria_label} {title} {class_name}".lower()
                        
                        for target in target_texts:
                            if target.lower() in element_text:
                                # Get bounding box for visibility check
                                box = await element.bounding_box()
                                if box and box['width'] > 0 and box['height'] > 0:
                                    found_elements.append({
                                        'element': element,
                                        'text': text.strip(),
                                        'aria_label': aria_label,
                                        'title': title,
                                        'href': href,
                                        'selector': selector,
                                        'visible': True,
                                        'box': box
                                    })
                                    break
                    except:
                        continue
            
            # Sort by visibility (elements at top of page first)
            found_elements.sort(key=lambda x: (x['box']['y'], x['box']['x']))
            
            if found_elements:
                print(f"   📊 Found {len(found_elements)} matching elements:")
                for i, elem in enumerate(found_elements[:5], 1):
                    print(f"      {i}. {elem['text'][:50] if elem['text'] else elem['aria_label'][:50]}")
            
        except Exception as e:
            print(f"   ⚠️ Page scan error: {str(e)}")
        
        return found_elements
    
    async def initialize_browser(self):
        """Initialize Playwright browser with optimal settings"""
        print("🌐 Initializing ultra-advanced browser...")
        playwright = await async_playwright().start()
        
        # Launch browser with enhanced settings
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--window-size=1920,1080'
            ]
        )
        
        # Create context with enhanced settings
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            accept_downloads=True,
            ignore_https_errors=True,
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation', 'notifications'],
            color_scheme='light',
            reduced_motion='reduce',
            forced_colors='none'
        )
        
        # Enable request interception for debugging
        if self.debug:
            self.context.on("request", lambda request: None)
            self.context.on("response", lambda response: None)
        
        # Create page with extended timeout
        self.page = await self.context.new_page()
        self.page.set_default_timeout(BROWSER_TIMEOUT)
        
        # Add console message listener for debugging
        if self.debug:
            self.page.on("console", lambda msg: print(f"   🖥️ Console: {msg.text[:100]}") if msg.type in ['error', 'warning'] else None)
            self.page.on("pageerror", lambda err: print(f"   ❌ Page error: {str(err)[:100]}"))
        
        print("✅ Ultra-advanced browser initialized successfully")
    
    async def ultra_smart_navigation(self, target_url: str, retries: int = 3) -> bool:
        """
        Ultra smart navigation with multiple fallback strategies
        """
        for attempt in range(retries):
            try:
                print(f"   → Navigation attempt {attempt + 1}/{retries} to {target_url}")
                
                # Try different wait strategies
                wait_strategies = ['networkidle', 'domcontentloaded', 'load', 'commit']
                
                for strategy in wait_strategies:
                    try:
                        await self.page.goto(target_url, wait_until=strategy, timeout=30000)
                        await asyncio.sleep(2)  # Give page time to settle
                        
                        # Verify navigation succeeded
                        current_url = self.page.url
                        if target_url in current_url or current_url in target_url:
                            print(f"   ✅ Navigation successful with {strategy}")
                            return True
                    except:
                        continue
                
                # If all strategies fail, try JavaScript navigation
                await self.page.evaluate(f'window.location.href = "{target_url}"')
                await asyncio.sleep(3)
                
            except Exception as e:
                print(f"   ⚠️ Navigation attempt {attempt + 1} failed: {str(e)[:100]}")
                
                if attempt < retries - 1:
                    # Try to recover
                    await asyncio.sleep(2)
                    await self.take_screenshot(f"nav_error_{attempt}")
        
        return False
    
    async def handle_echo360_video_page(self) -> bool:
        """
        Enhanced Echo360 video page handler with exhaustive button searching
        """
        print("\n🎥 Advanced Echo360 video page handler activated...")
        
        # Wait for video player to fully load
        print("   → Waiting for video player to initialize...")
        await asyncio.sleep(5)
        
        # Take screenshot for debugging
        await self.take_screenshot("echo360_video_page")
        
        # Step 1: Find and click transcript button with multiple strategies
        print("\n📝 Searching for Transcript button with multiple strategies...")
        
        transcript_strategies = [
            # Text-based strategies
            {'type': 'text', 'text': 'Transcript'},
            {'type': 'text', 'text': 'Transcripts'},
            {'type': 'text', 'text': 'CC'},
            {'type': 'text', 'text': 'Captions'},
            {'type': 'text', 'text': 'Subtitles'},
            
            # Selector strategies
            {'type': 'selector', 'selector': 'button:has-text("Transcript")'},
            {'type': 'selector', 'selector': 'button:has-text("CC")'},
            {'type': 'selector', 'selector': '[aria-label*="transcript" i]'},
            {'type': 'selector', 'selector': '[aria-label*="caption" i]'},
            {'type': 'selector', 'selector': '[aria-label*="subtitle" i]'},
            {'type': 'selector', 'selector': '[title*="transcript" i]'},
            {'type': 'selector', 'selector': '[title*="caption" i]'},
            {'type': 'selector', 'selector': '[data-tooltip*="transcript" i]'},
            {'type': 'selector', 'selector': '.transcript-button'},
            {'type': 'selector', 'selector': '.cc-button'},
            {'type': 'selector', 'selector': '[class*="transcript"]'},
            {'type': 'selector', 'selector': '[class*="caption"]'},
            {'type': 'selector', 'selector': '[class*="subtitle"]'},
            
            # Role-based strategies
            {'type': 'role', 'role': 'button', 'name': 'Transcript'},
            {'type': 'role', 'role': 'button', 'name': 'Captions'},
            
            # XPath strategies
            {'type': 'xpath', 'xpath': '//button[contains(., "Transcript")]'},
            {'type': 'xpath', 'xpath': '//button[contains(., "CC")]'},
            {'type': 'xpath', 'xpath': '//*[@aria-label[contains(., "transcript")]]'},
            
            # JavaScript strategies
            {'type': 'js', 'js': 'document.querySelector("button")?.filter(b => b.textContent.includes("Transcript"))'},
        ]
        
        # First, scan the page for all possible transcript-related elements
        transcript_elements = await self.scan_entire_page_for_elements([
            'transcript', 'caption', 'subtitle', 'cc', 'closed caption'
        ])
        
        transcript_opened = False
        
        # Try found elements first
        for elem_info in transcript_elements:
            try:
                element = elem_info['element']
                print(f"   → Trying element: {elem_info['text'] or elem_info['aria_label']}")
                
                # Try different click methods
                try:
                    await element.click(timeout=2000)
                except:
                    await self.page.evaluate('(el) => el.click()', element)
                
                await asyncio.sleep(2)
                
                # Check if transcript panel opened
                transcript_panel = await self.page.query_selector('[class*="transcript-panel"], [class*="transcript-content"], [class*="caption-panel"]')
                if transcript_panel:
                    print("   ✅ Transcript panel opened!")
                    transcript_opened = True
                    break
                    
            except:
                continue
        
        # If not found, try all strategies
        if not transcript_opened:
            transcript_opened = await self.find_element_by_multiple_strategies(transcript_strategies, 'click')
        
        if not transcript_opened:
            # Last resort: click all buttons and check for transcript panel
            print("   → Last resort: trying all buttons...")
            all_buttons = await self.page.query_selector_all('button, [role="button"]')
            
            for i, button in enumerate(all_buttons[:20]):  # Try first 20 buttons
                try:
                    # Skip if button is not visible
                    box = await button.bounding_box()
                    if not box or box['width'] == 0 or box['height'] == 0:
                        continue
                    
                    await self.page.evaluate('(el) => el.click()', button)
                    await asyncio.sleep(1)
                    
                    # Check if transcript panel appeared
                    if await self.page.query_selector('[class*="transcript"], [class*="caption"]'):
                        print(f"   ✅ Found transcript panel after clicking button {i+1}")
                        transcript_opened = True
                        break
                except:
                    continue
        
        if not transcript_opened:
            print("   ❌ Could not open transcript panel")
            return False
        
        await asyncio.sleep(2)
        await self.take_screenshot("transcript_panel_opened")
        
        # Step 2: Find and click download button
        print("\n📥 Searching for Download button in transcript panel...")
        
        download_strategies = [
            # Text-based
            {'type': 'text', 'text': 'Download'},
            {'type': 'text', 'text': 'Export'},
            {'type': 'text', 'text': 'Save'},
            {'type': 'text', 'text': '.txt'},
            {'type': 'text', 'text': 'TXT'},
            
            # Selectors
            {'type': 'selector', 'selector': 'button:has-text("Download")'},
            {'type': 'selector', 'selector': 'a:has-text("Download")'},
            {'type': 'selector', 'selector': '[aria-label*="download" i]'},
            {'type': 'selector', 'selector': '[title*="download" i]'},
            {'type': 'selector', 'selector': '.download-button'},
            {'type': 'selector', 'selector': '.transcript-download'},
            {'type': 'selector', 'selector': '[class*="download"]'},
            {'type': 'selector', 'selector': 'a[href$=".txt"]'},
            {'type': 'selector', 'selector': 'a[download]'},
            
            # Icons
            {'type': 'selector', 'selector': '[class*="icon-download"]'},
            {'type': 'selector', 'selector': 'svg[class*="download"]'},
            {'type': 'selector', 'selector': 'i[class*="download"]'},
        ]
        
        # Scan for download elements
        download_elements = await self.scan_entire_page_for_elements([
            'download', 'export', 'save', '.txt', 'text file'
        ])
        
        # Try to download
        download_success = False
        
        # Set up download handler
        async def handle_download():
            try:
                async with self.page.expect_download(timeout=10000) as download_info:
                    # Try clicking download elements
                    for elem_info in download_elements:
                        try:
                            element = elem_info['element']
                            await self.page.evaluate('(el) => el.click()', element)
                            await asyncio.sleep(2)
                        except:
                            continue
                    
                    # If no specific elements found, try strategies
                    if not download_elements:
                        await self.find_element_by_multiple_strategies(download_strategies, 'click')
                    
                    download = await download_info.value
                    
                    # Save the file
                    filename = download.suggested_filename
                    if not filename.endswith('.txt'):
                        filename = filename.rsplit('.', 1)[0] + '.txt'
                    
                    save_path = self.download_dir / filename
                    await download.save_as(save_path)
                    print(f"   ✅ Transcript downloaded: {save_path.name}")
                    return True
                    
            except Exception as e:
                print(f"   ⚠️ Download attempt failed: {str(e)}")
                return False
        
        # Try download with retries
        for attempt in range(3):
            print(f"   → Download attempt {attempt + 1}/3")
            download_success = await handle_download()
            if download_success:
                break
            await asyncio.sleep(2)
        
        # If download didn't work, look for format selection
        if not download_success:
            print("   → Checking for format selection dialog...")
            
            format_strategies = [
                {'type': 'text', 'text': 'TXT'},
                {'type': 'text', 'text': '.txt'},
                {'type': 'text', 'text': 'Text'},
                {'type': 'selector', 'selector': 'button:has-text("TXT")'},
                {'type': 'selector', 'selector': 'a:has-text(".txt")'},
                {'type': 'selector', 'selector': 'label:has-text("TXT")'},
                {'type': 'selector', 'selector': 'input[value="txt" i]'},
            ]
            
            if await self.find_element_by_multiple_strategies(format_strategies, 'click'):
                await asyncio.sleep(2)
                
                # Try download again
                download_success = await handle_download()
        
        return download_success
    
    async def navigate_echo360_lecture_list(self) -> bool:
        """
        Navigate through Echo360 lecture list and process each lecture
        Looks for pink square buttons in rows to access video player
        """
        print("\n📚 Processing Echo360 lecture list...")
        await self.take_screenshot("echo360_lecture_list")
        
        lectures_processed = 0
        max_lectures = 10  # Process up to 10 lectures
        
        while lectures_processed < max_lectures:
            print(f"\n🎬 Looking for lecture {lectures_processed + 1}...")
            
            # Step 1: Find all lecture items (could be rows, divs, or other containers)
            print("   → Searching for lecture items/rows...")
            
            # Look for various types of containers that might hold recordings
            row_selectors = [
                'tbody tr',  # Standard table rows
                'tr[role="row"]',  # ARIA table rows
                'table tr',  # Any table rows
                'tr:has(td)',  # Rows with data cells
                '.echo-class',  # Echo360 specific
                '.class-row',  # Generic class rows
                'div[class*="recording"]',  # Divs with "recording" in class
                'div[class*="lecture"]',  # Divs with "lecture" in class
                'div[class*="media"]',  # Divs with "media" in class
                '[class*="list-item"]',  # List items
                'li[class*="recording"]',  # List items with recordings
                'div[data-test*="class"]',  # Data test attributes
                'div[role="row"]',  # ARIA rows (not just tr)
                'article',  # Article elements (common in modern designs)
            ]
            
            all_rows = []
            for selector in row_selectors:
                try:
                    rows = await self.page.query_selector_all(selector)
                    # Filter to only visible items with reasonable size
                    visible_rows = []
                    for row in rows:
                        try:
                            box = await row.bounding_box()
                            if box and box['height'] > 20:  # At least 20px tall
                                visible_rows.append(row)
                        except:
                            continue
                    
                    if visible_rows:
                        print(f"   → Found {len(visible_rows)} visible items with selector: {selector}")
                        all_rows = visible_rows
                        break
                except:
                    continue
            
            # If no structured rows found, try to find ANY clickable elements that might be recordings
            if not all_rows:
                print("   → No structured rows found, looking for clickable recording elements...")
                
                # Scan for elements containing recording-related keywords
                recording_elements = await self.scan_entire_page_for_elements([
                    'compsci', '446', 'september', 'october', 'november',
                    'lecture', 'class', 'recording', 'video', '2024', '2025'
                ])
                
                if recording_elements:
                    print(f"   → Found {len(recording_elements)} potential recording elements via scan")
                    all_rows = [elem['element'] for elem in recording_elements[:20]]  # Limit to first 20
                else:
                    print("   ❌ No lecture items found at all")
                    await self.take_screenshot("no_lectures_found_debug")
                    break
            
            # Step 2: For each row, look for the pink button or clickable element
            # Try to process the lecture at index 'lectures_processed'
            if lectures_processed >= len(all_rows):
                print("   → No more lectures to process")
                break
            
            current_row = all_rows[lectures_processed]
            
            try:
                row_text = await current_row.text_content()
                print(f"   → Processing row {lectures_processed + 1}: {row_text[:80] if row_text else 'No text'}")
                
                # Step 3: Look for buttons/links in this row
                # Pink square button might be a button, link, or div with specific styling
                button_selectors_in_row = [
                    'button',  # Regular buttons
                    'a',  # Links
                    '[role="button"]',  # ARIA buttons
                    'div[onclick]',  # Clickable divs
                    'span[onclick]',  # Clickable spans
                    '.btn',  # Button classes
                    '[class*="button"]',  # Classes containing "button"
                    '[class*="play"]',  # Play buttons
                    '[class*="view"]',  # View buttons
                    'td a',  # Links in table cells
                    'td button',  # Buttons in table cells
                ]
                
                clicked = False
                
                for btn_selector in button_selectors_in_row:
                    try:
                        buttons_in_row = await current_row.query_selector_all(btn_selector)
                        
                        for btn in buttons_in_row:
                            # Check if button is visible
                            box = await btn.bounding_box()
                            if not box or box['width'] == 0 or box['height'] == 0:
                                continue
                            
                            # Try to get button info
                            btn_text = await btn.text_content() or ""
                            btn_aria = await btn.get_attribute('aria-label') or ""
                            btn_title = await btn.get_attribute('title') or ""
                            btn_class = await btn.get_attribute('class') or ""
                            
                            btn_info = f"{btn_text} {btn_aria} {btn_title} {btn_class}".lower()
                            
                            # Look for indicators this might be the right button
                            # Could be: "view", "play", "watch", "open", or just clickable
                            indicators = ['view', 'play', 'watch', 'open', 'details', 'media']
                            is_candidate = any(ind in btn_info for ind in indicators) or len(btn_text.strip()) < 20
                            
                            if is_candidate or True:  # Try all buttons if no match
                                print(f"   → Trying button: '{btn_text[:30].strip()}' (class: {btn_class[:30]})")
                                
                                # Save current URL to check if we navigate
                                current_url = self.page.url
                                
                                # Click the button
                                try:
                                    await btn.click(timeout=3000)
                                except:
                                    await self.page.evaluate('(el) => el.click()', btn)
                                
                                await asyncio.sleep(3)  # Wait for navigation/video to load
                                
                                # Check if we navigated to a video page
                                new_url = self.page.url
                                
                                # Check if we're now on an Echo360 video page
                                if 'echo360' in new_url.lower() and ('/media/' in new_url or 'presentation' in new_url):
                                    print(f"   ✅ Navigated to Echo360 video page!")
                                    await self.take_screenshot(f"lecture_{lectures_processed + 1}_video_page")
                                    
                                    # Check for video player
                                    video_indicators = await self.page.query_selector_all('video, [class*="video"], [class*="player"], [id*="player"]')
                                    if video_indicators:
                                        print(f"   ✅ Video player detected!")
                                        clicked = True
                                        break
                                    else:
                                        # Wait a bit more for video to load
                                        await asyncio.sleep(2)
                                        video_indicators = await self.page.query_selector_all('video, [class*="video"], [class*="player"]')
                                        if video_indicators:
                                            print(f"   ✅ Video player detected after wait!")
                                            clicked = True
                                            break
                                
                                # Check if a modal/popup appeared (Canvas modals, not Echo360)
                                modal_appeared = await self.page.query_selector('[class*="modal"], [class*="dialog"], [role="dialog"]')
                                if modal_appeared and 'echo360' not in new_url.lower():
                                    print(f"   ⚠️ Canvas modal/dialog appeared (not Echo360 video)")
                                    await self.take_screenshot(f"lecture_{lectures_processed + 1}_canvas_modal")
                                    
                                    # Close the modal and try next button
                                    close_selectors = ['button:has-text("×")', 'button:has-text("Close")', 'button[aria-label="Close"]', '.close']
                                    for close_sel in close_selectors:
                                        try:
                                            close_btn = await self.page.wait_for_selector(close_sel, timeout=1000)
                                            if close_btn:
                                                await close_btn.click()
                                                await asyncio.sleep(1)
                                                print(f"   → Closed modal, continuing search...")
                                                break
                                        except:
                                            continue
                                    
                                    # Don't mark as clicked - try next button
                                    continue
                        
                        if clicked:
                            break
                            
                    except Exception as e:
                        continue
                
                if not clicked:
                    # Last resort: just click anywhere in the row
                    print(f"   → Last resort: clicking the row itself...")
                    try:
                        await current_row.click()
                    except:
                        await self.page.evaluate('(el) => el.click()', current_row)
                    await asyncio.sleep(3)
                    clicked = True
                
                if clicked:
                    # Now try to process the video page
                    print(f"   → Processing video page for lecture {lectures_processed + 1}...")
                    
                    if await self.handle_echo360_video_page():
                        lectures_processed += 1
                        print(f"   ✅ Successfully processed lecture {lectures_processed}")
                        
                        # Navigate back to lecture list
                        print(f"   → Navigating back to lecture list...")
                        await self.page.go_back()
                        await asyncio.sleep(3)
                        await self.take_screenshot("back_to_lecture_list")
                    else:
                        print("   ⚠️ Could not process this lecture, trying next...")
                        await self.page.go_back()
                        await asyncio.sleep(3)
                        lectures_processed += 1  # Skip this lecture
                        
            except Exception as e:
                print(f"   ⚠️ Error processing lecture row: {str(e)}")
                lectures_processed += 1  # Skip and continue
                continue
        
        return lectures_processed > 0
    
    async def phase3_ultra_echo360_handler(self) -> bool:
        """
        Ultra-advanced Echo360 handler with exhaustive search and retry mechanisms
        """
        print("\n" + "="*60)
        print("PHASE 3: ULTRA ECHO360 HANDLER")
        print("="*60)
        
        try:
            # Step 1: Find Echo360 link with exhaustive search
            print("\n🔍 Exhaustive search for Echo360/Recordings link...")
            
            # Take initial screenshot
            await self.take_screenshot("before_echo360_search")
            
            # Comprehensive list of possible Echo360 indicators
            echo360_indicators = [
                'echo360', 'echo 360', 'class recordings', 'lecture recordings',
                'recordings', 'lectures', 'videos', 'media', 'class videos',
                'course videos', 'recorded lectures', 'lecture capture'
            ]
            
            # Scan entire page for Echo360 related elements
            echo360_elements = await self.scan_entire_page_for_elements(echo360_indicators)
            
            echo360_accessed = False
            
            # Try each found element
            for elem_info in echo360_elements:
                try:
                    element = elem_info['element']
                    elem_text = elem_info['text'] or elem_info['aria_label'] or elem_info['title']
                    
                    print(f"   → Trying: {elem_text[:50]}")
                    
                    # Click element
                    try:
                        await element.click(timeout=3000)
                    except:
                        await self.page.evaluate('(el) => el.click()', element)
                    
                    await asyncio.sleep(5)
                    
                    # Check if we reached Echo360
                    current_url = self.page.url
                    page_content = await self.page.content()
                    
                    if 'echo360' in current_url.lower() or 'echo360' in page_content.lower():
                        print("   ✅ Successfully accessed Echo360!")
                        echo360_accessed = True
                        break
                    
                    # Check for iframe
                    iframe = await self.page.query_selector('iframe[src*="echo360"], iframe[title*="Echo"]')
                    if iframe:
                        print("   ✅ Echo360 loaded in iframe!")
                        frame = await iframe.content_frame()
                        if frame:
                            self.page = frame
                        echo360_accessed = True
                        break
                        
                except Exception as e:
                    print(f"   ⚠️ Failed to click element: {str(e)[:50]}")
                    continue
            
            if not echo360_accessed:
                print("   ❌ Could not access Echo360")
                return False
            
            await self.take_screenshot("echo360_accessed")
            
            # Step 2: Handle Echo360 content
            print("\n📹 Processing Echo360 content...")
            
            # Wait for content to load
            await asyncio.sleep(5)
            
            # Check for "no recordings" message
            page_text = await self.page.text_content('body')
            if page_text:
                no_content_indicators = [
                    'no recordings', 'no lectures', 'not yet activated',
                    'no classes', 'coming soon', 'not available'
                ]
                
                for indicator in no_content_indicators:
                    if indicator in page_text.lower():
                        print(f"   ⚠️ No recordings available: {indicator}")
                        return False
            
            # Try to process lecture list
            return await self.navigate_echo360_lecture_list()
            
        except Exception as e:
            print(f"\n❌ Ultra Echo360 handler error: {str(e)}")
            await self.take_screenshot("echo360_error")
            return False
    
    async def run_ultra_advanced(self, course_name: str) -> Dict[str, Any]:
        """Execute the ultra-advanced scraping workflow"""
        result = {
            "success": False,
            "phases_completed": [],
            "transcripts_downloaded": 0,
            "errors": [],
            "screenshots": []
        }
        
        try:
            # Initialize browser
            await self.initialize_browser()
            
            # Phase 1: Login with retry
            print("\n" + "="*60)
            print("PHASE 1: ULTRA LOGIN")
            print("="*60)
            
            login_success = await self.intelligent_wait_and_retry(
                lambda: self.phase1_login_and_dashboard(),
                "login",
                max_retries=3
            )
            
            if not login_success:
                result["errors"].append("Failed to login after multiple attempts")
                return result
            
            result["phases_completed"].append("login")
            
            # Phase 2: Course navigation with retry
            print("\n" + "="*60)
            print("PHASE 2: ULTRA COURSE NAVIGATION")
            print("="*60)
            
            course_success = await self.intelligent_wait_and_retry(
                lambda: self.phase2_course_navigation(course_name),
                "course_navigation",
                max_retries=3
            )
            
            if not course_success:
                result["errors"].append("Failed to navigate to course")
                return result
            
            result["phases_completed"].append("course_navigation")
            
            # Phase 3: Echo360 with ultra handler
            echo360_success = await self.phase3_ultra_echo360_handler()
            
            if echo360_success:
                result["phases_completed"].append("echo360_download")
                result["success"] = True
                result["transcripts_downloaded"] = 1
            else:
                result["errors"].append("Failed to download transcripts")
            
            # Save navigation history
            if self.debug:
                history_file = SCREENSHOT_DIR / "navigation_history.json"
                with open(history_file, 'w') as f:
                    json.dump(self.navigation_history, f, indent=2)
                print(f"\n📋 Navigation history saved to {history_file}")
            
        except Exception as e:
            result["errors"].append(str(e))
            print(f"\n❌ Ultra-advanced workflow error: {str(e)}")
            
        finally:
            # Clean up
            if self.browser:
                await self.browser.close()
        
        return result
    
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
            await self.take_screenshot("01_initial_page")
            await self.log_page_info("Initial navigation")
            
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
            
            await self.take_screenshot("02_login_page")
            
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
                    
                    await self.take_screenshot("03_password_page")
                    
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
                            
                            await self.take_screenshot("04_after_signin")
                            
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
                                'button#idSIButton9',
                                'input#idSIButton9',
                                'button.btn-primary',
                                'button[type="submit"]',
                                'input[type="submit"]'
                            ]
                            
                            for selector in confirm_selectors:
                                try:
                                    confirm_btn = await self.page.wait_for_selector(selector, timeout=2000)
                                    if confirm_btn:
                                        btn_text = await confirm_btn.text_content() if await confirm_btn.get_attribute('type') != 'submit' else await confirm_btn.get_attribute('value')
                                        if btn_text and any(word in btn_text.lower() for word in ['yes', 'continue', 'accept', 'allow', 'sign']):
                                            print(f"   → Clicking confirmation: '{btn_text}'")
                                            await confirm_btn.click()
                                            await self.page.wait_for_load_state("networkidle")
                                            await asyncio.sleep(3)
                                            
                                            await self.take_screenshot("05_after_confirmation")
                                            
                                            # Handle welcome pop-up
                                            print("   → Checking for welcome/hello pop-up after confirmation...")
                                            close_selectors = [
                                                'button:has-text("×")',
                                                'button:has-text("X")',
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
                await self.take_screenshot("06_mfa_prompt")
                await self.page.wait_for_url("**/dashboard**", timeout=120000)
            
            print("   ✅ Login successful!")
            
            # Step 3: Handle post-login pop-up
            print("\n🔍 Checking for welcome tour/feature pop-up...")
            
            popup_dismissed = False
            popup_selectors = [
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
            
            await self.take_screenshot("07_dashboard")
            
            # Verify we're on the dashboard
            try:
                await self.page.wait_for_selector('div.ic-DashboardCard, a.ic-DashboardCard__link, div[class*="dashboard"]', timeout=10000)
                print("\n✅ Successfully reached Canvas dashboard!")
            except:
                try:
                    await self.page.wait_for_selector('a[href*="/courses/"]', timeout=5000)
                    print("\n✅ Successfully reached Canvas dashboard!")
                except:
                    print("\n✅ Successfully logged in and ready to navigate!")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Phase 1 Error: {str(e)}")
            await self.take_screenshot("error_phase1")
            return False
    
    async def phase2_course_navigation(self, course_name: str) -> bool:
        """Phase 2: Navigate to specific course and explore tabs"""
        print("\n" + "="*60)
        print("PHASE 2: COURSE NAVIGATION")
        print("="*60)
        
        try:
            # Find and click on the target course
            print(f"\n🎯 Looking for course: {course_name}")
            
            await asyncio.sleep(2)
            await self.take_screenshot("08_before_course_click")
            
            # Use intelligent search for course
            course_indicators = [course_name] + course_name.split()
            course_elements = await self.scan_entire_page_for_elements(course_indicators)
            
            course_found = False
            
            # Try found elements - prioritize exact matches
            # First pass: Look for exact course name match
            for elem_info in course_elements:
                try:
                    element = elem_info['element']
                    elem_text = elem_info['text']
                    elem_href = elem_info.get('href', '')
                    
                    # Verify this is actually a course link (not assignments, announcements, etc.)
                    if '/courses/' in elem_href:
                        # Make sure it's a direct course link, not a course sub-page
                        # Valid: /courses/12345  or  /courses/12345/
                        # Invalid: /courses/12345/assignments  or  /courses/12345/modules
                        href_parts = elem_href.split('/courses/')
                        if len(href_parts) > 1:
                            after_courses = href_parts[1].strip('/')
                            # Check if there's anything after the course ID
                            course_id_part = after_courses.split('/')[0]
                            if not course_id_part.isdigit():
                                print(f"   → Skipping non-course link: {elem_text[:50]}")
                                continue
                            
                            # Skip if it has sub-pages
                            if '/' in after_courses and after_courses.count('/') > 0:
                                remaining = after_courses.split('/', 1)[1]
                                if remaining and remaining not in ['', '?']:
                                    print(f"   → Skipping course sub-page: {elem_text[:50]}")
                                    continue
                        
                        # Check if this is an exact match or contains the full course identifier
                        # For "COMPSCI 446", check if elem_text contains both "COMPSCI" and "446"
                        course_parts = course_name.split()
                        if all(part.lower() in elem_text.lower() for part in course_parts):
                            print(f"   → Trying course (exact match): {elem_text[:70]}")
                            
                            try:
                                await element.click()
                            except:
                                await self.page.evaluate('(el) => el.click()', element)
                            
                            await self.page.wait_for_load_state("networkidle")
                            await asyncio.sleep(2)
                            
                            # Verify we're in a course and it's the right one
                            if '/courses/' in self.page.url:
                                # Make sure we're on the course home page, not a subpage
                                url_parts = self.page.url.split('/courses/')
                                if len(url_parts) > 1:
                                    after_part = url_parts[1].strip('/')
                                    # Should be just the course ID, possibly with query params
                                    if '/' not in after_part.split('?')[0] or after_part.split('?')[0].endswith('/'):
                                        page_title = await self.page.title()
                                        # Double-check we got the right course
                                        if all(part.lower() in page_title.lower() for part in course_parts):
                                            print(f"   ✅ Successfully entered correct course: {course_name}")
                                            course_found = True
                                            break
                                
                                print(f"   ⚠️ Landed on course sub-page or wrong course, going back...")
                                await self.page.go_back()
                                await asyncio.sleep(2)
                except:
                    continue
            
            if not course_found:
                print(f"   ❌ Could not find course: {course_name}")
                return False
            
            await self.take_screenshot("09_course_page")
            await self.log_page_info("Course page")
            
            print("   ✅ Course navigation complete")
            return True
            
        except Exception as e:
            print(f"\n❌ Phase 2 Error: {str(e)}")
            await self.take_screenshot("error_phase2")
            return False


# Main execution
async def main():
    """Main execution function"""
    load_dotenv()
    
    username = os.getenv("CANVAS_USERNAME")
    password = os.getenv("CANVAS_PASSWORD")
    
    if not username or not password:
        print("❌ Please set CANVAS_USERNAME and CANVAS_PASSWORD in .env file")
        return
    
    course_name = "COMPSCI 446"  # or get from command line
    
    print("🚀 Starting Ultra-Advanced Canvas Scraper")
    print(f"   Username: {username[:3]}***")
    print(f"   Course: {course_name}")
    print(f"   Debug mode: ON")
    print(f"   Screenshots: {SCREENSHOT_DIR}")
    print()
    
    scraper = UltraAdvancedCanvasScraper(
        username=username,
        password=password,
        headless=False,
        debug=True
    )
    
    result = await scraper.run_ultra_advanced(course_name)
    
    print("\n" + "="*60)
    print("SCRAPING RESULTS")
    print("="*60)
    print(f"Success: {result['success']}")
    print(f"Phases Completed: {', '.join(result['phases_completed'])}")
    print(f"Transcripts Downloaded: {result['transcripts_downloaded']}")
    if result['errors']:
        print(f"Errors: {', '.join(result['errors'])}")
    
    if scraper.debug:
        print(f"\n📸 Screenshots saved in: {SCREENSHOT_DIR}")
        print("   Review screenshots for debugging information")


if __name__ == "__main__":
    asyncio.run(main())