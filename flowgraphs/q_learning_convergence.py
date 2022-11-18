import ofdm_txrx_rl as txrx
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
import random
from scipy import signal
#from scipy.fft import fftshift
import sys
import time

top_block_cls = txrx.ofdm_txrx_rl
episode_num = 150
cumulative_reward_list = np.zeros(episode_num)
bit_error_rate = np.zeros(episode_num)
num_channels = 4
values = [0,1]
num_values = len(values)
time_window = 1
num_actions = num_channels
num_states = num_values**(num_actions*time_window)
Q = np.zeros((num_states, num_actions))
min_epsilon = 0.001
max_epsilon = 1
decay_rate = 0.02
packet_error_rate = np.zeros(episode_num)
packet_errors = np.zeros(episode_num)
sensing_errors = np.zeros(episode_num)
positions = [random.randint(0,num_channels-1) for i in range(0,num_channels)]
positions2 = [random.randint(0,num_channels-1) for i in range(0,num_channels)]
Fs = 2e6
data1 = []
data2 = []
total_data = []
matplotlib.rcParams.update({'font.size': 28})

def decay_epsilon(t):
	epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * t)
	return epsilon


for each_episode in range(episode_num):
	if each_episode == 0:
		open('/home/alysemjones/rl_ofdm_dsa/data_logs/packet_errors.txt', 'w').close()
	tb = top_block_cls()
	tb.epy_block_0.epsilon = decay_epsilon(each_episode)
	tb.epy_block_0.Q = Q
	tb.run()
	#tb.start()
	#time.sleep(10)
	#tb.stop()
	Q = tb.epy_block_0.Q
	print(each_episode, tb.epy_block_0.cumulative_reward)
	print(tb.epy_block_0.packet_no_error, tb.epy_block_0.total_packets)
	cumulative_reward_list[each_episode] = tb.epy_block_0.cumulative_reward
	packet_error_rate[each_episode] = (tb.epy_block_0.total_packets-tb.epy_block_0.packet_no_error)
	if tb.epy_block_0.total_packets < 500:
		sensing_errors[each_episode] = tb.epy_block_0.tot_sensing_errors+(500-tb.epy_block_0.total_packets)
		packet_errors[each_episode] = tb.epy_block_0.tot_packet_errors+(500-tb.epy_block_0.total_packets)
	else:
		sensing_errors[each_episode] = tb.epy_block_0.tot_sensing_errors
		packet_errors[each_episode] = tb.epy_block_0.tot_packet_errors
		
	#bit_error_rate[each_episode] = ber(tb)
	#if each_episode == 4 or each_episode == 144:
	#if each_episode == 0 or each_episode == 2:
	#data1 = tb.blocks_vector_sink_x_0.data()
	#total_data.extend(data1[0:int(len(data1))])

# packet error rate
file1 = open('/home/alysemjones/rl_ofdm_dsa/data_logs/packet_errors.txt', "a")
file1.write(str(packet_error_rate))
file1.write("\n")
file1.close()
# packet errors
file2 = open('/home/alysemjones/rl_ofdm_dsa/data_logs/total_packet_errors.txt', "a")
file2.write(str(num_channels) + ' Channels: ' + str(packet_errors))
file2.write("\n")
file2.close()
# sensing errors
file3 = open('/home/alysemjones/rl_ofdm_dsa/data_logs/sensing_errors.txt', "a")
file3.write(str(num_channels) + ' Channels: ' + str(sensing_errors))
file3.write("\n")
file3.close()
# goodput
goodput = 84*8/(int(tb.head_size/tb.time_steps)/tb.wide_samp_rate)
file4 = open('/home/alysemjones/rl_ofdm_dsa/data_logs/goodput.txt', "a")
file4.write(str(num_channels) + ' Channels: ' + str(goodput))
file4.write("\n")
file4.close()
# number of states (memory)
file5 = open('/home/alysemjones/rl_ofdm_dsa/data_logs/memory.txt', "a")
file5.write(str(num_channels) + ' Channels: ' + str(tb.epy_block_0.num_states))
file5.write("\n")
file5.close() 

#plt.figure(figsize=(20, 20))
#plt.specgram(np.array(total_data), NFFT=1024, Fs=Fs)
#f2, t2, Sxx2 = signal.spectrogram(data2, Fs)
#plt.pcolormesh(t1, f1, Sxx1, shading='gourand')
#plt.pcolormesh(t2, f2, Sxx2, shading='gourand')
#packet_error_rate = [pow(10,i) for i in packet_error_rate]
#plt.plot([*range(episode_num)],packet_error_rate)
#plt.yscale('log')
#plt.xlabel('Time [sec]')
#plt.ylabel('Frequency [Hz]')
#plt.savefig('/home/alysemjones/rl_ofdm_dsa/data/spectrogram.png')
