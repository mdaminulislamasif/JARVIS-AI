import bpy
import os

# --- PROFESSIONAL BLENDER IMPROVEMENT SCRIPT ---
def improve_jarvis_face(input_path, output_path):
    # Clear existing scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # 1. Import the GLB model
    bpy.ops.import_scene.gltf(filepath=input_path)
    
    # Find the face object
    obj = None
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            obj = o
            break
            
    if not obj:
        print("ERROR: No mesh found in GLB!")
        return

    bpy.context.view_layer.objects.active = obj
    
    # 2. Smooth the Mesh (Subdivision Surface)
    mod = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    mod.levels = 1
    mod.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    # 3. Setup Basic Shape Keys for Animation
    if not obj.data.shape_keys:
        obj.shape_key_add(name="Basis")
    
    # Create MouthOpen Shape Key
    sk_mouth = obj.shape_key_add(name="MouthOpen")
    # Simulate mouth opening by pulling lower vertices down (approximation)
    for v in sk_mouth.data:
        # If vertex is in the lower jaw area (rough estimate based on coordinates)
        if v.co.z < -0.2 and abs(v.co.x) < 0.3:
            v.co.z -= 0.15 
            v.co.y += 0.05
            
    # Create EyeBlink Shape Key
    sk_blink = obj.shape_key_add(name="EyeBlink")
    for v in sk_blink.data:
        # If vertex is in eye area
        if v.co.z > 0.25 and v.co.z < 0.4 and abs(v.co.x) > 0.2:
            v.co.z -= 0.1 # Close eyes
            
    # 4. Export the Improved Model
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB', export_apply=True)
    print(f"SUCCESS: Improved model saved to {output_path}")

# Run the process
input_file = r"c:\Users\PHP\Desktop\ai\jarvis_face.glb"
output_file = r"c:\Users\PHP\Desktop\ai\jarvis_face_pro.glb"
improve_jarvis_face(input_file, output_file)
