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

    # EEGデータのインポート
    electrodes = ['p7', 'p8']
    eeg = EEG()
    eeg.import_data('datas/19950305-40Hz-ASSR-carrier-500Hz-closedeyes-31.10.16-12.44.06.csv', electrodes)
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
    plt.plot(eeg.time, eeg.p8, label="p8", color="green")
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
    pxx, freqs, bins, im = plt.specgram(eeg.p8, NFFT=N, Fs=128, noverlap=0, window=hammingWindow)
    plt.xlabel("time [second]")
    plt.ylabel("frequency [Hz]")
    plt.ylim(0, 64)

    plt.show()
