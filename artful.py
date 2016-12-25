# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
import numpy as np

from EEGData import *
from EEGAnalyze import *
from FileSelect import *

if __name__=="__main__":
    # ファイル一覧
    print(get_matched_files('datas/', r".+\.csv"))
    print(get_matched_files('datas/', r".+\.edf"))

    # データ取得
    electrodes = ['o2']
    eeg = EEG()
    eeg.import_data('datas/19950305-alpha-27.10.16-15.27.48.csv', electrodes)
    eeg.remove_dc_offset()

    channel_data = eeg.o2 # ここを変える

    # alpha, beta, theta波形が128Hzで得られる
    alpha_timewave = []
    beta_timewave = []
    theta_timewave = []
    N = 128
    for i in range(len(channel_data)-N):
        alpha_timewave.append(get_alpha_index(N, channel_data[i:i+N], eeg.sampling_rate))
        beta_timewave.append(get_beta_index(N, channel_data[i:i+N], eeg.sampling_rate))
        theta_timewave.append(get_theta_index(N, channel_data[i:i+N], eeg.sampling_rate))

    # 1Hzに平均化して, attention indexを得る
    attention_index_timewave = []
    for i in range(int(len(channel_data)/eeg.sampling_rate)):
        alpha =  np.mean(alpha_timewave[i*eeg.sampling_rate: (i+1)*eeg.sampling_rate])
        beta = np.mean(beta_timewave[i*eeg.sampling_rate: (i+1)*eeg.sampling_rate])
        theta = np.mean(theta_timewave[i*eeg.sampling_rate: (i+1)*eeg.sampling_rate])
        attention_index_timewave.append(beta / (alpha + theta))

    # 5秒ごとに中間値をとる
    median_filtered_attention_index = []
    time_1Hz = []
    for i in range(len(attention_index_timewave)):
        if i == 0:
            median_filtered_attention_index.append(attention_index_timewave[0])
        elif i < 5:
            median_filtered_attention_index.append(np.median(attention_index_timewave[:i]))
        else:
            median_filtered_attention_index.append(np.median(attention_index_timewave[i-5:i]))
        time_1Hz.append(i)

    # 移動平均をとる (EWMA: Exponential Weighted Moving Average)
    """
        S(t) = A(t)                           : t=1
               c * A(t-1) + (1-c) * S(t-1)    : t
    """
    smoothed_attention_index = []
    c = 0.2                                                                     # regularization constant
    for i in range(len(median_filtered_attention_index)):
        if i == 0:
            smoothed_attention_index.append(median_filtered_attention_index[i])
        else:
            smoothed_attention_index.append(c * median_filtered_attention_index[i-1] + (1-c) * smoothed_attention_index[i-1])

    plt.plot(time_1Hz, smoothed_attention_index)
    plt.grid()
    plt.show()
