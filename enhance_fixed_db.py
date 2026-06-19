"""Quick script to enhance the fixed database"""
import sqlite3
import subprocess
import platform
import os
import glob

# Find the fixed database
fixed_dbs = glob.glob('jarvis_memory.db.fixed-*')
fixed_dbs.sort(reverse=True)
db_path = fixed_dbs[0] if fixed_dbs else None

if not db_path:
    print("No fixed database found!")
    exit(1)

print(f"Enhancing: {db_path}\n")

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10, shell=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            return lines[1].strip() if len(lines) > 1 else None
    except Exception as e:

        print(f"⚠️ Error: {e}")
        return None

# Gather info
info = {
    'os_caption': run_cmd('wmic os get Caption'),
    'os_architecture': run_cmd('wmic os get OSArchitecture'),
    'os_build': run_cmd('wmic os get BuildNumber'),
    'computer_manufacturer': run_cmd('wmic computersystem get Manufacturer'),
    'computer_model': run_cmd('wmic computersystem get Model'),
    'cpu_name': run_cmd('wmic cpu get Name'),
    'cpu_cores': run_cmd('wmic cpu get NumberOfCores'),
    'cpu_logical_processors': run_cmd('wmic cpu get NumberOfLogicalProcessors'),
    'bios_version': run_cmd('wmic bios get Version'),
    'gpu_name': run_cmd('wmic path win32_VideoController get Name'),
    'windows_directory': os.environ.get('WINDIR', 'C:\\Windows'),
    'program_files': os.environ.get('ProgramFiles', 'C:\\Program Files'),
    'user_profile': os.environ.get('USERPROFILE', ''),
    'python_implementation': platform.python_implementation(),
}

# Update database
conn = sqlite3.connect(db_path, timeout=10)
cursor = conn.cursor()

for key, value in info.items():
    if value:
        category = 'system' if key.startswith(('os_', 'computer_')) else 'hardware' if key.startswith(('cpu_', 'bios_', 'gpu_')) else 'paths' if key.startswith(('windows_', 'program_', 'user_')) else 'software'
        cursor.execute("INSERT OR REPLACE INTO system_info (key, value, category, updated_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", (key, str(value), category))
        print(f"[+] {key}: {str(value)[:60]}")

conn.commit()
conn.close()

print(f"\n[SUCCESS] Enhanced {db_path}")
print("View with: python view_database.py")
