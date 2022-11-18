import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 28})
from mpl_toolkits.mplot3wd import Axes3D 

time_steps = 100
num_zeros = np.arange(1000,5100,200)
num_samps = 800
wide_samp_rate = 32e6
signal_samp_rate = 1e6
goodput = np.zeros(len(num_zeros))
sensing_errors = [70,69,68,70,80,76,82,70,50,27,29,19,8,9,12,1,0,2,2,0,0]

for i in range(len(num_zeros)):
	head_size = int((num_zeros[i]*2+num_samps)*(wide_samp_rate/(signal_samp_rate))*time_steps)
	time_each_epoch = (int(head_size/time_steps))/wide_samp_rate
	goodput[i] = (84*8/time_each_epoch)/(1e3)
	print(84*8/time_each_epoch)

num_zeros = [(800/(x+800))*100 for x in num_zeros]
print(num_zeros)
fig = plt.figure(figsize=(20, 20))
'''
plt.plot(num_zeros, goodput)
plt.yticks(np.arange(50,275,25))
plt.xticks(np.arange(10,50,5))
plt.axhline(y=77.5, color='r', linestyle='-')
plt.axvline(x=16.9, color='r', linestyle='-')
plt.xlabel('Duty Cycle (%)',fontweight='bold')
plt.ylabel('Goodput (kbps)',fontweight='bold')

'''
plt.plot(num_zeros, sensing_errors)
plt.yticks(np.arange(0,105,5))
plt.xticks(np.arange(10,50,5))
plt.axhline(y=5, color='r', linestyle='-')
plt.axvline(x=16.9, color='r', linestyle='-')
plt.xlabel('Duty Cycle (%)',fontweight='bold')
plt.ylabel('Percentage of Sensing Errors (%)',fontweight='bold')

plt.show()
