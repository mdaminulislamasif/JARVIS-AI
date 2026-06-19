## 3D Face (jarvis_face.glb)

If `jarvis_face.glb` exists in the project root, `jarvis_panel.py` will open a separate 3D window and drive it with states:
`idle`, `listening`, `thinking`, `speaking`.

### Install

Python deps:
- `panda3d`
- `panda3d-gltf`

Install:
`pip install panda3d panda3d-gltf`

### Notes

- If your `.glb` contains animations, the first animation will auto-loop.
- Even without mouth rigging, the face will “speak” via bob/scale/turn motions.
