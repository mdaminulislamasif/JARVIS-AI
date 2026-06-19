# Windows 10 Navigation & Environment Guide

This guide describes the standard layout, folder hierarchy, registry path resolution, and common directory mappings in a standard Windows 10 installation. It serves as a reference manual for both the user and the JARVIS AI assistant.

---

## 1. Directory Structure Mappings

On Windows, standard user data is stored within the user's profile directory, generally found at `%USERPROFILE%` (e.g. `C:\Users\<Username>`).

| Folder Name | Shortcut Path | Physical Path | Purpose |
| :--- | :--- | :--- | :--- |
| **Desktop** | `%USERPROFILE%\Desktop` | `C:\Users\<Username>\Desktop` | Active workspace files, shortcuts |
| **Downloads** | `%USERPROFILE%\Downloads` | `C:\Users\<Username>\Downloads` | Downloaded files and packages |
| **Documents** | `%USERPROFILE%\Documents` | `C:\Users\<Username>\Documents` | User documents, text files, notes |
| **AppData (Local)** | `%USERPROFILE%\AppData\Local` | `C:\Users\<Username>\AppData\Local` | Local application cache, programs (e.g., Python, VS Code installations) |
| **AppData (Roaming)** | `%USERPROFILE%\AppData\Roaming` | `C:\Users\<Username>\AppData\Roaming` | Portable application settings, configs |
| **Temp Directory** | `%TEMP%` | `C:\Users\<Username>\AppData\Local\Temp` | Temporary scratch files (e.g., screenshots, video captures) |
| **Program Files** | `C:\Program Files` | `C:\Program Files` | 64-bit installed software programs |
| **Program Files (x86)**| `C:\Program Files (x86)` | `C:\Program Files (x86)` | 32-bit installed software programs |
| **System32** | `C:\Windows\System32` | `C:\Windows\System32` | Core OS executable tools (e.g., cmd.exe, calc.exe, osk.exe) |

---

## 2. Standard Windows Settings Mappings

You can open specific Settings pages using Windows Protocol URIs (run via `start ms-settings:<page>`):

*   **Settings Home:** `ms-settings:`
*   **Time & Date:** `ms-settings:dateandtime`
*   **Sound / Volume Settings:** `ms-settings:sound`
*   **Display Settings:** `ms-settings:display`
*   **WiFi / Network Settings:** `ms-settings:network-wifi`
*   **Bluetooth Settings:** `ms-settings:bluetooth`
*   **Power & Sleep Settings:** `ms-settings:powersleep`
*   **Windows Update:** `ms-settings:windowsupdate`
*   **Installed Apps:** `ms-settings:appsfeatures`

---

## 3. Application Path Resolution Logic

When launching an app (e.g. `"chrome"`, `"notepad"`, `"vscode"`), the system checks the following layers sequentially:

1.  **Absolute Path:** If the path is absolute and exists, run it directly.
2.  **Windows Registry App Paths:**
    *   `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths`
    *   `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths`
    *   This is where applications like Chrome, Edge, and Excel register their main executables.
3.  **Environment Variable `PATH`:** Checks folders registered in system/user environment path.
4.  **Common Program Folders:**
    *   `C:\Program Files`
    *   `C:\Program Files (x86)`
    *   `C:\Windows\System32`
    *   `%USERPROFILE%\AppData\Local\Programs`
    *   Subdirectories up to 3 levels deep are scanned dynamically.

---

## 4. Key Keyboard & Mouse Shortcuts

Windows 10 provides several key keyboard shortcuts to navigate windows and control execution:

*   `Win + D` : Minimizes all windows and displays the Desktop.
*   `Win + E` : Opens a new File Explorer window.
*   `Win + R` : Opens the Run dialog box.
*   `Ctrl + Shift + Esc` : Opens the Task Manager.
*   `Alt + F4` : Closes the active window.
*   `Win + Up Arrow` : Maximizes the active window.
*   `Win + Down Arrow` : Minimizes the active window.
