"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import pmt
import numpy as np
from gnuradio import gr
import time
import random


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,num_channels=8,wide_samp_rate=2e6, cent_freqs=[],log_file=None):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Cognitive Engine',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.num_channels = num_channels
        self.wide_samp_rate = wide_samp_rate
        self.cent_freqs = cent_freqs
        self.log_file = log_file
        self.samp_rate = int(self.wide_samp_rate/(1e6))
        self.msg_port_name_tx = 'tx_freq'
        self.msg_port_name_rx = 'rx_freq'
        self.msg_port_name_int = 'int_cent_freq'
        self.msg_port_name_int2 = 'int2_cent_freq'
        #self.msg_port_name_reward = 'reward'
        self.msg_input_sensing = 'sensing_results'
        self.msg_input_packet = 'packet_results'
        self.msg_input_change_rx = 'rx_handler_psd'
        #self.msg_input_change_rx2 = 'rx_handler_chan'
        self.message_port_register_out(pmt.intern(self.msg_port_name_tx))
        self.message_port_register_out(pmt.intern(self.msg_port_name_rx))
        self.message_port_register_out(pmt.intern(self.msg_port_name_int))
        self.message_port_register_out(pmt.intern(self.msg_port_name_int2))
        #self.message_port_register_out(pmt.intern(self.msg_port_name_reward))
        self.message_port_register_in(pmt.intern(self.msg_input_sensing))
        self.set_msg_handler(pmt.intern(self.msg_input_sensing), self.handle_msg_sensing)
        self.message_port_register_in(pmt.intern(self.msg_input_packet))
        self.set_msg_handler(pmt.intern(self.msg_input_packet), self.handle_msg_packet)
        self.message_port_register_in(pmt.intern(self.msg_input_change_rx))
        self.set_msg_handler(pmt.intern(self.msg_input_change_rx), self.handle_msg_rx_freq)
        #self.message_port_register_in(pmt.intern(self.msg_input_change_rx2))
        #self.set_msg_handler(pmt.intern(self.msg_input_change_rx2), self.handle_msg_rx_freq2)
        #self.cent_freqs = np.arange(-int((self.samp_rate/2)+(self.samp_rate/(self.num_channels*2))),int((self.samp_rate/2)+(self.samp_rate/(self.num_channels*2))),self.samp_rate/self.num_channels)
        #self.cent_freqs = self.cent_freqs[1:]
        print(self.cent_freqs)
        self.position = 0
        self.count_sensor = 0
        self.count_packet = 0
        self.counter = 0
        self.count = 0
        self.packet = False
        self.packet_flag = False
        self.sensor_flag = False
        self.cent_freq = -500000
        self.int_freq = -83333
        self.int2_freq = 83333
        self.packet_errors = 0
        self.tot_packet_errors = 0
        self.sensing_errors = 0
        self.tot_sensing_errors = 0
        self.pos = []
        self.int_pos = random.sample(range(0,self.num_channels-1),self.num_channels-1)
        self.int2_pos = random.sample(range(0,self.num_channels-1),self.num_channels-1)
        ### RL Stuff ### 
        self.min_epsilon = 0.001
        self.max_epsilon = 1
        self.decay_rate = 0.085
        self.alpha = 0.9
        self.gamma = 0.1
        self.values = [0,1]
        self.num_values = len(self.values)
        self.time_window = 1
        self.num_actions = self.num_channels
        self.num_states = self.num_values**(self.num_actions*self.time_window)
        self.epsilon = 0
        self.policy = np.zeros(self.num_states)
        self.Q = np.zeros((self.num_states, self.num_actions))
        self.action_space = [*range(self.num_actions)]
        self.a = 0
        self.cumulative_reward = 0
        self.next_state = np.zeros(self.num_actions)
        self.s_next = 0
        self.state = np.zeros(self.num_actions)
        self.s = 0
        self.sensing_errors_list = []
        self.reward_list = []
        self.tot_packet_errors_list = []
        self.epsilon_count = 0
        self.reward = 0
        self.cumulative_reward_list = []
        self.packet_error_list = []
        self.sensing_error_list = []
        self.previous_reward = 0
        self.count_previous = 0
        self.change = 0
        self.empty = []
        self.previous_state = []
        self.start_time = 0
        self.time_diff = 0
        self.time_diff_avg = 0
        self.time_diff_avg_list = []
    
    def handle_msg_sensing(self, msg): 
    	self.channels = pmt.to_python(msg)
    	if self.count == 0:
    	   print(self.channels)
    	self.channels = [0 if i < 2 else 1 for i in self.channels]
    	self.count_sensor += 1
    	self.sensor_flag = True
    	if self.count_sensor < 100*102:
    	   self.pos = []
    	   self.sensing_errors = 0
    	   self.packet_errors = 0
    	   self.reinforcement_learning()

    def handle_msg_packet(self, msg):
    	packetVal = pmt.to_python(msg)
    	self.counter += 1
    	if packetVal == False:
    		self.packet = False
    	else:
    		self.packet = True
    		self.count_packet += 1
    		self.packet_flag = True
    	#if self.counter < 1000:
    	#    self.change_frequency()
    	#    PMT_msg_send =  pmt.dict_add(pmt.make_dict(), pmt.intern("transmit"), pmt.to_pmt('Send Frame'))
    	#    self.message_port_pub(pmt.intern(self.msg_port_name_send), PMT_msg_send)
    	    #zmq_socket_packet.send(pmt.serialize_str(pmt.to_pmt('Send Frame')))
    	   
    	#if self.sensor_flag == True and self.packet_flag == True:
    	#       self.check_synch()
    
    #def handle_msg_rx_freq2(self, msg):
    #    self.start_time = time.time()
        
    def handle_msg_rx_freq(self, msg):
        end_time = time.time()
        self.check_sensing_errors()
        #print(self.pos, self.channels)
        #print(self.count, self.count_packet, self.counter, self.pos, self.channels, self.packet, self.tot_sensing_errors, self.tot_packet_errors)
        self.time_diff += end_time - self.start_time
        #print(self.int_pos, self.int2_pos)
        if self.packet == True:
           self.reward = 1
        else:
           self.reward = 0
        if self.count % 100 == 0:
           '''
           if self.count > 100*45 and self.change == 0:
              if self.cumulative_reward < 95:
                 self.epsilon_count = 0
                 self.count_previous = 0
                 self.change = 1
           '''
           #PMT_msg_reward =  pmt.dict_add(pmt.make_dict(), pmt.intern("reward"), pmt.from_float(100-self.cumulative_reward))
           #self.message_port_pub(pmt.intern(self.msg_port_name_reward), PMT_msg_reward)  
           self.time_diff_avg = self.time_diff/100
           print(self.count, self.epsilon, self.count_packet, self.previous_reward, self.cumulative_reward, self.tot_sensing_errors, self.tot_packet_errors, self.time_diff_avg)
           print(self.count, self.cumulative_reward)
           self.previous_reward = self.cumulative_reward
           self.cumulative_reward_list.append(self.cumulative_reward)
           self.packet_error_list.append(self.tot_packet_errors)
           self.sensing_error_list.append(self.tot_sensing_errors)
           self.time_diff_avg_list.append(self.time_diff_avg)
           self.cumulative_reward = 0
           self.tot_sensing_errors = 0
           self.tot_packet_errors = 0
           self.count_packet = 0
           self.time_diff = 0
           self.time_diff_avg = 0
        self.packet_flag = False
        self.count += 1
        self.packet = False
        '''
        if self.count == 100*40:
           print(self.int_pos, self.int2_pos)
           self.int_pos = random.sample(range(0,self.num_channels-1),self.num_channels-1)
           self.int2_pos = random.sample(range(0,self.num_channels-1),self.num_channels-1)    
           print(self.int_pos, self.int2_pos)
           self.position = 0      
        '''  
        if self.count == 10000:
           self.save_data()
    
    def save_data(self):
        f = open(self.log_file, "a")
        f.write("Reward: " + str(self.cumulative_reward_list) + "\n")
        f.write("Sensing Errors: " + str(self.sensing_error_list) + "\n")
        f.write("Packet Errors: " + str(self.packet_error_list) + "\n")
        f.write("Time diff: " + str(self.time_diff_avg_list) + "\n")
        f.write("\n")
        f.close()
    
    def check_sensing_errors(self):
        c = 0
        idx_list = []
        if self.count != 0:
        	for i in self.pos:
        		idx = np.where(np.array(self.cent_freqs) == i)[0][0]
        		idx_list.append(idx)
        		if self.channels[idx] == 0:
        			self.sensing_errors = 1
        		if sum(self.channels) > 3:
        			self.sensing_errors = 1
        		c += 1
        	if (idx_list[1] == idx_list[0]) and self.packet != False:
        	    self.packet_errors = 1
        	if (idx_list[2] == idx_list[0]) and self.packet != False:
        	    self.packet_errors = 1
        	if sum(self.channels) == 1 and self.packet != False:
        	    self.packet_errors = 1
        	if (idx_list[1] == idx_list[2]) and (idx_list[0] != idx_list[1]):
        	    if self.packet != True:
        	       self.packet_errors = 1
        	    else:
        	       self.packet_errors = 0
        if self.sensing_errors == 1:
               self.tot_sensing_errors += 1
        if self.packet_errors == 1:
               self.tot_packet_errors += 1
        #print(idx_list, self.packet, self.tot_packet_errors)

    def convertIndexToTuple(self,state):
    	return(tuple(int(x) for x in np.base_repr(state, self.num_values, self.num_actions)[-self.num_actions::]))
    
    def convertTupleToIndex(self,state):
    	return(int("".join(str(x) for x in state), self.num_values))
    
    def reset(self):
    	for s in range(self.num_states):
    		self.policy[s] = random.randrange(0,self.num_channels)
    
    def decay_epsilon(self,t):
    	epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * t)
    	return epsilon

    def choose_action(self,t):
    	p = random.uniform(0,1)
    	if self.count % 100 == 0:
    		self.epsilon = self.decay_epsilon(self.epsilon_count)
    		self.epsilon_count += 1
    	#if self.count == 100*20:
    	#	print(self.count)
    	#	self.epsilon_count == 0
    	'''
    	if t <= int(self.time_steps*0.25):
    		epsilon = 0.90
    	elif t <= int(self.time_steps*0.5) and t > int(self.time_steps*0.25):
    		epsilon = 0.75
    	elif t <= int(self.time_steps*0.75) and t > int(self.time_steps*0.5):
    		epsilon = 0.25
    	else:
    		epsilon = 0.01
    	'''
    	if p > self.epsilon:
    		if self.count % 100 == 0:
    			self.policy = self.Q.argmax(axis=1)
    		a = self.policy[self.s]
    	else:
    		a = random.choice(list(enumerate(self.cent_freqs)))[0]
    	return a
    
    def reinforcement_learning(self):
        if self.count == 0:
                self.pos.append(int(self.cent_freqs[0]))
                self.pos.append(int(self.int_freq))
                self.pos.append(int(self.int2_freq))
        else:
                self.pos.append(int(self.cent_freq))
                self.pos.append(int(self.int_freq))
                self.pos.append(int(self.int2_freq))
        
        self.cumulative_reward += self.reward
        self.next_state = [int(x) for x in self.channels]
        self.s_next = int(self.convertTupleToIndex(self.next_state))
        # update Q matrix
        self.metric = self.alpha * (self.reward + self.gamma * np.max(self.Q[int(self.s_next), :]) - self.Q[self.s,self.a])
        self.Q[self.s,self.a] += self.metric
        	
        # update state to next state
        self.state = self.next_state
        self.s = int(self.convertTupleToIndex(self.state))

        # choose next action
        self.a = int(self.choose_action(self.count))
        self.cent_freq = self.cent_freqs[self.a]
        
        #self.cent_freq = self.cent_freqs[self.position]
        #self.int_freq = self.cent_freqs[self.int_pos[self.position]]
        #self.int2_freq = self.cent_freqs[self.int2_pos[self.position]]
        self.int_freq = self.cent_freqs[3]
        self.int2_freq = self.cent_freqs[self.position]
        self.position += 1
        if self.position == len(self.cent_freqs)-1:
           self.position = 0
        
        #self.empty = [i for i,val in enumerate(self.channels) if val==0]
        #idx = random.choice(self.empty)
        #self.cent_freq = self.cent_freqs[idx]
        
        PMT_msg_tx =  pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(self.cent_freq))
        self.message_port_pub(pmt.intern(self.msg_port_name_tx), PMT_msg_tx)
        PMT_msg_rx =  pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(-self.cent_freq))
        self.message_port_pub(pmt.intern(self.msg_port_name_rx), PMT_msg_rx)
        PMT_msg_int =  pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(self.int_freq))
        self.message_port_pub(pmt.intern(self.msg_port_name_int), PMT_msg_int)
        PMT_msg_int2 =  pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(self.int2_freq))
        self.message_port_pub(pmt.intern(self.msg_port_name_int2), PMT_msg_int2)  
                  
    def work(self, input_items, output_items):
        return len(input_items[0])
