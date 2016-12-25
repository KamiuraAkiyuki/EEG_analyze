# -*- coding: utf-8 -*-

import glob
import re
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from EEGData import *

if __name__== '__main__':
    files = glob.glob('datas/*')
    csv_files = [file for file in files if re.match(r".+\.csv", file)]
    edf_files = [file for file in files if re.match(r".+\.edf", file)]
    print(csv_files)
    print(edf_files)

    electrodes = ['o1', 'o2']
    eeg = EEG()
    eeg.import_data('datas/19950305-alpha-27.10.16-15.27.48.csv', electrodes)
    eeg.remove_dc_offset()
    eeg.normalize('o1')
    eeg.normalize('o2')

    nyquist_frequency = eeg.sampling_rate / 2.0  # ナイキスト周波数
    fc1 = 7.0 / nyquist_frequency
    fc2 = 13.0 / nyquist_frequency
    numtaps = 255  # フィルタ係数の数

    b = scipy.signal.firwin(numtaps, [fc1, fc2], pass_zero=False)
    y = scipy.signal.lfilter(b, 1, eeg.o2)

    plt.subplot(2, 2, 1)
    plt.plot(eeg.time, eeg.o2)
    plt.show()