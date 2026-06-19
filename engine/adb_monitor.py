import subprocess
import time
import os

def get_devices(adb_path):
    try:
        # Run adb.exe to check connected devices
        res = subprocess.run(f'"{adb_path}" devices', shell=True, capture_output=True, text=True)
        lines = res.stdout.strip().split("\n")[1:]
        devices = []
        for line in lines:
            if line.strip() and "device" in line and "devices" not in line and "unauthorized" not in line:
                devices.append(line.split()[0])
        return devices
    except Exception:
        return []

def main():
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    adb_path = os.path.join(workspace, "platform-tools", "adb.exe")
    if not os.path.exists(adb_path):
        adb_path = "adb"
        
    scrcpy_exe = os.path.join(workspace, "scrcpy", "scrcpy-win64-v2.4", "scrcpy.exe")
    
    print("[*] ADB Hotplug Auto-Mirroring Monitor started...")
    
    # Auto-mirror already connected devices on startup
    initial_devices = get_devices(adb_path)
    for serial in initial_devices:
        print(f"[+] Device already connected on startup ({serial}). Launching mirroring...")
        if os.path.exists(scrcpy_exe):
            subprocess.Popen(f'"{scrcpy_exe}" -s {serial} --always-on-top', shell=True)
        else:
            subprocess.Popen(f'scrcpy -s {serial} --always-on-top', shell=True)
            
    known_devices = set(initial_devices)
    
    while True:
        try:
            current_devices = set(get_devices(adb_path))
            new_devices = current_devices - known_devices
            
            for serial in new_devices:
                print(f"[+] Symphony ATOM 5 connected via USB ({serial}). Launching mirroring...")
                if os.path.exists(scrcpy_exe):
                    subprocess.Popen(f'"{scrcpy_exe}" -s {serial} --always-on-top', shell=True)
                else:
                    subprocess.Popen(f'scrcpy -s {serial} --always-on-top', shell=True)
                
            known_devices = current_devices
            time.sleep(2)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error in monitor loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
