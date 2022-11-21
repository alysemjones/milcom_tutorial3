import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 28})

chan_4 = [64, 44, 50, 58, 67, 53, 51, 55, 48, 38, 35, 33, 35, 29, 28, 36, 21, 21, 17, 19, 16, 14, 18, 18, 12, 14, 15, 10, 14, 8, 8, 9, 10, 14, 10, 7, 10, 5, 7, 9, 8, 7, 5, 7, 5, 9, 3, 9, 6, 1, 0, 3, 3, 5, 6, 4, 3, 0, 1, 1, 7, 7, 3, 3, 3, 1, 2, 0, 0, 1, 4, 1, 2, 2, 2, 1, 2, 2, 4, 2, 2, 1, 5, 2, 4, 0, 4, 3, 3, 5, 3, 0, 7, 3, 2, 2, 1, 0, 1, 2] 
chan_8 = [19, 23, 27, 29, 16, 24, 14, 19, 14, 13, 21, 6, 8, 9, 9, 6, 10, 6, 5, 3, 7, 8, 1, 3, 1, 3, 2, 6, 4, 5, 4, 1, 1, 2, 1, 0, 1, 0, 1, 3, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
chan_12 = [14, 14, 16, 17, 11, 14, 4, 17, 9, 6, 12, 13, 12, 10, 14, 8, 11, 11, 11, 7, 10, 11, 6, 10, 7, 6, 9, 8, 10, 11, 8, 8, 10, 9, 8, 11, 8, 8, 10, 10, 8, 9, 8, 7, 7, 8, 8, 8, 8, 9, 9, 8, 9, 9, 8, 8, 8, 8, 8, 9, 8, 7, 9, 8, 8, 9, 8, 8, 9, 8, 8, 10, 8, 8, 9, 8, 8, 9, 8, 8, 9, 7, 8, 9, 8, 8, 9, 8, 8, 9, 8, 8, 9, 8, 7, 9, 8, 7, 9, 8] 
print(chan_4)
print(chan_8)
print(chan_12)

plt.figure(figsize=(20, 20))
plt.plot(*[range(0,100)],chan_4,label='4 channels')
plt.plot(*[range(0,100)],chan_8,label='8 channels')
plt.plot(*[range(0,100)],chan_12,label='12 channels')
plt.xlabel('Epoch')
plt.ylabel('Number of Packer Errors')
plt.title('Performance of Q-learning for Varying Channel Sizes')
plt.legend()
plt.show()
