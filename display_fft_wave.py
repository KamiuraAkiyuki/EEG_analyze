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
    electrodes = ['o1', 'o2']
    eeg = EEG()
    eeg.import_data('datas/19950305-alpha-27.10.16-15.27.48.csv', electrodes)
    eeg.remove_dc_offset()