
import bpy
import os
import math

def setup_ultimate_jarvis_face():
    # 1. Paths
    import_path = r"c:\Users\PHP\Desktop\ai\jarvis_learned_files\human_head.glb"
    export_path = r"c:\Users\PHP\Desktop\ai\jarvis_face.glb"
    
    # 2. Clear Scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # 3. Import Head Model
    if os.path.exists(import_path):
        bpy.ops.import_scene.gltf(filepath=import_path)
    else:
        bpy.ops.mesh.primitive_monkey_add(size=1.0)
        
    obj = bpy.context.active_object
    obj.name = "JARVIS_Face"
    
    # 4. Premium Material: White Ceramic + Subsurface
    mat = bpy.data.materials.new(name="JARVIS_Ceramic")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    # White Ceramic Look
    bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.02
    bsdf.inputs['Metallic'].default_value = 0.1
    # Subsurface Scattering for "Soft Ceramic" feel
    bsdf.inputs['Subsurface Weight'].default_value = 0.2
    bsdf.inputs['Subsurface Radius'].default_value = (0.1, 0.1, 0.1)
    
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # 5. Neon Wireframe Overlay (Holographic Effect)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.duplicate()
    glow = bpy.context.active_object
    glow.name = "JARVIS_Glow_Overlay"
    glow.scale *= 1.003 # Slightly larger
    
    # Holographic Material
    glow_mat = bpy.data.materials.new(name="Neon_Blue_Hologram")
    glow_mat.use_nodes = True
    g_nodes = glow_mat.node_tree.nodes
    g_nodes.clear()
    
    # Emission + Transparent mix
    output = g_nodes.new('ShaderNodeOutputMaterial')
    emission = g_nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (0.0, 0.8, 1.0, 1.0) # Neon Blue
    emission.inputs['Strength'].default_value = 15.0
    
    # Link
    glow_mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    
    # Wireframe Modifier
    wire = glow.modifiers.new(name="Wireframe", type='WIREFRAME')
    wire.thickness = 0.0015
    wire.use_replace = True
    
    glow.data.materials[0] = glow_mat

    # 6. Advanced Shape Keys (Lip Sync & Blinking)
    # Ensure we work on the main face object
    bpy.context.view_layer.objects.active = obj
    
    if not obj.shape_keys:
        obj.shape_key_add(name="Basis")
    
    # MouthOpen (More controlled)
    if "MouthOpen" not in obj.shape_keys.key_blocks:
        key = obj.shape_key_add(name="MouthOpen")
        # Identify mouth vertices (usually around the center bottom of the head)
        # We'll use a weight based on proximity to a "mouth point"
        for v in key.data:
            # Simple heuristic: lower middle part of the face
            # Assuming Y is forward, Z is up, X is sideways
            dist_x = abs(v.co.x)
            dist_z = abs(v.co.z + 0.3) # Offset Z to center on mouth
            if dist_x < 0.3 and v.co.z < 0.0 and v.co.z > -0.8:
                # Falloff weight
                weight = (1.0 - dist_x/0.3) * (1.0 - dist_z/0.5)
                v.co.z -= 0.15 * max(0, weight)

    # EyeBlink
    if "EyeBlink" not in obj.shape_keys.key_blocks:
        key = obj.shape_key_add(name="EyeBlink")
        for v in key.data:
            # Heuristic for eyes
            if abs(v.co.x) > 0.1 and abs(v.co.x) < 0.5 and v.co.z > 0.0 and v.co.z < 0.4:
                v.co.z -= 0.05 # Close eyes
                
    # Smile
    if "Smile" not in obj.shape_keys.key_blocks:
        key = obj.shape_key_add(name="Smile")
        for v in key.data:
            if abs(v.co.x) > 0.2 and abs(v.co.x) < 0.5 and v.co.z < 0.0 and v.co.z > -0.4:
                v.co.z += 0.05
                v.co.x += 0.02 if v.co.x > 0 else -0.02

    # 7. Rigging (Basic Bone for stability)
    bpy.ops.object.armature_add(location=(0, 0, 0))
    arm = bpy.context.active_object
    arm.name = "JARVIS_Skeleton"
    
    obj.select_set(True)
    glow.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    # 8. Export with everything
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        export_morph=True,
        export_skins=True,
        export_materials='EXPORT',
        export_apply=True
    )
    print(f"--- SUCCESS: JARVIS PREMIUM FACE CREATED AT {export_path} ---")

if __name__ == "__main__":
    setup_ultimate_jarvis_face()
