# coding: utf-8

import wave
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal

from EEGData import *
from EEGAnalyze import *
from FileSelect import *

if __name__=="__main__":
    wav_path = "wav_data/"
    audio_path = wav_path + "tirutiru.wav"
    wav_file = wave.open(audio_path, 'rb')

    print(wav_file.getnchannels())
    print(wav_file.getframerate())
    print(wav_file.getnframes())
    print(wav_file.getparams())

    frame_rate = wav_file.getframerate()
    time = [x/frame_rate for x in range(wav_file.getnframes())]

    data = wav_file.readframes(wav_file.getnframes()) #frameの読み込み
    data = np.frombuffer(data, dtype= "int16") #numpy.arrayに変換
    # data = FIR_high_pass_filter(data, 100, 128)
    frame_data = wav_file.getframerate()

    time = time[:2*int(frame_rate/2)]
    data = data[:2*int(frame_rate/2)]

    envelope = abs(signal.hilbert(data))
    N = 64
    hammingWindow = np.hamming(N)
    

    plt.subplot(2, 1, 1)
    plt.plot(time, data)
    plt.plot(time, envelope)
    plt.grid()

    plt.subplot(2, 1, 2)
    pxx, freqs, bins, im = plt.specgram(envelope, NFFT=N, Fs=128, noverlap=0, window=hammingWindow)
    plt.plot()
    plt.savefig("spectrogram.png", transparent=True)
    plt.show()

    wav_file.close()