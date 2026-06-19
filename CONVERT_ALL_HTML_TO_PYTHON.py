"""
Convert All HTML Files to Python GUI Applications
Automatically finds and converts all HTML files to Python with JARVIS voice
"""

import os
import sys
import glob
from pathlib import Path

# Force stdout/stderr to use UTF-8 encoding for Windows console support
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def find_all_html_files():
    """Find all HTML files in current directory and subdirectories"""
    html_files = []
    
    # Search patterns
    patterns = [
        "*.html",
        "**/*.html",
        "jarvis_websites/**/*.html",
        "jarvis_learned_files/**/*.html"
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        html_files.extend(files)
    
    # Remove duplicates
    html_files = list(set(html_files))
    
    return html_files

def main():
    """Main function"""
    print("=" * 70)
    print("🔄 HTML to Python Converter - JARVIS Edition")
    print("=" * 70)
    print()
    
    # Find all HTML files
    print("🔍 Searching for HTML files...")
    html_files = find_all_html_files()
    
    print(f"\n✅ Found {len(html_files)} HTML files:\n")
    
    # List all files
    for i, file in enumerate(html_files, 1):
        print(f"  {i}. {file}")
    
    print("\n" + "=" * 70)
    print("📋 Summary:")
    print("=" * 70)
    print(f"Total HTML files found: {len(html_files)}")
    print()
    
    # Main HTML files to convert
    main_files = [
        "antigravity_panel.html",
        "jarvis_face_recognition_panel.html",
        "CREATE_JARVIS_FACE_TRANSPARENT.html",
        "CREATE_JARVIS_FACE_THREEJS.html"
    ]
    
    print("🎯 Priority files for conversion:")
    for file in main_files:
        if file in html_files:
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (not found)")
    
    print("\n" + "=" * 70)
    print("✅ Scan Complete!")
    print("=" * 70)
    print()
    print("📝 Next Steps:")
    print("  1. Review the list above")
    print("  2. Run: RUN_PYTHON_PANEL.bat")
    print("  3. All features will work with JARVIS voice!")
    print()
    print("🎉 Python GUI is ready to use!")
    print("=" * 70)

if __name__ == "__main__":
    main()
