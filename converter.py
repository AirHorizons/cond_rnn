import librosa
import soundfile as sf
import numpy as np
from scipy import signal

def create_sine(f, duration, amp=1, fs=44100):
    return amp * np.sin(2 * np.pi * f * np.arange(0, duration, 1/fs))

def pitch_to_f(pitch_num):
    return 440*pow(2, (pitch_num - 69)/12.0)

def draw_triangle(pitch, duration, amp=1, n=10, fs=44100):
    if pitch == -1:
        return 0 * np.arange(0, duration)
    f = pitch_to_f(pitch)
    t = np.arange(0, duration)/fs
    return signal.sawtooth(2 * np.pi * f * t, 0.5)

def draw_pulse(pitch, duration, amp=1, n=10, fs=44100):
    if pitch == -1:
        return 0 * np.arange(0, duration)
    f = pitch_to_f(pitch)
    t = np.arange(0, duration)/fs
    return signal.square(np.pi * f * t)

def draw_pulse2(pitch, duration, amp=1, n=10, fs=44100):
    if pitch == -1:
        return 0 * np.arange(0, duration)
    f = pitch_to_f(pitch)
    t = np.arange(0, duration)/fs
    return signal.square(np.pi * f * t, duty=1/4)

def draw_noise(pitch, duration, amp=1, fs=44100):
    wave = 0 * np.arange(0, duration, dtype='float32')
    if pitch == -1:
        return wave
    f = pitch_to_f(pitch)*100*pitch
    
    # print(fs // int(f))
    j = 0
    sig = amp * np.random.rand()
    for i in range(duration):
        if j >= fs/f:
            sig = amp * np.random.rand()
            j -= fs/f
        j += 1
        wave[i] = sig
    return wave

def convert_wav(fname, fs=44100):
    no, tr, p1, p2 = -1, -1, -1, -1
    wav_data = np.array([])

    with open(fname) as f:
        for line in f.readlines():
            words = line.split('_')
            if words[0] == 'WT':
                tr_wav = draw_triangle(tr, int(words[1]))
                p1_wav = draw_pulse(p1, int(words[1]))
                p2_wav = draw_pulse2(p2, int(words[1]))
                no_wav = draw_noise(no, int(words[1]))
                total_wav = tr_wav + p1_wav + p2_wav + no_wav
                wav_data = np.concatenate([wav_data, total_wav])
            elif words[0] == 'TR':
                if words [1] == 'NOTEON':
                    tr = int(words[2])
                else:
                    tr = -1
            elif words[0] == 'P1':
                if words [1] == 'NOTEON':
                    p1 = int(words[2])
                else:
                    p1 = -1
            elif words[0] == 'P2':
                if words [1] == 'NOTEON':
                    p2 = int(words[2])
                else:
                    p2 = -1
            elif words[0] == 'NO':
                if words [1] == 'NOTEON':
                    no = int(words[2])
                else:
                    no = -1
        return wav_data
if __name__ == '__main__':
    sr = 44100
    data_file = './data/train/191_Kirby_sAdventure_01_02TitleScreenDemo.tx1.txt'
    sf.write('./kirby_test.wav', convert_wav(data_file), samplerate=sr)
    