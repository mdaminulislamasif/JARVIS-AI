import customtkinter as ctk
import psutil
import threading
import time
import math
import os

# --- ANTIGRAVITY HUD: PREMIUM NEURAL INTERFACE ---
class AntigravityHUD(ctk.CTkToplevel):
    def __init__(self, parent=None):
        if parent is None:
            super().__init__()
        else:
            super().__init__(parent)

        # Window Configuration
        self.title("ANTIGRAVITY NEURAL CORE")
        self.geometry("350x500+1550+50")  # Bottom right position
        self.overrideredirect(True)        # Borderless
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.9)
        self.configure(fg_color="#010306")

        # Neon Styles
        self.neon_cyan  = "#00FFFE"
        self.neon_green = "#00FF41"

        # Running flag — set False when window is destroyed to stop the thread
        self._running = True
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._setup_ui()
        self._start_telemetry()

    def _on_close(self):
        self._running = False
        self.destroy()

    def _setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(header, text="[ NEURAL LINK ]",
                     font=("Courier New", 14, "bold"),
                     text_color=self.neon_cyan).pack(side="left")
        ctk.CTkLabel(header, text="ONLINE",
                     font=("Courier New", 10),
                     text_color=self.neon_green).pack(side="right")

        # Wave Animation Canvas
        self.canvas = ctk.CTkCanvas(self, height=120,
                                    bg="#010306", highlightthickness=0)
        self.canvas.pack(fill="x", padx=10, pady=5)

        # Telemetry Frame
        self.telemetry = ctk.CTkFrame(self, fg_color="#05070A",
                                       border_width=1, border_color="#002233")
        self.telemetry.pack(fill="x", padx=10, pady=10)

        self.cpu_label = ctk.CTkLabel(self.telemetry, text="CPU: 0%",
                                       font=("Courier New", 12),
                                       text_color=self.neon_cyan)
        self.cpu_label.pack(anchor="w", padx=10, pady=5)

        self.ram_label = ctk.CTkLabel(self.telemetry, text="RAM: 0%",
                                       font=("Courier New", 12),
                                       text_color=self.neon_cyan)
        self.ram_label.pack(anchor="w", padx=10, pady=5)

        # Neural Log
        ctk.CTkLabel(self, text="[ ACTIVITY LOG ]",
                     font=("Courier New", 10, "bold"),
                     text_color="#555555").pack(pady=5)
        self.log_area = ctk.CTkTextbox(self, fg_color="#000000",
                                        font=("Courier New", 10),
                                        text_color="#00AA00", height=200)
        self.log_area.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_area.insert("end", "[*] Neural Core Initialized...\n")
        self.log_area.insert("end", "[+] Antigravity HUD Linked.\n")

    # ── Telemetry ─────────────────────────────────────────────────────────────
    def _start_telemetry(self):
        """Collect CPU/RAM and wave data in a background thread,
        then SAFELY push every update to the main Tkinter thread via after()."""
        def _collect():
            t = 0.0
            while self._running:
                try:
                    cpu  = psutil.cpu_percent(interval=None)
                    ram  = psutil.virtual_memory().percent

                    # Build wave point list (pure Python — no GUI calls)
                    points = []
                    for x in range(0, 330, 5):
                        y = (60
                             + math.sin(t + x * 0.05) * 20
                             + math.cos(t * 0.5 + x * 0.1) * 10)
                        points.extend([x, y])

                    # Schedule GUI update on the main thread
                    if self._running:
                        self.after(0, self._apply_update, cpu, ram, points)

                    t += 0.1
                    time.sleep(0.05)
                except Exception as e:
                    print(f"[HUD] Telemetry collect error: {e}")
                    time.sleep(1)

        threading.Thread(target=_collect, daemon=True, name="HUD-Telemetry").start()

    def _apply_update(self, cpu: float, ram: float, wave_points: list):
        """Called on the MAIN thread via after() — safe to touch any widget."""
        if not self._running:
            return
        try:
            self.cpu_label.configure(text=f"CPU: {cpu:.0f}%")
            self.ram_label.configure(text=f"RAM: {ram:.0f}%")

            self.canvas.delete("wave")
            if len(wave_points) >= 4:
                self.canvas.create_line(
                    wave_points,
                    fill=self.neon_cyan,
                    width=2,
                    tags="wave",
                    smooth=True,
                )
        except Exception:
            pass  # Window may have been destroyed

    # ── Public API ───────────────────────────────────────────────────────────
    def add_log(self, msg: str):
        """Thread-safe log append (can be called from any thread)."""
        self.after(0, self._append_log, msg)

    def _append_log(self, msg: str):
        try:
            self.log_area.insert("end", f"[*] {msg}\n")
            self.log_area.see("end")
        except Exception:
            pass


if __name__ == "__main__":
    app = AntigravityHUD()
    app.mainloop()
