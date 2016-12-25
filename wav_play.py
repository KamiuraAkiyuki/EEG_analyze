# coding: utf-8

import wave
import pyaudio

from EEGData import *
from EEGAnalyze import *
from FileSelect import *

if __name__=="__main__":
    wav_path = "wav_data/"
    audio_path = wav_path + "tirutiru.wav"
    wav_file = wave.open(audio_path, 'rb')

    chunk = 4096
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wav_file.getsampwidth()),
                    channels=wav_file.getnchannels(),
                    rate=wav_file.getframerate(),
                    output=True)
    stream.start_stream()
    remain = wav_file.getnframes()
    while remain > 0:
        try:
            buf = wav_file.readframes(min(chunk, remain))
            stream.write(buf)
            remain -= chunk
        except KeyboardInterrupt:
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    wav_file.close()


