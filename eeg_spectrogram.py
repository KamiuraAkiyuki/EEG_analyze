# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy as np
import glob
import re

from EEGData import *

if __name__=="__main__":
    
    files = glob.glob('datas/*')
    csv_files = [file for file in files if re.match(r".+\.csv", file)]
    edf_files = [file for file in files if re.match(r".+\.edf", file)]
    print(csv_files)
    print(edf_files)

    electrodes = ['af3', 'o2']

    # EEGデータのインポート
    eeg = EEG()
    eeg.import_data('datas/19950305-alpha-27.10.16-15.27.48.csv', electrodes)
    eeg.remove_dc_offset()

    # 信号処理
    N = 256
    hammingWindow = np.hamming(N)
    # hanningWindow = np.hamming(N)
    # bartlettWindow = np.bartlett(N)
    # blackmanWindow = np.blackman(N)
    # kaiserWindow = np.kaiser(N, 5)

    """
        波形の表示
    """
    plt.subplot(3, 1, 1)
    plt.title("EEG-data")
    plt.xlabel("time [second]")
    plt.ylabel("voltage [V]")
    plt.plot(eeg.time, eeg.o2, label="o2", color="green")
    plt.ylim(-500, 500)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.xlabel("time [second]")
    plt.ylabel("trigger")
    plt.plot(eeg.time, eeg.trigger)
    plt.ylim(-0.1, 1.1)
    plt.legend()

    """ 
        スペクトログラムの表示 
    """
    plt.subplot(3, 1, 3)
    pxx, freqs, bins, im = plt.specgram(eeg.o2, NFFT=N, Fs=128, noverlap=0, window=hammingWindow)
    plt.xlabel("time [second]")
    plt.ylabel("frequency [Hz]")
    plt.ylim(0, 20)

    plt.show()
