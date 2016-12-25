# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import csv
import time
import pandas as pd

from EEGData import *
from EEGAnalyze import *
from FileSelect import *

def csv_reader(data_path):
    f = open(data_path, 'r')
    csv_data = list(csv.reader(f))
    f.close()
    return csv_data

def get_electrode_data(csv_data, csv_index):
    electrode_data = []
    for li in range(1, len(csv_data)):
        electrode_data.append(float(csv_data[li][csv_index]))
    return electrode_data

def erp_average(electrode_data, marker_data):
    electrode_data = FIR_band_pass_filter(electrode_data, 0.1, 30, 128)
    electrode_data = FIR_band_stop_filter(electrode_data, 7, 13, 128)
    # electrode_data = electrode_data[:76800]
    all_erp_data = []
    for li in range(len(electrode_data)):
        if int(marker_data[li]) == 1:
            temp = []
            if li < len(electrode_data) - 64 and li > 12:
                if max(electrode_data[li-12: li+64]) > 100.: continue
                if min(electrode_data[li-12: li+64]) < -100.: continue
                all_erp_data.append(electrode_data[li-12: li+64])
    print(np.array(all_erp_data).shape)
    averaged_erp_data = list(np.mean(np.array(all_erp_data), axis=0))

    stddev = np.std(np.array(all_erp_data), axis=0)
    upper_sigma = []
    lower_sigma = []
    for i in range(len(stddev)):
        upper_sigma.append(averaged_erp_data[i] + stddev[i])
        lower_sigma.append(averaged_erp_data[i] - stddev[i])
    return [averaged_erp_data, upper_sigma, lower_sigma]

if __name__=="__main__":

    print_matched_files('datas/', r".*\.csv")

    # 'af3=2', 'f7=3', 'f3=4', 'fc5=5', 't7=6', 'p7=7', 'o1=8', 'o2=9', 'p8=10', 't8=11', 'fc6=12', 'f4=13', 'f8=14', 'af4=15'
    electrode_index = 4

    attended_csv_data = csv_reader('datas/kawashima-auditory-erp-auditory-attended-23.12.16.16.19.12.csv')
    attended_electrode_data = get_electrode_data(attended_csv_data, electrode_index) # electrode data

    unattended_csv_data = csv_reader('datas/kawashima-auditory-erp-visual-attended-23.12.16.16.35.12.csv')
    unattended_electrode_data = get_electrode_data(unattended_csv_data, electrode_index) # electrode data

    attended_ave = np.mean(attended_electrode_data)
    unattended_ave = np.mean(unattended_electrode_data)
    ave = (attended_ave + unattended_ave)/2

    attended_electrode_data = [ x - ave for x in attended_electrode_data]
    attended_marker_data = get_electrode_data(attended_csv_data, 19) # marker
    attended_averaged_erp_data, attended_upper_sigma, attended_lower_sigma = erp_average(attended_electrode_data, attended_marker_data)

    unattended_electrode_data = [ x - ave for x in unattended_electrode_data]
    unattended_marker_data = get_electrode_data(unattended_csv_data, 19) # marker
    unattended_averaged_erp_data, unattended_upper_sigma, unattended_lower_sigma = erp_average(unattended_electrode_data, unattended_marker_data)

    time = [ i/128. for i in range(-12, 64)]

    # plt.subplot(2, 1, 1)
    plt.plot(time, attended_averaged_erp_data, label='attended', color="blue")
    plt.gca().invert_yaxis()
    # plt.plot(time, attended_upper_sigma, '--', color="blue")
    # plt.plot(time, attended_lower_sigma, '--', color="blue")
    plt.plot(time, unattended_averaged_erp_data, label='unattended', color="green")
    # plt.plot(time, unattended_upper_sigma, '--', color="green")
    # plt.plot(time, unattended_lower_sigma, '--', color="green")
    # plt.legend()
    plt.grid()

    # plt.subplot(2, 1, 2)
    # # spectrum
    # N = 64
    # hammingWindow = np.hamming(N)
    # freq_list = np.fft.fftfreq(N, d=1.0/128)
    # spectrum = np.fft.fft(hammingWindow * attended_averaged_erp_data[:N])
    # amplitude_spectrum = [ np.sqrt(c.real ** 2 + c.imag ** 2) for c in spectrum ]
    # plt.plot(freq_list, amplitude_spectrum)
    # plt.xlim(0, )
    # plt.savefig("images/oddball.png", transparent=True)
    plt.show()

