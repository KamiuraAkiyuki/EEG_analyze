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

    filepath = 'datas/19950305-eyeblink-27.10.16-15.18.06.csv' 
    electrodes = ['af3', 'f7', 'f3', 'fc5', 't7', 'p7', 'o1', 'o2', 'p8', 't8', 'fc6', 'f4', 'f8', 'af4']
    eeg = EEG()
    eeg.import_data(filepath, electrodes)
    eeg.remove_dc_offset()

    plt.subplot(7, 2, 1)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.af3, label="af3", color="blue")

    plt.subplot(7, 2, 2)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.f7, label="f7")

    plt.subplot(7, 2, 3)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.f3, label="f3")

    plt.subplot(7, 2, 4)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.fc5, label="fc5")

    plt.subplot(7, 2, 5)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.t7, label="t7")

    plt.subplot(7, 2, 6)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.p7, label="p7")

    plt.subplot(7, 2, 7)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.o1, label="o1")

    plt.subplot(7, 2, 8)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.af4, label="af4")

    plt.subplot(7, 2, 9)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.f8, label="f8")

    plt.subplot(7, 2, 10)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.f4, label="f4")

    plt.subplot(7, 2, 11)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.fc6, label="fc6")

    plt.subplot(7, 2, 12)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.t8, label="t8")

    plt.subplot(7, 2, 13)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.p8, label="p8")

    plt.subplot(7, 2, 14)
    plt.xlabel("time[second]")
    plt.ylabel("voltage[V]")
    plt.plot(eeg.time, eeg.p8, label="p8")

    plt.show()
