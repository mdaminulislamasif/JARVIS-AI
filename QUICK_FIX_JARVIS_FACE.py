"""
Quick JARVIS Face 3D Fixer (No Blender Required)
=================================================
This script performs basic fixes on GLB files without requiring Blender.
For advanced fixes, use FIX_JARVIS_FACE_3D.py with Blender.

Features:
- Validates GLB file structure
- Checks file integrity
- Creates backup
- Provides diagnostic information
"""

import os
import sys
import shutil
import struct
import json
from pathlib import Path

def print_header():
    print("=" * 60)
    print("JARVIS Face 3D Quick Fixer")
    print("=" * 60)
    print()

def validate_glb_file(filepath):
    """Validate GLB file structure"""
    print(f"[1/5] Validating GLB file: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"  ✗ ERROR: File not found: {filepath}")
        return False
    
    file_size = os.path.getsize(filepath)
    print(f"  ✓ File exists (Size: {file_size:,} bytes)")
    
    if file_size == 0:
        print(f"  ✗ ERROR: File is empty (0 bytes)")
        return False
    
    if file_size < 100:
        print(f"  ✗ ERROR: File too small (likely corrupt)")
        return False
    
    # Read GLB header
    try:
        with open(filepath, 'rb') as f:
            # GLB header: magic (4 bytes), version (4 bytes), length (4 bytes)
            magic = f.read(4)
            version = struct.unpack('<I', f.read(4))[0]
            length = struct.unpack('<I', f.read(4))[0]
            
            if magic != b'glTF':
                print(f"  ✗ ERROR: Invalid GLB magic number: {magic}")
                return False
            
            print(f"  ✓ Valid GLB file (Version: {version}, Length: {length})")
            
            if version != 2:
                print(f"  ! WARNING: GLB version {version} (expected 2)")
            
            if length != file_size:
                print(f"  ! WARNING: Length mismatch (header: {length}, actual: {file_size})")
            
            return True
            
    except Exception as e:
        print(f"  ✗ ERROR: Failed to read GLB header: {e}")
        return False

def create_backup(filepath):
    """Create backup of original file"""
    print(f"\n[2/5] Creating backup...")
    
    backup_path = filepath + ".backup"
    
    try:
        shutil.copy2(filepath, backup_path)
        print(f"  ✓ Backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"  ✗ ERROR: Failed to create backup: {e}")
        return False

def analyze_glb_content(filepath):
    """Analyze GLB content"""
    print(f"\n[3/5] Analyzing GLB content...")
    
    try:
        with open(filepath, 'rb') as f:
            # Skip header (12 bytes)
            f.seek(12)
            
            # Read first chunk header
            chunk_length = struct.unpack('<I', f.read(4))[0]
            chunk_type = f.read(4)
            
            if chunk_type == b'JSON':
                print(f"  ✓ Found JSON chunk (Length: {chunk_length} bytes)")
                
                # Read JSON data
                json_data = f.read(chunk_length).decode('utf-8')
                gltf = json.loads(json_data)
                
                # Analyze content
                print(f"\n  GLB Content Analysis:")
                print(f"  - Asset version: {gltf.get('asset', {}).get('version', 'unknown')}")
                
                if 'meshes' in gltf:
                    print(f"  - Meshes: {len(gltf['meshes'])}")
                    for i, mesh in enumerate(gltf['meshes']):
                        print(f"    • Mesh {i}: {mesh.get('name', 'unnamed')}")
                
                if 'materials' in gltf:
                    print(f"  - Materials: {len(gltf['materials'])}")
                else:
                    print(f"  ! WARNING: No materials found")
                
                if 'textures' in gltf:
                    print(f"  - Textures: {len(gltf['textures'])}")
                
                if 'nodes' in gltf:
                    print(f"  - Nodes: {len(gltf['nodes'])}")
                
                if 'scenes' in gltf:
                    print(f"  - Scenes: {len(gltf['scenes'])}")
                
                return True
            else:
                print(f"  ✗ ERROR: Expected JSON chunk, got: {chunk_type}")
                return False
                
    except Exception as e:
        print(f"  ✗ ERROR: Failed to analyze GLB: {e}")
        return False

def check_jarvis_compatibility(filepath):
    """Check if GLB is compatible with JARVIS"""
    print(f"\n[4/5] Checking JARVIS compatibility...")
    
    issues = []
    warnings = []
    
    # Check file size
    file_size = os.path.getsize(filepath)
    if file_size > 10 * 1024 * 1024:  # 10 MB
        warnings.append(f"Large file size ({file_size / 1024 / 1024:.1f} MB) - may slow down JARVIS")
    
    # Check if jarvis_face.png exists
    png_path = Path(filepath).parent / "jarvis_face.png"
    if not png_path.exists():
        warnings.append(f"jarvis_face.png not found - JARVIS may show 'NO_FACE'")
    
    # Check JARVIS panel configuration
    panel_path = Path(filepath).parent / "jarvis_panel.py"
    if panel_path.exists():
        try:
            with open(panel_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'FACE_GLB_PATH' not in content:
                    issues.append("FACE_GLB_PATH not found in jarvis_panel.py")
                else:
                    print("  ✓ FACE_GLB_PATH found in jarvis_panel.py")
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    if issues:
        print("\n  Issues found:")
        for issue in issues:
            print(f"    ✗ {issue}")
    
    if warnings:
        print("\n  Warnings:")
        for warning in warnings:
            print(f"    ! {warning}")
    
    if not issues and not warnings:
        print("  ✓ No compatibility issues found")
    
    return len(issues) == 0

def provide_recommendations(filepath):
    """Provide recommendations"""
    print(f"\n[5/5] Recommendations:")
    
    print("\n  For best results:")
    print("  1. Use FIX_JARVIS_FACE_3D.py with Blender for complete fix")
    print("  2. Ensure jarvis_face.png exists in the same directory")
    print("  3. Keep GLB file size under 5 MB")
    print("  4. Use smooth shading and proper normals")
    print("  5. Add cyan/blue material for JARVIS theme")
    
    print("\n  Quick fixes you can try:")
    print("  • Run: FIX_JARVIS_FACE_3D.bat")
    print("  • Or manually fix in Blender (see JARVIS_FACE_3D_FIX_GUIDE_BANGLA.md)")
    
    print("\n  If JARVIS shows 'NO_FACE':")
    print("  • Check if jarvis_face.glb is in the correct directory")
    print("  • Check if jarvis_face.png exists")
    print("  • Restart JARVIS after replacing the file")

def main():
    print_header()
    
    # Get input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = input("Enter path to GLB file (or drag and drop): ").strip('"')
    
    if not input_file:
        # Try default location
        input_file = r"C:\Users\PHP\Documents\Untitled.glb"
        print(f"Using default location: {input_file}")
    
    print()
    
    # Validate file
    if not validate_glb_file(input_file):
        print("\n" + "=" * 60)
        print("VALIDATION FAILED")
        print("=" * 60)
        print("\nThe GLB file has issues. Please:")
        print("1. Check if the file is corrupt")
        print("2. Try re-exporting from Blender")
        print("3. Use FIX_JARVIS_FACE_3D.py for automatic fix")
        return
    
    # Create backup
    create_backup(input_file)
    
    # Analyze content
    analyze_glb_content(input_file)
    
    # Check compatibility
    is_compatible = check_jarvis_compatibility(input_file)
    
    # Provide recommendations
    provide_recommendations(input_file)
    
    # Summary
    print("\n" + "=" * 60)
    if is_compatible:
        print("ANALYSIS COMPLETE - File appears valid")
    else:
        print("ANALYSIS COMPLETE - Issues found")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Run FIX_JARVIS_FACE_3D.bat for automatic fix")
    print("2. Or manually fix in Blender")
    print("3. Copy fixed file to JARVIS directory as jarvis_face.glb")
    print("4. Restart JARVIS")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        print(f"\n\nERROR: {e}")
    finally:
        print()
        input("Press Enter to exit...")
