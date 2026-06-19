"""
JARVIS Auto API Key Generator
==============================
After login, automatically:
  1. Generates a default key name from the user's account (e.g. JARVIS-User-20260504)
  2. Opens Google AI Studio with the key name pre-filled in the URL
  3. Watches clipboard for the key the moment user clicks "Create"
  4. Auto-applies the key to jarvis_config.txt and the user account
  5. Falls back to manual paste if automation is unavailable

Also supports Selenium-based full automation if selenium + chromedriver are installed.
"""
import os
import re
import time
import threading
import webbrowser
import urllib.parse
from typing import Callable, Optional

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Key name generator ────────────────────────────────────────────────────────

def make_default_key_name(display_name: str = "", email: str = "") -> str:
    """
    Generate a clean default key name from the user's account info.
    Example: JARVIS-User-20260504
    """
    # Extract first name from display_name or email prefix
    name = display_name.strip()
    if not name and email:
        name = email.split("@")[0]
    # Keep only alphanumeric + hyphen, capitalize first letter
    name = re.sub(r"[^a-zA-Z0-9]", "", name)[:12]
    name = name.capitalize() if name else "User"
    date = time.strftime("%Y%m%d")
    return f"JARVIS-{name}-{date}"


# ── Clipboard watcher ─────────────────────────────────────────────────────────

def watch_clipboard_for_key(
    timeout: int = 180,
    on_found: Callable[[str], None] = None,
    on_timeout: Callable[[], None] = None,
) -> Optional[str]:
    """
    Block until a Gemini API key (AIza..., 39 chars) appears in clipboard.
    Calls on_found(key) when detected.
    Returns the key or None on timeout.
    """
    try:
        import pyperclip
    except ImportError:
        return None

    deadline = time.time() + timeout
    last = ""
    try:
        last = pyperclip.paste().strip()
    except Exception:
        print("⚠️ Error occurred but was silently ignored")

    while time.time() < deadline:
        try:
            curr = pyperclip.paste().strip()
        except Exception:
            time.sleep(1)
            continue

        if curr != last and _is_valid_gemini_key(curr):
            if on_found:
                on_found(curr)
            return curr
        last = curr
        time.sleep(0.8)

    if on_timeout:
        on_timeout()
    return None


def _is_valid_gemini_key(s: str) -> bool:
    s = s.strip()
    if len(s) < 20:
        return False
    import re
    return bool(re.match(r"^[a-zA-Z0-9_\-\.]+$", s))


# ── Open AI Studio with pre-filled key name ───────────────────────────────────

def open_aistudio_create_key(key_name: str = "JARVIS-Key") -> str:
    """
    Open Google AI Studio API key page.
    Returns the URL opened.
    """
    # AI Studio doesn't support pre-filling via URL params,
    # but we open the page and copy the name to clipboard so user can paste it.
    url = "https://aistudio.google.com/app/apikey"
    try:
        import pyperclip
        pyperclip.copy(key_name)
    except Exception:
        print("⚠️ Error occurred but was silently ignored")
    webbrowser.open(url)
    return url


# ── Selenium automation (optional, best effort) ───────────────────────────────

def try_selenium_create_key(key_name: str, on_status: Callable[[str], None] = None) -> Optional[str]:
    """
    Try to fully automate key creation using Selenium.
    Returns the API key string if successful, None otherwise.
    Requires: pip install selenium  +  chromedriver in PATH
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.keys import Keys
    except ImportError:
        if on_status:
            on_status("Selenium not installed. Using clipboard method.")
        return None

    try:
        if on_status:
            on_status("Starting Chrome for auto key creation...")

        opts = Options()
        opts.add_argument("--start-maximized")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=opts)
        wait   = WebDriverWait(driver, 30)

        # Navigate to AI Studio API key page
        driver.get("https://aistudio.google.com/app/apikey")
        if on_status:
            on_status("Opened AI Studio. Please sign in if prompted...")

        # Wait for page to load (up to 60s for login)
        time.sleep(5)

        # Look for "Create API key" button
        try:
            create_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    "//*[contains(text(),'Create API key') or contains(text(),'Create new key')]"
                ))
            )
            create_btn.click()
            if on_status:
                on_status("Clicked Create API key...")
            time.sleep(2)
        except Exception:
            if on_status:
                on_status("Could not find Create button. Please create key manually.")
            driver.quit()
            return None

        # Try to find key name input and fill it
        try:
            name_input = driver.find_element(By.XPATH,
                "//input[@placeholder or @aria-label]"
            )
            name_input.clear()
            name_input.send_keys(key_name)
            time.sleep(0.5)
        except Exception:
            pass  # Name field may not exist

        # Click confirm/create
        try:
            confirm = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    "//*[contains(text(),'Create') and not(contains(text(),'new'))]"
                ))
            )
            confirm.click()
            if on_status:
                on_status("Key creation confirmed. Extracting key...")
            time.sleep(3)
        except Exception:
            print("⚠️ Error occurred but was silently ignored")

        # Try to find the key value on the page
        key = None
        try:
            # Look for the key text (AIza...)
            elements = driver.find_elements(By.XPATH, "//*[contains(text(),'AIza')]")
            for el in elements:
                txt = el.text.strip()
                if _is_valid_gemini_key(txt):
                    key = txt
                    break
        except Exception:
            print("⚠️ Error occurred but was silently ignored")

        # Try copy button
        if not key:
            try:
                copy_btns = driver.find_elements(By.XPATH,
                    "//*[contains(@aria-label,'copy') or contains(@title,'copy') or contains(text(),'Copy')]"
                )
                for btn in copy_btns:
                    try:
                        btn.click()
                        time.sleep(0.5)
                        import pyperclip
                        clip = pyperclip.paste().strip()
                        if _is_valid_gemini_key(clip):
                            key = clip
                            break
                    except Exception:
                        continue
            except Exception:
                print("⚠️ Error occurred but was silently ignored")

        driver.quit()

        if key:
            if on_status:
                on_status(f"[OK] Key auto-created: {key[:10]}****")
            return key
        else:
            if on_status:
                on_status("Key created but could not extract. Check AI Studio.")
            return None

    except Exception as e:
        if on_status:
            on_status(f"Selenium error: {str(e)[:80]}")
        return None


# ── Main entry point ──────────────────────────────────────────────────────────

def auto_create_and_apply_key(
    display_name: str = "",
    email: str = "",
    on_status: Callable[[str], None] = None,
    on_done: Callable[[str], None] = None,
    timeout: int = 180,
) -> None:
    """
    Full auto key creation flow (runs in a background thread).
    1. Generate default key name from account
    2. Try Selenium automation first
    3. Fall back to clipboard watch
    4. Apply key when found
    5. Call on_done(key) when complete
    """
    def _run():
        key_name = make_default_key_name(display_name, email)

        if on_status:
            on_status(f"Key name: {key_name}")

        # Step 1: Try Selenium
        key = try_selenium_create_key(key_name, on_status=on_status)

        # Step 2: Clipboard fallback
        if not key:
            if on_status:
                on_status(f"Opening AI Studio... Key name '{key_name}' copied to clipboard.")
                on_status("In AI Studio: click 'Create API key', paste the name, click Create, then copy the key.")
            open_aistudio_create_key(key_name)
            key = watch_clipboard_for_key(
                timeout=timeout,
                on_found=lambda k: on_status(f"[OK] Key detected: {k[:10]}****") if on_status else None,
                on_timeout=lambda: on_status("[!] Timeout. Add key manually via Neural Protocols.") if on_status else None,
            )

        # Step 3: Apply
        if key:
            _apply_key(key, email, on_status)
            if on_done:
                on_done(key)
        else:
            if on_status:
                on_status("[!] No key obtained. You can add it manually later.")

    threading.Thread(target=_run, daemon=True).start()


def _apply_key(key: str, email: str, on_status: Callable = None):
    """Write key to config and account."""
    from core.auth import auto_apply_key_to_config
    ok = auto_apply_key_to_config(key, email)
    if ok and on_status:
        on_status(f"[OK] Key applied to JARVIS: {key[:10]}****")
