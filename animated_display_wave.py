# -*- coding: utf-8 -*- 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

from EEGData import *
from EEGAnalyze import *
from FileSelect import *

if __name__=="__main__":

    # ファイル一覧
    print(get_matched_files('datas/', r".+\.csv"))
    print(get_matched_files('datas/', r".+\.edf"))

    # EEGデータ取得
    electrodes = ['f3']
    eeg = EEG()
    eeg.import_data('datas/kawashima-auditory-erp-auditory-attended-close-20.12.16.14.23.17.csv', electrodes)
    eeg.remove_dc_offset()

    channel_data = eeg.f3  # ここを変更する

    chunk = 1024
 
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.25)
    l, = plt.plot(eeg.time[:chunk], channel_data[:chunk], lw=2, color='blue')
    plt.xlim(0, int(chunk/eeg.sampling_rate))

    axtimeslider = plt.axes([0.1, 0.1, 0.80, 0.03], axisbg='lightgoldenrodyellow')

    timeslider = Slider(axtimeslider, 'time', 0., len(eeg.time)-chunk, valinit=0.)

    def update(val):
        start_time = int(timeslider.val)
        # l.set_xdata(eeg.time[start_time:start_time+chunk])
        l.set_ydata(channel_data[start_time:start_time+chunk])
        fig.canvas.draw_idle()
        
    timeslider.on_changed(update)

    plt.show()