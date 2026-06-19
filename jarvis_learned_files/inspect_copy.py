
from panda3d.core import Filename
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
import os

class Inspector(ShowBase):
    def __init__(self):
        super().__init__(windowType='none')
        # Check current dir and parent
        model_path = r"jarvis_face - Copy.glb"
        if not os.path.exists(model_path):
            model_path = os.path.join("..", model_path)
            
        if not os.path.exists(model_path):
            print(f"File not found: {model_path}")
            return
        
        print(f"Inspecting {model_path}...")
        
        try:
            actor = Actor(model_path)
            print(f"Actor loaded successfully.")
            actor.ls()
            # Try to see morphs
            char = actor.getPart("modelRoot")
            if char:
                print("Character found.")
        except Exception as e:
            print(f"Failed to load as Actor: {e}")
            
        print("Done.")
        os._exit(0)

if __name__ == "__main__":
    Inspector()
