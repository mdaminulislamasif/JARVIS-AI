"""
JARVIS Login Window
Full-screen animated login with:
  - Email / Password (create account or sign in)
  - Google / Microsoft / Apple OAuth buttons
  - Auto API key fetch + apply after login
  - Remember Me session
  - Neon cyberpunk design matching the main panel
"""
import os
import math
import time
import threading
import webbrowser
import customtkinter as ctk
from PIL import Image, ImageTk

from core.auth import (
    create_account, login_email, oauth_google, oauth_microsoft, oauth_apple,
    auto_fetch_gemini_key, auto_apply_key_to_config, get_session, logout,
    _save_session,
)
from core.key_generator import auto_create_and_apply_key, make_default_key_name

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Animated neon background canvas ──────────────────────────────────────────
class _NeonBG(ctk.CTkCanvas):
    def __init__(self, master, **kw):
        super().__init__(master, highlightthickness=0, bg="#02050A", **kw)
        self._t = 0.0
        self._animate()

    def _animate(self):
        self._t += 0.03
        self.delete("all")
        w = self.winfo_width() or 900
        h = self.winfo_height() or 700
        cx, cy = w // 2, h // 2
        t = self._t

        # Pulsing outer rings
        for i, (r_base, color, dash) in enumerate([
            (min(w, h) * 0.42, "#001133", (4, 8)),
            (min(w, h) * 0.36, "#002244", (2, 6)),
            (min(w, h) * 0.30, "#003355", (1, 4)),
        ]):
            r = r_base + 8 * math.sin(t * 1.2 + i)
            self.create_oval(cx - r, cy - r * 0.85, cx + r, cy + r * 0.85,
                             outline=color, width=1, dash=dash)

        # Rotating arc
        ang = (t * 30) % 360
        self.create_arc(cx - min(w,h)*0.38, cy - min(w,h)*0.38*0.85,
                        cx + min(w,h)*0.38, cy + min(w,h)*0.38*0.85,
                        outline="#00F3FF", width=2, start=ang, extent=55, style="arc")
        self.create_arc(cx - min(w,h)*0.38, cy - min(w,h)*0.38*0.85,
                        cx + min(w,h)*0.38, cy + min(w,h)*0.38*0.85,
                        outline="#00F3FF", width=2, start=ang + 180, extent=55, style="arc")

        # Orbital dots
        for i in range(6):
            a = t * 0.6 + i * (math.pi / 3)
            r = min(w, h) * 0.40
            x = cx + r * math.cos(a)
            y = cy + r * math.sin(a) * 0.85
            self.create_oval(x - 3, y - 3, x + 3, y + 3, fill="#00F3FF", outline="")

        # Scan line
        sy = (cy - 200 + int(t * 80)) % (h + 50) - 25
        self.create_line(cx - 300, sy, cx + 300, sy, fill="#001122", width=1, dash=(2, 4))

        self.after(33, self._animate)


# ── Login Window ──────────────────────────────────────────────────────────────
class LoginWindow(ctk.CTkToplevel):
    """
    Shown before the main panel. Calls on_success(session) when login succeeds.
    """

    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.title("JARVIS — AUTHENTICATION REQUIRED")
        self.geometry("900x700")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#02050A")
        self.attributes("-topmost", True)
        self.grab_set()  # modal

        self._mode = "login"   # "login" | "register"
        self._status_msg = ""
        self._key_watcher_active = False

        self._build_ui()
        self._start_clipboard_watcher()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Animated background
        self.bg = _NeonBG(self, width=900, height=700)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Central card
        self.card = ctk.CTkFrame(self, width=440, height=580,
                                 fg_color="#05080F",
                                 border_width=1, border_color="#00F3FF",
                                 corner_radius=16)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Logo / title
        ctk.CTkLabel(self.card, text="[*] JARVIS",
                     font=("Courier New", 32, "bold"),
                     text_color="#00F3FF").pack(pady=(30, 0))
        ctk.CTkLabel(self.card, text="ANTIGRAVITY PRIME — SECURE ACCESS",
                     font=("Courier New", 11),
                     text_color="#334455").pack(pady=(0, 20))

        # Tab buttons (Login / Register)
        tab_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        tab_frame.pack(fill="x", padx=30)
        self._login_tab = ctk.CTkButton(
            tab_frame, text="SIGN IN", width=180, height=36,
            fg_color="#003355", hover_color="#005577",
            font=("Courier New", 13, "bold"),
            command=lambda: self._switch_mode("login"))
        self._login_tab.pack(side="left", padx=(0, 5))
        self._reg_tab = ctk.CTkButton(
            tab_frame, text="CREATE ACCOUNT", width=180, height=36,
            fg_color="#001122", hover_color="#002233",
            font=("Courier New", 13, "bold"),
            command=lambda: self._switch_mode("register"))
        self._reg_tab.pack(side="left")

        # Form fields
        form = ctk.CTkFrame(self.card, fg_color="transparent")
        form.pack(fill="x", padx=30, pady=10)

        # Display name (register only)
        self._name_label = ctk.CTkLabel(form, text="Display Name",
                                        font=("Courier New", 11), text_color="#555555")
        self._name_entry = ctk.CTkEntry(form, placeholder_text="Your name...",
                                        height=40, fg_color="#000000",
                                        border_color="#002233", text_color="#00F3FF",
                                        font=("Courier New", 13))

        # Email
        ctk.CTkLabel(form, text="Email Address",
                     font=("Courier New", 11), text_color="#555555").pack(anchor="w", pady=(8, 0))
        self._email_entry = ctk.CTkEntry(form, placeholder_text="you@example.com",
                                         height=40, fg_color="#000000",
                                         border_color="#002233", text_color="#00F3FF",
                                         font=("Courier New", 13))
        self._email_entry.pack(fill="x", pady=(2, 0))

        # Password
        ctk.CTkLabel(form, text="Password",
                     font=("Courier New", 11), text_color="#555555").pack(anchor="w", pady=(8, 0))
        self._pw_entry = ctk.CTkEntry(form, placeholder_text="••••••••",
                                      height=40, fg_color="#000000",
                                      border_color="#002233", text_color="#00F3FF",
                                      font=("Courier New", 13), show="•")
        self._pw_entry.pack(fill="x", pady=(2, 0))
        self._pw_entry.bind("<Return>", lambda e: self._submit())

        # Remember me
        self._remember = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(form, text="Remember me (30 days)",
                        variable=self._remember,
                        font=("Courier New", 11), text_color="#334455",
                        fg_color="#003355", hover_color="#005577").pack(anchor="w", pady=(10, 0))

        # Status label
        self._status_lbl = ctk.CTkLabel(self.card, text="",
                                        font=("Courier New", 11),
                                        text_color="#FF3131", wraplength=380)
        self._status_lbl.pack(pady=(5, 0))

        # Submit button
        self._submit_btn = ctk.CTkButton(
            self.card, text=">> SIGN IN", height=46,
            fg_color="#003355", hover_color="#005577",
            font=("Courier New", 15, "bold"), text_color="#00F3FF",
            command=self._submit)
        self._submit_btn.pack(fill="x", padx=30, pady=(8, 0))

        # Bypass button
        self._bypass_btn = ctk.CTkButton(
            self.card, text="🔓 BYPASS / GUEST ACCESS", height=38,
            fg_color="#331100", hover_color="#552200",
            font=("Courier New", 13, "bold"), text_color="#FF8800",
            command=self._bypass_login)
        self._bypass_btn.pack(fill="x", padx=30, pady=(6, 0))

        # Divider
        div = ctk.CTkFrame(self.card, height=1, fg_color="#112233")
        div.pack(fill="x", padx=30, pady=15)
        ctk.CTkLabel(self.card, text="— OR CONTINUE WITH —",
                     font=("Courier New", 10), text_color="#223344").pack()

        # OAuth buttons
        oauth_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        oauth_frame.pack(pady=10)

        self._make_oauth_btn(oauth_frame, "[G]  Google",    "#1a1a2e", "#2a2a4e",
                             self._oauth_google).pack(side="left", padx=6)
        self._make_oauth_btn(oauth_frame, "[M]  Microsoft", "#1a1a2e", "#2a2a4e",
                             self._oauth_microsoft).pack(side="left", padx=6)
        self._make_oauth_btn(oauth_frame, "[A]  Apple",     "#1a1a2e", "#2a2a4e",
                             self._oauth_apple).pack(side="left", padx=6)

        # Auto key fetch hint
        self._key_status = ctk.CTkLabel(
            self.card,
            text="[KEY] Watching clipboard for Gemini API key...",
            font=("Courier New", 10), text_color="#223344")
        self._key_status.pack(pady=(5, 0))

        ctk.CTkButton(
            self.card, text="Get Free API Key →", height=28,
            fg_color="transparent", hover_color="#001122",
            font=("Courier New", 10), text_color="#334455",
            command=lambda: webbrowser.open("https://aistudio.google.com/app/apikey")
        ).pack(pady=(2, 10))

        # Server status bar
        self._server_bar = ctk.CTkFrame(self.card, fg_color="#030608",
                                        border_width=1, border_color="#112233",
                                        corner_radius=6)
        self._server_bar.pack(fill="x", padx=20, pady=(0, 8))
        self._server_dot = ctk.CTkLabel(self._server_bar, text="[*]",
                                        font=("Courier New", 11), text_color="#333333")
        self._server_dot.pack(side="left", padx=(8, 4))
        self._server_lbl = ctk.CTkLabel(self._server_bar,
                                        text="Checking server...",
                                        font=("Courier New", 10), text_color="#334455")
        self._server_lbl.pack(side="left")
        ctk.CTkButton(self._server_bar, text="[CFG]", width=40, height=22,
                      fg_color="transparent", hover_color="#112233",
                      font=("Courier New", 10), text_color="#334455",
                      command=self._show_server_config).pack(side="right", padx=4)
        # Check server in background
        threading.Thread(target=self._check_server_status, daemon=True).start()

    def _make_oauth_btn(self, parent, text, fg, hover, cmd):
        return ctk.CTkButton(parent, text=text, width=120, height=38,
                             fg_color=fg, hover_color=hover,
                             font=("Courier New", 11, "bold"), text_color="#AABBCC",
                             command=cmd)

    def _switch_mode(self, mode: str):
        self._mode = mode
        if mode == "register":
            self._login_tab.configure(fg_color="#001122")
            self._reg_tab.configure(fg_color="#003355")
            self._submit_btn.configure(text=">> CREATE ACCOUNT")
            # Show name field
            self._name_entry.pack(fill="x", pady=(2, 0), before=self._email_entry)
            self._name_label.pack(in_=self._name_entry.master,
                                  anchor="w", pady=(8, 0), before=self._name_entry)
        else:
            self._login_tab.configure(fg_color="#003355")
            self._reg_tab.configure(fg_color="#001122")
            self._submit_btn.configure(text=">> SIGN IN")
            self._name_label.pack_forget()
            self._name_entry.pack_forget()
        self._set_status("")

    def _set_status(self, msg: str, color: str = "#FF3131"):
        self._status_lbl.configure(text=msg, text_color=color)

    # ── Form submit ───────────────────────────────────────────────────────────

    def _submit(self):
        email = self._email_entry.get().strip()
        pw    = self._pw_entry.get()
        remember = self._remember.get()

        if not email or not pw:
            self._set_status("Please enter email and password.")
            return

        self._submit_btn.configure(state="disabled", text="PROCESSING...")

        def _run():
            if self._mode == "register":
                name = self._name_entry.get().strip() or email.split("@")[0]
                ok, msg = create_account(email, pw, name)
                if ok:
                    ok2, result = login_email(email, pw, remember)
                    if ok2:
                        self.after(0, lambda: self._on_login_success(result))
                    else:
                        self.after(0, lambda: self._set_status(str(result)))
                        self.after(0, lambda: self._submit_btn.configure(
                            state="normal", text=">> CREATE ACCOUNT"))
                else:
                    self.after(0, lambda: self._set_status(msg))
                    self.after(0, lambda: self._submit_btn.configure(
                        state="normal", text=">> CREATE ACCOUNT"))
            else:
                ok, result = login_email(email, pw, remember)
                if ok:
                    self.after(0, lambda: self._on_login_success(result))
                else:
                    self.after(0, lambda: self._set_status(str(result)))
                    self.after(0, lambda: self._submit_btn.configure(
                        state="normal", text=">> SIGN IN"))

        threading.Thread(target=_run, daemon=True).start()

    # ── OAuth handlers ────────────────────────────────────────────────────────

    def _oauth_google(self):
        self._set_status("Opening Google sign-in + AI Studio...", "#00FF41")
        threading.Thread(target=self._run_oauth, args=("google",), daemon=True).start()

    def _oauth_microsoft(self):
        self._set_status("Opening Microsoft sign-in + AI Studio...", "#00FF41")
        threading.Thread(target=self._run_oauth, args=("microsoft",), daemon=True).start()

    def _oauth_apple(self):
        self._set_status("Opening Apple sign-in + AI Studio...", "#00FF41")
        threading.Thread(target=self._run_oauth, args=("apple",), daemon=True).start()

    def _run_oauth(self, provider: str):
        if provider == "google":
            session = oauth_google()
        elif provider == "microsoft":
            session = oauth_microsoft()
        else:
            session = oauth_apple()

        self.after(0, lambda: self._set_status(
            f"[OK] {provider.capitalize()} sign-in opened. Copy your API key from AI Studio.",
            "#00FF41"))
        self.after(0, lambda: self._key_status.configure(
            text="[KEY] Watching clipboard -- paste your Gemini API key here...",
            text_color="#00FF41"))
        # Start watching for key
        self._watch_for_key(session)

    def _watch_for_key(self, session: dict, timeout: int = 120):
        """Watch clipboard for an API key and auto-apply it."""
        try:
            import pyperclip
            deadline = time.time() + timeout
            last = pyperclip.paste()
            while time.time() < deadline:
                curr = pyperclip.paste().strip()
                if curr != last and len(curr) >= 20:
                    auto_apply_key_to_config(curr, session.get("email", ""))
                    session["api_key"] = curr
                    # Update session file
                    _save_session(
                        session.get("email", ""),
                        session.get("display_name", ""),
                        session.get("provider", ""),
                        True, curr,
                        server_token=session.get("server_token", "")
                    )
                    self.after(0, lambda k=curr: self._key_status.configure(
                        text=f"[OK] API Key auto-applied: {k[:10]}****",
                        text_color="#00FF41"))
                    self.after(500, lambda: self._on_login_success(session))
                    return
                last = curr
                time.sleep(1)
            self.after(0, lambda: self._key_status.configure(
                text="[!] No key detected. You can add it later in Neural Protocols.",
                text_color="#FF8800"))
            # Login anyway without key
            self.after(1000, lambda: self._on_login_success(session))
        except Exception as e:
            self.after(0, lambda: self._on_login_success(session))

    # ── Server status ─────────────────────────────────────────────────────────

    def _check_server_status(self):
        try:
            from server.auth_client import get_client
            client = get_client()
            online = client.is_online()
            url    = client.get_server_url()
            if online:
                self.after(0, lambda: self._server_dot.configure(text_color="#00FF41"))
                self.after(0, lambda: self._server_lbl.configure(
                    text=f"Server ONLINE: {url}", text_color="#00FF41"))
            else:
                self.after(0, lambda: self._server_dot.configure(text_color="#FF8800"))
                self.after(0, lambda: self._server_lbl.configure(
                    text=f"Server OFFLINE -- using local auth", text_color="#FF8800"))
        except Exception:
            self.after(0, lambda: self._server_dot.configure(text_color="#555555"))
            self.after(0, lambda: self._server_lbl.configure(
                text="Local auth only", text_color="#555555"))

    def _show_server_config(self):
        """Popup to configure the auth server URL."""
        popup = ctk.CTkToplevel(self)
        popup.title("Server Config")
        popup.geometry("420x220")
        popup.configure(fg_color="#02050A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text="AUTH SERVER URL",
                     font=("Courier New", 14, "bold"), text_color="#00F3FF").pack(pady=15)
        ctk.CTkLabel(popup, text="Enter the URL of your JARVIS Auth Server:",
                     font=("Courier New", 10), text_color="#555555").pack()

        try:
            from server.auth_client import _load_server_url
            current_url = _load_server_url()
        except Exception:
            current_url = "http://localhost:7700"

        url_entry = ctk.CTkEntry(popup, height=40, font=("Courier New", 13),
                                 fg_color="#05080F", text_color="#00F3FF")
        url_entry.insert(0, current_url)
        url_entry.pack(fill="x", padx=20, pady=10)

        status_lbl = ctk.CTkLabel(popup, text="", font=("Courier New", 10))
        status_lbl.pack()

        def _save():
            url = url_entry.get().strip()
            if not url:
                return
            try:
                from server.auth_client import get_client
                client = get_client()
                client.set_server_url(url)
                online = client.is_online()
                if online:
                    status_lbl.configure(text=f"[OK] Connected to {url}", text_color="#00FF41")
                    threading.Thread(target=self._check_server_status, daemon=True).start()
                else:
                    status_lbl.configure(text="✗ Cannot reach server", text_color="#FF3131")
            except Exception as e:
                status_lbl.configure(text=f"Error: {e}", text_color="#FF3131")

        ctk.CTkButton(popup, text="SAVE & TEST", height=38,
                      fg_color="#003344", hover_color="#005566",
                      command=_save).pack(fill="x", padx=20, pady=8)

        ctk.CTkLabel(popup,
                     text="Start server: python server/start_server.py",
                     font=("Courier New", 9), text_color="#334455").pack()

    def _start_clipboard_watcher(self):
        def _watch():
            try:
                import pyperclip
                last = ""
                # WARNING: Infinite loop - ensure break condition exists
                while True:
                    curr = pyperclip.paste().strip()
                    if curr != last and len(curr) >= 20:
                        self._pending_key = curr
                        auto_apply_key_to_config(curr, "guest@jarvis.local")
                        session = {
                            "email": "guest@jarvis.local",
                            "display_name": "Guest User",
                            "provider": "guest",
                            "remember": True,
                            "api_key": curr
                        }
                        self.after(0, lambda k=curr: self._key_status.configure(
                            text=f"[KEY] API Key detected & applied: {k[:10]}****",
                            text_color="#00FF41"))
                        self.after(500, lambda: self._on_login_success(session))
                        break
                    last = curr
                    time.sleep(1.5)
            except Exception:
                print("⚠️ Error occurred but was silently ignored")
        threading.Thread(target=_watch, daemon=True).start()

    # ── Success ───────────────────────────────────────────────────────────────

    def _on_login_success(self, session: dict):
        name    = session.get("display_name", "User")
        email   = session.get("email", "")
        api_key = session.get("api_key", "")

        # Apply any pending clipboard key first
        pending = getattr(self, "_pending_key", "")
        if pending and not api_key:
            auto_apply_key_to_config(pending, email)
            session["api_key"] = pending
            api_key = pending

        self._set_status(f"[OK] Welcome, {name}!", "#00FF41")

        if api_key:
            # Key already exists — go straight to main panel
            self.after(800, lambda: self._launch_main(session))
        else:
            # No key — show auto-create key dialog
            self.after(600, lambda: self._show_key_setup(session))

    def _show_key_setup(self, session: dict):
        """
        Full-screen key setup dialog shown after login when no API key exists.
        Offers: Auto-create (Selenium), clipboard watch, or manual paste.
        """
        name     = session.get("display_name", "User")
        email    = session.get("email", "")
        key_name = make_default_key_name(name, email)

        # Overlay on top of login card
        overlay = ctk.CTkFrame(self, fg_color="#02050A",
                               border_width=1, border_color="#00F3FF",
                               corner_radius=16)
        overlay.place(relx=0.5, rely=0.5, anchor="center", width=460, height=500)

        ctk.CTkLabel(overlay, text="API KEY SETUP",
                     font=("Courier New", 22, "bold"),
                     text_color="#00F3FF").pack(pady=(25, 4))
        ctk.CTkLabel(overlay,
                     text=f"Hello {name}! JARVIS needs a Gemini API key to think.",
                     font=("Courier New", 11), text_color="#556677",
                     wraplength=400).pack(pady=(0, 4))

        # Default key name display
        name_frame = ctk.CTkFrame(overlay, fg_color="#05080F",
                                  border_width=1, border_color="#002233",
                                  corner_radius=8)
        name_frame.pack(fill="x", padx=25, pady=8)
        ctk.CTkLabel(name_frame, text="Default key name:",
                     font=("Courier New", 10), text_color="#445566").pack(anchor="w", padx=10, pady=(6, 0))
        self._key_name_entry = ctk.CTkEntry(
            name_frame, height=36, font=("Courier New", 13),
            fg_color="#000000", border_color="#003344", text_color="#00F3FF")
        self._key_name_entry.insert(0, key_name)
        self._key_name_entry.pack(fill="x", padx=10, pady=(2, 8))

        # Status log box
        self._key_log = ctk.CTkTextbox(overlay, height=100,
                                       font=("Consolas", 11),
                                       fg_color="#030608", text_color="#00FF41",
                                       border_width=1, border_color="#002233")
        self._key_log.pack(fill="x", padx=25, pady=4)
        self._key_log.insert("end", f"Key name ready: {key_name}\n")
        self._key_log.insert("end", "Choose an option below to get your free API key.\n")

        def _log(msg):
            self.after(0, lambda m=msg: (
                self._key_log.insert("end", m + "\n"),
                self._key_log.see("end")
            ))

        def _done(key):
            session["api_key"] = key
            _save_session(email, name, session.get("provider", "email"), True, key, 
                          server_token=session.get("server_token", ""))
            self.after(0, lambda: self._launch_main(session))

        # Button row
        btn_frame = ctk.CTkFrame(overlay, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=8)

        def _auto_create():
            kn = self._key_name_entry.get().strip() or key_name
            _log(f"Starting auto-create for key: {kn}")
            auto_create_and_apply_key(
                display_name=name, email=email,
                on_status=_log, on_done=_done, timeout=180,
            )

        def _open_studio():
            kn = self._key_name_entry.get().strip() or key_name
            _log(f"Opening AI Studio... Key name '{kn}' copied to clipboard.")
            _log("Create a key, copy it, and JARVIS will auto-detect it.")
            import pyperclip
            try:
                pyperclip.copy(kn)
            except Exception:
                print("⚠️ Error occurred but was silently ignored")
            import webbrowser
            webbrowser.open("https://aistudio.google.com/app/apikey")
            # Start watching clipboard
            def _watch():
                from core.key_generator import watch_clipboard_for_key
                key = watch_clipboard_for_key(
                    timeout=180,
                    on_found=lambda k: _log(f"[OK] Key detected: {k[:10]}****"),
                    on_timeout=lambda: _log("[!] Timeout. Paste key manually below."),
                )
                if key:
                    _done(key)
            threading.Thread(target=_watch, daemon=True).start()

        ctk.CTkButton(btn_frame, text="[AUTO] Auto-Create Key",
                      height=40, fg_color="#003300", hover_color="#005500",
                      font=("Courier New", 12, "bold"), text_color="#00FF41",
                      command=_auto_create).pack(fill="x", pady=3)

        ctk.CTkButton(btn_frame, text="[WEB] Open AI Studio + Watch Clipboard",
                      height=40, fg_color="#003344", hover_color="#005566",
                      font=("Courier New", 12, "bold"), text_color="#00F3FF",
                      command=_open_studio).pack(fill="x", pady=3)

        # Manual paste row
        paste_frame = ctk.CTkFrame(overlay, fg_color="transparent")
        paste_frame.pack(fill="x", padx=25, pady=4)
        self._manual_key_entry = ctk.CTkEntry(
            paste_frame, placeholder_text="Paste API key here (AIza...)",
            height=38, fg_color="#000000", border_color="#002233",
            text_color="#00F3FF", font=("Consolas", 12))
        self._manual_key_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        def _manual_apply():
            k = self._manual_key_entry.get().strip()
            if len(k) < 20:
                _log("[!] Invalid key format. Must be at least 20 characters.")
                return
            auto_apply_key_to_config(k, email)
            _log(f"[OK] Key applied: {k[:10]}****")
            _done(k)

        ctk.CTkButton(paste_frame, text="APPLY", width=70, height=38,
                      fg_color="#004422", hover_color="#006644",
                      font=("Courier New", 12, "bold"), text_color="#00FF41",
                      command=_manual_apply).pack(side="left")

        # Skip button
        ctk.CTkButton(overlay, text="Skip for now (add key later)",
                      height=30, fg_color="transparent", hover_color="#111111",
                      font=("Courier New", 10), text_color="#334455",
                      command=lambda: self._launch_main(session)).pack(pady=(4, 10))

    def _bypass_login(self):
        # Load keys directly from config file to avoid circular imports
        keys = []
        cfg_path = os.path.join(_BASE, 'jarvis_config.txt')
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, 'r') as f:
                    keys = [line.strip() for line in f.readlines()
                            if line.strip() and len(line.strip()) >= 20]
            except Exception:
                pass
        api_key = keys[0] if keys else ""
        session = _save_session(
            email="guest@jarvis.local",
            display_name="Guest User",
            provider="guest",
            remember=True,
            api_key=api_key
        )
        self._set_status("[OK] Bypassing login...", "#00FF41")
        self.after(500, lambda: self._on_login_success(session))

    def _launch_main(self, session: dict):
        self.grab_release()
        self.destroy()
        self.on_success(session)


def check_and_login(root, on_success, force_login=False):
    """
    Auto-login as Guest user using the API key in jarvis_config.txt to bypass login screen,
    unless force_login is True (which happens when logging out).
    """
    if force_login:
        LoginWindow(root, on_success)
        return

    session = get_session()
    if session and session.get("email"):
        on_success(session)
        return

    keys = []
    cfg_path = os.path.join(_BASE, 'jarvis_config.txt')
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r') as f:
                keys = [line.strip() for line in f.readlines()
                        if line.strip() and len(line.strip()) >= 20]
        except Exception:
            pass
    api_key = keys[0] if keys else ""
    session = _save_session(
        email="guest@jarvis.local",
        display_name="Guest User",
        provider="guest",
        remember=True,
        api_key=api_key
    )
    on_success(session)
