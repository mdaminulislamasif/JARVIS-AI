"""
JARVIS PC MIC TO PHONE STREAMER
===============================
Streams PC microphone audio to Android phone over USB (via ADB reverse) or Wi-Fi.
Plays PC mic audio directly out of the phone speakers / system audio.

How to use:
  1. Run this script: python pc_mic_streamer.py
  2. Forward port via ADB: adb reverse tcp:8010 tcp:8010
  3. On the phone, open Google Chrome (or VLC) and visit: http://localhost:8010
  4. The PC microphone audio will stream live to the phone!
"""

import pyaudio
import socket
import threading
import sys
import os
import numpy as np

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
PORT = 8010
GAIN_FACTOR = 3.0  # 3x volume boost for clear sound

def get_wav_header(sample_rate, bits_per_sample, channels):
    """Generate a 44-byte WAV header with maximum file size for infinite streaming."""
    header = bytearray(44)
    header[0:4] = b'RIFF'
    header[4:8] = b'\xff\xff\xff\xff'  # infinite data size
    header[8:12] = b'WAVE'
    header[12:16] = b'fmt '
    header[16:20] = b'\x10\x00\x00\x00'  # subchunk1size (16)
    header[20:22] = b'\x01\x00'  # audio format (1 = PCM)
    header[22:24] = channels.to_bytes(2, 'little')
    header[24:28] = sample_rate.to_bytes(4, 'little')
    header[28:32] = (sample_rate * channels * (bits_per_sample // 8)).to_bytes(4, 'little')
    header[32:34] = (channels * (bits_per_sample // 8)).to_bytes(2, 'little')
    header[34:36] = bits_per_sample.to_bytes(2, 'little')
    header[36:40] = b'data'
    header[40:44] = b'\xff\xff\xff\xff'  # infinite data size
    return bytes(header)

def start_server():
    p = pyaudio.PyAudio()
    
    # Auto-detect working input device index
    best_idx = None
    preferred_keywords = ['usb audio', 'usb mic', 'microphone (usb', 'headset', 'external']
    for i in range(p.get_device_count()):
        try:
            info = p.get_device_info_by_index(i)
            if info.get('maxInputChannels', 0) > 0:
                name_lower = info.get('name', '').lower()
                if any(x in name_lower for x in ['speaker', 'spdif', 'hdmi', 'digital audio', 'output']):
                    continue
                if any(kw in name_lower for kw in preferred_keywords):
                    best_idx = i
                    break
        except Exception:
            pass
            
    if best_idx is None:
        for i in range(p.get_device_count()):
            try:
                info = p.get_device_info_by_index(i)
                if info.get('maxInputChannels', 0) > 0:
                    name_lower = info.get('name', '').lower()
                    if any(x in name_lower for x in ['speaker', 'spdif', 'hdmi', 'digital audio', 'output']):
                        continue
                    best_idx = i
                    break
            except Exception:
                pass

    if best_idx is not None:
        try:
            device_name = p.get_device_info_by_index(best_idx).get('name')
            print(f"[INFO] Auto-detected working microphone index {best_idx}: {device_name}")
        except Exception:
            pass
    
    # Try to open microphone input stream
    stream = None
    rate_to_use = RATE
    rates_to_try = [48000, 44100, 16000]
    
    if best_idx is not None:
        try:
            device_info = p.get_device_info_by_index(best_idx)
            default_rate = int(device_info.get('defaultSampleRate', 0))
            if default_rate > 0 and default_rate not in rates_to_try:
                rates_to_try.insert(0, default_rate)
        except Exception:
            pass
            
    for r in rates_to_try:
        try:
            if best_idx is not None:
                stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=r,
                                input=True,
                                input_device_index=best_idx,
                                frames_per_buffer=CHUNK)
            else:
                stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=r,
                                input=True,
                                frames_per_buffer=CHUNK)
            rate_to_use = r
            print(f"[OK] Microphone initialized successfully at {r}Hz.")
            break
        except Exception:
            continue

    if stream is None:
        print("[ERR] Failed to open PC Microphone after trying all sample rates.")
        p.terminate()
        return

    # Start TCP socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('0.0.0.0', PORT))
        server_socket.listen(5)
        print(f"[INFO] PC Mic HTTP Streamer running on port {PORT}...")
        print(f"[INFO] To connect via ADB, run: adb reverse tcp:{PORT} tcp:{PORT}")
        print(f"[INFO] Then open Chrome/VLC on the phone and visit: http://localhost:{PORT}")
    except Exception as e:
        print(f"[ERR] Failed to bind server socket: {e}")
        stream.stop_stream()
        stream.close()
        p.terminate()
        return

    clients = []
    lock = threading.Lock()

    def handle_client(conn, addr):
        print(f"[+] Client connected from {addr}")
        try:
            # Receive HTTP request headers
            request = conn.recv(1024)
            if b"GET " in request:
                # Send HTTP WAV streaming response
                http_headers = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: audio/wav\r\n"
                    "Connection: keep-alive\r\n"
                    "Pragma: no-cache\r\n"
                    "Cache-Control: no-cache\r\n\r\n"
                )
                conn.sendall(http_headers.encode('utf-8'))
                conn.sendall(get_wav_header(rate_to_use, 16, CHANNELS))
                
                with lock:
                    clients.append(conn)
                    
                # Keep socket alive by listening for disconnects
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
        except Exception:
            pass
        finally:
            print(f"[-] Client disconnected from {addr}")
            with lock:
                if conn in clients:
                    clients.remove(conn)
            conn.close()

    def accept_connections():
        while True:
            try:
                conn, addr = server_socket.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
            except Exception:
                break

    threading.Thread(target=accept_connections, daemon=True).start()

    print("\n[OK] Audio streaming active! Speak into your PC mic to test.")
    print("Press Ctrl+C to stop streaming.")

    try:
        while True:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                # Apply dynamic Automatic Gain Control (AGC)
                audio_array = np.frombuffer(data, dtype=np.int16)
                max_amp = np.max(np.abs(audio_array))
                if max_amp > 100:  # Threshold to avoid over-amplifying background silence
                    target_peak = 30000
                    dynamic_gain = target_peak / max_amp
                    # Keep gain within a high-sensitivity range (1.0x to 12.0x boost)
                    dynamic_gain = min(max(dynamic_gain, 1.0), 12.0)
                else:
                    dynamic_gain = 1.0
                
                boosted_array = np.clip(audio_array * dynamic_gain, -32768, 32767).astype(np.int16)
                data = boosted_array.tobytes()
            except Exception:
                continue
                
            # Broadcast PCM audio chunk to all active HTTP clients
            with lock:
                disconnected = []
                for client in clients:
                    try:
                        client.sendall(data)
                    except Exception:
                        disconnected.append(client)
                for client in disconnected:
                    if client in clients:
                        clients.remove(client)
                        try:
                            client.close()
                        except Exception:
                            pass
    except KeyboardInterrupt:
        print("\n[INFO] Stopping streamer...")
    finally:
        server_socket.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("[OK] Streamer stopped.")

if __name__ == "__main__":
    start_server()
