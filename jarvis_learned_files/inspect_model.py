
from panda3d.core import Filename
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
import os

class Inspector(ShowBase):
    def __init__(self):
        super().__init__(windowType='none')
        # Use absolute path for model
        model_path = r"c:\Users\PHP\Desktop\ai\jarvis_face.glb"
        if not os.path.exists(model_path):
            print(f"File not found: {model_path}")
            return
        
        print(f"Inspecting {model_path}...")
        
        # Try to load as Actor to see animations
        try:
            actor = Actor(model_path)
            anims = actor.getAnimNames()
            print(f"Animations found: {anims}")
        except Exception as e:
            print(f"Failed to load as Actor: {e}")
            
        # Inspect scene graph
        model = self.loader.loadModel(Filename.fromOsSpecific(model_path))
        model.ls()
        
        print("Done.")
        os._exit(0)

if __name__ == "__main__":
    Inspector()
