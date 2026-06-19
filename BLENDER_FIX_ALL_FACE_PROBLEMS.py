"""
JARVIS 3D FACE MASTER FIXER - Blender Automation
================================================
Comprehensive script to fix all face problems in Blender

Features:
✓ Import GLB model
✓ Fix mesh topology
✓ Remove duplicate vertices
✓ Repair normals
✓ Add materials (white ceramic with cyan glow)
✓ Add shape keys for animations (MouthOpen, EyeBlink)
✓ Optimize geometry
✓ Add lighting setup
✓ Export clean GLB
"""

import bpy
import os
import sys

# Configuration
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(PROJECT_DIR, "jarvis_face.glb")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "jarvis_face_fixed.glb")

print("\n" + "="*70)
print("JARVIS 3D FACE MASTER FIXER - BLENDER AUTOMATION")
print("="*70 + "\n")

# ===== STEP 1: Clear Scene =====
print("[1/12] Clearing Blender scene...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Clear orphan data
for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)

for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)

print("✓ Scene cleared")

# ===== STEP 2: Import GLB =====
print(f"\n[2/12] Importing face model: {INPUT_FILE}")
if not os.path.exists(INPUT_FILE):
    print(f"ERROR: File not found: {INPUT_FILE}")
    sys.exit(1)

try:
    bpy.ops.import_scene.gltf(filepath=INPUT_FILE)
    print("✓ Face model imported successfully")
except Exception as e:
    print(f"ERROR: Import failed: {e}")
    sys.exit(1)

# Get the imported object
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

if not obj:
    print("ERROR: No mesh found after import")
    sys.exit(1)

print(f"✓ Found mesh object: {obj.name}")

# Select it
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# ===== STEP 3: Fix Mesh Topology =====
print(f"\n[3/12] Fixing mesh topology...")
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Remove duplicate vertices
bpy.ops.mesh.remove_doubles(threshold=0.0001)
print("✓ Removed duplicate vertices")

# Delete loose geometry
bpy.ops.mesh.delete_loose()
print("✓ Deleted loose geometry")

# Fill holes
bpy.ops.mesh.fill_holes(sides=4)
print("✓ Filled mesh holes")

# Recalculate normals
bpy.ops.mesh.normals_make_consistent(inside=False)
print("✓ Recalculated normals")

# Back to object mode
bpy.ops.object.mode_set(mode='OBJECT')
print("✓ Topology fixed")

# ===== STEP 4: Apply Smoothing =====
print(f"\n[4/12] Applying smoothing...")
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.object.mode_set(mode='OBJECT')

# Add Smooth modifier
smooth_mod = obj.modifiers.new(name="Smooth", type='SMOOTH')
smooth_mod.iterations = 2
bpy.ops.object.modifier_apply(modifier="Smooth")
print("✓ Smoothing applied")

# ===== STEP 5: Create White Ceramic Material =====
print(f"\n[5/12] Creating white ceramic material...")

# Remove existing materials
obj.data.materials.clear()

# Create material
mat = bpy.data.materials.new(name="JarvisSkin")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
nodes.clear()

# Create shader nodes
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
fresnel = nodes.new(type='ShaderNodeFresnel')
edge_ramp = nodes.new(type='ShaderNodeValToRGB')
emission = nodes.new(type='ShaderNodeEmission')
mix_shader = nodes.new(type='ShaderNodeMixShader')

# Configure BSDF for warm cyber skin
bsdf.inputs['Base Color'].default_value = (0.78, 0.64, 0.56, 1.0)
bsdf.inputs['Subsurface'].default_value = 0.13
bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.7, 0.55)
bsdf.inputs['Roughness'].default_value = 0.28
bsdf.inputs['Metallic'].default_value = 0.12
bsdf.inputs['Specular'].default_value = 0.55
bsdf.inputs['IOR'].default_value = 1.42

# Configure rim glow
fresnel.inputs['IOR'].default_value = 1.4
edge_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
edge_ramp.color_ramp.elements[1].color = (0.0, 0.5, 1.0, 1.0)
edge_ramp.inputs['Fac'].default_value = 0.65

emission.inputs['Color'].default_value = (0.0, 0.4, 1.0, 1.0)
emission.inputs['Strength'].default_value = 0.3

# Connect nodes
links.new(fresnel.outputs['Fac'], edge_ramp.inputs['Fac'])
links.new(edge_ramp.outputs['Color'], emission.inputs['Color'])
links.new(bsdf.outputs['BSDF'], mix_shader.inputs[1])
links.new(emission.outputs['Emission'], mix_shader.inputs[2])
links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

# Assign material and force all polygons to use it
obj.data.materials.clear()
obj.data.materials.append(mat)
for poly in obj.data.polygons:
    poly.material_index = 0
print("✓ Skin material created and assigned to all mesh faces")

# ===== STEP 6: Add Cyan Eye Lights =====
print(f"\n[6/12] Adding cyan eye glow lighting...")

# Add eye accent lights for beautiful glowing eyes
eye_locations = [(-0.16, 0.28, 0.24), (0.16, 0.28, 0.24)]
for index, loc in enumerate(eye_locations, start=1):
    bpy.ops.object.light_add(type='POINT', location=loc)
    light = bpy.context.active_object
    light.name = f"EyeGlowLight_{index}"
    light.data.energy = 40.0
    light.data.color = (0.0, 0.55, 1.0)
    light.data.shadow_soft_size = 0.2
    print(f"✓ Eye glow light {index} placed at {loc}")

# Add a soft blue fill light for the face
bpy.ops.object.light_add(type='AREA', location=(0, -1.2, 0.4), rotation=(1.3, 0, 0))
fill_eye = bpy.context.active_object
fill_eye.name = "BlueFillLight"
fill_eye.data.shape = 'RECTANGLE'
fill_eye.data.size = 1.5
fill_eye.data.size_y = 0.8
fill_eye.data.energy = 35.0
fill_eye.data.color = (0.0, 0.35, 1.0)
print("✓ Soft blue fill light added")

# Set world to dark blue for stronger contrast
if bpy.context.scene.world is None:
    bpy.context.scene.world = bpy.data.worlds.new("JarvisWorld")
world = bpy.context.scene.world
world.use_nodes = True
world.node_tree.nodes.clear()
bg = world.node_tree.nodes.new(type='ShaderNodeBackground')
bg.inputs['Color'].default_value = (0.02, 0.04, 0.1, 1.0)
world_output = world.node_tree.nodes.new(type='ShaderNodeOutputWorld')
world.node_tree.links.new(bg.outputs['Background'], world_output.inputs['Surface'])
print("✓ Dark blue world background set")

print("✓ Eye lighting and blue speaker style applied")

# ===== STEP 7: Add Shape Keys for Animation =====
print(f"\n[7/12] Adding shape keys for animation...")

# Create basis shape key
if not obj.data.shape_keys:
    obj.shape_key_add(name="Basis")
    print("✓ Created Basis shape key")

# Add MouthOpen shape key
mouth_key = obj.shape_key_add(name="MouthOpen")
mouth_key.value = 0.0
print("✓ Created MouthOpen shape key")

# Add EyeBlink shape key
blink_key = obj.shape_key_add(name="EyeBlink")
blink_key.value = 0.0
print("✓ Created EyeBlink shape key")

# Add HeadShake shape key
head_key = obj.shape_key_add(name="HeadShake")
head_key.value = 0.0
print("✓ Created HeadShake shape key")

# Create vertex groups for armature deformation
print(f"\n[8/12] Creating vertex groups for rigging...")
head_group = obj.vertex_groups.new(name="Head")
all_verts = [v.index for v in obj.data.vertices]
head_group.add(all_verts, 1.0, 'REPLACE')
print("✓ Assigned all vertices to Head vertex group")

# ===== STEP 9: Optimize Geometry =====
print(f"\n[9/12] Optimizing geometry...")

bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Dissolve limited faces (reduce complexity)
bpy.ops.mesh.dissolve_limited(angle_limit=1.0)

bpy.ops.object.mode_set(mode='OBJECT')
print("✓ Geometry optimized")

# ===== STEP 9: Add Armature (Skeleton) =====
print(f"\n[9/12] Adding armature for rigging...")

# Deselect all
bpy.ops.object.select_all(action='DESELECT')

# Add armature
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm_obj = bpy.context.active_object
arm_obj.name = "JARVIS_Armature"

# Create bones
bones = arm_obj.data.edit_bones

# Root bone (Neck)
root_bone = bones[0]
root_bone.name = "Neck"
root_bone.head = (0, 0, -0.3)
root_bone.tail = (0, 0, 0.1)

# Head bone
head_bone = bones.new("Head")
head_bone.parent = root_bone
head_bone.head = (0, 0, 0.1)
head_bone.tail = (0, 0, 0.5)

# Exit edit mode
bpy.ops.object.mode_set(mode='OBJECT')

# Add armature modifier to face
arm_mod = obj.modifiers.new(name="Armature", type='ARMATURE')
arm_mod.object = arm_obj
arm_mod.use_vertex_groups = True
print("✓ Armature with bones created")

# Create animation action for head and shape keys
print(f"\n[10/12] Creating face animation...")
if not arm_obj.animation_data:
    arm_obj.animation_data_create()
bone_action = bpy.data.actions.new(name="JarvisFaceBoneAction")
arm_obj.animation_data.action = bone_action

# Animate head bone rotation
head_bone_path = 'pose.bones["Head"].rotation_euler'
fcurves = []
for idx in range(3):
    fcurves.append(bone_action.fcurves.new(data_path=head_bone_path, index=idx))

# Set keyframes for a subtle head turn and nod
fcurves[2].keyframe_points.add(3)
fcurves[2].keyframe_points[0].co = (1, 0)
fcurves[2].keyframe_points[1].co = (20, 0.2)
fcurves[2].keyframe_points[2].co = (40, 0)
for fc in fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'SINE'

# Animate shape keys on the face object
if not obj.animation_data:
    obj.animation_data_create()
shape_action = bpy.data.actions.new(name="JarvisFaceShapeAction")
obj.animation_data.action = shape_action
mouth_fcurve = shape_action.fcurves.new(data_path='key_blocks["MouthOpen"].value')
eye_fcurve = shape_action.fcurves.new(data_path='key_blocks["EyeBlink"].value')
head_fcurve = shape_action.fcurves.new(data_path='key_blocks["HeadShake"].value')

mouth_fcurve.keyframe_points.add(5)
mouth_fcurve.keyframe_points[0].co = (1, 0)
mouth_fcurve.keyframe_points[1].co = (8, 1)
mouth_fcurve.keyframe_points[2].co = (14, 0.35)
mouth_fcurve.keyframe_points[3].co = (22, 0.9)
mouth_fcurve.keyframe_points[4].co = (30, 0.2)
mouth_fcurve.keyframe_points[5].co = (38, 0)

eye_fcurve.keyframe_points.add(4)
eye_fcurve.keyframe_points[0].co = (1, 0)
eye_fcurve.keyframe_points[1].co = (10, 1)
eye_fcurve.keyframe_points[2].co = (12, 0)
eye_fcurve.keyframe_points[3].co = (24, 0)

head_fcurve.keyframe_points.add(3)
head_fcurve.keyframe_points[0].co = (1, 0)
head_fcurve.keyframe_points[1].co = (20, 0.1)
head_fcurve.keyframe_points[2].co = (40, 0)

for fcurve in (mouth_fcurve, eye_fcurve, head_fcurve):
    for kp in fcurve.keyframe_points:
        kp.interpolation = 'BEZIER'

print("✓ Face animation created")

# ===== STEP 11: Setup Lighting =====
print(f"\n[11/12] Setting up lighting...")

# Add directional light
bpy.ops.object.light_add(type='SUN', location=(2, 2, 3))
sun = bpy.context.active_object
sun.data.energy = 2.0
sun.data.angle = 0.5
print("✓ Sun light added")

# Add fill light
bpy.ops.object.light_add(type='POINT', location=(-2, -1, 1.5))
fill = bpy.context.active_object
fill.data.energy = 0.5
fill.data.color = (0.5, 0.7, 1.0)
print("✓ Fill light added")

# ===== STEP 11: Scale and Position =====
print(f"\n[11/12] Positioning face...")

# Reset obj selection
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

# Scale to reasonable size
obj.scale = (1.5, 1.5, 1.5)

# Position
obj.location = (0, 0, 0)
obj.rotation_euler = (0, 0, 0)

print("✓ Face scaled and positioned")

# ===== STEP 12: Export GLB =====
print(f"\n[12/12] Exporting fixed face model...")
print(f"Output: {OUTPUT_FILE}")

try:
    bpy.ops.export_scene.gltf(
        filepath=OUTPUT_FILE,
        export_format='GLB',
        export_apply=True,
        export_animations=True,
        export_materials=True,
        export_original_specular=False
    )
    print("✓ Face exported successfully with animation!")
except Exception as e:
    print(f"ERROR: Export failed: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("✅ JARVIS 3D FACE FIXED AND OPTIMIZED!")
print("="*70)
print(f"\n✓ Output saved: {OUTPUT_FILE}")
print(f"✓ File size: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")
print("\nCompleted tasks:")
print("  ✓ Mesh topology fixed")
print("  ✓ Duplicate vertices removed")
print("  ✓ Normals recalculated")
print("  ✓ Smoothing applied")
print("  ✓ White ceramic material added")
print("  ✓ Cyan glow effects added")
print("  ✓ Shape keys for animation created")
print("  ✓ Geometry optimized")
print("  ✓ Armature skeleton added")
print("  ✓ Professional lighting setup")
print("  ✓ Face positioned and scaled")
print("\n✅ The 3D face is ready for use!\n")

# Exit Blender
bpy.ops.wm.quit_blender()
