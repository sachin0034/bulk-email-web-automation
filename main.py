import streamlit as st
import pandas as pd
import openai
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import os
from datetime import datetime
import traceback

# Page configuration
st.set_page_config(
    page_title="Maven Email Automation",
    page_icon="📧",
    layout="wide"
)

# Custom CSS for better styling - Updated to match dark theme with orange accents
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #e86b0f;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(232, 107, 15, 0.3);
    }
    .upload-section {
        background-color: #605e5e;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #e86b0f;
        box-shadow: 0 4px 8px rgba(232, 107, 15, 0.2);
    }
    .results-section {
        background-color: #605e5e;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #e86b0f;
        box-shadow: 0 4px 8px rgba(232, 107, 15, 0.2);
    }
    .email-item {
        background-color: #000000;
        color: #f7f7f7;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #e86b0f;
        box-shadow: 0 2px 4px rgba(232, 107, 15, 0.3);
        transition: all 0.3s ease;
    }
    .email-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(232, 107, 15, 0.5);
    }
    .automation-section {
        background-color: #605e5e;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #e86b0f;
        box-shadow: 0 4px 8px rgba(232, 107, 15, 0.2);
    }
    .progress-bar {
        background-color: #000000;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 2px solid #e86b0f;
    }
    .debug-log {
        background-color: #000000;
        color: #f7f7f7;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e86b0f;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        max-height: 400px;
        overflow-y: auto;
        box-shadow: inset 0 0 10px rgba(232, 107, 15, 0.1);
    }
    .stButton > button {
        background-color: #e86b0f !important;
        color: #000000 !important;
        border: 2px solid #e86b0f !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #000000 !important;
        color: #e86b0f !important;
        border-color: #e86b0f !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(232, 107, 15, 0.4) !important;
    }
    .stTextInput > div > div > input {
        background-color: #000000 !important;
        color: #f7f7f7 !important;
        border: 2px solid #605e5e !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #e86b0f !important;
        box-shadow: 0 0 8px rgba(232, 107, 15, 0.3) !important;
    }
    .stSelectbox > div > div > div {
        background-color: #000000 !important;
        color: #f7f7f7 !important;
        border: 2px solid #605e5e !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > div > div:focus {
        border-color: #e86b0f !important;
        box-shadow: 0 0 8px rgba(232, 107, 15, 0.3) !important;
    }
    .stFileUploader > div > div > div {
        background-color: #000000 !important;
        color: #f7f7f7 !important;
        border: 2px solid #605e5e !important;
        border-radius: 8px !important;
    }
    .stFileUploader > div > div > div:hover {
        border-color: #e86b0f !important;
    }
    .stProgress > div > div > div > div {
        background-color: #e86b0f !important;
    }
    .stProgress > div > div > div > div > div {
        background-color: #e86b0f !important;
    }
    .stSuccess {
        background-color: #605e5e !important;
        color: #e86b0f !important;
        border: 2px solid #e86b0f !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    .stError {
        background-color: #605e5e !important;
        color: #ff6b6b !important;
        border: 2px solid #ff6b6b !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    .stWarning {
        background-color: #605e5e !important;
        color: #ffd93d !important;
        border: 2px solid #ffd93d !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    .stInfo {
        background-color: #605e5e !important;
        color: #4ecdc4 !important;
        border: 2px solid #4ecdc4 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

def debug_log(message, log_container=None):
    """Enhanced debug logging function"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    debug_message = f"[{timestamp}] {message}"
    
    # Print to console
    print(debug_message)
    
    # Also display in Streamlit if container provided
    if log_container:
        if 'debug_messages' not in st.session_state:
            st.session_state.debug_messages = []
        st.session_state.debug_messages.append(debug_message)
        
        # Keep only last 50 messages to prevent memory issues
        if len(st.session_state.debug_messages) > 50:
            st.session_state.debug_messages = st.session_state.debug_messages[-50:]
        
        log_container.markdown(
            f'<div class="debug-log">{"<br>".join(st.session_state.debug_messages)}</div>',
            unsafe_allow_html=True
        )

def extract_emails_from_text(text):
    """Extract emails from text using regex pattern"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return list(set(emails))  # Remove duplicates

def extract_emails_with_openai(text, api_key):
    """Extract emails using OpenAI API for better accuracy"""
    try:
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an email extraction expert. Extract all valid email addresses from the given text. Return only the emails, one per line, without any additional text or formatting."
                },
                {
                    "role": "user",
                    "content": f"Extract all email addresses from this text:\n\n{text}"
                }
            ],
            max_tokens=500,
            temperature=0
        )
        
        # Extract emails from the response
        extracted_text = response.choices[0].message.content.strip()
        emails = [email.strip() for email in extracted_text.split('\n') if '@' in email]
        
        # Also use regex as backup
        regex_emails = extract_emails_from_text(text)
        
        # Combine and remove duplicates
        all_emails = list(set(emails + regex_emails))
        return all_emails
        
    except Exception as e:
        st.error(f"Error using OpenAI API: {str(e)}")
        # Fallback to regex extraction
        return extract_emails_from_text(text)

def process_csv_file(uploaded_file, api_key):
    """Process uploaded CSV file and extract emails"""
    try:
        # Read CSV file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            # Try to read as CSV anyway
            df = pd.read_csv(uploaded_file)
        
        # Convert DataFrame to string for processing
        csv_text = df.to_string(index=False)
        
        # Extract emails using OpenAI API
        emails = extract_emails_with_openai(csv_text, api_key)
        
        return emails, df
        
    except Exception as e:
        st.error(f"Error processing CSV file: {str(e)}")
        return [], None

def test_chrome_setup():
    """Test Chrome driver setup with detailed debugging"""
    debug_messages = []
    
    def log_debug(msg):
        debug_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        print(msg)
    
    try:
        log_debug("🔍 Starting Chrome driver test...")
        
        # Detect environment
        import platform
        is_windows = platform.system().lower() == "windows"
        is_render = os.environ.get('RENDER', False)
        
        log_debug(f"🔍 Environment detected: {'Windows' if is_windows else 'Linux/Render'}")
        
        # Configure Chrome options based on environment
        chrome_options = Options()
        
        if is_windows:
            # Windows-specific options
            log_debug("🪟 Using Windows Chrome configuration")
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            # Windows user data directory
            import tempfile
            temp_dir = tempfile.gettempdir()
            chrome_options.add_argument(f'--user-data-dir={temp_dir}/chrome-user-data')
            chrome_options.add_argument(f'--disk-cache-dir={temp_dir}/chrome-cache')
            
        else:
            # Linux/Render options
            log_debug("🐧 Using Linux/Render Chrome configuration")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            if is_render:
                chrome_options.binary_location = "/usr/bin/google-chrome"
        
        log_debug("✓ Chrome options configured")
        
        # Try webdriver-manager first (works on both platforms)
        try:
            log_debug("📦 Trying webdriver-manager...")
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            log_debug("✓ webdriver-manager imported successfully")
            
            service = Service(ChromeDriverManager().install())
            log_debug("✓ ChromeDriver service created")
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_debug("✅ Chrome driver initialized successfully with webdriver-manager!")
            
            # Test navigation
            driver.get("https://www.google.com")
            log_debug("✅ Test navigation successful")
            
            driver.quit()
            log_debug("✅ Chrome driver test completed successfully!")
            return True, debug_messages
            
        except Exception as e:
            log_debug(f"❌ webdriver-manager failed: {str(e)}")
            log_debug(f"Full error: {traceback.format_exc()}")
            
            # Try system ChromeDriver on Linux/Render
            if not is_windows:
                log_debug("🔄 Trying system ChromeDriver on Linux...")
                try:
                    from selenium.webdriver.chrome.service import Service
                    
                    chrome_driver_path = "/usr/local/bin/chromedriver"
                    log_debug(f"🔧 Using system ChromeDriver: {chrome_driver_path}")
                    
                    service = Service(chrome_driver_path)
                    log_debug("✓ ChromeDriver service created")
                    
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    log_debug("✅ Chrome driver initialized successfully with system ChromeDriver!")
                    
                    # Test navigation
                    driver.get("https://www.google.com")
                    log_debug("✅ Test navigation successful")
                    
                    driver.quit()
                    log_debug("✅ Chrome driver test completed successfully!")
                    return True, debug_messages
                    
                except Exception as e2:
                    log_debug(f"❌ System ChromeDriver also failed: {str(e2)}")
                    log_debug(f"Full error: {traceback.format_exc()}")
            
            # Final fallback - direct initialization
            log_debug("🔄 Trying direct Chrome driver...")
            try:
                driver = webdriver.Chrome(options=chrome_options)
                log_debug("✅ Chrome driver initialized with direct method!")
                
                # Test navigation
                driver.get("https://www.google.com")
                log_debug("✅ Test navigation successful")
                
                driver.quit()
                log_debug("✅ Chrome driver test completed successfully!")
                return True, debug_messages
                
            except Exception as e3:
                log_debug(f"❌ Direct Chrome driver also failed: {str(e3)}")
                log_debug(f"Full error: {traceback.format_exc()}")
                return False, debug_messages
                
    except Exception as e:
        log_debug(f"❌ Critical error in Chrome setup test: {str(e)}")
        log_debug(f"Full error: {traceback.format_exc()}")
        return False, debug_messages

def automate_maven_signup(emails, maven_url, delay_between_emails=2, log_container=None):
    """Automate Maven signup process with enhanced debugging"""
    
    debug_log(f"🚀 STARTING MAVEN AUTOMATION", log_container)
    debug_log(f"📧 Number of emails to process: {len(emails)}", log_container)
    debug_log(f"⏱️ Delay between emails: {delay_between_emails} seconds", log_container)
    debug_log(f"📋 Email list: {emails[:3]}{'...' if len(emails) > 3 else ''}", log_container)
    
    if not emails:
        debug_log("❌ ERROR: No emails provided to process!", log_container)
        return []
    
    # Detect environment (Windows vs Linux/Render)
    import platform
    is_windows = platform.system().lower() == "windows"
    is_render = os.environ.get('RENDER', False)
    
    debug_log(f"🔍 Environment detected: {'Windows' if is_windows else 'Linux/Render'}", log_container)
    
    # Configure Chrome options based on environment
    chrome_options = Options()
    
    if is_windows:
        # Windows-specific options
        debug_log("🪟 Using Windows Chrome configuration", log_container)
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # Windows user data directory
        import tempfile
        temp_dir = tempfile.gettempdir()
        chrome_options.add_argument(f'--user-data-dir={temp_dir}/chrome-user-data')
        chrome_options.add_argument(f'--data-path={temp_dir}/chrome-data-path')
        chrome_options.add_argument(f'--disk-cache-dir={temp_dir}/chrome-cache')
        chrome_options.add_argument(f'--media-cache-dir={temp_dir}/chrome-media-cache')
        
    else:
        # Linux/Render options
        debug_log("🐧 Using Linux/Render Chrome configuration", log_container)
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')  # Required for root user
        chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        chrome_options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
        chrome_options.add_argument('--disable-extensions')  # Disable extensions
        chrome_options.add_argument('--disable-web-security')  # Disable web security
        chrome_options.add_argument('--allow-running-insecure-content')  # Allow insecure content
        
        # Additional options for stability
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        
        # Set Chrome binary location for Render
        if is_render:
            chrome_options.binary_location = "/usr/bin/google-chrome"
        
        # Set user data directory to avoid conflicts
        chrome_options.add_argument('--user-data-dir=/tmp/chrome-user-data')
        chrome_options.add_argument('--data-path=/tmp/chrome-data-path')
        chrome_options.add_argument('--homedir=/tmp')
        chrome_options.add_argument('--disk-cache-dir=/tmp/chrome-cache')
        chrome_options.add_argument('--media-cache-dir=/tmp/chrome-media-cache')
        chrome_options.add_argument('--disk-cache-size=1')
        chrome_options.add_argument('--media-cache-size=1')
        chrome_options.add_argument('--aggressive-cache-discard')
        chrome_options.add_argument('--memory-pressure-off')
        chrome_options.add_argument('--max_old_space_size=4096')
    
    chrome_options.add_argument('--verbose')  # More verbose logging
    
    debug_log("✓ Chrome options configured", log_container)
    
    driver = None
    results = []
    
    try:
        debug_log("🔧 Attempting to initialize Chrome driver...", log_container)
        
        # Try webdriver-manager first (works on both Windows and Linux)
        try:
            debug_log("📦 Trying webdriver-manager...", log_container)
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            chrome_driver_path = ChromeDriverManager().install()
            debug_log(f"✓ ChromeDriver downloaded to: {chrome_driver_path}", log_container)
            
            service = Service(chrome_driver_path)
            debug_log("✓ ChromeDriver service created", log_container)
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            debug_log("✅ Chrome driver initialized successfully with webdriver-manager!", log_container)
            
        except Exception as e:
            debug_log(f"❌ webdriver-manager failed: {str(e)}", log_container)
            debug_log(f"📋 Full error trace: {traceback.format_exc()}", log_container)
            
            # Try system ChromeDriver on Linux/Render
            if not is_windows:
                debug_log("🔄 Trying system ChromeDriver on Linux...", log_container)
                try:
                    from selenium.webdriver.chrome.service import Service
                    
                    # Use system ChromeDriver installed during build
                    chrome_driver_path = "/usr/local/bin/chromedriver"
                    debug_log(f"🔧 Using system ChromeDriver: {chrome_driver_path}", log_container)
                    
                    service = Service(chrome_driver_path)
                    debug_log("✓ ChromeDriver service created", log_container)
                    
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    debug_log("✅ Chrome driver initialized successfully with system ChromeDriver!", log_container)
                    
                except Exception as e2:
                    debug_log(f"❌ System ChromeDriver also failed: {str(e2)}", log_container)
                    debug_log(f"📋 Full error trace: {traceback.format_exc()}", log_container)
            
            # Final fallback - direct initialization
            if 'driver' not in locals():
                debug_log("🔄 Trying direct Chrome driver initialization...", log_container)
                try:
                    driver = webdriver.Chrome(options=chrome_options)
                    debug_log("✅ Chrome driver initialized successfully with direct method!", log_container)
                except Exception as e3:
                    debug_log(f"❌ All Chrome initialization methods failed!", log_container)
                    debug_log(f"📋 Final error: {str(e3)}", log_container)
                    raise Exception(f"All Chrome initialization methods failed. Last error: {str(e3)}")
        
        # Test that driver is working
        debug_log("🧪 Testing driver with simple navigation...", log_container)
        driver.get("https://www.google.com")
        debug_log(f"✓ Test navigation successful. Current URL: {driver.current_url}", log_container)
        
        # Navigate to Maven website
        maven_url = 'https://maven.com/p/1f7efa/context-engineering-agentic-rag-for-product-managers?utm_medium=ll_share_link&utm_source=instructor'
        debug_log(f"🌐 Navigating to Maven website: {maven_url}", log_container)
        driver.get(maven_url)
        
        # Wait for the page to load
        debug_log("⏳ Waiting for page to load...", log_container)
        time.sleep(5)
        
        current_url = driver.current_url
        page_title = driver.title
        debug_log(f"✓ Page loaded successfully!", log_container)
        debug_log(f"📄 Current URL: {current_url}", log_container)
        debug_log(f"📝 Page title: {page_title}", log_container)
        
        # Check if page loaded correctly
        if "maven.com" not in current_url.lower():
            debug_log("⚠️ WARNING: Might not be on the correct Maven page", log_container)
        
        # Process each email
        for i, email in enumerate(emails):
            debug_log(f"📧 Processing email {i+1}/{len(emails)}: {email}", log_container)
            
            try:
                # Look for email input field with multiple selectors
                debug_log("🔍 Looking for email input field...", log_container)
                wait = WebDriverWait(driver, 15)
                
                email_input = None
                selectors_to_try = [
                    'input[placeholder="Your email"][type="text"]',
                    'input[type="email"]',
                    'input[placeholder*="email" i]',
                    'input[name*="email" i]',
                    'input[id*="email" i]'
                ]
                
                for selector in selectors_to_try:
                    try:
                        debug_log(f"🔍 Trying selector: {selector}", log_container)
                        email_input = wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        debug_log(f"✅ Found email input with selector: {selector}", log_container)
                        break
                    except TimeoutException:
                        debug_log(f"❌ Selector failed: {selector}", log_container)
                        continue
                
                if not email_input:
                    debug_log("❌ ERROR: Could not find email input field with any selector!", log_container)
                    
                    # Debug: Print page source snippet
                    page_source_snippet = driver.page_source[:1000]
                    debug_log(f"📄 Page source snippet: {page_source_snippet}...", log_container)
                    
                    results.append({
                        'email': email,
                        'status': 'error',
                        'timestamp': datetime.now().isoformat(),
                        'message': 'Email input field not found'
                    })
                    continue
                
                # Clear and fill the input
                debug_log(f"✏️ Clearing and entering email: {email}", log_container)
                email_input.clear()
                time.sleep(0.5)  # Small delay after clear
                email_input.send_keys(email)
                
                # Verify email was entered
                entered_value = email_input.get_attribute('value')
                debug_log(f"✓ Email entered. Field value: {entered_value}", log_container)
                
                if entered_value != email:
                    debug_log(f"⚠️ WARNING: Entered value '{entered_value}' doesn't match expected '{email}'", log_container)
                
                # Wait for input to register
                time.sleep(1)
                
                # Look for submit button with multiple approaches
                debug_log("🔍 Looking for submit button...", log_container)
                
                submit_button = None
                button_selectors = [
                    "//button[contains(text(), 'Sign up for free')]",
                    "//button[contains(text(), 'Sign up')]",
                    "//input[@type='submit']",
                    "//button[@type='submit']",
                    "//button[contains(@class, 'submit')]",
                    "//a[contains(text(), 'Sign up')]"
                ]
                
                for selector in button_selectors:
                    try:
                        debug_log(f"🔍 Trying button selector: {selector}", log_container)
                        submit_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        debug_log(f"✅ Found submit button with selector: {selector}", log_container)
                        break
                    except TimeoutException:
                        debug_log(f"❌ Button selector failed: {selector}", log_container)
                        continue
                
                if submit_button:
                    debug_log("🖱️ Clicking submit button...", log_container)
                    submit_button.click()
                    debug_log(f"✅ Form submitted successfully for: {email}", log_container)
                    
                    # Record success
                    results.append({
                        'email': email,
                        'status': 'success',
                        'timestamp': datetime.now().isoformat(),
                        'message': 'Form submitted successfully'
                    })
                    
                    # Brief wait to see any page response
                    time.sleep(2)
                    
                    # After successful submission - refresh page to reset form state
                    debug_log("🔄 Refreshing page to reset form state...", log_container)
                    driver.refresh()
                    debug_log("⏳ Waiting for page to fully reload...", log_container)
                    time.sleep(3)  # Wait for page to fully reload
                    
                    # Wait for form to be ready again
                    debug_log("🔍 Waiting for form to be ready after refresh...", log_container)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
                    debug_log("✅ Form is ready for next email", log_container)
                    
                else:
                    debug_log(f"❌ ERROR: Submit button not found for: {email}", log_container)
                    results.append({
                        'email': email,
                        'status': 'error',
                        'timestamp': datetime.now().isoformat(),
                        'message': 'Submit button not found'
                    })
                
                # Wait between submissions
                if i < len(emails) - 1:
                    debug_log(f"⏳ Waiting {delay_between_emails} seconds before next email...", log_container)
                    time.sleep(delay_between_emails)
                
            except Exception as e:
                error_msg = f"Error processing {email}: {str(e)}"
                debug_log(f"❌ {error_msg}", log_container)
                debug_log(f"📋 Full error trace: {traceback.format_exc()}", log_container)
                
                results.append({
                    'email': email,
                    'status': 'error',
                    'timestamp': datetime.now().isoformat(),
                    'message': str(e)
                })
        
        debug_log("🎉 All emails processed successfully!", log_container)
        debug_log(f"📊 Final results: {len(results)} total, {len([r for r in results if r['status'] == 'success'])} successful, {len([r for r in results if r['status'] == 'error'])} errors", log_container)
        
        return results
        
    except Exception as e:
        error_msg = f"Critical error occurred: {str(e)}"
        debug_log(f"💥 {error_msg}", log_container)
        debug_log(f"📋 Full error trace: {traceback.format_exc()}", log_container)
        
        # Add error to results if we have emails but hit a critical error
        if emails and not results:
            results = [{
                'email': email,
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'message': f"Critical automation error: {str(e)}"
            } for email in emails]
        
        return results
        
    finally:
        if driver:
            debug_log("🔄 Closing browser...", log_container)
            try:
                driver.quit()
                debug_log("✓ Browser closed successfully.", log_container)
            except Exception as e:
                debug_log(f"⚠️ Error closing browser: {str(e)}", log_container)

def main():
    # Header
    st.markdown('<h1 class="main-header">📧 Maven Email Automation</h1>', unsafe_allow_html=True)
    st.markdown("Upload a CSV file with names and emails, then automate Maven signup process for all emails.")
    
    # Sidebar for API key input
    with st.sidebar:
        st.header("🔑 OpenAI API Configuration")
        api_key = st.text_input(
            "Enter your OpenAI API Key",
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
        
        if api_key:
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your OpenAI API key")
        
        st.markdown("---")
        
        # Chrome driver test section
        st.header("🧪 Chrome Driver Test")
        if st.button("Test Chrome Setup"):
            with st.spinner("Testing Chrome driver..."):
                success, debug_messages = test_chrome_setup()
                
            if success:
                st.success("✅ Chrome driver is working!")
            else:
                st.error("❌ Chrome driver test failed!")
            
            # Show debug messages
            st.text_area("Debug Log", "\n".join(debug_messages), height=300)
        
        st.markdown("---")
        st.markdown("### How to use:")
        st.markdown("1. Test Chrome driver setup first")
        st.markdown("2. Enter your OpenAI API key")
        st.markdown("3. Upload a CSV file with names and emails")
        st.markdown("4. Extract emails from the CSV")
        st.markdown("5. Configure automation settings")
        st.markdown("6. Start Maven automation")
        
        st.markdown("---")
        st.markdown("### Features:")
        st.markdown("- AI-powered email extraction")
        st.markdown("- Selenium automation for Maven")
        st.markdown("- Enhanced debugging and logging")
        st.markdown("- Progress tracking")
        st.markdown("- Error handling and logging")
        st.markdown("- CSV preview and download")
    
    # Main content area
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to continue.")
        return
    
    # File upload section
    with st.container():
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.header("📁 Upload CSV File")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file containing names and email addresses"
        )
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Show file info
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.2f} KB",
                "File type": uploaded_file.type
            }
            st.json(file_details)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Process file and extract emails
    emails = []
    df = None
    
    if uploaded_file is not None and st.button("🚀 Extract Emails", type="primary"):
        with st.spinner("Processing file and extracting emails..."):
            emails, df = process_csv_file(uploaded_file, api_key)
        
        if emails:
            st.success(f"✅ Successfully extracted {len(emails)} unique emails!")
            
            # Results section
            with st.container():
                st.markdown('<div class="results-section">', unsafe_allow_html=True)
                st.header(f"📧 Extracted Emails ({len(emails)} found)")
                
                # Show first 10 emails as preview
                if len(emails) <= 10:
                    for i, email in enumerate(emails, 1):
                        st.markdown(f'<div class="email-item">{i}. {email}</div>', unsafe_allow_html=True)
                else:
                    for i, email in enumerate(emails[:10], 1):
                        st.markdown(f'<div class="email-item">{i}. {email}</div>', unsafe_allow_html=True)
                    st.info(f"... and {len(emails) - 10} more emails")
                
                # Download button for emails
                emails_text = '\n'.join(emails)
                st.download_button(
                    label="📥 Download Emails as TXT",
                    data=emails_text,
                    file_name="extracted_emails.txt",
                    mime="text/plain"
                )
                
                # Download as CSV
                emails_df = pd.DataFrame(emails, columns=['Email'])
                csv_data = emails_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Emails as CSV",
                    data=csv_data,
                    file_name="extracted_emails.csv",
                    mime="text/csv"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Show CSV preview
            if df is not None:
                st.header("📊 CSV Preview")
                st.dataframe(df.head(10))
                
                # Show statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    st.metric("Total Columns", len(df.columns))
                with col3:
                    st.metric("Emails Found", len(emails))
        else:
            st.warning("No emails found in the uploaded file.")
    
    # Store emails in session state to persist across reruns
    if emails:
        st.session_state.emails = emails
    
    # Get emails from session state if available
    if 'emails' in st.session_state and st.session_state.emails:
        emails = st.session_state.emails
    
    # Automation section
    if emails:
        with st.container():
            st.markdown('<div class="automation-section">', unsafe_allow_html=True)
            st.header("🤖 Maven Automation")
            st.markdown("Configure settings for automatic Maven signup with extracted emails.")
            
            # Automation settings
            col1, col2 = st.columns(2)
            with col1:
                delay_between_emails = st.slider(
                    "Delay between emails (seconds)",
                    min_value=1,
                    max_value=10,
                    value=2,
                    help="Time to wait between form submissions"
                )
            
            with col2:
                st.info(f"Total Emails: {len(emails)}")
            
            # Maven URL input
            st.markdown("### 🌐 Maven URL Configuration")
            maven_url = st.text_input(
                "Enter Maven URL to automate",
                value="https://maven.com/p/1f7efa/context-engineering-agentic-rag-for-product-managers?utm_medium=ll_share_link&utm_source=instructor",
                help="Enter the full Maven URL where you want to automate the signup process",
                placeholder="https://maven.com/p/..."
            )
            
            if maven_url:
                st.success(f"✅ Target URL: {maven_url}")
            else:
                st.warning("⚠️ Please enter a Maven URL to continue")
            
            # Initialize session state for automation
            if 'automation_running' not in st.session_state:
                st.session_state.automation_running = False
            
            # Debug log container
            debug_container = st.empty()
            
            # Start automation button
            col1, col2 = st.columns([1, 1])
            with col1:
                start_automation = st.button(
                    "🚀 Start Maven Automation", 
                    type="primary", 
                    disabled=st.session_state.automation_running or not maven_url,
                    help="Click to start the automated Maven signup process (requires valid URL)"
                )
            
            with col2:
                if st.session_state.automation_running:
                    if st.button("🛑 Stop Automation", type="secondary"):
                        st.session_state.automation_running = False
                        st.warning("Automation stopped by user")
            
            # Show current status
            if st.session_state.automation_running:
                st.info("🔄 Automation is currently running... Please wait and watch the debug log below.")
            
            if start_automation:
                # Validate URL before starting
                if not maven_url or not maven_url.strip():
                    st.error("❌ Please enter a valid Maven URL to start automation")
                    return
                
                if not maven_url.startswith("https://maven.com"):
                    st.warning("⚠️ Warning: URL doesn't start with 'https://maven.com'. Are you sure this is a Maven URL?")
                    if not st.button("Continue anyway", key="continue_anyway"):
                        return
                
                st.session_state.automation_running = True
                
                # Clear previous debug messages
                if 'debug_messages' in st.session_state:
                    st.session_state.debug_messages = []
                
                st.info("🚀 Starting Maven automation... Watch the debug log below for detailed progress.")
                
                try:
                    # Run automation with debug logging
                    results = automate_maven_signup(emails, maven_url, delay_between_emails, debug_container)
                    
                    if results:
                        st.success("✅ Maven automation completed!")
                        
                        # Save results to session state
                        st.session_state.automation_results = results
                        
                        # Save results to file
                        results_json = json.dumps(results, indent=2)
                        
                        # Show results summary
                        success_count = len([r for r in results if r['status'] == 'success'])
                        error_count = len([r for r in results if r['status'] == 'error'])
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Processed", len(results))
                        with col2:
                            st.metric("Successful", success_count, delta=f"{success_count}/{len(results)}")
                        with col3:
                            st.metric("Errors", error_count, delta=f"{error_count}/{len(results)}")
                        
                        # Download results
                        st.download_button(
                            label="📥 Download Results JSON",
                            data=results_json,
                            file_name=f"maven_automation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                        
                        # Show results details
                        if st.checkbox("Show detailed results"):
                            st.json(results)
                        
                        # Show error details if any
                        if error_count > 0:
                            st.warning(f"⚠️ {error_count} emails had errors during processing")
                            with st.expander("View Error Details"):
                                error_emails = [r for r in results if r['status'] == 'error']
                                for error in error_emails:
                                    st.text(f"❌ {error['email']}: {error['message']}")
                    else:
                        st.error("❌ Maven automation failed! Check the debug log for details.")
                        
                except Exception as e:
                    st.error(f"❌ Critical automation error: {str(e)}")
                    st.text_area("Error Details", traceback.format_exc(), height=200)
                    
                finally:
                    st.session_state.automation_running = False
            
            # Show debug log if we have messages
            if 'debug_messages' in st.session_state and st.session_state.debug_messages:
                with st.expander("🔍 Debug Log", expanded=st.session_state.automation_running):
                    st.markdown(
                        f'<div class="debug-log">{"<br>".join(st.session_state.debug_messages)}</div>',
                        unsafe_allow_html=True
                    )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit, OpenAI API, and Selenium | "
        "[GitHub](https://github.com) | "
        "[Documentation](https://docs.streamlit.io)"
    )

if __name__ == "__main__":
    main()