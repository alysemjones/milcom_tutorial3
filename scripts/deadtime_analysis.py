import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 28})

zeros_800 = [31, 34, 28, 33, 25, 28, 38, 25, 26, 33, 17, 28, 28, 17, 17, 19, 27, 18, 25, 22, 13, 20, 23, 18, 18, 16, 20, 19, 15, 13, 15, 15, 17, 14, 16, 12, 17, 17, 18, 12, 12, 13, 13, 14, 15, 12, 13, 12, 14, 11, 18, 15, 14, 14, 7, 13, 7, 13, 7, 8, 9, 9, 11, 9, 14, 12, 15, 14, 14, 11, 15, 12, 14, 13, 18, 17, 15, 13, 13, 12, 10, 14, 15, 13, 9, 11, 11, 10, 9, 11, 14, 7, 8, 9, 14, 11, 14, 13, 13, 11]
zeros_2000 = [19, 23, 27, 29, 16, 24, 14, 19, 14, 13, 21, 6, 8, 9, 9, 6, 10, 6, 5, 3, 7, 8, 1, 3, 1, 3, 2, 6, 4, 5, 4, 1, 1, 2, 1, 0, 1, 0, 1, 3, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
duty_cycle_800 = round((800/(800+800*2))*100)
duty_cycle_2000 = round((800/(800+2000*2))*100)

plt.figure(figsize=(20, 20))
plt.plot(*[range(0,100)],zeros_800,label='duty cycle = 33%')
plt.plot(*[range(0,100)],zeros_2000,label='duty cycle = 17%')
plt.xlabel('Epoch')
plt.ylabel('Number of Packet Errors')
plt.title('Performance of Q-leaning for 8 Channels with Varying Duty Cycles')
plt.legend()
plt.show()
 
