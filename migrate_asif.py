import shutil
import os

src = r"D:\AA ASIF\New folder\New folder"
dst = r"C:\Users\PHP\Desktop\ai\asif_hacker_suite"

if not os.path.exists(dst):
    os.makedirs(dst)

try:
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print(f"SUCCESS: Files moved to {dst}")
except Exception as e:
    print(f"FAILED: {e}")
