import numpy as np
import matplotlib.pyplot as plt

time_steps = 100
num_zeros = 2500
num_samps = 800
wide_samp_rate = 20e6
signal_samp_rate = 1e6
num_channels = [4,6,8,10,12,14,16,18,20]
goodput = np.zeros(len(num_channels))
memory = np.zeros(len(num_channels))

head_size = int((num_zeros*2+num_samps)*(wide_samp_rate/(signal_samp_rate))*time_steps)
time_each_epoch = (int(head_size/time_steps))/wide_samp_rate

for i in range(len(num_channels)):
	memory[i] = 2**(num_channels[i])

fig, ax = plt.subplots()
ax.set_yticks(memory)
ax.set_yticklabels(['16','64','256','1024','4096','16384','65536','262144','1048576'])
ax.plot(num_channels, memory)
plt.show()	
