# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt

from EEGData import *
from EEGAnalyze import *
from FileSelect import *

if __name__=="__main__":
    # ファイル一覧
    # eeg_data_path = select_csv_file()

    # EEGデータ取得
    electrodes = ['o1', 'o2']
    eeg = EEG()
    eeg.import_data('datas/19950305-alpha-27.10.16-15.27.48.csv', electrodes)
    eeg.remove_dc_offset()

    electrode_data = eeg.o2

    # electrode data spectrum
    start = 0
    N = 512
    electrode_amplitude_spectrum, electrode_freq_list = fft_amplitude_spectrum(electrode_data[start: start + N], N, eeg.sampling_rate)

    # normalize amplitude
    normalized_amp_data = electrode_data / np.max([abs(x) for x in electrode_data])

    # normalized fft spectrum
    normalized_amplitude_spectrum, normalized_freq_list = fft_amplitude_spectrum(normalized_amp_data[start: start + N], N, eeg.sampling_rate)

    plt.subplot(2, 2, 1)
    plt.plot(eeg.time, electrode_data)

    plt.subplot(2, 2, 2)
    plt.plot(electrode_freq_list, electrode_amplitude_spectrum)
    plt.xlim(0,)

    plt.subplot(2, 2, 3)
    plt.plot(eeg.time, normalized_amp_data)

    plt.subplot(2, 2, 4)
    plt.plot(normalized_freq_list, normalized_amplitude_spectrum)
    plt.xlim(0, )

    plt.show()