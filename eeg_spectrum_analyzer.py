# -*- coding: utf-8 -*-

import csv
import numpy as np
import matplotlib.pyplot as plt
import glob
import re
from EEGData import *

if __name__=='__main__':
    files = glob.glob('datas/*')
    csv_files = [file for file in files if re.match(r".+\.csv", file)]
    edf_files = [file for file in files if re.match(r".+\.edf", file)]
    print(csv_files)
    print(edf_files)

    datapath = "datas/19950305-alpha-27.10.16-15.27.48.csv"
    electrodes = ["af3", "o1", "o2", "af4"]
    eeg = EEG()
    eeg.import_data(datapath, electrodes)
    eeg.remove_dc_offset() 
    eeg.normalize('o2')

    start = 0
    N = 512

    hammingWindow = np.hamming(N)  # ハミング窓
    hanningWindow = np.hanning(N)  # ハニング窓
    blackmanWindow = np.blackman(N)  # ブラックマン窓
    bartlettWindow = np.bartlett(N)  # バートレット窓

    windowed_eeg_data = hammingWindow * eeg.af3[start: start + N]

    windowed_eeg_spectrum = np.fft.fft(windowed_eeg_data)
    freq_list = np.fft.fftfreq(N, d=1.0/eeg.sampling_rate)

    windowed_eeg_amplitude = [ np.sqrt(c.real ** 2 + c.imag ** 2) for c in windowed_eeg_spectrum ]

    plt.plot(freq_list, windowed_eeg_amplitude, marker='o', linestyle='-')
    plt.xlim(0, 64)
    plt.show()
