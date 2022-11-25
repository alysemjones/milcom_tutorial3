#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OFDM End-to-End Stream Testing (with GUI)
# Author: Alyse Jones and William "Chris" Headley
# GNU Radio version: 3.10.4.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from math import erfc
from math import log10
from math import sqrt
from ofdm_rx_hier_usrp import ofdm_rx_hier_usrp  # grc-generated hier_block
from ofdm_tx_hier_usrp import ofdm_tx_hier_usrp  # grc-generated hier_block
import numpy as np
import ofdm_txrx_only_epy_block_0_0 as epy_block_0_0  # embedded python block
import ofdm_txrx_only_epy_block_2 as epy_block_2  # embedded python block
import time



from gnuradio import qtgui

class ofdm_txrx_only(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM End-to-End Stream Testing (with GUI)", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("OFDM End-to-End Stream Testing (with GUI)")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ofdm_txrx_only")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.wide_samp_rate = wide_samp_rate = 1e6
        self.num_zeros = num_zeros = 2000
        self.num_header_symbs = num_header_symbs = 3
        self.num_data_symbs = num_data_symbs = 7
        self.num_channels = num_channels = 8
        self.time_steps = time_steps = 100
        self.signal_samp_rate = signal_samp_rate = wide_samp_rate/num_channels
        self.num_samps = num_samps = num_data_symbs*80+num_header_symbs*80
        self.front_pad = front_pad = num_zeros
        self.back_pad = back_pad = num_zeros
        self.snr = snr = 20
        self.head_size = head_size = int((front_pad+back_pad+num_samps)*(signal_samp_rate/(signal_samp_rate))*time_steps)
        self.freq_usrp = freq_usrp = 2.35e9
        self.fft_len = fft_len = int(64)
        self.cent_freq_list = cent_freq_list = [int(i) for i in np.linspace(-wide_samp_rate/2+signal_samp_rate/2, wide_samp_rate/2-signal_samp_rate/2, num_channels)]
        self.tx_gain = tx_gain = 35
        self.taps = taps = firdes.low_pass_2(1.0,1,1/num_channels/2,(1/num_channels)*0.1,80,window.WIN_BLACKMAN_HARRIS)
        self.samps_per_symb = samps_per_symb = float(wide_samp_rate/signal_samp_rate)
        self.rx_gain = rx_gain = 35
        self.rand_seed = rand_seed = int(time.time())
        self.num_samps_per_step = num_samps_per_step = head_size/time_steps
        self.noise_volt = noise_volt = pow(1.0/(fft_len*2*pow(10.0,snr/10.0)),0.5)
        self.linear_gain = linear_gain = 650
        self.freq_fosphor = freq_fosphor = 0
        self.channel_map = channel_map = [int(num_channels/2) + i*1 if i < int(num_channels/2) else -int(num_channels/2)+i*1 for i in range(num_channels)]
        self.cent_freq_rx = cent_freq_rx = -cent_freq_list[0]+freq_usrp
        self.cent_freq = cent_freq = cent_freq_list[0]+freq_usrp
        self.buffer_percentage = buffer_percentage = 0.25
        self.N = N = num_channels*8

        ##################################################
        # Blocks
        ##################################################
        self.ofdm_tx_hier_usrp_0 = ofdm_tx_hier_usrp(
            back_pad=back_pad,
            buffer_percentage=buffer_percentage,
            front_pad=front_pad,
        )
        self.ofdm_rx_hier_usrp_0 = ofdm_rx_hier_usrp(
            cent_freq=int(-cent_freq+freq_usrp),
            signal_samp_rate=signal_samp_rate,
            threshold=0.96,
            wide_samp_rate=wide_samp_rate,
        )
        self.mmse_resampler_xx_0_0 = filter.mmse_resampler_cc(0, (wide_samp_rate/signal_samp_rate))
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, (signal_samp_rate/wide_samp_rate))
        self.low_pass_filter_0_0 = filter.interp_fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                wide_samp_rate,
                (signal_samp_rate/2),
                (0.25*signal_samp_rate/2),
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.interp_fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                wide_samp_rate,
                (signal_samp_rate/2),
                (0.25*signal_samp_rate/2),
                window.WIN_HAMMING,
                6.76))
        self.fft_vxx_0 = fft.fft_vcc(N, True, window.blackmanharris(N), True, 1)
        self.epy_block_2 = epy_block_2.blk(num_chans=num_channels, N=N)
        self.epy_block_0_0 = epy_block_0_0.blk(num_channels=num_channels, wide_samp_rate=wide_samp_rate, cent_freqs=cent_freq_list, log_file='../data_logs/results.txt')
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0.1,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=False)
        self.blocks_tagged_stream_align_0 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, 'burst_start')
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, N)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(1/sqrt(fft_len))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '../data/rx_bits.dat', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(N)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(wide_samp_rate, analog.GR_COS_WAVE, (int(-cent_freq+freq_usrp)), 1.0, 0, 0.0)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_c(wide_samp_rate, analog.GR_COS_WAVE, cent_freq_list[2], 2.5, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(wide_samp_rate, analog.GR_COS_WAVE, cent_freq_list[1], 2.5, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(wide_samp_rate, analog.GR_COS_WAVE, (int(cent_freq-freq_usrp)), 1.0, 0, 0.0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise_volt, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0_0, 'tx_freq'), (self.analog_sig_source_x_0, 'cmd'))
        self.msg_connect((self.epy_block_0_0, 'int_cent_freq'), (self.analog_sig_source_x_0_0, 'cmd'))
        self.msg_connect((self.epy_block_0_0, 'int2_cent_freq'), (self.analog_sig_source_x_0_0_0, 'cmd'))
        self.msg_connect((self.epy_block_0_0, 'rx_freq'), (self.analog_sig_source_x_0_1, 'cmd'))
        self.msg_connect((self.epy_block_0_0, 'tx_freq'), (self.ofdm_tx_hier_usrp_0, 'send_burst'))
        self.msg_connect((self.epy_block_2, 'energy_vec'), (self.epy_block_0_0, 'sensing_results'))
        self.msg_connect((self.epy_block_2, 'packet_len_psd'), (self.epy_block_0_0, 'rx_handler_psd'))
        self.msg_connect((self.ofdm_rx_hier_usrp_0, 'packet_data'), (self.epy_block_0_0, 'packet_results'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_tagged_stream_align_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.epy_block_2, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_1, 2))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_tagged_stream_align_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.mmse_resampler_xx_0_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.mmse_resampler_xx_0_0, 0), (self.ofdm_rx_hier_usrp_0, 0))
        self.connect((self.ofdm_rx_hier_usrp_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.ofdm_tx_hier_usrp_0, 0), (self.mmse_resampler_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_txrx_only")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_wide_samp_rate(self):
        return self.wide_samp_rate

    def set_wide_samp_rate(self, wide_samp_rate):
        self.wide_samp_rate = wide_samp_rate
        self.set_cent_freq_list([int(i) for i in np.linspace(-self.wide_samp_rate/2+self.signal_samp_rate/2, self.wide_samp_rate/2-self.signal_samp_rate/2, self.num_channels)])
        self.set_samps_per_symb(float(self.wide_samp_rate/self.signal_samp_rate))
        self.set_signal_samp_rate(self.wide_samp_rate/self.num_channels)
        self.analog_sig_source_x_0.set_sampling_freq(self.wide_samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.wide_samp_rate)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.wide_samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.wide_samp_rate)
        self.epy_block_0_0.wide_samp_rate = self.wide_samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wide_samp_rate, (self.signal_samp_rate/2), (0.25*self.signal_samp_rate/2), window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.wide_samp_rate, (self.signal_samp_rate/2), (0.25*self.signal_samp_rate/2), window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio((self.signal_samp_rate/self.wide_samp_rate))
        self.mmse_resampler_xx_0_0.set_resamp_ratio((self.wide_samp_rate/self.signal_samp_rate))
        self.ofdm_rx_hier_usrp_0.set_wide_samp_rate(self.wide_samp_rate)

    def get_num_zeros(self):
        return self.num_zeros

    def set_num_zeros(self, num_zeros):
        self.num_zeros = num_zeros
        self.set_back_pad(self.num_zeros)
        self.set_front_pad(self.num_zeros)

    def get_num_header_symbs(self):
        return self.num_header_symbs

    def set_num_header_symbs(self, num_header_symbs):
        self.num_header_symbs = num_header_symbs
        self.set_num_samps(self.num_data_symbs*80+self.num_header_symbs*80)

    def get_num_data_symbs(self):
        return self.num_data_symbs

    def set_num_data_symbs(self, num_data_symbs):
        self.num_data_symbs = num_data_symbs
        self.set_num_samps(self.num_data_symbs*80+self.num_header_symbs*80)

    def get_num_channels(self):
        return self.num_channels

    def set_num_channels(self, num_channels):
        self.num_channels = num_channels
        self.set_N(self.num_channels*8)
        self.set_cent_freq_list([int(i) for i in np.linspace(-self.wide_samp_rate/2+self.signal_samp_rate/2, self.wide_samp_rate/2-self.signal_samp_rate/2, self.num_channels)])
        self.set_channel_map([int(self.num_channels/2) + i*1 if i < int(self.num_channels/2) else -int(self.num_channels/2)+i*1 for i in range(self.num_channels)])
        self.set_signal_samp_rate(self.wide_samp_rate/self.num_channels)
        self.set_taps(firdes.low_pass_2(1.0,1,1/self.num_channels/2,(1/self.num_channels)*0.1,80,window.WIN_BLACKMAN_HARRIS))
        self.epy_block_0_0.num_channels = self.num_channels
        self.epy_block_2.num_chans = self.num_channels

    def get_time_steps(self):
        return self.time_steps

    def set_time_steps(self, time_steps):
        self.time_steps = time_steps
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.signal_samp_rate/(self.signal_samp_rate))*self.time_steps))
        self.set_num_samps_per_step(self.head_size/self.time_steps)

    def get_signal_samp_rate(self):
        return self.signal_samp_rate

    def set_signal_samp_rate(self, signal_samp_rate):
        self.signal_samp_rate = signal_samp_rate
        self.set_cent_freq_list([int(i) for i in np.linspace(-self.wide_samp_rate/2+self.signal_samp_rate/2, self.wide_samp_rate/2-self.signal_samp_rate/2, self.num_channels)])
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.signal_samp_rate/(self.signal_samp_rate))*self.time_steps))
        self.set_samps_per_symb(float(self.wide_samp_rate/self.signal_samp_rate))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wide_samp_rate, (self.signal_samp_rate/2), (0.25*self.signal_samp_rate/2), window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.wide_samp_rate, (self.signal_samp_rate/2), (0.25*self.signal_samp_rate/2), window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio((self.signal_samp_rate/self.wide_samp_rate))
        self.mmse_resampler_xx_0_0.set_resamp_ratio((self.wide_samp_rate/self.signal_samp_rate))
        self.ofdm_rx_hier_usrp_0.set_signal_samp_rate(self.signal_samp_rate)

    def get_num_samps(self):
        return self.num_samps

    def set_num_samps(self, num_samps):
        self.num_samps = num_samps
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.signal_samp_rate/(self.signal_samp_rate))*self.time_steps))

    def get_front_pad(self):
        return self.front_pad

    def set_front_pad(self, front_pad):
        self.front_pad = front_pad
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.signal_samp_rate/(self.signal_samp_rate))*self.time_steps))
        self.ofdm_tx_hier_usrp_0.set_front_pad(self.front_pad)

    def get_back_pad(self):
        return self.back_pad

    def set_back_pad(self, back_pad):
        self.back_pad = back_pad
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.signal_samp_rate/(self.signal_samp_rate))*self.time_steps))
        self.ofdm_tx_hier_usrp_0.set_back_pad(self.back_pad)

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.set_noise_volt(pow(1.0/(self.fft_len*2*pow(10.0,self.snr/10.0)),0.5))

    def get_head_size(self):
        return self.head_size

    def set_head_size(self, head_size):
        self.head_size = head_size
        self.set_num_samps_per_step(self.head_size/self.time_steps)

    def get_freq_usrp(self):
        return self.freq_usrp

    def set_freq_usrp(self, freq_usrp):
        self.freq_usrp = freq_usrp
        self.set_cent_freq(self.cent_freq_list[0]+self.freq_usrp)
        self.set_cent_freq_rx(-self.cent_freq_list[0]+self.freq_usrp)
        self.analog_sig_source_x_0.set_frequency((int(self.cent_freq-self.freq_usrp)))
        self.analog_sig_source_x_0_1.set_frequency((int(-self.cent_freq+self.freq_usrp)))
        self.ofdm_rx_hier_usrp_0.set_cent_freq(int(-self.cent_freq+self.freq_usrp))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_noise_volt(pow(1.0/(self.fft_len*2*pow(10.0,self.snr/10.0)),0.5))
        self.blocks_multiply_const_vxx_1.set_k(1/sqrt(self.fft_len))

    def get_cent_freq_list(self):
        return self.cent_freq_list

    def set_cent_freq_list(self, cent_freq_list):
        self.cent_freq_list = cent_freq_list
        self.set_cent_freq(self.cent_freq_list[0]+self.freq_usrp)
        self.set_cent_freq_rx(-self.cent_freq_list[0]+self.freq_usrp)
        self.analog_sig_source_x_0_0.set_frequency(self.cent_freq_list[1])
        self.analog_sig_source_x_0_0_0.set_frequency(self.cent_freq_list[2])
        self.epy_block_0_0.cent_freqs = self.cent_freq_list

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_rand_seed(self):
        return self.rand_seed

    def set_rand_seed(self, rand_seed):
        self.rand_seed = rand_seed

    def get_num_samps_per_step(self):
        return self.num_samps_per_step

    def set_num_samps_per_step(self, num_samps_per_step):
        self.num_samps_per_step = num_samps_per_step

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt
        self.analog_noise_source_x_0.set_amplitude(self.noise_volt)

    def get_linear_gain(self):
        return self.linear_gain

    def set_linear_gain(self, linear_gain):
        self.linear_gain = linear_gain

    def get_freq_fosphor(self):
        return self.freq_fosphor

    def set_freq_fosphor(self, freq_fosphor):
        self.freq_fosphor = freq_fosphor

    def get_channel_map(self):
        return self.channel_map

    def set_channel_map(self, channel_map):
        self.channel_map = channel_map

    def get_cent_freq_rx(self):
        return self.cent_freq_rx

    def set_cent_freq_rx(self, cent_freq_rx):
        self.cent_freq_rx = cent_freq_rx

    def get_cent_freq(self):
        return self.cent_freq

    def set_cent_freq(self, cent_freq):
        self.cent_freq = cent_freq
        self.analog_sig_source_x_0.set_frequency((int(self.cent_freq-self.freq_usrp)))
        self.analog_sig_source_x_0_1.set_frequency((int(-self.cent_freq+self.freq_usrp)))
        self.ofdm_rx_hier_usrp_0.set_cent_freq(int(-self.cent_freq+self.freq_usrp))

    def get_buffer_percentage(self):
        return self.buffer_percentage

    def set_buffer_percentage(self, buffer_percentage):
        self.buffer_percentage = buffer_percentage
        self.ofdm_tx_hier_usrp_0.set_buffer_percentage(self.buffer_percentage)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.epy_block_2.N = self.N




def main(top_block_cls=ofdm_txrx_only, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
