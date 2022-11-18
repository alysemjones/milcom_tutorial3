"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import pmt
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,num_channels=8,wide_samp_rate=2e6):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Freq Control',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig = []
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.num_channels = num_channels
        self.wide_samp_rate = wide_samp_rate
        self.samp_rate = int(self.wide_samp_rate/(1e6))
        self.msg_port_name_tx = 'tx_cent_freq'
        self.msg_port_name_rx = 'rx_cent_freq'
        self.message_port_register_out(pmt.intern(self.msg_port_name_rx))
        self.message_port_register_out(pmt.intern(self.msg_port_name_tx))
        self.cent_freqs = np.arange(int(-(self.samp_rate/2)+1),int(self.samp_rate/2),1/8)
        self.position = 0

    def work(self, input_items, output_items):
        tag_tuple = self.get_tags_in_window(0, 0, len(input_items[0]))

        for tag in tag_tuple:
            if (pmt.to_python(tag.key) == 'packet_len'):
                cent_freq = self.cent_freqs[self.position]*1e6
                self.position += 1
                if self.position == len(self.cent_freqs):
                    self.position = 0
                PMT_msg_tx =  pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(cent_freq))
                PMT_msg_rx =  pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(-cent_freq))
                self.message_port_pub(pmt.intern(self.msg_port_name_tx), PMT_msg_tx)
                self.message_port_pub(pmt.intern(self.msg_port_name_rx), PMT_msg_rx)
        
        return len(input_items[0])
