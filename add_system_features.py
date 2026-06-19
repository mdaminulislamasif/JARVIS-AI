"""
Add System Features to JARVIS
Blender-style 3D, Download Manager, System Management, Hardware Monitoring, etc.

Bengali: JARVIS এ সিস্টেম ফিচার যোগ করুন
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

def add_system_features(db_path):
    """Add system features to JARVIS database"""
    import sqlite3
    
    print("=" * 80)
    print("  ADDING SYSTEM FEATURES TO JARVIS")
    print("  JARVIS এ সিস্টেম ফিচার যোগ করা হচ্ছে")
    print("=" * 80)
    print(f"\nDatabase: {db_path}\n")
    
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    
    # Add system info
    print("[1/5] Adding system information...")
    system_info = [
        ('blender_3d_enabled', 'true', 'software'),
        ('download_manager_enabled', 'true', 'software'),
        ('system_services_enabled', 'true', 'software'),
        ('hardware_monitoring_enabled', 'true', 'software'),
        ('keyboard_automation_enabled', 'true', 'software'),
        ('mouse_automation_enabled', 'true', 'software'),
        ('desktop_management_enabled', 'true', 'software'),
    ]
    
    for key, value, category in system_info:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"  [+] {key}: {value}")
    
    # Add knowledge base
    print("\n[2/5] Adding knowledge base...")
    knowledge = [
        # Blender-style 3D Features
        (
            'Blender 3D - Overview',
            'JARVIS 3D Features: Complete 3D modeling, animation, and rendering like Blender. '
            'Features: 3D modeling (mesh editing, sculpting, modifiers), Animation (keyframes, '
            'rigging, character animation), Rendering (Cycles, Eevee, materials, lighting), '
            'Video editing (sequencer, effects, transitions), Compositing (nodes, color grading), '
            'Python scripting (automation, custom tools, add-ons). Supports: OBJ, FBX, STL, '
            'GLTF, Collada, Alembic formats. Tools: Extrude, Bevel, Loop cut, Knife, Proportional '
            'editing, Snap, Mirror, Array, Subdivision surface.',
            'blender_3d'
        ),
        (
            'Blender 3D - Modeling',
            '3D Modeling Tools: Edit mode, Object mode, Sculpt mode. Mesh editing: Vertices, '
            'Edges, Faces manipulation. Tools: Extrude, Inset, Bevel, Loop cut, Knife tool, '
            'Subdivide, Merge, Separate. Modifiers: Array, Mirror, Solidify, Subdivision surface, '
            'Boolean, Bevel, Displace, Shrinkwrap. Sculpting: Dynamic topology, Multiresolution, '
            'Brushes (Draw, Clay, Grab, Smooth, Pinch, Inflate). Primitives: Cube, Sphere, '
            'Cylinder, Cone, Torus, Plane, Monkey (Suzanne). Curves: Bezier, NURBS, Path.',
            'blender_modeling'
        ),
        (
            'Blender 3D - Animation',
            'Animation System: Keyframe animation, Timeline, Dope sheet, Graph editor, NLA editor. '
            'Rigging: Armatures, Bones, IK/FK, Constraints, Weight painting, Bone groups. '
            'Character animation: Walk cycles, Run cycles, Jump, Facial animation, Lip sync. '
            'Motion paths: Follow path, Motion tracking, Camera tracking. Animation tools: '
            'Auto-keyframe, Onion skinning, Grease pencil, Shape keys, Drivers. Physics: '
            'Rigid body, Soft body, Cloth, Fluid, Smoke, Fire, Hair, Particles.',
            'blender_animation'
        ),
        (
            'Blender 3D - Rendering',
            'Rendering Engines: Cycles (ray tracing, physically accurate), Eevee (real-time, '
            'fast preview), Workbench (solid/wireframe). Materials: Principled BSDF, Shader '
            'nodes, Textures (Image, Procedural), UV mapping, PBR workflow. Lighting: Point, '
            'Sun, Spot, Area lights, HDRI environment, Light probes, Global illumination. '
            'Camera: Perspective, Orthographic, Panoramic, Depth of field, Motion blur. '
            'Render settings: Resolution, Samples, Denoising, Render layers, Passes (Diffuse, '
            'Specular, Normal, Z-depth). Output: PNG, JPEG, EXR, TIFF, MP4, AVI.',
            'blender_rendering'
        ),
        (
            'Blender 3D - Video Editing',
            'Video Sequencer: Non-linear video editor, Timeline, Strips (Video, Audio, Image, '
            'Text). Editing: Cut, Trim, Split, Slip, Slide, Crossfade, Wipe transitions. '
            'Effects: Color correction, Glow, Blur, Transform, Speed control, Reverse, '
            'Stabilization. Audio: Waveform display, Volume, Pitch, Fade in/out, Audio mixing. '
            'Text: Title cards, Credits, Subtitles, Animated text. Export: MP4, AVI, MOV, '
            'WebM, Various codecs (H.264, H.265, VP9). Proxy: Low-res preview for smooth editing.',
            'blender_video'
        ),
        
        # Download Manager
        (
            'Download Manager - Overview',
            'JARVIS Download Manager: Full-featured download manager like IDM, Free Download '
            'Manager. Features: Multi-threaded downloads (up to 32 connections), Resume broken '
            'downloads, Download queue, Schedule downloads, Speed limiter, Bandwidth control, '
            'Browser integration (Chrome, Firefox, Edge), Categories (Documents, Videos, Music, '
            'Software), Download history, Virus scanning, Automatic file organization. '
            'Protocols: HTTP, HTTPS, FTP, FTPS, SFTP. Media: YouTube, Vimeo, Dailymotion, '
            'Facebook, Instagram, Twitter video downloads.',
            'download_manager'
        ),
        (
            'Download Manager - Features',
            'Download Features: Pause/Resume downloads, Retry failed downloads, Download '
            'acceleration (split files), Mirror search, Checksum verification (MD5, SHA1, SHA256), '
            'ZIP preview, Automatic antivirus scan, Download complete notification, Shutdown PC '
            'after downloads. Queue management: Priority queue, Sequential downloads, Parallel '
            'downloads, Download later. Browser integration: Capture downloads, Context menu, '
            'Download all links, Batch downloads. Speed: Speed limiter, Schedule speed, '
            'Global/Per-download limits. Organization: Auto-categorize, Custom folders, '
            'File naming rules, Duplicate detection.',
            'download_features'
        ),
        (
            'Download Manager - Media Downloads',
            'Media Download: YouTube video/audio download, Playlist download, Channel download, '
            'Quality selection (4K, 1080p, 720p, 480p, 360p), Format selection (MP4, WebM, MKV, '
            'MP3, M4A, WAV), Subtitle download, Thumbnail download. Supported sites: YouTube, '
            'Vimeo, Dailymotion, Facebook, Instagram, Twitter, TikTok, Reddit, Twitch, SoundCloud. '
            'Features: Batch download, Auto-convert, Metadata tagging, Playlist management. '
            'Audio: Extract audio from video, Audio quality selection, ID3 tags, Album art.',
            'media_downloads'
        ),
        
        # System Services
        (
            'System Services - Management',
            'Windows Services Management: View all services, Service status (Running, Stopped, '
            'Paused), Start/Stop/Restart services, Service startup type (Automatic, Manual, '
            'Disabled, Automatic Delayed), Service dependencies, Service description, Service '
            'account, Service recovery options. Common services: Windows Update, Windows Defender, '
            'Print Spooler, DHCP Client, DNS Client, Windows Firewall, Remote Desktop, Task '
            'Scheduler, Windows Search, Superfetch, Windows Time. Service control: net start, '
            'net stop, sc query, sc config, Get-Service, Start-Service, Stop-Service.',
            'system_services'
        ),
        (
            'System Services - Startup Programs',
            'Startup Management: View startup programs, Enable/Disable startup items, Startup '
            'impact (High, Medium, Low), Startup delay, Startup location (Registry, Startup '
            'folder, Task Scheduler). Startup locations: HKEY_CURRENT_USER\\Software\\Microsoft\\'
            'Windows\\CurrentVersion\\Run, HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\'
            'CurrentVersion\\Run, %AppData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup, '
            '%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup. Tools: Task Manager '
            'Startup tab, msconfig, Autoruns, PowerShell Get-StartupProgram.',
            'startup_programs'
        ),
        (
            'System Services - Task Scheduler',
            'Task Scheduler: View scheduled tasks, Create tasks, Modify tasks, Delete tasks, '
            'Task triggers (Time, Logon, Startup, Idle, Event), Task actions (Run program, '
            'Send email, Display message), Task conditions (Idle, AC power, Network), Task '
            'settings (Allow on demand, Stop if runs too long, Restart on failure). Common tasks: '
            'Windows Update, Disk Cleanup, Defragmentation, Backup, Antivirus scan. Task history: '
            'Last run time, Last run result, Next run time. PowerShell: Get-ScheduledTask, '
            'New-ScheduledTask, Register-ScheduledTask.',
            'task_scheduler'
        ),
        
        # Permissions
        (
            'Permissions - File & Folder',
            'File/Folder Permissions: View permissions, Modify permissions (requires admin), '
            'Permission types: Full control, Modify, Read & execute, List folder contents, Read, '
            'Write. Users/Groups: Administrators, Users, Everyone, SYSTEM, Authenticated Users. '
            'Advanced permissions: Traverse folder, List folder, Read attributes, Read extended '
            'attributes, Create files, Create folders, Write attributes, Write extended attributes, '
            'Delete, Delete subfolders and files, Read permissions, Change permissions, Take '
            'ownership. Inheritance: Enable/Disable inheritance, Copy inherited permissions, '
            'Remove inherited permissions. Tools: icacls, cacls, Get-Acl, Set-Acl.',
            'file_permissions'
        ),
        (
            'Permissions - User & App',
            'User Permissions: User accounts, User groups, Group membership, User rights, '
            'Security policies, Password policies, Account lockout policies. App Permissions: '
            'Windows 10/11 app permissions, Location, Camera, Microphone, Notifications, '
            'Account info, Contacts, Calendar, Phone calls, Call history, Email, Tasks, '
            'Messaging, Radios, Background apps, App diagnostics, Documents, Pictures, Videos, '
            'File system. Privacy settings: General, Speech, Inking & typing, Diagnostics & '
            'feedback, Activity history, Location, Camera, Microphone, Voice activation, '
            'Notifications, Account info, Contacts, Calendar, Phone calls, Call history, Email, '
            'Tasks, Messaging, Radios, Other devices, Background apps, App diagnostics, '
            'Automatic file downloads, Documents, Pictures, Videos, File system.',
            'user_app_permissions'
        ),
        
        # Hardware Monitoring
        (
            'Hardware Monitoring - CPU & RAM',
            'CPU Monitoring: CPU model, Cores, Threads, Base clock, Boost clock, Cache (L1, L2, '
            'L3), Architecture, Socket, TDP, Virtualization, CPU usage (overall, per core), '
            'CPU frequency (current, min, max), CPU temperature, CPU voltage, CPU power. '
            'RAM Monitoring: Total RAM, Used RAM, Available RAM, RAM speed, RAM type (DDR3, '
            'DDR4, DDR5), RAM slots, RAM modules, RAM manufacturer, RAM timings, RAM voltage, '
            'RAM temperature. Tools: Task Manager, Resource Monitor, Performance Monitor, '
            'HWiNFO, CPU-Z, GPU-Z, MSI Afterburner, Open Hardware Monitor, Core Temp, '
            'SpeedFan, AIDA64.',
            'cpu_ram_monitoring'
        ),
        (
            'Hardware Monitoring - GPU & Disk',
            'GPU Monitoring: GPU model, GPU memory, GPU clock, Memory clock, GPU usage, '
            'GPU temperature, GPU fan speed, GPU power, GPU voltage, VRAM usage, Driver version, '
            'DirectX version, OpenGL version, CUDA cores, Shader units. Disk Monitoring: '
            'Disk model, Disk size, Disk type (HDD, SSD, NVMe), Disk interface (SATA, NVMe, '
            'USB), Disk usage, Disk health (SMART), Disk temperature, Read/Write speed, '
            'Disk partitions, File system (NTFS, FAT32, exFAT), Free space, Used space. '
            'Tools: CrystalDiskInfo, CrystalDiskMark, HD Tune, HDDScan, Samsung Magician, '
            'Intel SSD Toolbox.',
            'gpu_disk_monitoring'
        ),
        (
            'Hardware Monitoring - Network & Battery',
            'Network Monitoring: Network adapters, Network speed, Upload/Download speed, '
            'Network usage, IP address (IPv4, IPv6), MAC address, Subnet mask, Default gateway, '
            'DNS servers, Network type (Ethernet, Wi-Fi, Bluetooth), Signal strength, Network '
            'latency, Packet loss, Network connections, Open ports. Battery Monitoring (Laptops): '
            'Battery level, Battery status (Charging, Discharging, Full), Battery health, '
            'Battery capacity (Design, Full charge, Current), Battery wear level, Battery '
            'technology (Li-ion, Li-Po), Battery voltage, Battery temperature, Charge/Discharge '
            'rate, Time remaining, Power plan. Tools: NetSpeedMonitor, NetWorx, GlassWire, '
            'Wireshark, BatteryInfoView, BatteryCare.',
            'network_battery_monitoring'
        ),
        
        # Keyboard Automation
        (
            'Keyboard - Shortcuts & Automation',
            'Windows Shortcuts (Already included): Win+E, Win+R, Win+L, Win+D, Win+I, Win+X, '
            'Alt+Tab, Ctrl+C, Ctrl+V, Ctrl+Z, Ctrl+Y, Ctrl+A, Ctrl+S, Ctrl+P, Ctrl+F, '
            'Ctrl+Shift+Esc, Win+Tab, Win+Ctrl+D, Win+Ctrl+Left/Right, Win+Shift+S, Win+V, '
            'Win+Period, Win+Semicolon. Custom Hotkeys: Create custom shortcuts, Assign actions '
            'to keys, Key combinations (Ctrl, Alt, Shift, Win), Global hotkeys, Application-'
            'specific hotkeys. Keyboard Automation: Auto-type text, Keyboard macros, Text '
            'expansion, Clipboard manager, Keystroke recording, Keystroke playback, Delay between '
            'keys, Key press duration. Tools: AutoHotkey, PhraseExpress, Clavier+, WinHotKey.',
            'keyboard_automation'
        ),
        (
            'Keyboard - Macros & Text Expansion',
            'Keyboard Macros: Record keystrokes, Playback keystrokes, Loop macros, Conditional '
            'macros, Macro editor, Macro library, Import/Export macros, Hotkey triggers. '
            'Text Expansion: Abbreviations, Auto-complete, Snippets, Templates, Variables '
            '(Date, Time, Clipboard), Formatted text, Rich text, Images, Cursor positioning. '
            'Use cases: Email templates, Code snippets, Signatures, Addresses, Phone numbers, '
            'Common phrases, Corrections, Emojis. Advanced: Scripting, Conditional expansion, '
            'Form filling, Multi-step automation, Window-specific expansion.',
            'keyboard_macros'
        ),
        
        # Mouse Automation
        (
            'Mouse - Control & Automation',
            'Mouse Automation: Auto-click, Click at coordinates, Mouse movement, Drag and drop, '
            'Right-click, Middle-click, Double-click, Triple-click, Mouse wheel scroll, '
            'Horizontal scroll. Click types: Single click, Double click, Click and hold, '
            'Click interval, Click count, Random clicks. Mouse movement: Move to coordinates, '
            'Move relative, Smooth movement, Instant movement, Random movement, Follow path. '
            'Recording: Record mouse actions, Playback actions, Loop actions, Edit recording, '
            'Save/Load recordings. Tools: AutoClicker, OP Auto Clicker, GS Auto Clicker, '
            'Mouse Recorder, TinyTask.',
            'mouse_automation'
        ),
        (
            'Mouse - Gestures & Settings',
            'Mouse Gestures: Custom gestures, Gesture actions (Back, Forward, Close, Minimize, '
            'Maximize, New tab, Close tab, Refresh, Scroll to top, Scroll to bottom), Gesture '
            'recognition, Gesture trails, Gesture sensitivity. Mouse Settings: Pointer speed, '
            'Acceleration, Precision (Enhance pointer precision), Button configuration (Swap '
            'buttons, Primary button), Double-click speed, Click lock, Pointer visibility '
            '(Show pointer trails, Hide pointer while typing, Show location), Scroll settings '
            '(Lines per notch, Scroll inactive windows). Custom Cursors: Cursor themes, Cursor '
            'size, Cursor color, Animated cursors, Cursor packs. Tools: StrokesPlus, gMote, '
            'Mouse Gestures for Windows.',
            'mouse_gestures'
        ),
        
        # Desktop Management
        (
            'Desktop - Management & Screenshots',
            'Desktop Features: Desktop screenshot (Full screen, Window, Region, Scrolling), '
            'Desktop recording (Video, GIF), Screenshot tools (Snipping Tool, Snip & Sketch, '
            'Win+Shift+S), Screenshot formats (PNG, JPEG, BMP, GIF), Screenshot editor (Crop, '
            'Annotate, Highlight, Arrow, Text, Blur). Desktop Cleanup: Icon arrangement (Auto '
            'arrange, Align to grid, Sort by name/size/date), Desktop icons (Show/Hide), '
            'Unused icon cleanup, Desktop files organization. Wallpaper: Static wallpaper, '
            'Slideshow, Solid color, Wallpaper fit (Fill, Fit, Stretch, Tile, Center), '
            'Wallpaper position, Multiple monitor wallpapers. Tools: ShareX, Greenshot, '
            'Lightshot, Snagit, OBS Studio, ScreenToGif.',
            'desktop_management'
        ),
        (
            'Desktop - Windows & Virtual Desktops',
            'Window Management: Window list (All windows, Active window), Window position (X, Y), '
            'Window size (Width, Height), Minimize, Maximize, Restore, Close, Always on top, '
            'Window transparency, Window opacity, Snap windows (Win+Left/Right, Win+Up/Down), '
            'Cascade windows, Stack windows, Show windows side by side. Virtual Desktops: '
            'Create desktop (Win+Ctrl+D), Switch desktop (Win+Ctrl+Left/Right), Close desktop '
            '(Win+Ctrl+F4), Task view (Win+Tab), Move window to desktop, Desktop wallpaper per '
            'desktop, Desktop names. Taskbar: Taskbar position (Bottom, Top, Left, Right), '
            'Taskbar visibility (Auto-hide, Always visible), Taskbar size, Pinned apps, '
            'System tray icons, Notification area, Taskbar buttons (Combine, Never combine). '
            'Tools: PowerToys FancyZones, DisplayFusion, AquaSnap, WindowGrid.',
            'window_virtual_desktops'
        ),
        (
            'Desktop - Display Settings',
            'Display Settings: Resolution (1920x1080, 2560x1440, 3840x2160, etc.), Refresh rate '
            '(60Hz, 75Hz, 120Hz, 144Hz, 240Hz), Scaling (100%, 125%, 150%, 175%, 200%), '
            'Orientation (Landscape, Portrait, Landscape flipped, Portrait flipped), Multiple '
            'displays (Duplicate, Extend, Second screen only, PC screen only), Primary display, '
            'Display arrangement, Display identification. Color: Color profile, Color calibration, '
            'Color depth (8-bit, 10-bit), HDR, Night light (Blue light filter, Schedule, Color '
            'temperature). Advanced: Custom resolution, Refresh rate override, GPU scaling, '
            'Integer scaling, Variable refresh rate (G-Sync, FreeSync). Tools: Custom Resolution '
            'Utility (CRU), Monitor Asset Manager, DisplayCAL.',
            'display_settings'
        ),
        
        # System Utilities
        (
            'System Utilities - Process Management',
            'Process Management: View running processes, Process list, Process tree, Process '
            'details (PID, CPU usage, Memory usage, Disk usage, Network usage, Threads, Handles, '
            'User, Command line), Kill process, Kill process tree, Process priority (Realtime, '
            'High, Above normal, Normal, Below normal, Low), Process affinity (CPU cores), '
            'Process suspend/resume. System processes: System, Registry, smss.exe, csrss.exe, '
            'wininit.exe, services.exe, lsass.exe, svchost.exe, explorer.exe. Tools: Task Manager, '
            'Process Explorer, Process Hacker, System Explorer, Process Monitor. PowerShell: '
            'Get-Process, Stop-Process, Start-Process, Wait-Process.',
            'process_management'
        ),
        (
            'System Utilities - Registry & Environment',
            'Registry Editor (SAFE): View registry, Registry hives (HKEY_CLASSES_ROOT, '
            'HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG), Search '
            'registry, Export registry, Import registry, Backup registry, Registry favorites, '
            'Registry permissions. Common keys: Run, RunOnce, Uninstall, File associations, '
            'Shell extensions, Context menu, Startup programs. Environment Variables: System '
            'variables, User variables, PATH, TEMP, TMP, USERPROFILE, ProgramFiles, SystemRoot, '
            'COMPUTERNAME, USERNAME. Variable management: View, Add, Edit, Delete, Expand. '
            'PATH management: Add to PATH, Remove from PATH, Reorder PATH, Clean PATH. '
            'Tools: Registry Editor (regedit), Rapid Environment Editor, Path Editor.',
            'registry_environment'
        ),
        (
            'System Utilities - Cleanup & Maintenance',
            'System Cleanup: Temp files cleanup (%TEMP%, C:\\Windows\\Temp), Cache cleanup '
            '(Browser cache, Thumbnail cache, Font cache, DNS cache, Icon cache), Log files '
            'cleanup (Windows logs, Application logs, Event logs), Recycle bin (Empty, View '
            'contents, Restore items), Disk cleanup (Windows Disk Cleanup, cleanmgr), Old '
            'Windows installation cleanup (Windows.old), Windows Update cleanup (WinSxS, '
            'Update cache). Maintenance: Disk defragmentation (HDD only), TRIM (SSD), Disk '
            'check (chkdsk), System file check (sfc /scannow), DISM repair, Windows Update, '
            'Driver updates, Malware scan, Disk space analyzer. Tools: CCleaner, BleachBit, '
            'Glary Utilities, Wise Disk Cleaner, TreeSize, WinDirStat, SpaceSniffer.',
            'system_cleanup'
        ),
    ]
    
    for topic, content, source in knowledge:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    # Add preferences
    print("\n[3/5] Adding user preferences...")
    preferences = [
        ('blender_3d_renderer', 'Eevee'),
        ('download_manager_threads', '16'),
        ('download_manager_speed_limit', '0'),
        ('hardware_monitoring_interval', '1000'),
        ('keyboard_automation_enabled', 'true'),
        ('mouse_automation_enabled', 'true'),
        ('desktop_screenshot_format', 'PNG'),
        ('virtual_desktops_enabled', 'true'),
    ]
    
    for key, value in preferences:
        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (key, value))
        print(f"  [+] {key}: {value}")
    
    conn.commit()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM system_info")
    sys_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    kb_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_preferences")
    pref_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Summary
    print("\n" + "=" * 80)
    print("  SYSTEM FEATURES ADDED SUCCESSFULLY!")
    print("  সিস্টেম ফিচার সফলভাবে যোগ করা হয়েছে!")
    print("=" * 80)
    print(f"  Database: {os.path.abspath(db_path)}")
    print(f"  Total system info: {sys_count} entries")
    print(f"  Total knowledge: {kb_count} entries")
    print(f"  Total preferences: {pref_count} entries")
    print(f"  Total entries: {sys_count + kb_count + pref_count}")
    print("\n  Features Added:")
    print("  ✅ Blender-style 3D (Modeling, Animation, Rendering, Video)")
    print("  ✅ Download Manager (Multi-threaded, Resume, Media downloads)")
    print("  ✅ System Services (Services, Startup, Task Scheduler)")
    print("  ✅ Permissions (File, Folder, User, App)")
    print("  ✅ Hardware Monitoring (CPU, RAM, GPU, Disk, Network, Battery)")
    print("  ✅ Keyboard Automation (Shortcuts, Macros, Text expansion)")
    print("  ✅ Mouse Automation (Auto-click, Gestures, Recording)")
    print("  ✅ Desktop Management (Screenshots, Windows, Virtual desktops)")
    print("  ✅ System Utilities (Process, Registry, Cleanup)")
    print("\n  JARVIS now has advanced system features!")
    print("  JARVIS এখন উন্নত সিস্টেম ফিচার পেয়েছে!")
    print("=" * 80)

def main():
    print("\n🔧 Adding System Features to JARVIS")
    print("🔧 JARVIS এ সিস্টেম ফিচার যোগ করা হচ্ছে\n")
    
    db_path = find_database()
    
    if not db_path:
        print("[ERROR] No working database found!")
        print("[ত্রুটি] কোনো কার্যকর ডাটাবেস পাওয়া যায়নি!")
        return
    
    print(f"[INFO] Found database: {db_path}\n")
    
    try:
        add_system_features(db_path)
        print("\n✅ SUCCESS! System features added to JARVIS.")
        print("✅ সফল! JARVIS এ সিস্টেম ফিচার যোগ করা হয়েছে।")
    except Exception as e:
        print(f"\n[ERROR] Failed to add system features: {e}")
        print(f"[ত্রুটি] সিস্টেম ফিচার যোগ করতে ব্যর্থ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
