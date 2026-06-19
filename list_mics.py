import pyaudio
pa = pyaudio.PyAudio()
print("Input devices:")
for i in range(pa.get_device_count()):
    d = pa.get_device_info_by_index(i)
    if d["maxInputChannels"] > 0:
        print("  [%d] %s - %dHz" % (i, d["name"], int(d["defaultSampleRate"])))
pa.terminate()
