
import trimesh
import numpy as np
import os

def create_jarvis_procedural():
    print("Generating JARVIS Face Mesh...")
    
    # 1. Create a sphere and squash it into a mask shape
    mesh = trimesh.creation.uv_sphere(radius=0.5, count=[32, 32])
    
    # Squash Y axis to make it a mask
    mesh.vertices[:, 1] *= 0.4
    # Slightly elongate Z axis for head shape
    mesh.vertices[:, 2] *= 1.2
    
    # 2. Add "MouthOpen" Morph Target (Shape Key)
    # Target: move bottom vertices down
    target_vertices = mesh.vertices.copy()
    min_z = target_vertices[:, 2].min()
    mask = target_vertices[:, 2] < (min_z + 0.3)
    target_vertices[mask, 2] -= 0.1
    target_vertices[mask, 1] += 0.05
    
    # 3. Apply Materials (White Base + Blue Tint)
    mesh.visual = trimesh.visual.ColorVisuals(
        vertex_colors=np.full((len(mesh.vertices), 4), [255, 255, 255, 255])
    )
    
    # 4. Export to GLB
    save_path = r"c:\Users\PHP\Desktop\ai\jarvis_learned_files\jarvis_face.glb"
    mesh.export(save_path)
    print(f"SUCCESS! New JARVIS Face created at: {save_path}")

if __name__ == "__main__":
    create_jarvis_procedural()
