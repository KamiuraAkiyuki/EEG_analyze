# -*- coding: utf-8 -*-

import numpy as np 
import matplotlib.pyplot as plt 
import struct
import scipy.signal as sg
import wave

"""
    A = 1.0  # amplitude 
    f0 = 40  # fundamental frequency
    fc = 500  # carrier wave frequency
    fs = 8000.0  # sampling frequency
    duration = 10.0  # duration
"""
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
    plt.title = "AM modulated wave"
    plt.xlabel = "time(s)"
    plt.ylabel = "amplitude"
    plt.xlim(0, 5.0 / f0)
    plt.plot(time_s, data, label="sound", color="blue")
    plt.show()

    data = struct.pack("h" * len(data), *data)
    return data

def save(data, fs, bit, filename):
    # 波形データをwavファイルに出力
    wf = wave.open(filename, "w")
    wf.setnchannels(1)
    wf.setsampwidth(bit / 8)
    wf.setframerate(fs)
    wf.writeframes(data)
    wf.close()


if __name__=="__main__":
    A = 1.0  # amplitude 
    f0 = 40  # fundamental frequency
    fc = 500  # carrier wave frequency
    fs = 8000.0  # sampling frequency
    duration = 120.0  # duration

    data = create_am_wave(A, f0, fc, fs, duration)
    save(data, 8000.0, 16, "am_wave/am-500-40-sin.wav")
