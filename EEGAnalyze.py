# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal

def print_band_index(N, eeg_list, sampling_rate):
    fft = np.fft.fft(eeg_list[:N])
    spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]
    freq_list = list(np.fft.fftfreq(N, d=1.0/sampling_rate))

    print("delta (1-3Hz) = " + str(np.mean(spectrum[freq_list.index(1):freq_list.index(3)])))
    print("theta (4-7Hz) = " + str(np.mean(spectrum[freq_list.index(4):freq_list.index(7)])))
    print("alpha (7-13Hz) = " + str(np.mean(spectrum[freq_list.index(7):freq_list.index(13)])))
    print("beta (13-30Hz) = " + str(np.mean(spectrum[freq_list.index(13):freq_list.index(30)])))

def get_alpha_index(N, eeg_list, sampling_rate):
    fft = np.fft.fft(eeg_list[:N])
    spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]
    freq_list = list(np.fft.fftfreq(N, d=1.0/sampling_rate))
    return np.mean(spectrum[freq_list.index(7):freq_list.index(13)])

def get_beta_index(N, eeg_list, sampling_rate):
    fft = np.fft.fft(eeg_list[:N])
    spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]
    freq_list = list(np.fft.fftfreq(N, d=1.0/sampling_rate))
    return np.mean(spectrum[freq_list.index(13):freq_list.index(30)])

def get_theta_index(N, eeg_list, sampling_rate):
    fft = np.fft.fft(eeg_list[:N])
    spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]
    freq_list = list(np.fft.fftfreq(N, d=1.0/sampling_rate))
    return np.mean(spectrum[freq_list.index(4):freq_list.index(7)])

def get_delta_index(N, eeg_list, sampling_rate):
    fft = np.fft.fft(eeg_list[:N])
    spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]
    freq_list = list(np.fft.fftfreq(N, d=1.0/sampling_rate))
    return np.mean(spectrum[freq_list.index(1):freq_list.index(3)])

def get_attention_index(N, eeg_list, sampling_rate):
    # attention index = beta / (alpha + theta)
    alpha = get_alpha_index(N, eeg_list, sampling_rate)
    beta = get_beta_index(N, eeg_list, sampling_rate)
    theta = get_theta_index(N, eeg_list, sampling_rate)
    attention_index = beta / (alpha + theta)
    return attention_index

def FIR_low_pass_filter(normalized_eeg_list, cutoff, sampling_rate, numtaps=255):
    nyquist_frequency = sampling_rate / 2.0
    cutoff_n = cutoff / nyquist_frequency
    b = scipy.signal.firwin(numtaps, cutoff_n)
    y = scipy.signal.lfilter(b, 1, normalized_eeg_list)
    return list(y)

def FIR_high_pass_filter(normalized_eeg_list, cutoff, sampling_rate, numtaps=255):
    nyquist_frequency = sampling_rate / 2.0
    cutoff_n = cutoff / nyquist_frequency
    b = scipy.signal.firwin(numtaps, cutoff_n, pass_zero=False) 
    y = scipy.signal.lfilter(b, 1, normalized_eeg_list)
    return list(y)

def FIR_band_pass_filter(normalized_eeg_list, cutoff_low, cutoff_high, sampling_rate, numtaps=255):
    nyquist_frequency = sampling_rate / 2.0
    cutoff_low_n = cutoff_low / nyquist_frequency
    cutoff_high_n = cutoff_high / nyquist_frequency
    b = scipy.signal.firwin(numtaps, [cutoff_low_n, cutoff_high_n], pass_zero=False)
    y = scipy.signal.lfilter(b, 1, normalized_eeg_list)

    return list(y)

def FIR_band_stop_filter(normalized_eeg_list, cutoff_low, cutoff_high, sampling_rate, numtaps=255):
    nyquist_frequency = sampling_rate / 2.0
    cutoff_low_n = cutoff_low / nyquist_frequency
    cutoff_high_n = cutoff_high / nyquist_frequency
    b = scipy.signal.firwin(numtaps, [cutoff_low_n, cutoff_high_n])
    y = scipy.signal.lfilter(b, 1, normalized_eeg_list)
    return list(y)

def fft_amplitude_spectrum(eeg_list, N, sampling_rate):
    window = np.hamming(N)
    freq_list = np.fft.fftfreq(N, d=1.0/sampling_rate)
    windowed_eeg_list = window*eeg_list[:N]
    fft_spectrum = np.fft.fft(windowed_eeg_list)
    fft_amplitude_spectrum = [np.sqrt(c.real**2 + c.imag**2) for c in fft_spectrum]
    return [fft_amplitude_spectrum, freq_list]


