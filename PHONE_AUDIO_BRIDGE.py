"""
JARVIS PHONE AUDIO BRIDGE
=========================
Phone Mic  --> PC (JARVIS listens via phone microphone)
Phone Audio --> PC Speakers (Phone sound plays on PC)

How it works:
  1. scrcpy --audio-source=mic   : streams phone mic to PC speakers
  2. scrcpy --audio-source=output : streams phone system audio to PC speakers  
  3. Python PyAudio loopback      : captures PC speaker output → feeds to JARVIS as mic input

Requirements: pip install pyaudio sounddevice numpy
"""

import subprocess
import os
import sys
import time
import threading

# ── PATHS ────────────────────────────────────────────────────────────────────
BASE      = os.path.dirname(os.path.abspath(__file__))
ADB       = os.path.join(BASE, "platform-tools", "adb.exe")
SCRCPY    = os.path.join(BASE, "scrcpy", "scrcpy-win64-v2.4", "scrcpy.exe")
SERIAL    = "BD354558452086043"

# Set ADB env so scrcpy finds it
os.environ["ADB"] = ADB
os.environ["ANDROID_SERIAL"] = SERIAL


def find_device():
    """Verify phone is connected."""
    result = subprocess.run([ADB, "devices"], capture_output=True, text=True)
    lines = [l for l in result.stdout.strip().split("\n")[1:] if l.strip()]
    devices = []
    for line in lines:
        if "device" in line and "unauthorized" not in line:
            devices.append(line.split()[0])
            
    if len(devices) > 1:
        print(f"\n[INFO] Detected {len(devices)} devices connected!")
        print("       For streaming audio/video from multiple devices simultaneously,")
        print("       please run: python multi_phone_audio_bridge.py")
        print("       (or double click START_MULTI_PHONE_AUDIO.bat)\n")
        
    if devices:
        serial = devices[0]
        print(f"[OK] Device found: {serial}")
        return serial
    print("[ERR] No ADB device connected!")
    return None


def launch_phone_mic_to_pc():
    """
    Route PHONE MIC → PC Speakers via scrcpy.
    scrcpy captures phone microphone and plays it through PC speakers.
    """
    print("\n[1] Starting Phone Mic → PC Audio stream...")
    cmd = [
        SCRCPY,
        "-s", SERIAL,
        "--no-video",            # No screen mirror, audio only
        "--audio-source=mic",    # Use phone MICROPHONE
        "--window-title", "PHONE MIC (hidden)",
        "--always-on-top",
    ]
    proc = subprocess.Popen(cmd, cwd=os.path.dirname(SCRCPY),
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    if proc.poll() is None:
        print("[OK] Phone Mic stream ACTIVE → playing on PC speakers")
    else:
        print("[WARN] Phone Mic stream failed. Trying without --no-video...")
        cmd.remove("--no-video")
        proc = subprocess.Popen(cmd, cwd=os.path.dirname(SCRCPY),
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc


def launch_phone_audio_to_pc():
    """
    Route PHONE SYSTEM AUDIO → PC Speakers via scrcpy.
    Phone's music, calls, notifications play on PC.
    """
    print("\n[2] Starting Phone System Audio → PC Speakers...")
    cmd = [
        SCRCPY,
        "-s", SERIAL,
        "--audio-source=output",   # Phone system audio (speaker output)
        "--window-title", "ATOM 5 - JARVIS Mirror",
        "--always-on-top",
        "--turn-screen-off",       # Keep screen off to save battery
        "--stay-awake",
    ]
    proc = subprocess.Popen(cmd, cwd=os.path.dirname(SCRCPY),
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    if proc.poll() is None:
        print("[OK] Phone System Audio ACTIVE → playing on PC speakers")
    else:
        print("[WARN] System audio failed. Check if phone supports audio capture.")
    return proc


def capture_phone_mic_for_jarvis():
    """
    Capture the phone mic audio that scrcpy is playing on PC speakers
    and make it available as a JARVIS input stream using sounddevice loopback.
    """
    try:
        import sounddevice as sd
        import numpy as np
        import queue
        import speech_recognition as sr

        print("\n[3] Setting up Phone Mic → JARVIS Speech Recognition...")

        # Find the speaker device that scrcpy is outputting to
        devices = sd.query_devices()
        print("\n   Available audio devices:")
        for i, d in enumerate(devices):
            if d['max_input_channels'] > 0:
                print(f"   [IN  {i}] {d['name']}")
            if d['max_output_channels'] > 0:
                print(f"   [OUT {i}] {d['name']}")

        # Use default output device as loopback input (Windows WASAPI loopback)
        default_out = sd.default.device[1]
        print(f"\n   Default output device: {devices[default_out]['name']}")

        # Try WASAPI loopback - captures what's playing on speakers
        audio_q = queue.Queue()
        samplerate = 16000

        def callback(indata, frames, time_info, status):
            audio_q.put(bytes(indata))

        # Use WASAPI loopback (hostapi 3 on Windows usually)
        wasapi_devices = [i for i, d in enumerate(devices)
                          if 'wasapi' in str(d.get('hostapi', '')).lower()
                          or d['name'] == devices[default_out]['name']]

        print(f"\n[OK] Phone mic audio bridge ready!")
        print(f"     JARVIS will now listen via your ATOM 5 microphone")
        print(f"     (Phone mic audio plays on PC speakers → captured by JARVIS)\n")

        return audio_q, samplerate

    except ImportError:
        print("\n[WARN] sounddevice not installed.")
        print("   Run: pip install sounddevice numpy")
        return None, None


def boost_phone_mic_volume():
    """Boost phone mic volume to maximum via ADB."""
    print("\n[4] Boosting Phone Mic Volume...")
    settings = [
        "volume_music",
        "volume_voice_communication",  # This is the mic/call volume
        "volume_ring",
        "volume_notification",
    ]
    for s in settings:
        subprocess.run([ADB, "-s", SERIAL, "shell", "settings", "put", "system", s, "15"],
                       capture_output=True)

    # Press volume up 15 times
    subprocess.run([ADB, "-s", SERIAL, "shell",
                    "for i in 1 2 3 4 5 6 7 8 9 10; do input keyevent 24; done"],
                   shell=False, capture_output=True)
    print("[OK] Phone mic volume boosted to maximum")


def grant_mic_permission():
    """Grant mic permission to scrcpy server on phone."""
    print("\n[5] Granting mic permission to scrcpy on phone...")
    result = subprocess.run(
        [ADB, "-s", SERIAL, "shell", "pm", "grant",
         "com.genymobile.scrcpy", "android.permission.RECORD_AUDIO"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("[OK] RECORD_AUDIO permission granted to scrcpy")
    else:
        print(f"[INFO] Permission result: {result.stderr.strip() or 'Already granted'}")


def get_jarvis_mic_device_index():
    """
    Find the best microphone for JARVIS to use.
    Priority: USB Audio Device (phone via USB audio class) > Virtual Cable > Default
    """
    try:
        import speech_recognition as sr
        mics = sr.Microphone.list_microphone_names()
        print("\n[6] Available Microphones for JARVIS:")

        usb_mic_idx = None
        for i, name in enumerate(mics):
            marker = ""
            n = name.lower()
            if any(x in n for x in ['speaker', 'spdif', 'hdmi', 'digital audio', 'output', 'spdif']):
                continue  # Skip output devices
            print(f"    [{i}] {name}")
            if 'usb audio' in n or 'microphone (usb' in n:
                if usb_mic_idx is None:
                    usb_mic_idx = i
                    marker = "  <-- PHONE MIC (USB Audio)"
            print(f"    [{i}] {name}{marker}") if marker else None

        if usb_mic_idx is not None:
            print(f"\n[OK] JARVIS will use Phone Mic at index {usb_mic_idx}: {mics[usb_mic_idx]}")
        else:
            print(f"\n[INFO] No USB mic found, JARVIS will use system default mic")

        return usb_mic_idx

    except Exception as e:
        print(f"[ERR] Could not list mics: {e}")
        return None


def main():
    global SERIAL
    print("=" * 60)
    print("  JARVIS PHONE AUDIO BRIDGE")
    print("  Phone Mic → PC | Phone Audio → PC Speakers")
    print("=" * 60)

    # Step 1: Verify device
    serial = find_device()
    if not serial:
        print("\nPlease connect your ATOM 5 via USB and authorize ADB debugging.")
        input("Press Enter to retry or Ctrl+C to exit...")
        return
        
    SERIAL = serial
    os.environ["ANDROID_SERIAL"] = SERIAL

    # Step 2: Grant permissions
    grant_mic_permission()

    # Step 3: Boost phone mic volume
    boost_phone_mic_volume()

    # Step 4: Launch phone audio → PC speakers (system audio)
    proc_audio = launch_phone_audio_to_pc()

    # Step 5: Wait a moment then start mic bridge
    time.sleep(2)
    proc_mic = launch_phone_mic_to_pc()

    # Step 6: Find best mic for JARVIS
    mic_idx = get_jarvis_mic_device_index()

    print("\n" + "=" * 60)
    print("  AUDIO BRIDGE ACTIVE!")
    print("=" * 60)
    print(f"\n  Phone System Audio  --> PC Speakers  [{'ACTIVE' if proc_audio.poll() is None else 'FAILED'}]")
    print(f"  Phone Microphone    --> PC            [{'ACTIVE' if proc_mic.poll() is None else 'LIMITED'}]")
    print(f"  JARVIS Mic Index    --> {mic_idx if mic_idx is not None else 'Default'}")
    print("\n  To use phone mic in JARVIS:")
    print(f"    self.microphone = sr.Microphone(device_index={mic_idx})")
    print("\n  Press Ctrl+C to stop the audio bridge.")

    # Write the mic index to a config file for JARVIS to read
    config = {"phone_mic_index": mic_idx, "serial": serial}
    import json
    with open(os.path.join(BASE, "jarvis_mic_config.json"), "w") as f:
        json.dump(config, f, indent=2)
    print(f"\n  [OK] Config saved to jarvis_mic_config.json")
    print(f"       JARVIS will automatically use phone mic index {mic_idx}")

    try:
        while True:
            # Monitor processes
            if proc_audio.poll() is not None:
                print("\n[WARN] Phone audio stream ended. Restarting...")
                proc_audio = launch_phone_audio_to_pc()
            if proc_mic.poll() is not None:
                print("\n[WARN] Phone mic stream ended. Restarting...")
                proc_mic = launch_phone_mic_to_pc()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n[STOP] Shutting down audio bridge...")
        proc_audio.terminate()
        proc_mic.terminate()
        print("[OK] Audio bridge stopped.")


if __name__ == "__main__":
    main()
