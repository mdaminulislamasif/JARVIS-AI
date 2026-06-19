import bpy
import os
import math

def create_jarvis_face_from_scratch():
    export_path = r"c:\Users\asifg\OneDrive\Desktop\ai\jarvis_face.glb"
    
    # 1. Clear Scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # 2. Create Head Base using UV Sphere (best for head shape)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1.0,
        segments=32,
        ring_count=16,
        location=(0, 0, 0)
    )
    head = bpy.context.active_object
    head.name = "JARVIS_Head"
    
    # Scale to look more like a human head (taller than wide)
    head.scale = (0.9, 0.85, 1.1)
    bpy.ops.object.transform_apply(scale=True)
    
    # Apply smooth shading
    bpy.ops.object.shade_smooth()
    
    # 3. Skin-colored Material for Head
    skin_mat = bpy.data.materials.new(name="JARVIS_Skin")
    skin_mat.use_nodes = True
    nodes = skin_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    # Dark/warm skin tone (matches the real photo)
    bsdf.inputs['Base Color'].default_value = (0.35, 0.22, 0.15, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.6
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Subsurface Weight'].default_value = 0.15
    bsdf.inputs['Subsurface Radius'].default_value = (0.5, 0.2, 0.1)
    
    head.data.materials.append(skin_mat)
    
    # 4. Create EYES
    def make_eye(x_pos):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(x_pos, -0.78, 0.15))
        eye_white = bpy.context.active_object
        eye_white.name = "EyeWhite"
        
        eye_mat = bpy.data.materials.new(name="EyeWhite_Mat")
        eye_mat.use_nodes = True
        ew_bsdf = eye_mat.node_tree.nodes.get("Principled BSDF")
        ew_bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)
        ew_bsdf.inputs['Roughness'].default_value = 0.1
        eye_white.data.materials.append(eye_mat)
        
        # Pupil (dark)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(x_pos, -0.89, 0.15))
        pupil = bpy.context.active_object
        pupil.name = "Pupil"
        
        pupil_mat = bpy.data.materials.new(name="Pupil_Mat")
        pupil_mat.use_nodes = True
        p_nodes = pupil_mat.node_tree.nodes
        p_bsdf = p_nodes.get("Principled BSDF")
        p_bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
        pupil.data.materials.append(pupil_mat)
        
        return eye_white, pupil
    
    eye_l1, eye_l2 = make_eye(-0.3)
    eye_r1, eye_r2 = make_eye(0.3)
    
    # 5. Create EYEBROWS
    def make_eyebrow(x_pos, angle_deg):
        bpy.ops.mesh.primitive_cube_add(size=0.01, location=(x_pos, -0.85, 0.35))
        brow = bpy.context.active_object
        brow.name = "Eyebrow"
        brow.scale = (15, 1.5, 1.5)
        brow.rotation_euler = (0, 0, math.radians(angle_deg))
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        
        brow_mat = bpy.data.materials.new(name="Eyebrow_Mat")
        brow_mat.use_nodes = True
        br_bsdf = brow_mat.node_tree.nodes.get("Principled BSDF")
        br_bsdf.inputs['Base Color'].default_value = (0.02, 0.01, 0.005, 1.0)  # Very dark
        brow.data.materials.append(brow_mat)
        return brow
    
    brow_l = make_eyebrow(-0.3, 3)
    brow_r = make_eyebrow(0.3, -3)
    
    # 6. Create MASK (covers nose, mouth, chin area)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=32, ring_count=16, location=(0, 0, 0))
    mask_obj = bpy.context.active_object
    mask_obj.name = "JARVIS_Mask"
    mask_obj.scale = (0.905, 0.86, 1.105)
    bpy.ops.object.transform_apply(scale=True)
    
    # Delete vertices above nose (keep only bottom half)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for v in mask_obj.data.vertices:
        # Keep only front-facing, lower face region
        if v.co.z > 0.05 or v.co.y > 0.0:
            v.select = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.shade_smooth()
    
    # Matte Black Mask Material
    mask_mat = bpy.data.materials.new(name="JARVIS_Mask_Mat")
    mask_mat.use_nodes = True
    m_bsdf = mask_mat.node_tree.nodes.get("Principled BSDF")
    m_bsdf.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1.0)
    m_bsdf.inputs['Roughness'].default_value = 0.8
    m_bsdf.inputs['Metallic'].default_value = 0.0
    mask_obj.data.materials.append(mask_mat)
    
    # 7. Create EARPHONES (small cylinder in each ear)
    def make_earphone(x_pos):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.12, location=(x_pos, -0.05, 0.0))
        ear = bpy.context.active_object
        ear.name = "Earphone"
        ear.rotation_euler = (0, math.radians(90), 0)
        bpy.ops.object.transform_apply(rotation=True)
        
        ear_mat = bpy.data.materials.new(name="Earphone_Mat")
        ear_mat.use_nodes = True
        e_bsdf = ear_mat.node_tree.nodes.get("Principled BSDF")
        e_bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
        e_bsdf.inputs['Roughness'].default_value = 0.3
        e_bsdf.inputs['Metallic'].default_value = 0.7
        ear.data.materials.append(ear_mat)
        return ear
    
    ep_l = make_earphone(-1.0)
    ep_r = make_earphone(1.0)
    
    # 8. HAIR GEOMETRY (black hair on top of head)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.06, segments=16, ring_count=10, location=(0, 0, 0.25))
    hair = bpy.context.active_object
    hair.name = "JARVIS_Hair"
    hair.scale = (0.9, 0.85, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    
    # Delete lower portion to keep only the top
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for v in hair.data.vertices:
        if v.co.z < 0.2:
            v.select = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.shade_smooth()
    
    # Black hair material
    hair_mat = bpy.data.materials.new(name="JARVIS_Hair_Mat")
    hair_mat.use_nodes = True
    h_bsdf = hair_mat.node_tree.nodes.get("Principled BSDF")
    h_bsdf.inputs['Base Color'].default_value = (0.02, 0.01, 0.01, 1.0)
    h_bsdf.inputs['Roughness'].default_value = 0.7
    hair.data.materials.append(hair_mat)
    
    # 9. Shape Keys for Lip Sync / Blinking
    bpy.context.view_layer.objects.active = head
    head.select_set(True)
    # In Blender 4.x shape_keys lives on the data mesh, not the object
    if not head.data.shape_keys:
        head.shape_key_add(name="Basis")
    head.shape_key_add(name="MouthOpen")
    head.shape_key_add(name="EyeBlink")
    head.shape_key_add(name="Smile")
    
    # 10. Create simple armature for stability/bone control
    bpy.ops.object.armature_add(location=(0, 0, 0))
    arm = bpy.context.active_object
    arm.name = "JARVIS_Armature"
    
    # 11. Select all objects and parent to armature
    bpy.ops.object.select_all(action='DESELECT')
    for obj_name in ["JARVIS_Head", "JARVIS_Mask", "JARVIS_Hair"]:
        obj_ref = bpy.data.objects.get(obj_name)
        if obj_ref:
            obj_ref.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    try:
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    except Exception as pe:
        print(f"[WARN] Armature parent skipped: {pe}")
    
    # 12. Export as GLB
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        export_morph=True,
        export_skins=True,
        export_materials='EXPORT',
        export_apply=True
    )
    print(f"--- SUCCESS: JARVIS 3D MASKED FACE BUILT FROM SCRATCH -> {export_path} ---")

if __name__ == "__main__":
    create_jarvis_face_from_scratch()
