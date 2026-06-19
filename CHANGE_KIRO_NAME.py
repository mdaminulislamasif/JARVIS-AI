"""
Change Cheng Bot Name to ASIF or AI
================================
This script replaces all occurrences of "Cheng Bot" with your chosen name
in all documentation and markdown files.

Usage:
    python CHANGE_CHENG BOT_NAME.py
"""

import os
import re

def replace_in_file(filepath, replacements):
    """Replace text in a file"""
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        total_count = 0
        
        # Apply all replacements
        for old, new in replacements:
            count = content.count(old)
            if count > 0:
                content = content.replace(old, new)
                total_count += count
        
        if total_count == 0:
            return 0
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return total_count
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return 0

def replace_in_all_files(old_name, new_name):
    """Replace name in all markdown and text files"""
    
    # Prepare replacements (different cases)
    replacements = [
        (old_name.upper(), new_name.upper()),  # CHENG BOT → ASIF
        (old_name.capitalize(), new_name.capitalize()),  # Cheng Bot → Asif
        (old_name.lower(), new_name.lower()),  # cheng_bot → asif
    ]
    
    total_files = 0
    total_replacements = 0
    
    print(f"\nSearching for '{old_name}' in all files...")
    print("=" * 60)
    
    # File extensions to process
    extensions = ['.md', '.txt', '.json', '.py', '.bat']
    
    # Directories to skip
    skip_dirs = ['.git', '__pycache__', 'node_modules', '.pytest_cache', '.hypothesis']
    
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for filename in files:
            # Check extension
            if not any(filename.endswith(ext) for ext in extensions):
                continue
            
            filepath = os.path.join(root, filename)
            
            # Skip binary files
            if filename.endswith(('.glb', '.png', '.jpg', '.exe', '.dll', '.pyc')):
                continue
            
            count = replace_in_file(filepath, replacements)
            
            if count > 0:
                print(f"\n✓ {filepath}")
                print(f"  Replaced {count} occurrence(s)")
                total_files += 1
                total_replacements += count
    
    return total_files, total_replacements

def main():
    print("=" * 60)
    print("Cheng Bot Name Changer")
    print("=" * 60)
    print()
    print("This will replace 'Cheng Bot' with your chosen name")
    print("in all documentation files.")
    print()
    
    # Get new name
    print("Choose new name:")
    print("  1. ASIF")
    print("  2. AI")
    print("  3. Custom name")
    print()
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == '1':
        new_name = "ASIF"
    elif choice == '2':
        new_name = "AI"
    elif choice == '3':
        new_name = input("Enter custom name: ").strip()
        if not new_name:
            print("\nError: Name cannot be empty!")
            return
    else:
        print("\nInvalid choice!")
        return
    
    print()
    print(f"Will replace: Cheng Bot → {new_name}")
    print()
    
    # Confirm
    response = input("Continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y', 'হ্যাঁ', 'হা']:
        print("\nCancelled.")
        return
    
    print("\n" + "=" * 60)
    print("Starting replacement...")
    print("=" * 60)
    
    # Do replacement
    files, reps = replace_in_all_files("Cheng Bot", new_name)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Files modified: {files}")
    print(f"Total replacements: {reps}")
    print()
    
    if reps > 0:
        print(f"✓ SUCCESS! All 'Cheng Bot' replaced with '{new_name}'")
        print()
        print("Modified file types:")
        print("  - Markdown files (.md)")
        print("  - Text files (.txt)")
        print("  - JSON files (.json)")
        print("  - Python files (.py)")
        print("  - Batch files (.bat)")
        print()
        print("Note: Binary files (.glb, .png, etc.) were NOT modified")
    else:
        print("! No replacements made")
        print("  (No 'Cheng Bot' found in files)")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
