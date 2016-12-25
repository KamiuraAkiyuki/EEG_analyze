# -*- coding: utf-8 -*-

import wave
import numpy as np 
import struct
import matplotlib.pyplot as plt
import time

def create_sin_wave(A, f0, fs, times):
    # 振幅A、基本周波数f0, サンプリング周波数fs, 持続時間times(s)の正弦波を作成して返す
    data = [] # [-1.0, 1.0]の小数値が入った波を格納
    # サンプリング
    for n in np.arange(times * fs):
        s = A * np.sin(2 * np.pi * f0 * n / fs)
        if s > 1.0: s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
    # 振幅
    data = [int(x * 32767.0) for x in data]

    data = struct.pack("h" * len(data), *data)
    return data 

def create_am_wave(A, f0, fc, fs, duration):
    time_s = [] # time(second)
    data = []  # wave data

    for n in np.arange(duration * fs):
        s = (A * (1  + np.sin(2 * np.pi * f0 * n / fs))/2.0) * np.sin(2 * np.pi * fc * n / fs) 
        if s > 1.0: s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
        time_s.append((n+1) / fs)

    data = [ x * 32767.0 for x in data ]

    # 表示
    # plt.title = "AM modulated wave"
    # plt.xlabel = "time(s)"
    # plt.ylabel = "amplitude"
    # plt.xlim(0, 5.0 / f0)
    # plt.plot(time_s, data, label="sound", color="blue")
    # plt.show()

    data = struct.pack("h" * len(data), *data)
    return data

def play(data, fs, bit):
    import pyaudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=int(fs), output= True)
    chunk = 1024
    sp = 0
    buffer = data[sp:sp+chunk]
    while buffer != '':
        stream.write(buffer)
        sp = sp + chunk
        buffer = data[sp:sp+chunk]
    stream.close()
    p.terminate()

def save(data, fs, bit, filename):
    # 波形データをwavファイルに出力
    wf = wave.open(filename, "w")
    wf.setnchannels(1)
    wf.setsampwidth(bit / 8)
    wf.setframerate(fs)
    wf.writeframes(data)
    wf.close()

if __name__=='__main__':
    all_data = ""
    freqlist = [40]
    freqlist = [x/2.0 for x in freqlist]
    print "----- start -----"
    for f in freqlist:
        if f >= 0: data = create_sin_wave(1.0, f, 8000.0, 10)
        else: data = create_sin_wave(0.0, 1, 8000.0, 10)
        start = time.time()
        play(data, 8000, 16)
        elapsed_time = time.time() - start
        print "elased_time:{0}".format(elapsed_time) + "[sec]"
        all_data += data
    save(all_data, 8000, 16, "sine/sine.wav")

