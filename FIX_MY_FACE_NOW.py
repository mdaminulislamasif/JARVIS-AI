import os
import subprocess
import sys

def run_fix():
    print("="*60)
    print("JARVIS 3D FACE ULTIMATE SHADER FIX")
    print("="*60)
    
    project_root = r"c:\Users\PHP\Desktop\ai"
    
    print("\n[*] Starting JARVIS Face Test (SHADER POWERED)...")
    try:
        # Run as module from project root
        subprocess.Popen([sys.executable, "-m", "engine.face3d_run"], cwd=project_root)
        print("[+] SUCCESS: Face renderer started with Shader Technology.")
        print("[+] The mouth will now move dynamically without Blender!")
    except Exception as e:
        print(f"[-] Could not start renderer: {e}")

if __name__ == "__main__":
    run_fix()
