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

    mode = 1
    if (mode == 0):
        # EEGデータのインポート
        electrodes = ['af3', 'f7']
        eeg = EEG()
        eeg.import_data('datas/19950305-eyeblink-27.10.16-15.18.06.csv', electrodes)
        eeg.remove_dc_offset()

        # plt.subplot(2, 1, 1)
        plt.xlabel("time [second]")
        plt.ylabel("voltage [V]")
        plt.plot(eeg.time, eeg.af3, label="af3", color="blue")
        plt.plot(eeg.time, eeg.f7, label="f7", color="green")
        plt.legend()

        # plt.subplot(2, 1, 2)
        # plt.xlabel("time [second]")
        # plt.ylabel("voltage [V]")
        # plt.plot(eeg.time, eeg.af4, label="af4", color="blue")
        # plt.plot(eeg.time, eeg.o2, label="o2", color="green")
        # plt.legend()

        plt.show()
    elif (mode == 1):
        electrodes = ['af3']
        eeg = EEG()
        eeg.import_data('datas/19950305-eyeblink-27.10.16-15.18.06.csv', electrodes)
        eeg.remove_dc_offset()

        local_max_indexes = []
        for i in range(int(len(eeg.time)/1024)):
            local_max_indexes.append(i*1024 + eeg.af3[i*1024: (i+1)*1024].index(max(eeg.af3[i*1024: (i+1)*1024])))

        
        for ind in local_max_indexes:
            for j in range(-20, 40):


