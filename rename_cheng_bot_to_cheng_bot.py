import os
import re
import sys

# Ensure console can handle UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def rename_all_cheng_bot_to_cheng_bot(root_dir):
    print(f"Starting mass rename in: {root_dir}")
    
    # --- 1. RENAME FILES AND DIRECTORIES ---
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for filename in filenames:
            if "cheng_bot" in filename.lower():
                # Skip the script itself if needed, but it already renamed itself
                new_filename = filename.replace("cheng_bot", "cheng_bot").replace("Cheng Bot", "Cheng_Bot")
                old_file_path = os.path.join(dirpath, filename)
                new_file_path = os.path.join(dirpath, new_filename)
                
                try:
                    os.rename(old_file_path, new_file_path)
                except Exception as e:
                    print(f"⚠️ Error: {e}")

        for dirname in dirnames:
            if "cheng_bot" in dirname.lower():
                new_dirname = dirname.replace("cheng_bot", "cheng_bot").replace("Cheng Bot", "Cheng_Bot")
                old_dir_path = os.path.join(dirpath, dirname)
                new_dir_path = os.path.join(dirpath, new_dirname)
                
                try:
                    os.rename(old_dir_path, new_dir_path)
                except Exception as e:
                    print(f"⚠️ Error: {e}")

    # --- 2. REPLACE TEXT INSIDE FILES ---
    for dirpath, dirnames, filenames in os.walk(root_dir):
        skip_extensions = ['.exe', '.dll', '.pyc', '.glb', '.png', '.jpg', '.zip', '.git', '.pyo', '.pyd']
        
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in skip_extensions):
                continue
                
            file_path = os.path.join(dirpath, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if 'cheng_bot' in content.lower():
                    new_content = content.replace('Cheng Bot', 'Cheng Bot')
                    new_content = new_content.replace('cheng_bot', 'cheng_bot')
                    new_content = new_content.replace('CHENG BOT', 'CHENG BOT')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"[TEXT REPLACE] Success in: {filename}")
            except Exception as e:
                print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    target_root = r"c:\Users\PHP\Desktop\ai"
    rename_all_cheng_bot_to_cheng_bot(target_root)
    print("RENAME COMPLETE!")
