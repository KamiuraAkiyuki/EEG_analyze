# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy as np
import glob
import re

from EEGData import *

if __name__=="__main__":
    # ファイル一覧
    print(get_matched_files('datas/', r".+\.csv"))
    print(get_matched_files('datas/', r".+\.edf"))

    # EEGデータのインポート
    electrodes = ['af3', 'o2']
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
    mode:0 - 全体でのスペクトログラム
    mode:1 - 開眼, 閉眼別のスペクトログラム
    mode:2 - 開眼, 閉眼別の周波数分析
    """
    mode = 0
    if (mode == 0) :
        """
          波形の表示
        """
        # plt.subplot(2, 1, 1)
        # plt.title("EEG-data")
        # plt.xlabel("time [second]")
        # plt.ylabel("voltage [V]")
        # plt.plot(eeg.time, eeg.o2, label="o2", color="green")
        # plt.ylim(-500, 500)
        # plt.legend(fontsize=18)
        # plt.tick_params(labelsize=18)

        # plt.subplot(3, 1, 2)
        # plt.xlabel("time [second]")
        # plt.ylabel("trigger")
        # plt.plot(eeg.time, eeg.trigger)
        # plt.ylim(-0.1, 1.1)
        # plt.legend()

        """ 
          スペクトログラムの表示 
        """
        # plt.subplot(2, 1, 2)
        pxx, freqs, bins, im = plt.specgram(eeg.o2, NFFT=N, Fs=128, noverlap=0, window=hammingWindow)
        plt.xlabel("time [second]", fontsize=18)
        plt.ylabel("frequency [Hz]", fontsize=18)
        plt.ylim(0, 20)
        plt.legend(fontsize=18)
        plt.tick_params(labelsize=18)
        plt.savefig("specgram.png", transparent=True)

        plt.show()
    elif (mode == 1):
        open_eyes_o2 = []
        open_eyes_time = []
        closed_eyes_o2 = []
        closed_eyes_time = []

        # 開眼 -> 閉眼 -> 開眼 -> ...
        t_index = 0
        for ei in range(eeg.trigger.count(1)):
            if (ei == 0):
                next_index = t_index + eeg.trigger[t_index:].index(1)
            elif (ei == eeg.trigger.count(1) - 1):
                next_index = len(eeg.trigger)
            else:
                next_index = t_index + 1 + eeg.trigger[t_index + 1:].index(1)


            if (ei%2): # 閉眼 
                closed_eyes_o2.extend(eeg.o2[t_index: next_index - 1])
                closed_eyes_time.extend(eeg.time[t_index: next_index - 1])
            else: # 開眼
                open_eyes_o2.extend(eeg.o2[t_index: next_index - 1])
                open_eyes_time.extend(eeg.time[t_index: next_index - 1])
                
            t_index = next_index 

            if (t_index < len(eeg.trigger)):
                while (1):
                    if (eeg.trigger[t_index] == 1.0): 
                        t_index += 1
                    else: 
                        break

        # plt.subplot(4, 1, 1)
        plt.title('o2', fontsize=18)
        plt.xlabel('time [second]', fontsize=18)
        plt.ylabel('voltage', fontsize=18)
        plt.plot(open_eyes_time, open_eyes_o2, label="open eyes", color='green')
        plt.plot(closed_eyes_time, closed_eyes_o2, label="closed eyes", color='blue')
        plt.legend(fontsize=18)
        plt.tick_params(labelsize=18)

        # plt.subplot(4, 1, 2)
        # plt.title('trigger timing')
        # plt.xlabel('time [second]')
        # plt.ylabel('trigger')
        # plt.plot(eeg.time, eeg.trigger, color='black')
        # plt.legend()

        # plt.subplot(4, 1, 3)
        # plt.title('open eyes')
        # ppxx, freqs, bins, im = plt.specgram(open_eyes_o2, NFFT=N, Fs=128, noverlap=0, window=hammingWindow)
        # plt.xlabel("time [second]")
        # plt.ylabel("frequency [Hz]")
        # plt.ylim(0, 64)
        # plt.legend()

        # plt.subplot(4, 1, 4)
        # plt.title('close eyes')
        # ppxx, freqs, bins, im = plt.specgram(closed_eyes_o2, NFFT=N, Fs=128, noverlap=0, window=hammingWindow)
        # plt.xlabel("time [second]")
        # plt.ylabel("frequency [Hz]")
        # plt.ylim(0, 64)
        # plt.legend()
        plt.savefig("alpha-eeg-data.png", transparent=True)

        plt.show()
    elif (mode == 2): 
        open_eyes_o2 = []
        open_eyes_time = []
        closed_eyes_o2 = []
        closed_eyes_time = []

        # 開眼 -> 閉眼 -> 開眼 -> ...
        t_index = 0
        for ei in range(eeg.trigger.count(1)):
            if (ei == 0):
                next_index = t_index + eeg.trigger[t_index:].index(1)
            elif (ei == eeg.trigger.count(1) - 1):
                next_index = len(eeg.trigger)
            else:
                next_index = t_index + 1 + eeg.trigger[t_index + 1:].index(1)


            if (ei%2): # 閉眼 
                closed_eyes_o2.extend(eeg.o2[t_index: next_index - 1 - 128])
                closed_eyes_time.extend(eeg.time[t_index: next_index - 1])
            else: # 開眼
                open_eyes_o2.extend(eeg.o2[t_index: next_index - 1 - 128])
                open_eyes_time.extend(eeg.time[t_index: next_index - 1])
                
            t_index = next_index 

            if (t_index < len(eeg.trigger)):
                while (1):
                    if (eeg.trigger[t_index] == 1.0): 
                        t_index += 1
                    else: 
                        break

        N = 8192
        print(len(open_eyes_o2))
        hamming_window = np.hamming(N)
        freq_list = np.fft.fftfreq(N, d=1.0/eeg.sampling_rate)

        windowed_open_eyes_o2 = hamming_window * open_eyes_o2[0:N]
        windowed_open_eeg_spectrum = np.fft.fft(windowed_open_eyes_o2)
        windowed_open_eeg_amplitude = [ np.sqrt(c.real ** 2 + c.imag ** 2) for c in windowed_open_eeg_spectrum ]

        windowed_closed_eyes_o2 = hamming_window * closed_eyes_o2[0:N]
        windowed_closed_eeg_spectrum = np.fft.fft(windowed_closed_eyes_o2)
        windowed_closed_eeg_amplitude = [ np.sqrt(c.real ** 2 + c.imag ** 2) for c in windowed_closed_eeg_spectrum ]

        plt.plot(freq_list, windowed_closed_eeg_amplitude, label="open eyes", color='green')
        plt.plot(freq_list, windowed_open_eeg_amplitude, label="closed eyes", color='blue')
        plt.xlabel("frequency [Hz]", fontsize=18)
        plt.ylabel("amplitude spectrum", fontsize=18)
        plt.xlim(0, 64)
        plt.legend(fontsize=18)
        plt.tick_params(labelsize=18)
        plt.savefig("amplitude-spectrum.png", transparent=True)

