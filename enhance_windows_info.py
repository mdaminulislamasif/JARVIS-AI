"""
Enhance Windows 10 Pro Information in Database
Adds more detailed Windows system information
"""
import sqlite3
import subprocess
import platform
import os

def run_wmic_command(command):
    """Run WMIC command and return output"""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=10,
            shell=True
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                return lines[1].strip()
    except Exception as e:

        print(f"⚠️ Error: {e}")
        pass
    return None

def get_enhanced_windows_info():
    """Gather comprehensive Windows 10 Pro information"""
    info = {}
    
    print("Gathering enhanced Windows 10 Pro information...")
    
    # OS Information
    print("  [1/10] OS Information...")
    info['os_caption'] = run_wmic_command('wmic os get Caption')
    info['os_architecture'] = run_wmic_command('wmic os get OSArchitecture')
    info['os_build'] = run_wmic_command('wmic os get BuildNumber')
    info['os_install_date'] = run_wmic_command('wmic os get InstallDate')
    info['os_manufacturer'] = run_wmic_command('wmic os get Manufacturer')
    
    # Computer System
    print("  [2/10] Computer System...")
    info['computer_manufacturer'] = run_wmic_command('wmic computersystem get Manufacturer')
    info['computer_model'] = run_wmic_command('wmic computersystem get Model')
    info['computer_domain'] = run_wmic_command('wmic computersystem get Domain')
    info['computer_username'] = run_wmic_command('wmic computersystem get UserName')
    
    # Memory
    print("  [3/10] Memory Information...")
    mem_output = run_wmic_command('wmic computersystem get TotalPhysicalMemory')
    if mem_output:
        try:
            memory_bytes = int(mem_output)
            info['total_memory_gb'] = round(memory_bytes / (1024**3), 2)
            info['total_memory_mb'] = round(memory_bytes / (1024**2), 2)
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    # CPU
    print("  [4/10] CPU Information...")
    info['cpu_name'] = run_wmic_command('wmic cpu get Name')
    info['cpu_cores'] = run_wmic_command('wmic cpu get NumberOfCores')
    info['cpu_logical_processors'] = run_wmic_command('wmic cpu get NumberOfLogicalProcessors')
    info['cpu_max_clock_speed'] = run_wmic_command('wmic cpu get MaxClockSpeed')
    
    # BIOS
    print("  [5/10] BIOS Information...")
    info['bios_manufacturer'] = run_wmic_command('wmic bios get Manufacturer')
    info['bios_version'] = run_wmic_command('wmic bios get Version')
    info['bios_release_date'] = run_wmic_command('wmic bios get ReleaseDate')
    
    # Disk
    print("  [6/10] Disk Information...")
    info['disk_model'] = run_wmic_command('wmic diskdrive get Model')
    info['disk_size'] = run_wmic_command('wmic diskdrive get Size')
    
    # Network
    print("  [7/10] Network Information...")
    info['network_adapter'] = run_wmic_command('wmic nic where NetEnabled=true get Name')
    
    # Graphics
    print("  [8/10] Graphics Information...")
    info['gpu_name'] = run_wmic_command('wmic path win32_VideoController get Name')
    info['gpu_driver_version'] = run_wmic_command('wmic path win32_VideoController get DriverVersion')
    
    # Windows Features
    print("  [9/10] Windows Features...")
    info['windows_directory'] = os.environ.get('WINDIR', 'C:\\Windows')
    info['program_files'] = os.environ.get('ProgramFiles', 'C:\\Program Files')
    info['program_files_x86'] = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
    info['user_profile'] = os.environ.get('USERPROFILE', '')
    info['temp_directory'] = os.environ.get('TEMP', '')
    
    # Python Environment
    print("  [10/10] Python Environment...")
    info['python_version'] = platform.python_version()
    info['python_implementation'] = platform.python_implementation()
    info['python_compiler'] = platform.python_compiler()
    
    return info

def update_database(db_path, info):
    """Update database with enhanced information"""
    print(f"\nUpdating database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        
        # Map info to categories
        categories = {
            'os_': 'system',
            'computer_': 'system',
            'cpu_': 'hardware',
            'total_memory': 'hardware',
            'bios_': 'hardware',
            'disk_': 'hardware',
            'gpu_': 'hardware',
            'network_': 'network',
            'windows_': 'paths',
            'program_': 'paths',
            'user_': 'paths',
            'temp_': 'paths',
            'python_': 'software',
        }
        
        count = 0
        for key, value in info.items():
            if value:  # Only add non-empty values
                # Determine category
                category = 'other'
                for prefix, cat in categories.items():
                    if key.startswith(prefix):
                        category = cat
                        break
                
                cursor.execute("""
                    INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """, (key, str(value), category))
                count += 1
                print(f"  [+] {key}: {str(value)[:50]}")
        
        conn.commit()
        conn.close()
        
        print(f"\n[SUCCESS] Added/updated {count} system information entries")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Failed to update database: {e}")
        return False

def main():
    print("=" * 70)
    print("  ENHANCE WINDOWS 10 PRO INFORMATION")
    print("=" * 70)
    print()
    
    # Find database
    import glob
    
    # Check for main database first
    if os.path.exists('jarvis_memory.db'):
        db_path = 'jarvis_memory.db'
        print(f"[INFO] Using main database: {db_path}")
    else:
        # Find most recent fixed database
        fixed_dbs = glob.glob('jarvis_memory.db.fixed-*')
        if fixed_dbs:
            fixed_dbs.sort(reverse=True)
            db_path = fixed_dbs[0]
            print(f"[INFO] Using fixed database: {db_path}")
        else:
            print("[ERROR] No database found!")
            print("Run: python fix_database_windows10.py first")
            return
    
    # Gather information
    print()
    info = get_enhanced_windows_info()
    
    # Update database
    print()
    if update_database(db_path, info):
        print("\n" + "=" * 70)
        print("  ENHANCEMENT COMPLETE!")
        print("  View results with: python view_database.py")
        print("=" * 70)
    else:
        print("\n[ERROR] Enhancement failed")

if __name__ == "__main__":
    main()
