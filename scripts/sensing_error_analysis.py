import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 28})

zeros_800 = [21, 24, 26, 17, 21, 9, 40, 9, 26, 21, 10, 4, 23, 19, 3, 3, 15, 17, 36, 13, 5, 36, 0, 7, 11, 8, 30, 14, 7, 2, 3, 6, 7, 7, 6, 0, 13, 5, 0, 0, 0, 5, 0, 1, 2, 0, 1, 0, 0, 5, 6, 6, 8, 3, 8, 0, 4, 2, 7, 12, 4, 2, 2, 5, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 5, 11, 4, 10, 4, 2, 4, 3, 2, 6, 5, 3, 2, 0, 0, 0, 1, 6]
duty_cycle_800 = round((800/(800+800*2))*100)
average_error_800 = sum(zeros_800)/len(zeros_800)
zeros_2000 = [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
average_error_2000 = sum(zeros_2000)/len(zeros_2000)
duty_cycle_2000 = round((800/(800+2000*2))*100)
print(duty_cycle_800,duty_cycle_2000)

print(average_error_800,average_error_2000)
plt.figure(figsize=(20, 20))
plt.plot(*[range(0,100)],zeros_800,label='duty cycle = 33%')
plt.plot(*[range(0,100)],zeros_2000,label='duty cycle = 17%')
plt.xlabel('Epoch')
plt.ylabel('Number of Sensing Errors')
plt.title('Sensing Performance for 8 Channels with Varying Duty Cycles')
plt.legend()
plt.show()
