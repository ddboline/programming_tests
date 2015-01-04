"""
Discover the periods in ../../data/populations.txt
"""
import numpy as np
from scipy import fftpack
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile

def analyze_audio(prefix):
    rate, data = wavfile.read('%s.wav' % prefix)
    dt = 1./rate
    T = dt * data.shape[0]
    print dt, T

    #print np.linspace(0, tottime, data.shape[0])
    tvec = np.arange(0, T, dt)
    sig0 = data[:,0]
    sig1 = data[:,1]

    print np.sum(sig0), np.sum(sig1)

    plt.clf()
    plt.plot(tvec, sig0)
    plt.plot(tvec, sig1)
    xtickarray = range(0, 12, 2)
    plt.xticks(xtickarray, map(lambda x: '%d s' % x, xtickarray))
    plt.savefig('%s_time.png' % prefix)

    plt.clf()
    samp_freq0 = fftpack.fftfreq(sig0.size, d=dt)
    sig_fft0 = fftpack.fft(sig0)
    samp_freq1 = fftpack.fftfreq(sig1.size, d=dt)
    sig_fft1 = fftpack.fft(sig1)
    plt.plot(np.log(np.abs(samp_freq0)+1e-9), np.abs(sig_fft0))
    plt.plot(np.log(np.abs(samp_freq1)+1e-9), np.abs(sig_fft1))
    plt.xlim(np.log(10), np.log(40e3))
    xtickarray = np.log(np.array([20, 1e2, 3e2, 1e3, 3e3, 10e3, 30e3]))
    plt.xticks(xtickarray, ['20Hz', '100Hz', '300Hz', '1kHz', '3kHz', '10kHz', '30kHz'])
    plt.savefig('%s_freq.png' % prefix)

    return

if __name__ == '__main__':
    analyze_audio('broken_audio')
    analyze_audio('working_audio')
