"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import math

class blk(gr.sync_block):
    def __init__(self, num_chans=8, N=64):
        gr.sync_block.__init__(
            self,
            name='PSD Sensing',
            in_sig=[(np.float32,N)],
            out_sig=None
        )
        self.num_chans = num_chans
        self.N = N
               
        self.total_samps = 0
        self.total_epochs = 0  
        self.start_flag = 0
        self.fft_count = 0
                
        self.portName = 'energy_vec'
        self.message_port_register_out(pmt.intern(self.portName))    
       
        self.energy_vect = np.zeros(self.num_chans)
        
    def work(self, input_items, output_items):
        total_items = input_items[0].shape[0] * input_items[0].shape[1]
        self.total_samps += total_items
        tagTuple = self.get_tags_in_window(0, 0, input_items[0].shape[0])

        tags_found = []
        if not len(tagTuple) == 0:       
            for tag in tagTuple: 
                if not pmt.to_python(tag.key) == 'packet_len':
                   tag_vect_num = int(input_items[0].shape[0] - ((self.total_samps - tag.offset*self.N)/self.N))
                   tags_found.append([pmt.to_python(tag.key), tag_vect_num])
                
        for k in range(input_items[0].shape[0]):
            if not len(tags_found) == 0:        
                if tags_found[0][1] == k and tags_found[0][0] == 'burst_start':                              
                    self.fft_count = 0
                    self.start_flag = 1
                    self.total_epochs += 1
                    self.energy_vect = np.zeros(self.num_chans)
                    tags_found.pop(0)

            if self.start_flag == 1:
                chan_vals = input_items[0][k].reshape((self.num_chans, int(self.N/self.num_chans)))
                self.fft_count += 1
                for kk in range(self.num_chans):
                    self.energy_vect[kk] += np.mean(chan_vals[kk])
                        
            if not len(tags_found) == 0:
                if tags_found[0][1] == k and tags_found[0][0] == 'burst_end':                                
                    self.start_flag = 0                
                    #print('Finished Epoch #', self.total_epochs, ', FFTs Calculated: ', self.fft_count)
                    self.message_port_pub(pmt.intern(self.portName), pmt.to_pmt(self.energy_vect/self.fft_count))
                    tags_found.pop(0)                     
                                
        return len(input_items[0])                    
