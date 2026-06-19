import os
import sys
import ctypes
import subprocess
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_system32_path():
    import os
    sysnative = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Sysnative')
    if os.path.exists(sysnative):
        return sysnative
    return os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32')

def run_repairs():
    print("=========================================================")
    print("Windows System Repair Tool")
    print("=========================================================")
    
    system32 = get_system32_path()
    sc_path = os.path.join(system32, 'sc.exe')
    net_path = os.path.join(system32, 'net.exe')
    dism_path = os.path.join(system32, 'dism.exe')
    sfc_path = os.path.join(system32, 'sfc.exe')
    
    # 1. Start TrustedInstaller
    print("\n[1/3] Starting Windows Modules Installer service...")
    subprocess.run(f'"{sc_path}" config trustedinstaller start=auto', shell=True)
    subprocess.run(f'"{net_path}" start trustedinstaller', shell=True)
    
    # 2. DISM
    print("\n[2/3] Running DISM (Component Store Repair)...")
    print("This may take 10-20 minutes. Please do not close this window.")
    subprocess.run(f'"{dism_path}" /online /cleanup-image /restorehealth', shell=True)
    
    # 3. SFC
    print("\n[3/3] Running SFC (System File Checker)...")
    subprocess.run(f'"{sfc_path}" /scannow', shell=True)
    
    print("\n=========================================================")
    print("Repairs completed successfully!")
    print("It is recommended to restart your computer now.")
    print("=========================================================")
    input("\nPress Enter to close this window...")

if __name__ == "__main__":
    if is_admin():
        run_repairs()
    else:
        print("Requesting administrator privileges...")
        # Relaunch the script as administrator
        script_path = os.path.abspath(sys.argv[0])
        params = f'"{script_path}"'
        
        # Verb "runas" triggers UAC elevation prompt in Windows
        result = ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            params, 
            None, 
            1
        )
        
        if int(result) <= 32:
            print("[ERROR] Failed to elevate privileges. Please run this script manually as administrator.")
            time.sleep(5)
