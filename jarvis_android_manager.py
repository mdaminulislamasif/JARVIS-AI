#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS ANDROID DEVICE MANAGER
================================
ADB দিয়ে Android phone connect, screen mirror, control সব কিছু
"""

import os
import sys
import threading
import subprocess
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox
import time

_BASE = os.path.dirname(os.path.abspath(__file__))

# ADB paths to check
ADB_PATHS = [
    "adb",
    r"C:\Program Files (x86)\Android\android-sdk\platform-tools\adb.exe",
    r"C:\Users\{}\AppData\Local\Android\Sdk\platform-tools\adb.exe".format(os.environ.get("USERNAME", "")),
    r"C:\Android\platform-tools\adb.exe",
    os.path.join(_BASE, "platform-tools", "adb.exe"),
    os.path.join(_BASE, "adb.exe"),
]

def find_adb():
    """Find ADB executable"""
    for path in ADB_PATHS:
        try:
            result = subprocess.run([path, "version"],
                                    capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                return path
        except Exception:
            continue
    return None

def run_adb(cmd_args, adb_path="adb", timeout=10):
    """Run ADB command and return output"""
    try:
        result = subprocess.run(
            [adb_path] + cmd_args,
            capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1
    except Exception as e:
        return "", str(e), -1


class AndroidManager(ctk.CTkToplevel):
    def __init__(self, master=None, brain=None):
        super().__init__(master)
        self.brain = brain
        self.adb_path = None
        self.connected_device = None
        self.mirror_process = None

        self.title("JARVIS ANDROID DEVICE MANAGER")
        self.geometry("900x650")
        self.configure(fg_color="#02050A")
        ctk.set_appearance_mode("dark")
        self.attributes("-topmost", True)

        self._build_ui()
        threading.Thread(target=self._init_adb, daemon=True).start()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#05080F",
                               border_width=1, border_color="#003344")
        header.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(header, text="📱 ANDROID DEVICE MANAGER",
                     font=("Courier New", 18, "bold"),
                     text_color="#00F3FF").pack(side="left", padx=20, pady=10)

        self.status_label = ctk.CTkLabel(header,
                                          text="⏳ Checking ADB...",
                                          font=("Courier New", 11),
                                          text_color="#FFD700")
        self.status_label.pack(side="right", padx=20)

        # ADB Status + Install
        adb_frame = ctk.CTkFrame(self, fg_color="#030810",
                                  border_width=1, border_color="#002233")
        adb_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(adb_frame, text="[ ADB STATUS ]",
                     font=("Courier New", 10, "bold"),
                     text_color="#00FF41").pack(anchor="w", padx=10, pady=5)

        adb_btn_frame = ctk.CTkFrame(adb_frame, fg_color="transparent")
        adb_btn_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(adb_btn_frame, text="⬇ INSTALL ADB",
                      width=150, height=35,
                      fg_color="#003355", hover_color="#005577",
                      font=("Courier New", 11, "bold"),
                      command=self._install_adb).pack(side="left", padx=5)

        ctk.CTkButton(adb_btn_frame, text="🔍 FIND ADB",
                      width=120, height=35,
                      fg_color="#003333",
                      command=self._browse_adb).pack(side="left", padx=5)

        ctk.CTkButton(adb_btn_frame, text="🔄 REFRESH DEVICES",
                      width=150, height=35,
                      fg_color="#004400",
                      command=self._refresh_devices).pack(side="left", padx=5)

        self.adb_status_text = ctk.CTkLabel(adb_btn_frame,
                                             text="ADB: Not found",
                                             font=("Courier New", 11),
                                             text_color="#FF3131")
        self.adb_status_text.pack(side="left", padx=15)

        # Device list
        dev_frame = ctk.CTkFrame(self, fg_color="#030810",
                                  border_width=1, border_color="#002233")
        dev_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(dev_frame, text="[ CONNECTED DEVICES ]",
                     font=("Courier New", 10, "bold"),
                     text_color="#00FF41").pack(anchor="w", padx=10, pady=5)

        self.device_list = ctk.CTkTextbox(dev_frame, height=80,
                                           font=("Consolas", 11),
                                           fg_color="#030810",
                                           text_color="#00F3FF",
                                           border_width=0)
        self.device_list.pack(fill="x", padx=5, pady=5)

        # Actions
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=15, pady=5)

        # Row 1
        row1 = ctk.CTkFrame(actions, fg_color="transparent")
        row1.pack(fill="x", pady=3)

        btns_row1 = [
            ("📺 SCREEN MIRROR", self._screen_mirror, "#003355"),
            ("📸 SCREENSHOT", self._take_screenshot, "#004400"),
            ("🔊 DEVICE INFO", self._device_info, "#004433"),
            ("📁 FILE BROWSER", self._file_browser, "#334400"),
            ("🔋 BATTERY", self._battery_info, "#440033"),
        ]
        for text, cmd, color in btns_row1:
            ctk.CTkButton(row1, text=text, width=140, height=38,
                          fg_color=color, hover_color=self._lighten(color),
                          font=("Courier New", 10, "bold"),
                          command=cmd).pack(side="left", padx=3)

        # Row 2
        row2 = ctk.CTkFrame(actions, fg_color="transparent")
        row2.pack(fill="x", pady=3)

        btns_row2 = [
            ("📲 INSTALL APK", self._install_apk, "#440044"),
            ("🔤 TYPE TEXT", self._type_text, "#004444"),
            ("📋 COPY SCREEN", self._copy_screen_text, "#444400"),
            ("🔌 CONNECT WIFI", self._connect_wifi, "#003344"),
            ("⛔ STOP MIRROR", self._stop_mirror, "#440000"),
        ]
        for text, cmd, color in btns_row2:
            ctk.CTkButton(row2, text=text, width=140, height=38,
                          fg_color=color, hover_color=self._lighten(color),
                          font=("Courier New", 10, "bold"),
                          command=cmd).pack(side="left", padx=3)

        # Quick commands
        cmd_frame = ctk.CTkFrame(self, fg_color="transparent")
        cmd_frame.pack(fill="x", padx=15, pady=5)

        self.cmd_entry = ctk.CTkEntry(cmd_frame,
                                       placeholder_text="ADB command (e.g: shell pm list packages)",
                                       height=38, fg_color="#000000",
                                       border_color="#003344",
                                       font=("Consolas", 12))
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.cmd_entry.bind("<Return>", lambda e: self._run_custom_cmd())

        ctk.CTkButton(cmd_frame, text="RUN", width=80, height=38,
                      fg_color="#004466",
                      command=self._run_custom_cmd).pack(side="left")

        # Output terminal
        out_frame = ctk.CTkFrame(self, fg_color="#000000",
                                  border_width=1, border_color="#002233")
        out_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        ctk.CTkLabel(out_frame, text="[ OUTPUT ]",
                     font=("Courier New", 10, "bold"),
                     text_color="#FF3131").pack(anchor="w", padx=10, pady=3)

        self.output = ctk.CTkTextbox(out_frame,
                                      font=("Consolas", 11),
                                      fg_color="#000000",
                                      text_color="#00FF41",
                                      border_width=0)
        self.output.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def _init_adb(self):
        self.adb_path = find_adb()
        if self.adb_path:
            out, _, _ = run_adb(["version"], self.adb_path)
            version = out.split("\n")[0] if out else "Found"
            self.after(0, lambda: self.adb_status_text.configure(
                text=f"✅ ADB: {version[:30]}", text_color="#00FF41"))
            self.after(0, lambda: self.status_label.configure(
                text="✅ ADB Ready", text_color="#00FF41"))
            self._log(f"✅ ADB found: {self.adb_path}\n")
            self._refresh_devices()
        else:
            self.after(0, lambda: self.adb_status_text.configure(
                text="❌ ADB: Not found — Click INSTALL ADB",
                text_color="#FF3131"))
            self.after(0, lambda: self.status_label.configure(
                text="❌ ADB not installed", text_color="#FF3131"))
            self._log(
                "❌ ADB not found!\n\n"
                "📌 ADB install করুন:\n"
                "   1. Click '⬇ INSTALL ADB' button\n"
                "   2. অথবা manually install করুন:\n"
                "      https://developer.android.com/studio/releases/platform-tools\n\n"
                "📱 Phone setup:\n"
                "   1. Settings → About Phone → Build Number (7 বার tap)\n"
                "   2. Developer Options → USB Debugging ON\n"
                "   3. USB দিয়ে PC connect করুন\n"
            )

    def _install_adb(self):
        self._log("\n⬇ ADB download করা হচ্ছে...\n")

        def _do_install():
            try:
                # Download platform-tools
                import urllib.request
                import zipfile

                url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
                dest_zip = os.path.join(_BASE, "platform-tools.zip")
                dest_dir = _BASE

                self.after(0, lambda: self._log("⬇ Downloading platform-tools...\n"))
                urllib.request.urlretrieve(url, dest_zip)

                self.after(0, lambda: self._log("📦 Extracting...\n"))
                with zipfile.ZipFile(dest_zip, 'r') as z:
                    z.extractall(dest_dir)

                os.remove(dest_zip)

                new_adb = os.path.join(_BASE, "platform-tools", "adb.exe")
                if os.path.exists(new_adb):
                    self.adb_path = new_adb
                    self.after(0, lambda: self._log(
                        f"✅ ADB installed: {new_adb}\n\n"
                        "📱 Phone connect করুন USB দিয়ে\n"
                        "তারপর REFRESH DEVICES click করুন\n"))
                    self.after(0, lambda: self.adb_status_text.configure(
                        text="✅ ADB: Installed", text_color="#00FF41"))
                    self._refresh_devices()
                else:
                    self.after(0, lambda: self._log("❌ Install failed\n"))

            except Exception as e:
                self.after(0, lambda err=str(e):
                           self._log(f"❌ Install error: {err}\n\n"
                                     "Manual install: https://developer.android.com/studio/releases/platform-tools\n"))
                # Open download page
                webbrowser.open("https://developer.android.com/studio/releases/platform-tools")

        threading.Thread(target=_do_install, daemon=True).start()

    def _browse_adb(self):
        path = filedialog.askopenfilename(
            title="Select adb.exe",
            filetypes=[("ADB", "adb.exe"), ("All", "*.*")]
        )
        if path:
            self.adb_path = path
            self.adb_status_text.configure(
                text=f"✅ ADB: Custom path", text_color="#00FF41")
            self._log(f"✅ ADB set to: {path}\n")
            self._refresh_devices()

    def _refresh_devices(self):
        if not self.adb_path:
            self._log("❌ ADB not found. Install first.\n")
            return

        def _check():
            out, err, code = run_adb(["devices", "-l"], self.adb_path)
            self.after(0, lambda: self.device_list.delete("1.0", "end"))

            if out:
                lines = out.strip().split("\n")
                devices = [l for l in lines[1:] if l.strip() and "List" not in l]

                if not devices:
                    self.after(0, lambda: self.device_list.insert("end",
                        "❌ কোনো device connected নেই\n"
                        "📱 USB দিয়ে phone connect করুন\n"
                        "   Developer Options → USB Debugging ON করুন"))
                    self.connected_device = None
                else:
                    self.connected_device = devices[0].split()[0]
                    text = f"✅ {len(devices)} device(s) connected:\n"
                    for d in devices:
                        text += f"  📱 {d}\n"
                    self.after(0, lambda t=text: self.device_list.insert("end", t))
                    self.after(0, lambda: self.status_label.configure(
                        text=f"✅ {len(devices)} device connected",
                        text_color="#00FF41"))
            else:
                self.after(0, lambda: self.device_list.insert("end",
                    "❌ ADB devices error. Phone connected?"))

        threading.Thread(target=_check, daemon=True).start()

    def _screen_mirror(self):
        """Mirror Android screen using scrcpy"""
        self._log("\n📺 Screen mirror শুরু করছি...\n")

        def _run():
            # Check scrcpy
            try:
                result = subprocess.run(["scrcpy", "--version"],
                                        capture_output=True, timeout=3)
                if result.returncode == 0:
                    self.after(0, lambda: self._log("✅ scrcpy found! Starting mirror...\n"))
                    self.mirror_process = subprocess.Popen(
                        ["scrcpy", "--window-title", "JARVIS Android Mirror",
                         "--max-fps", "30", "--bit-rate", "4M"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    return
            except Exception:
                pass

            # scrcpy নেই — install guide
            self.after(0, lambda: self._log(
                "❌ scrcpy not installed!\n\n"
                "📥 Install করুন:\n"
                "  1. Winget: winget install Genymobile.scrcpy\n"
                "  2. অথবা: https://github.com/Genymobile/scrcpy/releases\n\n"
                "📱 যখন install হবে, SCREEN MIRROR আবার click করুন\n"
            ))

            # Try to install via winget
            try:
                self.after(0, lambda: self._log("⚙ winget দিয়ে install করার চেষ্টা...\n"))
                result = subprocess.run(
                    ["winget", "install", "Genymobile.scrcpy", "-e", "--silent"],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0:
                    self.after(0, lambda: self._log("✅ scrcpy installed! SCREEN MIRROR আবার click করুন\n"))
                else:
                    webbrowser.open("https://github.com/Genymobile/scrcpy/releases")
            except Exception as e:
                webbrowser.open("https://github.com/Genymobile/scrcpy/releases")

        threading.Thread(target=_run, daemon=True).start()

    def _stop_mirror(self):
        if self.mirror_process:
            self.mirror_process.terminate()
            self.mirror_process = None
            self._log("⛔ Screen mirror stopped\n")
        else:
            self._log("ℹ No active mirror\n")

    def _take_screenshot(self):
        if not self.adb_path or not self.connected_device:
            self._log("❌ Device connected নেই\n")
            return

        def _run():
            out, err, code = run_adb(["-s", self.connected_device,
                                       "shell", "screencap", "-p",
                                       "/sdcard/jarvis_screenshot.png"],
                                      self.adb_path)
            if code == 0:
                # Pull to PC
                dest = os.path.join(_BASE, "jarvis_uploads",
                                    f"android_screen_{int(time.time())}.png")
                out2, err2, code2 = run_adb(["-s", self.connected_device,
                                              "pull",
                                              "/sdcard/jarvis_screenshot.png",
                                              dest],
                                             self.adb_path)
                if code2 == 0:
                    self.after(0, lambda: self._log(f"✅ Screenshot saved: {dest}\n"))
                    # Open the image
                    os.startfile(dest)
                else:
                    self.after(0, lambda: self._log(f"❌ Pull failed: {err2}\n"))
            else:
                self.after(0, lambda: self._log(f"❌ Screenshot failed: {err}\n"))

        threading.Thread(target=_run, daemon=True).start()

    def _device_info(self):
        if not self.adb_path or not self.connected_device:
            self._log("❌ Device connected নেই\n")
            return

        def _run():
            cmds = [
                ("Brand/Model", ["shell", "getprop", "ro.product.brand"]),
                ("Model", ["shell", "getprop", "ro.product.model"]),
                ("Android Version", ["shell", "getprop", "ro.build.version.release"]),
                ("SDK Version", ["shell", "getprop", "ro.build.version.sdk"]),
                ("Serial", ["get-serialno"]),
                ("Screen Size", ["shell", "wm", "size"]),
                ("Screen Density", ["shell", "wm", "density"]),
            ]
            info = "\n📱 DEVICE INFO:\n" + "─" * 40 + "\n"
            for label, cmd in cmds:
                out, _, _ = run_adb(["-s", self.connected_device] + cmd,
                                     self.adb_path, timeout=5)
                info += f"  {label}: {out}\n"

            self.after(0, lambda i=info: self._log(i + "\n"))

        threading.Thread(target=_run, daemon=True).start()

    def _battery_info(self):
        if not self.adb_path or not self.connected_device:
            self._log("❌ Device connected নেই\n")
            return

        def _run():
            out, _, _ = run_adb(["-s", self.connected_device,
                                   "shell", "dumpsys", "battery"],
                                  self.adb_path, timeout=5)
            self.after(0, lambda o=out: self._log(f"\n🔋 BATTERY INFO:\n{o}\n"))

        threading.Thread(target=_run, daemon=True).start()

    def _install_apk(self):
        path = filedialog.askopenfilename(
            title="Select APK to install",
            filetypes=[("APK", "*.apk"), ("All", "*.*")]
        )
        if not path or not self.adb_path or not self.connected_device:
            return

        def _run():
            self.after(0, lambda: self._log(f"📲 Installing: {os.path.basename(path)}\n"))
            out, err, code = run_adb(["-s", self.connected_device,
                                       "install", "-r", path],
                                      self.adb_path, timeout=60)
            result = out + err
            self.after(0, lambda r=result: self._log(f"{'✅' if 'Success' in result else '❌'} {r}\n"))

        threading.Thread(target=_run, daemon=True).start()

    def _type_text(self):
        """Type text on connected device"""
        popup = ctk.CTkToplevel(self)
        popup.title("Type Text on Device")
        popup.geometry("400x150")
        popup.configure(fg_color="#02050A")
        popup.attributes("-topmost", True)

        entry = ctk.CTkEntry(popup, placeholder_text="Text to type...",
                              height=40, width=340,
                              fg_color="#000000", font=("Consolas", 13))
        entry.pack(pady=20)

        def _send():
            text = entry.get().replace(" ", "%s")
            popup.destroy()
            if self.adb_path and self.connected_device:
                run_adb(["-s", self.connected_device,
                          "shell", "input", "text", text], self.adb_path)
                self._log(f"⌨ Typed: {entry.get()}\n")

        entry.bind("<Return>", lambda e: _send())
        ctk.CTkButton(popup, text="SEND",
                      fg_color="#004466", command=_send).pack()

    def _file_browser(self):
        if not self.adb_path or not self.connected_device:
            self._log("❌ Device connected নেই\n")
            return

        def _run():
            out, _, _ = run_adb(["-s", self.connected_device,
                                   "shell", "ls", "/sdcard/"],
                                  self.adb_path, timeout=5)
            self.after(0, lambda o=out:
                       self._log(f"\n📁 /sdcard/ contents:\n{o}\n"))

        threading.Thread(target=_run, daemon=True).start()

    def _copy_screen_text(self):
        if not self.adb_path or not self.connected_device:
            self._log("❌ Device connected নেই\n")
            return

        def _run():
            out, _, _ = run_adb(["-s", self.connected_device,
                                   "shell", "dumpsys", "accessibility"],
                                  self.adb_path, timeout=5)
            self.after(0, lambda o=out[:2000]:
                       self._log(f"\n📋 Screen accessibility:\n{o}\n"))

        threading.Thread(target=_run, daemon=True).start()

    def _connect_wifi(self):
        """Connect ADB over WiFi"""
        popup = ctk.CTkToplevel(self)
        popup.title("WiFi ADB Connect")
        popup.geometry("420x200")
        popup.configure(fg_color="#02050A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text="Phone IP Address:",
                     font=("Courier New", 12), text_color="#00F3FF").pack(pady=10)

        entry = ctk.CTkEntry(popup, placeholder_text="e.g. 192.168.1.100",
                              height=40, width=300,
                              fg_color="#000000", font=("Consolas", 13))
        entry.pack(pady=5)

        status = ctk.CTkLabel(popup, text="",
                               font=("Courier New", 11), text_color="#00FF41")
        status.pack(pady=5)

        def _connect():
            ip = entry.get().strip()
            if not ip or not self.adb_path:
                return

            def _run():
                # First enable TCP mode via USB
                run_adb(["tcpip", "5555"], self.adb_path)
                time.sleep(1)
                # Connect
                out, err, code = run_adb(["connect", f"{ip}:5555"], self.adb_path)
                msg = out or err
                self.after(0, lambda m=msg: status.configure(text=m[:60]))
                self.after(0, lambda: self._log(f"📶 WiFi ADB: {msg}\n"))
                self._refresh_devices()

            threading.Thread(target=_run, daemon=True).start()

        ctk.CTkButton(popup, text="CONNECT",
                      fg_color="#004466", command=_connect).pack(pady=10)
        ctk.CTkLabel(popup,
                     text="Phone এ: Settings → WiFi → IP Address দেখুন",
                     font=("Courier New", 10),
                     text_color="#555555").pack()

    def _run_custom_cmd(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd or not self.adb_path:
            return
        self.cmd_entry.delete(0, "end")

        def _run():
            args = cmd.split()
            if self.connected_device and not any(a == "-s" for a in args):
                args = ["-s", self.connected_device] + args
            out, err, code = run_adb(args, self.adb_path, timeout=15)
            result = out or err or "No output"
            self.after(0, lambda r=result:
                       self._log(f"\n$ adb {cmd}\n{r}\n"))

        threading.Thread(target=_run, daemon=True).start()

    def _log(self, msg):
        self.output.insert("end", msg)
        self.output.see("end")

    def _lighten(self, hex_color):
        try:
            r = min(255, int(hex_color[1:3], 16) + 25)
            g = min(255, int(hex_color[3:5], 16) + 25)
            b = min(255, int(hex_color[5:7], 16) + 25)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color


def open_android_manager(master=None, brain=None):
    """Open Android Device Manager"""
    win = AndroidManager(master, brain)
    win.lift()
    win.focus_force()
    return win


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    win = AndroidManager(root)
    root.mainloop()
