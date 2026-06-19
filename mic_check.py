#!/usr/bin/env python3
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

results = []

# Step 1: Check packages
print("=== Checking packages ===")
try:
    import speech_recognition as sr
    print("[OK] speech_recognition")
except ImportError:
    print("[INSTALLING] speech_recognition...")
    subprocess.run([sys.executable, "-m", "pip", "install", "SpeechRecognition", "-q"])
    import speech_recognition as sr
    print("[OK] speech_recognition installed")

try:
    import pyaudio
    print("[OK] pyaudio")
except ImportError:
    print("[INSTALLING] pyaudio...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyaudio", "-q"])
    try:
        import pyaudio
        print("[OK] pyaudio installed")
    except:
        # Try pipwin
        print("[TRY] pipwin...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pipwin", "-q"])
        subprocess.run([sys.executable, "-m", "pipwin", "install", "pyaudio", "-q"])
        import pyaudio
        print("[OK] pyaudio via pipwin")

# Step 2: List microphones
print("\n=== Available Microphones ===")
try:
    import pyaudio
    pa = pyaudio.PyAudio()
    found_mics = []
    for i in range(pa.get_device_count()):
        dev = pa.get_device_info_by_index(i)
        if dev["maxInputChannels"] > 0:
            found_mics.append((i, dev["name"]))
            print(f"  [{i}] {dev['name']}")
    pa.terminate()
    if not found_mics:
        print("  NO microphones found!")
        results.append("NO_MIC")
    else:
        results.append("MIC_FOUND")
except Exception as e:
    print(f"  PyAudio error: {e}")
    results.append("PYAUDIO_ERROR")

# Step 3: Test mic
print("\n=== Testing Microphone ===")
try:
    r = sr.Recognizer()
    r.energy_threshold = 200
    r.pause_threshold = 1.5
    r.dynamic_energy_threshold = True
    
    mic = sr.Microphone()
    with mic as source:
        print("[OK] Microphone opened!")
        print("Calibrating ambient noise (1 second)...")
        r.adjust_for_ambient_noise(source, duration=1)
        print(f"Energy threshold: {r.energy_threshold:.0f}")
        results.append("MIC_OK")
        print("\n>>> 4 second er modhye kotha bolun...")
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=8)
            print("[OK] Audio captured!")
            
            # Try Bangla first
            for lang in ["bn-BD", "en-US", "en-IN"]:
                try:
                    text = r.recognize_google(audio, language=lang)
                    print(f"[OK] Recognized ({lang}): {text}")
                    results.append("RECOGNITION_OK")
                    break
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print(f"[ERR] Google API: {e}")
                    results.append("API_ERROR")
                    break
            else:
                print("[WARN] Could not recognize speech but mic works!")
                results.append("MIC_OK_NO_SPEECH")
        except sr.WaitTimeoutError:
            print("[WARN] No speech in 4 seconds — mic works but no sound detected")
            print("       Check: mic volume, not muted, correct device selected")
            results.append("TIMEOUT")

except OSError as e:
    print(f"[ERR] Mic OSError: {e}")
    results.append("OS_ERROR")
    print("\n=== FIXES TO TRY ===")
    print("1. Windows Settings > Privacy & Security > Microphone")
    print("   'Let apps access your microphone' = ON")
    print("2. Sound Settings > Input: correct device select করুন")
    print("3. Mic কি muted আছে? Volume check করুন")

except Exception as e:
    print(f"[ERR] Unexpected error: {e}")
    results.append("UNKNOWN_ERROR")

# Save results
with open("mic_check_result.txt", "w") as f:
    f.write("\n".join(results))
    f.write(f"\n\nAll results: {results}")

print(f"\n=== SUMMARY: {results} ===")
print("Result saved to: mic_check_result.txt")
