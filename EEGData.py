# -*- coding: utf-8 -*-

import csv
import re
import numpy as np 

class EEG():
    def __init__(self):
        self.time = []
        self.timestamp = []
        self.datetime = []
        self.af3 = []
        self.f7 = []
        self.f3 = []
        self.fc5 = []
        self.t7 = []
        self.p7 = []
        self.o1 = []
        self.o2 = []
        self.p8 = []
        self.t8 = []
        self.fc6 = []
        self.f4 = []
        self.f8 = []
        self.af4 = []
        self.marker = []
        self.electrode_list = ['af3', 'f7', 'f3', 'fc5', 't7', 'p7', 'o1', 'o2', 'p8', 't8', 'fc6', 'f4', 'f8', 'af4']
        self.valid_electrode_list = []
        self.sampling_rate = 0

    def select_import_data(self):
        pass

    def import_data(self, filepath, electrodes):
        f = open(filepath, 'rU')
        csv_data = csv.reader(f)
        li_data = list(csv_data)
        f.close()

        self.sampling_rate = int(re.search(u"[0-9]+", li_data[0][2].strip()).group(0))

        for ele in electrodes:
            if ele in self.electrode_list:
                self.valid_electrode_list.append(ele)
            else:
                print(ele + " is not included electrodes list of Emotiv Epoc+")

        for i in range(1, len(li_data)):
            self.time.append(float(li_data[i][22]) + float(li_data[i][23])/1000.)
            self.timestamp.append(float(li_data[i][22]) + float(li_data[i][23])/1000.)
            self.marker.append(float(li_data[i][19]))

        if 'af3' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.af3.append(float(li_data[i][2]))
        if 'f7' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.f7.append(float(li_data[i][3]))
        if 'f3' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.f3.append(float(li_data[i][4]))
        if 'fc5' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.fc5.append(float(li_data[i][5]))
        if 't7' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.t7.append(float(li_data[i][6]))
        if 'p7' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.p7.append(float(li_data[i][7]))
        if 'o1' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.o1.append(float(li_data[i][8]))
        if 'o2' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.o2.append(float(li_data[i][9]))
        if 'p8' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.p8.append(float(li_data[i][10]))
        if 't8' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.t8.append(float(li_data[i][11]))
        if 'fc6' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.fc6.append(float(li_data[i][12]))
        if 'f4' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.f4.append(float(li_data[i][13]))
        if 'f8' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.f8.append(float(li_data[i][14]))
        if 'af4' in self.valid_electrode_list: 
            for i in range(1, len(li_data)):
                self.af4.append(float(li_data[i][15]))

        self.time = [ y - self.time[0] for y in self.time ]

    def remove_dc_offset(self):
        if 'af3' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.af3)
            self.af3 = [ x - mean_of_data for x in self.af3 ]
        if 'f7' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.f7)
            self.f7 = [ x - mean_of_data for x in self.f7 ]
        if 'f3' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.f3)
            self.f3 = [ x - mean_of_data for x in self.f3 ]
        if 'fc5' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.fc5)
            self.fc5 = [ x - mean_of_data for x in self.fc5 ]
        if 't7' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.t7)
            self.t7 = [ x - mean_of_data for x in self.t7 ]
        if 'p7' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.p7)
            self.p7 = [ x - mean_of_data for x in self.p7 ]
        if 'o1' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.o1)
            self.o1 = [ x - mean_of_data for x in self.o1 ]
        if 'o2' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.o2)
            self.o2 = [ x - mean_of_data for x in self.o2 ]
        if 'p8' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.af3)
            self.p8 = [ x - mean_of_data for x in self.p8 ]
        if 't8' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.t8)
            self.t8 = [ x - mean_of_data for x in self.t8 ]
        if 'fc6' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.fc6)
            self.fc6 = [ x - mean_of_data for x in self.fc6 ]
        if 'f4' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.f4)
            self.f4 = [ x - mean_of_data for x in self.f4 ]
        if 'f8' in self.valid_electrode_list: 
            mean_of_data = np.mean(f8)
            self.f8 = [ x - mean_of_data for x in self.f8 ]
        if 'af4' in self.valid_electrode_list: 
            mean_of_data = np.mean(self.af4)
            self.af4 = [ x - mean_of_data for x in self.af4 ]

    def normalize(self, electrode):
        if 'af3' == electrode: 
            self.af3 = [ x/np.max(self.af3) for x in self.af3 ]
        elif 'f7' == electrode: 
            self.f7 = [ x/np.max(self.f7) for x in self.f7 ]
        elif 'f3' == electrode: 
            self.f3 = [ x/np.max(self.f3) for x in self.f3 ]
        elif 'fc5' == electrode: 
            self.fc5 = [ x/np.max(self.fc5) for x in self.fc5 ]
        elif 't7' == electrode: 
            self.t7 = [ x/np.max(self.t7) for x in self.t7 ]
        elif 'p7' == electrode: 
            self.p7 = [ x/np.max(self.p7) for x in self.p7 ]
        elif 'o1' == electrode: 
            self.o1 = [ x/np.max(self.o1) for x in self.o1 ]
        elif 'o2' == electrode: 
            self.o2 = [ x/np.max(self.o2) for x in self.o2 ]
        elif 'p8' == electrode: 
            self.p8 = [ x/np.max(self.p8) for x in self.p8 ]
        elif 't8' == electrode: 
            self.t8 = [ x/np.max(self.t8) for x in self.t8 ]
        elif 'fc6' == electrode: 
            self.fc6 = [ x/np.max(self.fc6) for x in self.fc6 ]
        elif 'f4' == electrode: 
            self.f4 = [ x/np.max(self.f4) for x in self.f4 ]
        elif 'f8' == electrode: 
            self.f8 = [ x/np.max(self.f8) for x in self.f8 ]
        elif 'af4' == electrode: 
            self.af4 = [ x/np.max(self.af4) for x in self.af4 ]

    def get_valid_electrode_list(self):
        return self.valid_electrode_list
    
