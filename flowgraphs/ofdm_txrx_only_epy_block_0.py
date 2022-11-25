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


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,cent_freqs=[],time_steps=10,cent_freq=0e6):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Cognitive Engine',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.cent_freqs = cent_freqs
        self.time_steps = time_steps
        self.cent_freq = cent_freq
        self.msg_port_name_tx = 'tx_cent_freq'
        self.msg_port_name_rx = 'rx_cent_freq'
        self.msg_input_packet = 'packet_results'
        self.count = 0
        self.pos = 0
        self.message_port_register_out(pmt.intern(self.msg_port_name_rx))
        self.message_port_register_out(pmt.intern(self.msg_port_name_tx))
        self.message_port_register_in(pmt.intern(self.msg_input_packet))
        self.set_msg_handler(pmt.intern(self.msg_input_packet), self.handle_msg_packet)
        self.start_time = time.time()

    def handle_msg_packet(self, msg):
    	# record packet results from the receiver here
		
    	# transmit again when the following conditions are met
    	if self.count == 0 or self.packet == True or (time.time()-self.start_time > 0.05):
    		self.control_freq() # decides the next action(s)
    		self.count += 1
    		self.start_time = time.time()
    
    def control_freq(self):
    	if self.count < self.time_steps:
    		self.previous_freq = self.cent_freq
    		# decide frequency here

    		# send new center frequency to the transmitter and receiver
    		PMT_msg_tx =  pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(self.cent_freq))
    		PMT_msg_rx =  pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(-self.cent_freq))
    		self.message_port_pub(pmt.intern(self.msg_port_name_tx), PMT_msg_tx)
    		self.message_port_pub(pmt.intern(self.msg_port_name_rx), PMT_msg_rx)
    		
    		# enforce diagonal hopping here

    		print(self.count,self.previous_freq,self.packet)	

    def work(self, input_items, output_items):
        return len(input_items[0])
