#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS MULTI-DEVICE AUDIO BRIDGE
================================
Routes audio (System Audio / Microphone) from multiple Android devices to PC simultaneously.
"""

import os
import sys
import time
import subprocess
import threading
import json

# ── PATHS ────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
ADB = os.path.join(BASE, "platform-tools", "adb.exe")
SCRCPY = os.path.join(BASE, "scrcpy", "scrcpy-win64-v2.4", "scrcpy.exe")

# Verify and set paths
if not os.path.exists(ADB):
    ADB = "adb.exe"  # Use path fallback
if not os.path.exists(SCRCPY):
    SCRCPY = "scrcpy.exe"  # Use path fallback

os.environ["ADB"] = ADB

def run_adb(args, timeout=10):
    try:
        res = subprocess.run([ADB] + args, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), -1

def get_connected_devices():
    """Detect all active, authorized ADB devices."""
    out, _, code = run_adb(["devices"])
    if code != 0:
        return []
    devices = []
    lines = out.strip().split("\n")[1:]
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices

def get_device_name(serial):
    """Retrieve device model/brand."""
    model, _, _ = run_adb(["-s", serial, "shell", "getprop", "ro.product.model"])
    brand, _, _ = run_adb(["-s", serial, "shell", "getprop", "ro.product.brand"])
    if model and brand:
        return f"{brand.capitalize()} {model}"
    elif model:
        return model
    return serial

def prepare_device(serial, name):
    """Grant mic permissions and boost volumes via ADB."""
    print(f"\n[+] Preparing device: {name} ({serial})")
    
    # 1. Grant permission
    print(f"    - Granting RECORD_AUDIO permission to scrcpy...")
    run_adb(["-s", serial, "shell", "pm", "grant", "com.genymobile.scrcpy", "android.permission.RECORD_AUDIO"])
    
    # 2. Boost volumes
    print(f"    - Boosting media and system volumes...")
    volumes = ["volume_music", "volume_voice_communication", "volume_ring", "volume_notification"]
    for vol in volumes:
        run_adb(["-s", serial, "shell", "settings", "put", "system", vol, "15"])
    
    run_adb(["-s", serial, "shell", "media", "volume", "--stream", "0", "--set", "15"])
    # Send Volume Up keyevents to be certain
    run_adb(["-s", serial, "shell", "for i in 1 2 3 4 5; do input keyevent 24; done"])
    print(f"    [OK] Device prepared successfully!")

def start_scrcpy(serial, name, mode):
    """
    Launch scrcpy stream in a subprocess.
    Modes:
      1: Screen Mirror + System Audio
      2: System Audio Only (No Video)
      3: Microphone Only (No Video)
    """
    processes = []
    
    if mode in (1, 2):
        # System Audio stream
        cmd = [
            SCRCPY,
            "-s", serial,
            "--audio-source=output",
            "--window-title", f"{name} - System Audio",
            "--always-on-top",
            "--stay-awake"
        ]
        if mode == 2:
            cmd.append("--no-video")
        else:
            cmd.extend(["--max-size", "1024", "--video-bit-rate", "6M"])
            
        print(f"    [+] Starting system audio stream for {name}...")
        proc = subprocess.Popen(cmd, cwd=os.path.dirname(SCRCPY) if os.path.exists(SCRCPY) else None,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        processes.append(proc)
        
    if mode == 3:
        # Mic stream (audio only)
        cmd = [
            SCRCPY,
            "-s", serial,
            "--audio-source=mic",
            "--no-video",
            "--window-title", f"{name} - Microphone"
        ]
        print(f"    [+] Starting microphone audio stream for {name}...")
        proc = subprocess.Popen(cmd, cwd=os.path.dirname(SCRCPY) if os.path.exists(SCRCPY) else None,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        processes.append(proc)

    return processes

def main():
    print("=" * 65)
    print("  JARVIS DYNAMIC MULTI-DEVICE AUDIO & MIRROR BRIDGE")
    print("=" * 65)
    
    # 1. Detect connected devices
    devices = get_connected_devices()
    if not devices:
        print("\n[!] No ADB devices detected.")
        print("    Please connect your devices via USB, enable USB Debugging, and authorize PC.")
        print("    Waiting for devices...")
        while not devices:
            time.sleep(2)
            devices = get_connected_devices()
            
    print(f"\n[OK] Detected {len(devices)} device(s):")
    device_info = {}
    for i, serial in enumerate(devices, 1):
        name = get_device_name(serial)
        device_info[serial] = name
        print(f"    {i}. {name} [Serial: {serial}]")
        
    # 2. Select Stream Mode
    print("\nSelect Stream Mode:")
    print("  [1] Screen Mirror + System Audio (Recommended)")
    print("  [2] System Audio Only (No video screen display)")
    print("  [3] Microphone Stream Only (Route phone mic to PC)")
    
    mode = 1
    try:
        choice = input("\nEnter choice [1-3] (default 1): ").strip()
        if choice in ("1", "2", "3"):
            mode = int(choice)
    except (KeyboardInterrupt, SystemExit):
        print("\nExiting...")
        return
    except EOFError:
        print("\n[INFO] Standard input EOF. Using default mode: 1 (Screen Mirror + System Audio)")
        mode = 1
        
    # 3. Initialize all devices
    for serial, name in device_info.items():
        prepare_device(serial, name)
        
    # 4. Launch streams
    all_processes = []
    for serial, name in device_info.items():
        procs = start_scrcpy(serial, name, mode)
        all_processes.extend(procs)
        
    # Let them initialize
    time.sleep(2)
    
    active_procs = [p for p in all_processes if p.poll() is None]
    if active_procs:
        print("\n" + "=" * 65)
        print("  AUDIO BRIDGE RUNNING SUCCESSFULLY!")
        print("=" * 65)
        print(f"  Streaming audio/video from {len(active_procs)} process(es) to PC.")
        print("  Press Ctrl+C to terminate all streams and exit.")
        print("=" * 65)
    else:
        print("\n[!] Failed to start streaming processes. Make sure scrcpy is installed and closed.")
        return

    # Keep script alive and monitor processes
    try:
        while True:
            time.sleep(2)
            # Verify status
            dead_procs = [p for p in all_processes if p.poll() is not None]
            if dead_procs:
                print("\n[!] One or more audio streams closed. Terminating others...")
                break
    except KeyboardInterrupt:
        print("\n\n[-] Ctrl+C detected. Shutting down all audio bridge connections...")
    finally:
        for p in all_processes:
            try:
                p.terminate()
            except Exception:
                pass
        print("[OK] Cleanup complete. Goodbye!")

if __name__ == "__main__":
    main()
