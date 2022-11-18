import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

num_channels = 8
wide_samp_rate = 1e6
signal_samp_rate = 1e6/num_channels
min_freq = -int(wide_samp_rate/2)
max_freq = int(wide_samp_rate/2)
freq_space = [int(i) for i in np.linspace(-wide_samp_rate/2+signal_samp_rate/2, wide_samp_rate/2-signal_samp_rate/2, num_channels)]
f = np.fromfile(open('data/rx_sig_4chan.dat'),dtype=np.complex64)
#with open('data/sensing_matrix.dat.npy','rb') as f1:
#    a = np.load(f1)
#print(a)
#f2 = np.fromfile(open('data/sensing.dat'),dtype=np.float32)
#print(f2)
print(len(f))
plt.specgram(f[0:1000000],NFFT=1024,Fs=1e6,noverlap=900)
plt.yticks(freq_space)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
##F,t,Sxx = signal.spectrogram(f)
#plt.pcolormesh(t,F,Sxx,shading='gourand')
plt.show()
#plt.imshow(matrix)
#plt.show()
