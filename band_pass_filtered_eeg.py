# -*- coding: utf-8 -*-

import glob
import re
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from EEGData import *
from EEGAnalyze import *
from FileSelect import *

if __name__== '__main__':
    # ファイル一覧
    print_matched_files('datas/', r".*\.csv")

    # EEGでーた取得
    electrodes = ['o1', 'o2']
    eeg = EEG()
    eeg.import_data('datas/19950305-alpha-27.10.16-15.27.48.csv', electrodes)
    eeg.remove_dc_offset()
    # eeg.normalize('o1')
    # eeg.normalize('o2')

    y = FIR_band_pass_filter(eeg.o2, 7.0, 13.0, eeg.sampling_rate, 255)

    N = 512 # FFTのサンプル数
    hanning_window = np.hanning(N)

    print("o2 length = " + str(len(eeg.o2)))
    O2 = np.fft.fft(eeg.o2[0:N])
    Y = np.fft.fft(y[0:N])
    spectrum_O2 = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in O2]
    spectrum_Y = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in Y]
    freq_list = np.fft.fftfreq(N, d=1.0/eeg.sampling_rate)

    plt.subplot(2, 2, 1)
    plt.plot(eeg.time, eeg.o2)

    plt.subplot(2, 2, 2)
    plt.plot(eeg.time, y)

    plt.subplot(2, 2, 3)
    plt.xlim(0, 64)
    # plt.ylim(0, 30)
    plt.plot(freq_list, spectrum_O2)

    plt.subplot(2, 2, 4)
    plt.xlim(0, 64)
    # plt.ylim(0, 30)
    plt.plot(freq_list, spectrum_Y)

    plt.show()