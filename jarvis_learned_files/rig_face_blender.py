import bpy
import os
import shutil

def apply_jarvis_perfection():
    # --- 1. STABILITY & ENGINE ---
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    
    # Clean existing Armatures to avoid duplicates
    for arm in bpy.data.armatures:
        bpy.data.armatures.remove(arm)

    # --- 2. SETUP PATHS ---
    input_path = r'c:\Users\PHP\Desktop\ai\jarvis_face.glb'
    
    # --- 3. FIND MESH ---
    obj = next((o for o in bpy.context.scene.objects if o.type == 'MESH'), None)
    if not obj:
        print("Error: No Mesh found!")
        return
    
    # Ensure mesh is active
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # --- 4. OPTIMIZE MESH (FIX LAG) ---
    print("Optimizing Mesh...")
    # Add Decimate to reduce poly count
    if "Optimize_Lag" not in obj.modifiers:
        dec_mod = obj.modifiers.new(name="Optimize_Lag", type='DECIMATE')
        dec_mod.ratio = 0.4 
        bpy.ops.object.modifier_apply(modifier="Optimize_Lag")
    
    # --- 5. ADD BONES (RIGGING) ---
    print("Adding Professional Skeleton (BONES)...")
    bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
    arm_obj = bpy.context.active_object
    arm_obj.name = "JARVIS_Rig"
    arm_data = arm_obj.data
    
    # Edit Bones
    bones = arm_data.edit_bones
    root_bone = bones[0]
    root_bone.name = "Neck"
    root_bone.head = (0, 0, -0.5)
    root_bone.tail = (0, 0, 0)
    
    head_bone = bones.new("Head")
    head_bone.head = (0, 0, 0)
    head_bone.tail = (0, 0, 0.8)
    head_bone.parent = root_bone
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Parent Mesh to Armature
    obj.select_set(True)
    arm_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    # --- 6. CREATE PERFORMANCE SHADER ---
    mat = bpy.data.materials.new(name="JARVIS_PRO_CORE")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1)
    bsdf.inputs['Roughness'].default_value = 0.1
    
    links.new(bsdf.outputs[0], output.inputs[0])
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # --- 7. EXPORT (SKELETAL VERSION) ---
    try:
        bpy.ops.export_scene.gltf(
            filepath=input_path, 
            export_format='GLB', 
            export_apply=True,
            export_morph=True,
            export_skins=True
        )
        print(f"SUCCESS: Skeletal Face (BONES) saved to {input_path}")
    except Exception as e:
        print(f"Export failed: {e}")

if __name__ == "__main__":
    apply_jarvis_perfection()
