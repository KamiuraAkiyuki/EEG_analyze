# -*- coding: utf-8 -*- 

import sys
import pyaudio
import wave
from datetime import datetime

if __name__=="__main__":
    p = pyaudio.PyAudio()
    count = p.get_device_count()
    devices = []
    for i in range(count):
        devices.append(p.get_device_info_by_index(i))

    fs = 44100
    chunk = 1024
    record_time = 10

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, input_device_index=0, frames_per_buffer=chunk)

    frames = []
    print("----- recording start -----")
    for i in range(0, int( fs / chunk * record_time)):
        data = stream.read(chunk)
        frames.append(data)
    print("----- recording end -----")

    stream.stop_stream()
    stream.close()
    p.terminate()

    waveFile = wave.open("recorded_wav/recorded-" + datetime.now().strftime("%Y-%m-%d-%H-%M") + ".wav", 'wb')
    waveFile.setnchannels(1)
    waveFile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(fs)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()