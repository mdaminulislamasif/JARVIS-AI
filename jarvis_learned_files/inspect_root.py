
from panda3d.core import Filename
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
import os

class Inspector(ShowBase):
    def __init__(self):
        super().__init__(windowType='none')
        model_path = r"c:\Users\PHP\Desktop\ai\jarvis_face.glb"
        if not os.path.exists(model_path):
            print(f"File not found: {model_path}")
            return
        
        print(f"Inspecting {model_path}...")
        
        try:
            actor = Actor(model_path)
            print(f"Actor loaded successfully.")
            # Check for character
            if actor.getPart("modelRoot"):
                print("Character data found.")
            else:
                print("No character data found.")
        except Exception as e:
            print(f"Failed to load as Actor: {e}")
            
        print("Done.")
        os._exit(0)

if __name__ == "__main__":
    Inspector()
