"""
Face3D controller — launches face3d_run.py as a subprocess and drives it
via a tiny state file.  The subprocess must run from the project root so
that `engine.face3d_run` resolves correctly as a module.
"""
import os
import subprocess
import sys
from typing import Optional


class Face3D:
    """
    Starts a separate Panda3D process (Panda3D must run in main thread).
    The panel writes a tiny state file to drive: idle / listening / thinking / speaking.
    """

    VALID_STATES = {"idle", "listening", "thinking", "speaking"}

    def __init__(self, glb_path: str, state_path: Optional[str] = None):
        self.glb_path = os.path.abspath(glb_path)
        # Project root = parent of the engine/ folder
        self._project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.state_path = state_path or os.path.join(self._project_root, "jarvis_face.state")
        self._proc: Optional[subprocess.Popen] = None

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start the face renderer subprocess (no-op if already running)."""
        if self.is_running():
            return
        if not os.path.exists(self.glb_path):
            raise FileNotFoundError(f"Face model not found: {self.glb_path}")

        # Write initial state before starting process
        try:
            with open(self.state_path, "w", encoding="utf-8") as f:
                f.write("idle")
        except Exception as e:
            print(f"[FACE3D] Could not write initial state file: {e}")
        
        self._proc = subprocess.Popen(
            [sys.executable, "-m", "engine.face3d_run"],
            cwd=self._project_root,          # must be project root for module resolution
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"[FACE3D] Started (PID {self._proc.pid})")

    def stop(self) -> None:
        """Terminate the face renderer subprocess."""
        proc = self._proc
        self._proc = None
        if not proc:
            return
        try:
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=3)
        except Exception:
            try:
                proc.kill()
            except Exception:
                print("⚠️ Error occurred but was silently ignored")
        print("[FACE3D] Stopped")

    def restart(self) -> None:
        """Stop then start — useful if the subprocess crashed."""
        self.stop()
        self.start()

    def is_running(self) -> bool:
        return bool(self._proc and self._proc.poll() is None)

    # ── State control ─────────────────────────────────────────────────────────

    def set_state(self, state: str) -> None:
        """Write the animation state to the shared state file."""
        s = (state or "idle").strip().lower()
        if s not in self.VALID_STATES:
            s = "idle"
        # Auto-restart if the subprocess died unexpectedly (but avoid recursion)
        if self._proc and self._proc.poll() is not None:
            print(f"[FACE3D] Subprocess exited unexpectedly — restarting...")
            self._proc = None  # Clear the dead process
            # Write state file first, then restart
            try:
                with open(self.state_path, "w", encoding="utf-8") as f:
                    f.write(s)
            except Exception as e:
                print(f"[FACE3D] Could not write state file: {e}")
            self.start()
            return
        try:
            with open(self.state_path, "w", encoding="utf-8") as f:
                f.write(s)
        except Exception as e:
            print(f"[FACE3D] Could not write state file: {e}")
