"""
JARVIS Face 3D Fixer - Blender Automation Script
=================================================
This script fixes common issues in 3D face models (.glb files) using Blender.

Features:
- Fixes mesh topology issues
- Repairs normals
- Removes duplicate vertices
- Fixes UV mapping
- Optimizes geometry
- Adds proper materials
- Exports clean GLB file

Usage:
1. Install Blender (https://www.blender.org/download/)
2. Run: blender --background --python FIX_JARVIS_FACE_3D.py -- <input.glb> <output.glb>
   OR
3. Open Blender, go to Scripting tab, load this script, and run it
"""

import bpy
import os
import sys
import math

# Configuration
INPUT_FILE = os.path.join(os.environ.get('USERPROFILE', ''), 'Documents', 'Untitled.glb')
OUTPUT_FILE = "jarvis_face_fixed.glb"

def clear_scene():
    """Clear all objects from the scene"""
    print("[1/10] Clearing scene...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    
    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)
    
    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

def import_glb(filepath):
    """Import GLB file"""
    print(f"[2/10] Importing GLB file: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        return None
    
    try:
        bpy.ops.import_scene.gltf(filepath=filepath)
        print(f"✓ Successfully imported: {filepath}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to import GLB: {e}")
        return None

def fix_mesh_topology(obj):
    """Fix mesh topology issues"""
    print(f"[3/10] Fixing mesh topology for: {obj.name}")
    
    # Select the object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select all
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Remove doubles (merge vertices by distance)
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    print("  ✓ Removed duplicate vertices")
    
    # Delete loose vertices/edges
    bpy.ops.mesh.delete_loose()
    print("  ✓ Deleted loose geometry")
    
    # Fill holes
    bpy.ops.mesh.fill_holes(sides=0)
    print("  ✓ Filled holes")
    
    # Recalculate normals
    bpy.ops.mesh.normals_make_consistent(inside=False)
    print("  ✓ Recalculated normals")
    
    # Back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

def fix_normals(obj):
    """Fix normal issues"""
    print(f"[4/10] Fixing normals for: {obj.name}")
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Add smooth shading
    bpy.ops.object.shade_smooth()
    
    # Add edge split modifier for sharp edges
    if "EdgeSplit" not in [mod.name for mod in obj.modifiers]:
        edge_split = obj.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
        edge_split.split_angle = math.radians(30)
        print("  ✓ Added edge split modifier")
    
    print("  ✓ Applied smooth shading")

def optimize_geometry(obj):
    """Optimize mesh geometry"""
    print(f"[5/10] Optimizing geometry for: {obj.name}")
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Triangulate faces (better for game engines)
    bpy.ops.mesh.quads_convert_to_tris()
    print("  ✓ Triangulated mesh")
    
    # Back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Get face count
    face_count = len(obj.data.polygons)
    print(f"  ✓ Face count: {face_count}")

def fix_uv_mapping(obj):
    """Fix UV mapping"""
    print(f"[6/10] Fixing UV mapping for: {obj.name}")
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Check if UV map exists
    if not obj.data.uv_layers:
        print("  ! No UV map found, creating smart UV project...")
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
        bpy.ops.object.mode_set(mode='OBJECT')
        print("  ✓ Created UV map")
    else:
        print(f"  ✓ UV map exists: {obj.data.uv_layers[0].name}")

def add_materials(obj):
    """Add or fix materials"""
    print(f"[7/10] Adding/fixing materials for: {obj.name}")
    
    # Check if material exists
    if not obj.data.materials:
        print("  ! No material found, creating default material...")
        
        # Create new material
        mat = bpy.data.materials.new(name="JARVIS_Face_Material")
        mat.use_nodes = True
        
        # Get nodes
        nodes = mat.node_tree.nodes
        nodes.clear()
        
        # Add Principled BSDF
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        
        # Set base color (cyan/blue for JARVIS)
        bsdf.inputs['Base Color'].default_value = (0.0, 0.95, 1.0, 1.0)  # Cyan
        bsdf.inputs['Metallic'].default_value = 0.8
        bsdf.inputs['Roughness'].default_value = 0.2
        bsdf.inputs['Emission'].default_value = (0.0, 0.5, 0.6, 1.0)  # Glow
        bsdf.inputs['Emission Strength'].default_value = 0.5
        
        # Add Material Output
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        # Link nodes
        mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material to object
        obj.data.materials.append(mat)
        print("  ✓ Created JARVIS material with cyan glow")
    else:
        print(f"  ✓ Material exists: {obj.data.materials[0].name}")

def center_object(obj):
    """Center object to origin"""
    print(f"[8/10] Centering object: {obj.name}")
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Set origin to geometry center
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    
    # Move to world origin
    obj.location = (0, 0, 0)
    
    print("  ✓ Object centered")

def apply_modifiers(obj):
    """Apply all modifiers"""
    print(f"[9/10] Applying modifiers for: {obj.name}")
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Apply all modifiers
    for modifier in obj.modifiers:
        try:
            bpy.ops.object.modifier_apply(modifier=modifier.name)
            print(f"  ✓ Applied modifier: {modifier.name}")
        except Exception as e:
            print(f"  ! Could not apply modifier {modifier.name}: {e}")

def export_glb(filepath):
    """Export as GLB"""
    print(f"[10/10] Exporting GLB file: {filepath}")
    
    try:
        bpy.ops.export_scene.gltf(
            filepath=filepath,
            export_format='GLB',
            export_texcoords=True,
            export_normals=True,
            export_materials='EXPORT',
            export_colors=True,
            export_cameras=False,
            export_lights=False,
            export_apply=True
        )
        print(f"✓ Successfully exported: {filepath}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to export GLB: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("JARVIS Face 3D Fixer - Starting...")
    print("=" * 60)
    
    # Get input/output files from command line if provided
    input_file = INPUT_FILE
    output_file = OUTPUT_FILE
    
    # Check for command line arguments
    if "--" in sys.argv:
        args = sys.argv[sys.argv.index("--") + 1:]
        if len(args) >= 1:
            input_file = args[0]
        if len(args) >= 2:
            output_file = args[1]
    
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print()
    
    # Clear scene
    clear_scene()
    
    # Import GLB
    if not import_glb(input_file):
        print("FAILED: Could not import GLB file")
        return
    
    # Get all mesh objects
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    if not mesh_objects:
        print("ERROR: No mesh objects found in the scene")
        return
    
    print(f"\nFound {len(mesh_objects)} mesh object(s)")
    print()
    
    # Process each mesh object
    for obj in mesh_objects:
        print(f"\n--- Processing: {obj.name} ---")
        
        # Fix mesh topology
        fix_mesh_topology(obj)
        
        # Fix normals
        fix_normals(obj)
        
        # Optimize geometry
        optimize_geometry(obj)
        
        # Fix UV mapping
        fix_uv_mapping(obj)
        
        # Add materials
        add_materials(obj)
        
        # Center object
        center_object(obj)
        
        # Apply modifiers
        apply_modifiers(obj)
        
        print(f"--- Finished: {obj.name} ---\n")
    
    # Export GLB
    if export_glb(output_file):
        print("\n" + "=" * 60)
        print("SUCCESS! JARVIS Face 3D has been fixed!")
        print("=" * 60)
        print(f"Fixed file saved to: {output_file}")
        print("\nYou can now use this file in JARVIS panel.")
    else:
        print("\nFAILED: Could not export fixed GLB file")

if __name__ == "__main__":
    main()
