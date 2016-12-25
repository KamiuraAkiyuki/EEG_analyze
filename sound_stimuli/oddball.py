# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import struct
import scipy.signal as sg
import wave
import random
from datetime import datetime
import time
import pyaudio
import csv
import sys
# import serial
# import serial.tools.list_ports

def create_random_stimuli_pattern():
    generated_sound_sections = []
    remain = 263
    for i in range(101):
        sound_section = []
        sound_section.extend([0, 0, 0])
        rand = random.randint(0, 32)
        if (remain == 0):
            pass
        elif (rand > remain):
            sound_section.extend([0 for j in range(remain)])
            remain = 0
        else:
            sound_section.extend([0 for j in range(rand)])
            remain = remain - rand
        sound_section.append(1)
        generated_sound_sections.append(sound_section)
    random.shuffle(generated_sound_sections)
    sound_list = []
    for section in generated_sound_sections:
        sound_list.extend(section)
    sound_list.pop()
    return sound_list

def create_random_stimuli_pattern2():
    random_sound_sections = [ round(np.random.chisquare(2.66)) for i in range(100) ]
    diff = np.sum(random_sound_sections) - 266
    print(diff)
    if diff < 0:
        for i in range(abs(int(diff))):
            random_sound_sections[i] += 1
    elif diff > 0:
        j = 0
        while diff > 0:
            if random_sound_sections[j] != 0:
                random_sound_sections[j] = random_sound_sections[j] - 1
                diff = diff - 1
            else:
                j += 1
    sound_list = []
    for i in range(len(random_sound_sections)):
        for j in range(3 + int(random_sound_sections[i])):
            sound_list.append(0)
        sound_list.append(1)
    return sound_list

def trapezoid_filter(fs):
    trapezoid = []
    for n in np.arange(fs * 0.01):
        trapezoid.append(n/(fs * 0.01))
    for n in np.arange(fs * 0.155):
        trapezoid.append(1)
    for n in np.arange(fs * 0.01):
        trapezoid.append(1 - n/(fs * 0.01))
    return trapezoid

def create_pi(hz):
    section_duration = 0.175
    fs = 8000
    data = []
    trapezoid = trapezoid_filter(8000)
    for n in np.arange(section_duration * fs):
        s =  trapezoid[int(n)] * np.sin(2 * np.pi * hz * n / fs)
        if s > 1.0: s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
    data = [int(x * 32767) for x in data]
    data = struct.pack("h" * len(data), *data)
    return data

def play (data, fs, bit):
    import pyaudio
    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=int(fs),
                    output= True)
    # チャンク単位でストリームに出力し音声を再生
    chunk = 1024
    sp = 0  # 再生位置ポインタ
    buffer = data[sp:sp+chunk]
    while buffer != '':
        stream.write(buffer)
        sp = sp + chunk
        buffer = data[sp:sp+chunk]
    stream.close()
    p.terminate()

if __name__=="__main__":

    # today = datetime.now().strftime('%Y-%m-%d-%H:%M')
    # f = open('oddball/' + today + '.csv', 'w')

    # csv_writer = csv.writer(f)

    random_pattern = create_random_stimuli_pattern2()

    high_tone = create_pi(1200) # struct packed data
    low_tone = create_pi(1000) # struct packed data

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=int(8000), output= True)

    # ser = serial.Serial()
    # ser.baudrate = 19200
    # ser.port = list(serial.tools.list_ports.comports())[1][0]

    # --------------------------------------- initialize end ---------------------------------------------
    print("press enter key to start: ")
    start_input = raw_input()
    time.sleep(2.0)

    for pattern in random_pattern:
        start_time = time.time()
        data = []
        # csv_row_data = []

        if pattern == 0:
            data = low_tone
            # csv_row_data.append('low')
        elif pattern == 1:
            data = high_tone
            # csv_row_data.append('high')

        chunk = 1024
        sp = 0
        stream.start_stream()
        # print(csv_row_data[0] + ": " + datetime.now().strftime("%Y/%m/%d-%H:%M:%S"))
        # csv_row_data.append(datetime.now())
        # if pattern == 0:
        #     ser.write(chr(1))
        # elif pattern == 1:
        #     ser.write(chr(2))
        buffer = data[sp:sp+chunk]
        while buffer != '':
            stream.write(buffer)
            sp = sp + chunk
            buffer = data[sp:sp+chunk]
        stream.stop_stream()

        elapsed_time = time.time() - start_time
        # soa = random.uniform(1.075 - elapsed_time, 1.275 - elapsed_time) # stimulus onset asynchrony
        soa = 1.175 - elapsed_time
        time.sleep(soa)
        # csv_writer.writerow(csv_row_data)

    stream.close()
    p.terminate()

    f.close()
