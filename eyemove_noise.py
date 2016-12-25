# -*- coding: utf-8 -*-

import glob
import re 

import csv
import numpy as np 
import matplotlib.pyplot as plt 

from EEGData import *

if __name__=='__main__':
    files = glob.glob('datas/*')
    csv_files = [file for file in files if re.match(r".+\.csv", file)]
    edf_files = [file for file in files if re.match(r".+\.edf", file)]
    print(csv_files)
    print(edf_files)

    # EEGデータのインポート
    electrodes = ['af3', 'af4', 'o1', 'o2']
    eeg = EEG()
    # eeg.import_data('datas/19950305-eyeblink-27.10.16-15.18.06.csv', electrodes)
    # eeg.import_data('datas/19950305-eyemovement-up-31.10.16-12.24.29.csv', electrodes)
    # eeg.import_data('datas/19950305-eyemovement-down-31.10.16-12.26.15.csv', electrodes)
    # eeg.import_data('datas/19950305-eyemovement-right-31.10.16-12.27.59.csv', electrodes) 
    # eeg.import_data('datas/19950305-eyemovement-left-31.10.16-12.29.49.csv', electrodes)
    eeg.import_data('datas/19950305-1-21.10.16-15.41.09.csv', electrodes)

    eeg.remove_dc_offset()

    # plt.subplot(2, 1, 1)
    plt.xlabel("time [second]", fontsize=18)
    plt.ylabel("voltage [uV]", fontsize=18)
    plt.plot(eeg.time, eeg.af3, label="af3")
    plt.plot(eeg.time, eeg.o1, label="o1")
    plt.legend(fontsize=18)
    plt.tick_params(labelsize=18)

    # plt.subplot(2, 1, 2)
    # plt.xlabel("time [second]")
    # plt.ylabel("voltage [V]")
    # plt.plot(eeg.time, eeg.af4, label="af4")
    # plt.plot(eeg.time, eeg.o2, label="o2")
    plt.savefig("images/headset_displacement.png", transparent=True)
    # plt.show()
