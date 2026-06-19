@echo off
chcp 65001 >nul
cd /d "C:\Users\asifg\OneDrive\Desktop\ai"
echo.
echo ================================================================
echo   JARVIS MICROPHONE DIAGNOSTIC AND FIX
echo ================================================================
echo.
python -c "
import sys, os
sys.path.insert(0, '.')

print('=== Step 1: Checking speech_recognition ===')
try:
    import speech_recognition as sr
    print('OK: speech_recognition installed')
except:
    print('MISSING: Installing...')
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'SpeechRecognition', 'pyaudio', '-q'])
    import speech_recognition as sr
    print('OK: Installed!')

print()
print('=== Step 2: Checking PyAudio ===')
try:
    import pyaudio
    pa = pyaudio.PyAudio()
    print('OK: PyAudio working')
    
    print()
    print('=== Step 3: Available Microphones ===')
    for i in range(pa.get_device_count()):
        dev = pa.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print(f'  [{i}] {dev[\"name\"]} (input channels: {dev[\"maxInputChannels\"]})')
    pa.terminate()
except ImportError:
    print('MISSING PyAudio! Installing...')
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyaudio', '-q'])
    print('Try again after install')
except Exception as e:
    print(f'PyAudio Error: {e}')

print()
print('=== Step 4: Testing Default Microphone ===')
try:
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 1.0
    r.dynamic_energy_threshold = True
    
    mic = sr.Microphone()
    with mic as source:
        print('Microphone opened successfully!')
        print('Calibrating...')
        r.adjust_for_ambient_noise(source, duration=1)
        print(f'Energy threshold: {r.energy_threshold:.0f}')
        print()
        print('>>> 5 seconds e kotha bolun...')
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print('Audio captured!')
            try:
                text = r.recognize_google(audio, language='bn-BD')
                print(f'Recognized (Bangla): {text}')
            except:
                try:
                    text = r.recognize_google(audio, language='en-US')
                    print(f'Recognized (English): {text}')
                except sr.UnknownValueError:
                    print('Could not understand audio (but mic IS working!)')
                except sr.RequestError as e:
                    print(f'Google API error: {e}')
        except sr.WaitTimeoutError:
            print('No speech detected (but mic IS working!)')
            print('HINT: Speak louder or check mic volume in Windows')
except OSError as e:
    print(f'MIC ERROR: {e}')
    print()
    print('=== SOLUTIONS ===')
    print('1. Windows Settings > Privacy > Microphone > Allow apps')
    print('2. Sound Settings > Input device select koren')
    print('3. Device Manager e mic check koren')
" 2>&1
echo.
echo ================================================================
echo   Done! Check results above
echo ================================================================
pause
