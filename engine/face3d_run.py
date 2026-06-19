
import math
import os
import sys
import time

# --- 1. SAFE IMPORTS ---
try:
    # pyrefly: ignore [missing-import]
    from panda3d.core import (
        AmbientLight, DirectionalLight, Filename, PointLight, 
        Vec4, NodePath, LColor, Shader, loadPrcFileData, 
        TransparencyAttrib, Character
    )
    from direct.showbase.ShowBase import ShowBase
    from direct.task import Task
    from direct.actor.Actor import Actor
    # GLTF support is automatic in panda3d-gltf
except ImportError as e:
    print(f"[!] CRITICAL: Missing libraries. Please run: pip install panda3d panda3d-gltf")
    print(f"Error detail: {e}")
    time.sleep(10)
    sys.exit(1)

# --- 2. LITE PERFORMANCE CONFIG ---
loadPrcFileData("", "window-title JARVIS Neural Face (FIXED)")
loadPrcFileData("", "win-size 600 600")
loadPrcFileData("", "win-origin -1 -1")
loadPrcFileData("", "undecorated 0")
loadPrcFileData("", "win-transparent 0")
loadPrcFileData("", "show-frame-rate-meter #t")
loadPrcFileData("", "sync-video 0") 
# loadPrcFileData("", "threading-model Cull/Draw") # REMOVED: Causes hangs on Intel

class FaceApp(ShowBase):
    def __init__(self, model_path: str, state_path: str):
        try:
            print("--- JARVIS RECOVERY BOOT ---")
            super().__init__()
            self.model_path = model_path
            self.state_path = state_path
            
            self.setBackgroundColor(0, 0, 0, 1)
            # gltf.patch_loader is not needed - panda3d-gltf works automatically
            
            # Load Model
            print(f">> Attempting to load: {model_path}")
            if not os.path.exists(model_path):
                print(f"[!] ERROR: Model not found at {model_path}")
                return

            # Use absolute path and convert to Panda3D format
            m_fn = Filename.fromOsSpecific(os.path.abspath(model_path))
            
            try:
                # Try loading as Actor first (for animations)
                self.face = Actor(m_fn.getFullpath())
                print("[OK] Actor loaded successfully.")
                
                # Bind joints for skeletal animation
                self.head_joint = self.face.control_joint(None, 'modelRoot', 'Head')
                self.eye_l_joint = self.face.control_joint(None, 'modelRoot', 'Eye_L')
                self.eye_r_joint = self.face.control_joint(None, 'modelRoot', 'Eye_R')
                self.eyelid_l_joint = self.face.control_joint(None, 'modelRoot', 'Eyelid_L')
                self.eyelid_r_joint = self.face.control_joint(None, 'modelRoot', 'Eyelid_R')
                self.jaw_joint = self.face.control_joint(None, 'modelRoot', 'Jaw')
                print("[OK] Skeleton joints controlled.")
            except Exception as actor_err:
                print(f"[!] Actor load failed: {actor_err}. Trying static model...")
                self.face = self.loader.loadModel(m_fn.getFullpath())
                self.head_joint = None
                self.eye_l_joint = None
                self.eye_r_joint = None
                self.eyelid_l_joint = None
                self.eyelid_r_joint = None
                self.jaw_joint = None
            
            self.face.reparentTo(self.render)
            self.face.setPos(0, 5.0, -0.6) # Balanced position
            self.face.setH(0)  # Use natural model orientation
            self.face.setScale(1.8)
            self.face.setTwoSided(True)  # Ensure face is visible even if normals are reversed
            
            # Setup Lights
            self._setup_lights()
            self.render.setShaderAuto() # Re-enabled now that mesh is optimized
            
            # Animation State
            self.current_state = "idle"
            self.last_state_check = 0
            self.mouth_val = 0.0
            self.blink_val = 0.0
            self.blink_timer = 0.0
            
            print("[ONLINE] JARVIS Face is now Online.")
            self.taskMgr.add(self._update, "update_task")
            
        except Exception as e:
            print(f"\n[!] STARTUP ERROR: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(30)
            sys.exit(1)

    def _setup_lights(self):
        # Warm Ambient Light
        al = AmbientLight("al")
        al.setColor(Vec4(0.4, 0.4, 0.45, 1))
        alnp = self.render.attachNewNode(al)
        self.render.setLight(alnp)

        # Front point light simulating warm studio key light
        self.pl = PointLight("pl")
        self.pl.setColor(Vec4(1.0, 0.95, 0.9, 1.0)) # Warm human skin tone lighting
        self.plnp = self.camera.attachNewNode(self.pl)
        self.plnp.setPos(0, -2, 2)
        self.render.setLight(self.plnp)
        
        # Rim light to highlight details
        rl = DirectionalLight("rl")
        rl.setColor(Vec4(0.2, 0.3, 0.4, 1.0)) # Cool fill/rim
        rlnp = self.render.attachNewNode(rl)
        rlnp.setHpr(180, -30, 0)
        self.render.setLight(rlnp)

    def _update_morphs(self, now, dt):
        if now - self.last_state_check > 0.1: # Check every 0.1s instead of 1.0s
            if os.path.exists(self.state_path):
                try:
                    with open(self.state_path, "r") as f:
                        self.current_state = f.read().strip().lower()
                except Exception as e:
                    print(f"⚠️ Error: {e}")
            self.last_state_check = now

        target_mouth = 0.0
        if self.current_state in ["talking", "speaking"]:
            # Oscillate mouth opening value for speaking animation
            target_mouth = 0.3 + math.sin(now * 14) * 0.7
            if target_mouth < 0:
                target_mouth = 0.0
        
        self.mouth_val += (target_mouth - self.mouth_val) * dt * 10
        
        self.blink_timer -= dt
        if self.blink_timer <= 0:
            if self.blink_val < 0.1:
                self.blink_val = 1.0
                self.blink_timer = 0.15 # Blink duration
            else:
                self.blink_val = 0.0
                self.blink_timer = 3.0 + math.sin(now) * 2.0 # Wait before next blink
        
        # Apply jaw movement (mouth open/close)
        if self.jaw_joint:
            # Shift jaw down based on mouth value
            self.jaw_joint.setPos(0, 0, -self.mouth_val * 0.08)
            
        # Apply eyelid movements (blinking)
        if self.eyelid_l_joint:
            self.eyelid_l_joint.setPos(0, 0, -self.blink_val * 0.06)
        if self.eyelid_r_joint:
            self.eyelid_r_joint.setPos(0, 0, -self.blink_val * 0.06)
            
        # Add random eye darting movements (looking around) to make it look alive!
        if self.eye_l_joint and self.eye_r_joint:
            eye_angle_y = math.sin(now * 0.5) * 8 # horizontal look
            eye_angle_x = math.cos(now * 0.3) * 4 # vertical look
            self.eye_l_joint.setHpr(eye_angle_y, eye_angle_x, 0)
            self.eye_r_joint.setHpr(eye_angle_y, eye_angle_x, 0)

    def _update(self, task):
        try:
            now = time.time()
            dt = self.clock.getDt()
            
            # Neck swaying/head tilting (natural movement)
            if self.head_joint:
                self.head_joint.setHpr(math.sin(now * 0.6) * 3, 
                                       math.cos(now * 0.4) * 2, 
                                       math.sin(now * 1.0) * 1.5)
            else:
                # Fallback for static model
                self.face.setHpr(math.sin(now * 0.6) * 2, 
                                 math.cos(now * 0.4) * 1.5, 
                                 math.sin(now * 1.0) * 1.0)
                                 
            self._update_morphs(now, dt)
            
        except Exception as e:
            print(f"Update loop error: {e}")
            
        return Task.cont

def main():
    _project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(_project_dir, "jarvis_face.glb")
    state_path = os.path.join(_project_dir, "jarvis_face.state")

    app = FaceApp(model_path, state_path)
    app.run()

if __name__ == "__main__":
    main()
