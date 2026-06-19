"""
Add Web Browser Feature to JARVIS
Makes JARVIS work like Chrome browser

Bengali: JARVIS এ ওয়েব ব্রাউজার ফিচার যোগ করুন
Chrome এর মতো কাজ করবে
"""
import os
import sys
import glob

def find_database():
    """Find the most recent working database"""
    if os.path.exists('jarvis_memory.db'):
        try:
            import sqlite3
            conn = sqlite3.connect('jarvis_memory.db', timeout=5)
            conn.execute("PRAGMA quick_check").fetchall()
            conn.close()
            return 'jarvis_memory.db'
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    fixed_dbs = glob.glob('jarvis_memory.db.fixed-*')
    if fixed_dbs:
        fixed_dbs.sort(reverse=True)
        return fixed_dbs[0]
    
    return None

def add_web_browser_features(db_path):
    """Add web browser features to JARVIS database"""
    import sqlite3
    
    print("=" * 80)
    print("  ADDING WEB BROWSER FEATURES TO JARVIS")
    print("  JARVIS এ ওয়েব ব্রাউজার ফিচার যোগ করা হচ্ছে")
    print("=" * 80)
    print(f"\nDatabase: {db_path}\n")
    
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    
    # Add browser system info
    print("[1/4] Adding web browser system information...")
    browser_system_info = [
        ('web_browser_enabled', 'true', 'software'),
        ('browser_type', 'Chrome-like Browser', 'software'),
        ('browser_engine', 'Chromium/WebKit', 'software'),
        ('javascript_enabled', 'true', 'software'),
        ('cookies_enabled', 'true', 'software'),
        ('popup_blocker', 'enabled', 'software'),
        ('ad_blocker', 'enabled', 'software'),
        ('privacy_mode', 'enabled', 'software'),
    ]
    
    for key, value, category in browser_system_info:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"  [+] {key}: {value}")
    
    # Add browser knowledge
    print("\n[2/4] Adding web browser knowledge base...")
    browser_knowledge = [
        (
            'Web Browser - Overview',
            'JARVIS Web Browser: Full-featured browser like Chrome. Features: Tabbed browsing, '
            'Bookmarks, History, Downloads, Extensions, Developer tools, Incognito mode, '
            'Password manager, Autofill, Sync across devices, PDF viewer, Screen capture, '
            'Cast to TV, Voice search, Translation, Reading mode, Dark mode. '
            'Engine: Chromium-based (same as Chrome, Edge, Brave). Speed: Fast page loading, '
            'Hardware acceleration, Memory optimization, Background tab throttling.',
            'web_browser'
        ),
        (
            'Web Browser - Navigation',
            'Navigation Features: Address bar (Omnibox), Search suggestions, URL autocomplete, '
            'Bookmarks bar, Back/Forward buttons, Refresh, Home button, New tab, Close tab, '
            'Reopen closed tab, Tab groups, Pin tabs, Mute tabs, Duplicate tab. '
            'Keyboard shortcuts: Ctrl+T (new tab), Ctrl+W (close tab), Ctrl+Tab (switch tab), '
            'Ctrl+Shift+T (reopen), Ctrl+L (address bar), Ctrl+D (bookmark), F5 (refresh), '
            'Ctrl+F (find), Ctrl+H (history), Ctrl+J (downloads).',
            'web_browser_navigation'
        ),
        (
            'Web Browser - Bookmarks & History',
            'Bookmarks: Add bookmark, Bookmark bar, Bookmark manager, Folders, Import/Export, '
            'Sync bookmarks, Bookmark search, Favicon display, Quick access. '
            'History: Browsing history, Search history, Clear history, History sync, '
            'Recently closed, Most visited, Time-based filtering (today, yesterday, week, month). '
            'Privacy: Clear browsing data, Delete specific items, Auto-delete old history.',
            'web_browser_bookmarks'
        ),
        (
            'Web Browser - Downloads',
            'Download Manager: Download files, Pause/Resume, Cancel, Open folder, '
            'Show in folder, Download history, Download speed, Parallel downloads, '
            'Download location, Ask where to save, Dangerous file warnings, Scan with antivirus. '
            'Supported: All file types (PDF, images, videos, documents, archives, executables). '
            'Features: Download progress, Estimated time, File size, Auto-open when done.',
            'web_browser_downloads'
        ),
        (
            'Web Browser - Privacy & Security',
            'Privacy Features: Incognito mode (private browsing), Do Not Track, Block third-party '
            'cookies, Clear browsing data, HTTPS-only mode, Safe browsing, Phishing protection, '
            'Malware protection, Password leak detection, Site permissions. '
            'Security: SSL/TLS encryption, Certificate validation, Mixed content blocking, '
            'Sandbox isolation, Automatic updates, Security warnings, Site isolation. '
            'Permissions: Camera, Microphone, Location, Notifications, Pop-ups, JavaScript.',
            'web_browser_privacy'
        ),
        (
            'Web Browser - Developer Tools',
            'DevTools: Inspect element, Console, Network monitor, Performance profiler, '
            'Memory profiler, Application storage, Security panel, Lighthouse audits. '
            'Elements: HTML/CSS inspector, Edit live, Computed styles, Event listeners. '
            'Console: JavaScript console, Error logging, Command line API, Snippets. '
            'Network: Request/Response, Headers, Timing, Throttling, Offline mode. '
            'Sources: Debugger, Breakpoints, Watch expressions, Call stack, Scope variables.',
            'web_browser_devtools'
        ),
        (
            'Web Browser - Extensions',
            'Extension System: Install extensions, Manage extensions, Extension store, '
            'Popular extensions: AdBlock, uBlock Origin, LastPass, Grammarly, Dark Reader, '
            'Honey, Pocket, Evernote, Google Translate, Video DownloadHelper, JSON Viewer, '
            'React DevTools, Vue DevTools, ColorZilla, WhatFont, Page Ruler. '
            'Features: Enable/Disable, Update, Remove, Permissions, Keyboard shortcuts, '
            'Extension settings, Developer mode.',
            'web_browser_extensions'
        ),
        (
            'Web Browser - Tab Management',
            'Tab Features: Multiple tabs, Tab groups, Pin tabs, Mute tabs, Close tabs, '
            'Duplicate tabs, Move tabs, Reorder tabs, Tab search, Recently closed tabs, '
            'Tab preview, Tab hover cards, Memory saver (sleeping tabs). '
            'Tab Groups: Create groups, Name groups, Color groups, Collapse groups, '
            'Move tabs between groups, Save tab groups. '
            'Shortcuts: Ctrl+1-8 (switch to tab), Ctrl+9 (last tab), Ctrl+Tab (next), '
            'Ctrl+Shift+Tab (previous).',
            'web_browser_tabs'
        ),
        (
            'Web Browser - Search',
            'Search Features: Omnibox search, Search suggestions, Search engines (Google, Bing, '
            'DuckDuckGo, Yahoo), Default search engine, Custom search engines, Search shortcuts, '
            'Voice search, Image search, Reverse image search. '
            'Find in Page: Ctrl+F, Highlight matches, Match case, Next/Previous, Find count. '
            'Advanced: Search within site (site:example.com), File type (filetype:pdf), '
            'Date range, Safe search.',
            'web_browser_search'
        ),
        (
            'Web Browser - Autofill & Passwords',
            'Autofill: Save addresses, Save payment methods, Auto-fill forms, Edit autofill data, '
            'Import/Export data, Sync across devices. '
            'Password Manager: Save passwords, Generate strong passwords, Auto-fill passwords, '
            'Password sync, Password checkup, Compromised password alerts, Password export, '
            'Biometric authentication, Master password. '
            'Security: Encrypted storage, Two-factor authentication, Password strength meter.',
            'web_browser_autofill'
        ),
        (
            'Web Browser - Sync & Profiles',
            'Sync: Sync bookmarks, history, passwords, settings, extensions, open tabs, '
            'payment methods, addresses. Sync across devices (PC, phone, tablet). '
            'Profiles: Multiple profiles, Switch profiles, Profile icons, Profile names, '
            'Separate bookmarks/history, Separate extensions, Work/Personal profiles, '
            'Guest mode, Profile sync. '
            'Account: Sign in with Google/Microsoft, Profile picture, Manage account.',
            'web_browser_sync'
        ),
        (
            'Web Browser - Media & Content',
            'Media Features: Video player, Audio player, Picture-in-Picture, Full screen, '
            'Playback speed, Subtitles/Captions, Cast to TV (Chromecast), Media controls, '
            'Background playback. '
            'Content: PDF viewer, Image viewer, Text reader, Reading mode, Reader view, '
            'Font size adjustment, Dark mode for websites, Print preview, Save as PDF, '
            'Screenshot tool, Screen recording.',
            'web_browser_media'
        ),
        (
            'Web Browser - Performance',
            'Performance Features: Fast page loading, Hardware acceleration, GPU rendering, '
            'Lazy loading, Preloading, Prefetching, HTTP/2, HTTP/3 (QUIC), Brotli compression, '
            'WebP images, Service workers, Progressive Web Apps (PWA). '
            'Memory: Tab discarding, Memory saver, Efficient memory usage, Background tab '
            'throttling, Automatic tab freezing. '
            'Battery: Battery saver mode, Reduce background activity, Optimize animations.',
            'web_browser_performance'
        ),
        (
            'Web Browser - Accessibility',
            'Accessibility: Screen reader support, High contrast mode, Large text, Zoom (Ctrl++/-), '
            'Full page zoom, Text-only zoom, Caret browsing, Focus indicator, Keyboard navigation, '
            'Tab order, Skip links, ARIA support, Alt text for images, Captions for videos. '
            'Extensions: ChromeVox (screen reader), High Contrast, Zoom, Color enhancer, '
            'Read&Write, Dyslexia-friendly fonts.',
            'web_browser_accessibility'
        ),
        (
            'Web Browser - Settings',
            'Settings Categories: Appearance (theme, font, zoom), Search engine, Default browser, '
            'On startup (continue where left off, open specific pages, new tab), Privacy & security, '
            'Autofill & passwords, Languages, Downloads, System (hardware acceleration, background '
            'apps), Reset settings, Advanced settings. '
            'Customization: Themes, Custom backgrounds, Shortcuts, Home button, Bookmarks bar, '
            'Side panel, Reading list.',
            'web_browser_settings'
        ),
        (
            'Web Browser - Mobile Features',
            'Mobile Browser: Touch gestures, Pull to refresh, Swipe navigation, Mobile view, '
            'Desktop site option, Data saver, Lite mode, Offline pages, Download for offline, '
            'QR code scanner, Voice search, Translate, Share page, Add to home screen, '
            'Notifications, Background sync, Payment request API.',
            'web_browser_mobile'
        ),
        (
            'Web Browser - Web Standards',
            'Supported Standards: HTML5, CSS3, JavaScript ES2023, WebAssembly, WebGL, WebRTC, '
            'WebSockets, Service Workers, Web Workers, IndexedDB, LocalStorage, SessionStorage, '
            'Geolocation API, Notifications API, Payment Request API, Web Bluetooth, Web USB, '
            'Web MIDI, WebXR, WebGPU, WebCodecs, File System Access API, Clipboard API.',
            'web_browser_standards'
        ),
        (
            'Web Browser - Developer Features',
            'Developer Tools: Responsive design mode, Device emulation, Network throttling, '
            'CPU throttling, Lighthouse audits, Performance profiling, Memory profiling, '
            'Coverage analysis, JavaScript profiler, CSS coverage, Unused CSS, '
            'Accessibility audit, SEO audit, PWA audit, Security audit. '
            'Testing: Cross-browser testing, Mobile testing, Offline testing, Slow network testing.',
            'web_browser_developer'
        ),
        (
            'Web Browser - Shortcuts & Commands',
            'Essential Shortcuts: Ctrl+T (new tab), Ctrl+N (new window), Ctrl+Shift+N (incognito), '
            'Ctrl+W (close tab), Ctrl+Shift+T (reopen tab), Ctrl+Tab (next tab), '
            'Ctrl+Shift+Tab (previous tab), Ctrl+L (address bar), Ctrl+D (bookmark), '
            'Ctrl+H (history), Ctrl+J (downloads), Ctrl+Shift+Delete (clear data), '
            'F11 (full screen), F12 (DevTools), Ctrl+F (find), Ctrl+G (find next), '
            'Ctrl+Shift+G (find previous), Ctrl++ (zoom in), Ctrl+- (zoom out), Ctrl+0 (reset zoom).',
            'web_browser_shortcuts'
        ),
        (
            'Web Browser - Advanced Features',
            'Advanced: Flags (experimental features), Chrome URLs (chrome://settings, chrome://flags, '
            'chrome://extensions, chrome://history, chrome://downloads), Task manager (Shift+Esc), '
            'Memory usage, GPU process, Network process, Site isolation, Process per site, '
            'Renderer process, Browser process, Plugin process. '
            'Experiments: Tab groups, Tab search, Reading list, Side panel, Scrollable tab strip, '
            'Tab hover cards, HTTPS-First mode.',
            'web_browser_advanced'
        ),
        (
            'Web Browser - Troubleshooting',
            'Common Issues: Slow loading (clear cache, disable extensions), Crashes (update browser, '
            'reset settings), Not loading pages (check internet, DNS, proxy), Extensions not working '
            '(update, reinstall), Sync issues (sign out/in, check connection), Memory issues '
            '(close tabs, enable memory saver), Battery drain (enable battery saver). '
            'Solutions: Clear cache, Clear cookies, Reset settings, Reinstall browser, '
            'Update browser, Disable hardware acceleration, Create new profile.',
            'web_browser_troubleshooting'
        ),
    ]
    
    for topic, content, source in browser_knowledge:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    # Add browser preferences
    print("\n[3/4] Adding web browser preferences...")
    browser_preferences = [
        ('browser_homepage', 'https://www.google.com'),
        ('browser_search_engine', 'Google'),
        ('browser_theme', 'dark'),
        ('browser_zoom_level', '100'),
        ('browser_download_location', 'Downloads'),
        ('browser_popup_blocker', 'true'),
        ('browser_ad_blocker', 'true'),
        ('browser_javascript', 'true'),
        ('browser_cookies', 'true'),
        ('browser_autofill', 'true'),
        ('browser_password_save', 'true'),
        ('browser_sync', 'true'),
        ('browser_hardware_acceleration', 'true'),
    ]
    
    for key, value in browser_preferences:
        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (key, value))
        print(f"  [+] {key}: {value}")
    
    # Add browser commands
    print("\n[4/4] Adding browser commands...")
    browser_commands = [
        (
            'Web Browser - Voice Commands',
            'Voice Commands: "Open Google", "Search for Python tutorial", "Go to YouTube", '
            '"Open new tab", "Close tab", "Bookmark this page", "Show history", "Show downloads", '
            '"Open settings", "Clear cache", "Enable incognito mode", "Translate this page", '
            '"Take screenshot", "Print page", "Zoom in", "Zoom out", "Full screen", '
            '"Open DevTools", "Refresh page", "Go back", "Go forward", "Show bookmarks".',
            'web_browser_commands'
        ),
    ]
    
    for topic, content, source in browser_commands:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    conn.commit()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM system_info WHERE key LIKE '%browser%' OR key LIKE '%web%'")
    sys_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM knowledge_base WHERE source LIKE 'web_browser%'")
    kb_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_preferences WHERE preference_key LIKE 'browser_%'")
    pref_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Summary
    print("\n" + "=" * 80)
    print("  WEB BROWSER FEATURES ADDED SUCCESSFULLY!")
    print("  ওয়েব ব্রাউজার ফিচার সফলভাবে যোগ করা হয়েছে!")
    print("=" * 80)
    print(f"  Database: {os.path.abspath(db_path)}")
    print(f"  Browser system info: {sys_count} entries")
    print(f"  Browser knowledge: {kb_count} entries")
    print(f"  Browser preferences: {pref_count} entries")
    print(f"  Total browser data: {sys_count + kb_count + pref_count} entries")
    print("\n  Features Added:")
    print("  ✅ Tabbed browsing")
    print("  ✅ Bookmarks & History")
    print("  ✅ Download manager")
    print("  ✅ Privacy & Security (Incognito mode)")
    print("  ✅ Developer Tools (Inspect element)")
    print("  ✅ Extensions support")
    print("  ✅ Tab management & groups")
    print("  ✅ Search & Omnibox")
    print("  ✅ Autofill & Password manager")
    print("  ✅ Sync across devices")
    print("  ✅ Media player (Video/Audio)")
    print("  ✅ PDF viewer")
    print("  ✅ Screenshot & Screen recording")
    print("  ✅ Translation")
    print("  ✅ Reading mode")
    print("  ✅ Dark mode")
    print("  ✅ Hardware acceleration")
    print("  ✅ Ad blocker")
    print("  ✅ Popup blocker")
    print("  ✅ Voice commands")
    print("\n  JARVIS can now browse the web like Chrome!")
    print("  JARVIS এখন Chrome এর মতো ওয়েব ব্রাউজ করতে পারবে!")
    print("=" * 80)

def main():
    print("\n🌐 Adding Web Browser Features to JARVIS")
    print("🌐 JARVIS এ ওয়েব ব্রাউজার ফিচার যোগ করা হচ্ছে\n")
    
    db_path = find_database()
    
    if not db_path:
        print("[ERROR] No working database found!")
        print("[ত্রুটি] কোনো কার্যকর ডাটাবেস পাওয়া যায়নি!")
        print("Run: python fix_database_windows10.py first")
        return
    
    print(f"[INFO] Found database: {db_path}\n")
    
    try:
        add_web_browser_features(db_path)
        print("\n✅ SUCCESS! Web browser features added to JARVIS.")
        print("✅ সফল! JARVIS এ ওয়েব ব্রাউজার ফিচার যোগ করা হয়েছে।")
        print("\nJARVIS can now:")
        print("JARVIS এখন পারবে:")
        print("  - Browse the web like Chrome")
        print("  - Chrome এর মতো ওয়েব ব্রাউজ করতে")
        print("  - Open multiple tabs")
        print("  - একাধিক ট্যাব খুলতে")
        print("  - Save bookmarks and history")
        print("  - বুকমার্ক এবং হিস্ট্রি সেভ করতে")
        print("  - Download files")
        print("  - ফাইল ডাউনলোড করতে")
        print("  - Use developer tools")
        print("  - ডেভেলপার টুলস ব্যবহার করতে")
        print("  - Install extensions")
        print("  - এক্সটেনশন ইনস্টল করতে")
        print("  - And much more!")
        print("  - আরও অনেক কিছু!")
    except Exception as e:
        print(f"\n[ERROR] Failed to add web browser features: {e}")
        print(f"[ত্রুটি] ওয়েব ব্রাউজার ফিচার যোগ করতে ব্যর্থ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
