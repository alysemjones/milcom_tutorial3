"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, N=64, num_channels=8, samp_rate=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[(np.float32,N)],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.N = N
        self.num_channels = num_channels
        self.samp_rate = samp_rate
        self.energy_vect = np.zeros(self.num_channels)
        self.count = 0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        for i in range(len(input_items[0])):
        	self.count += 1
        	x = input_items[0][i].reshape((self.num_channels, int(self.N/self.num_channels)))
        	print(x.shape)      	
        	for j in range(self.num_channels):
        		self.energy_vect[j] = np.mean(x[j])
        	print(self.energy_vect/self.count)
        
        return len(input_items[0])
