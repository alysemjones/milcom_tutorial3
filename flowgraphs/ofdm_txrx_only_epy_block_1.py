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

    def __init__(self, num_chans=8):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Sensing',   # will show up in GRC
            in_sig=[(np.float32,num_chans)],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.num_chans = num_chans
        self.energy_vect = np.zeros(self.num_chans)
        self.start_flag = 0
        self.end_flag = 0
        self.num_samps = 0
        
        self.portName = 'energy_vec'
        self.message_port_register_out(pmt.intern(self.portName))
    
    def work(self, input_items, output_items):
        tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))
                
        start_index = 0
        end_index = len(input_items[0])
        for tag in tagTuple:
            if (pmt.to_python(tag.key) == 'burst_start') and ~start_index:
                self.energy_vect = np.zeros(self.num_chans)
                start_index = tag.offset - self.nitems_read(0)
                self.start_flag = 1
            if (pmt.to_python(tag.key) == 'burst_end') and ~end_index:
                end_index = tag.offset - self.nitems_read(0)
                self.end_flag = 1
                             
        if self.start_flag == 1:
            for i in range(start_index,end_index):
                self.energy_vect += input_items[0][i]
                self.num_samps += 1
            
        if self.end_flag == 1:
            self.message_port_pub(pmt.intern(self.portName), pmt.to_pmt(self.energy_vect/self.num_samps))
            self.start_flag = 0
            self.end_flag = 0
            self.num_samps = 0
        
        return len(input_items[0])
