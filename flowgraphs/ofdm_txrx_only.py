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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from math import erfc
from math import log10
from math import sqrt
from ofdm_rx_hier_tutorial import ofdm_rx_hier_tutorial  # grc-generated hier_block
from ofdm_tx_hier_usrp_tutorial import ofdm_tx_hier_usrp_tutorial  # grc-generated hier_block
import numpy as np
import ofdm_txrx_only_epy_block_0 as epy_block_0  # embedded python block
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
        self.num_zeros = num_zeros = 1000
        self.num_header_symbs = num_header_symbs = 3
        self.num_data_symbs = num_data_symbs = 7
        self.wide_samp_rate = wide_samp_rate = 32e6
        self.time_steps = time_steps = 10
        self.num_samps = num_samps = num_data_symbs*80+num_header_symbs*80
        self.front_pad = front_pad = num_zeros
        self.back_pad = back_pad = num_zeros
        self.snr = snr = 20
        self.signal_samp_rate = signal_samp_rate = 1e6
        self.num_channels = num_channels = 8
        self.head_size = head_size = int((front_pad+back_pad+num_samps)*(wide_samp_rate/(1e6))*time_steps)
        self.fft_len = fft_len = int(64)
        self.taps = taps = firdes.low_pass_2(1.0,1,(1/32)-0.01,0.01,80,window.WIN_BLACKMAN_HARRIS)
        self.samps_per_symb = samps_per_symb = float(wide_samp_rate/signal_samp_rate)
        self.rand_seed = rand_seed = int(time.time())
        self.num_samps_per_step = num_samps_per_step = head_size/time_steps
        self.noise_volt = noise_volt = pow(1.0/(fft_len*2*pow(10.0,snr/10.0)),0.5)
        self.cent_freq_list = cent_freq_list = [int(i) for i in np.linspace(-wide_samp_rate/2+signal_samp_rate/2, wide_samp_rate/2-signal_samp_rate/2, num_channels)]
        self.cent_freq = cent_freq = 0e6

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            (int(head_size/time_steps)), #size
            wide_samp_rate, #samp_rate
            "OFDM Burst", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-64, 64)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.ofdm_tx_hier_usrp_tutorial_0 = ofdm_tx_hier_usrp_tutorial(
            back_pad=500,
            buffer_percentage=0.25,
            front_pad=500,
        )
        self.ofdm_rx_hier_tutorial_0 = ofdm_rx_hier_tutorial(
            cent_freq=0e6,
            signal_samp_rate=125e3,
            threshold=0.96,
            wide_samp_rate=125e3,
        )
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, (signal_samp_rate/wide_samp_rate))
        self.low_pass_filter_0 = filter.interp_fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                wide_samp_rate,
                (signal_samp_rate/2),
                (0.25*signal_samp_rate/2),
                window.WIN_HAMMING,
                6.76))
        self.epy_block_0 = epy_block_0.blk(cent_freqs=cent_freq_list, time_steps=time_steps, cent_freq=cent_freq)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '../data/tx_bits.dat', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '../data/rx_bits.dat', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(wide_samp_rate, analog.GR_COS_WAVE, cent_freq, 1.0, 0, 0.0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise_volt, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'tx_cent_freq'), (self.analog_sig_source_x_0, 'cmd'))
        self.msg_connect((self.epy_block_0, 'rx_cent_freq'), (self.ofdm_rx_hier_tutorial_0, 'cent_freq'))
        self.msg_connect((self.epy_block_0, 'tx_cent_freq'), (self.ofdm_tx_hier_usrp_tutorial_0, 'send_burst'))
        self.msg_connect((self.ofdm_rx_hier_tutorial_0, 'packet_data'), (self.epy_block_0, 'packet_results'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_tag_gate_0, 0), (self.ofdm_rx_hier_tutorial_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.ofdm_rx_hier_tutorial_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.ofdm_tx_hier_usrp_tutorial_0, 1), (self.blocks_file_sink_0_0, 0))
        self.connect((self.ofdm_tx_hier_usrp_tutorial_0, 0), (self.mmse_resampler_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_txrx_only")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

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

    def get_wide_samp_rate(self):
        return self.wide_samp_rate

    def set_wide_samp_rate(self, wide_samp_rate):
        self.wide_samp_rate = wide_samp_rate
        self.set_cent_freq_list([int(i) for i in np.linspace(-self.wide_samp_rate/2+self.signal_samp_rate/2, self.wide_samp_rate/2-self.signal_samp_rate/2, self.num_channels)])
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.wide_samp_rate/(1e6))*self.time_steps))
        self.set_samps_per_symb(float(self.wide_samp_rate/self.signal_samp_rate))
        self.analog_sig_source_x_0.set_sampling_freq(self.wide_samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wide_samp_rate, (self.signal_samp_rate/2), (0.25*self.signal_samp_rate/2), window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio((self.signal_samp_rate/self.wide_samp_rate))
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.wide_samp_rate)

    def get_time_steps(self):
        return self.time_steps

    def set_time_steps(self, time_steps):
        self.time_steps = time_steps
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.wide_samp_rate/(1e6))*self.time_steps))
        self.set_num_samps_per_step(self.head_size/self.time_steps)
        self.epy_block_0.time_steps = self.time_steps

    def get_num_samps(self):
        return self.num_samps

    def set_num_samps(self, num_samps):
        self.num_samps = num_samps
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.wide_samp_rate/(1e6))*self.time_steps))

    def get_front_pad(self):
        return self.front_pad

    def set_front_pad(self, front_pad):
        self.front_pad = front_pad
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.wide_samp_rate/(1e6))*self.time_steps))

    def get_back_pad(self):
        return self.back_pad

    def set_back_pad(self, back_pad):
        self.back_pad = back_pad
        self.set_head_size(int((self.front_pad+self.back_pad+self.num_samps)*(self.wide_samp_rate/(1e6))*self.time_steps))

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.set_noise_volt(pow(1.0/(self.fft_len*2*pow(10.0,self.snr/10.0)),0.5))

    def get_signal_samp_rate(self):
        return self.signal_samp_rate

    def set_signal_samp_rate(self, signal_samp_rate):
        self.signal_samp_rate = signal_samp_rate
        self.set_cent_freq_list([int(i) for i in np.linspace(-self.wide_samp_rate/2+self.signal_samp_rate/2, self.wide_samp_rate/2-self.signal_samp_rate/2, self.num_channels)])
        self.set_samps_per_symb(float(self.wide_samp_rate/self.signal_samp_rate))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wide_samp_rate, (self.signal_samp_rate/2), (0.25*self.signal_samp_rate/2), window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio((self.signal_samp_rate/self.wide_samp_rate))

    def get_num_channels(self):
        return self.num_channels

    def set_num_channels(self, num_channels):
        self.num_channels = num_channels
        self.set_cent_freq_list([int(i) for i in np.linspace(-self.wide_samp_rate/2+self.signal_samp_rate/2, self.wide_samp_rate/2-self.signal_samp_rate/2, self.num_channels)])

    def get_head_size(self):
        return self.head_size

    def set_head_size(self, head_size):
        self.head_size = head_size
        self.set_num_samps_per_step(self.head_size/self.time_steps)

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_noise_volt(pow(1.0/(self.fft_len*2*pow(10.0,self.snr/10.0)),0.5))

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb

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

    def get_cent_freq_list(self):
        return self.cent_freq_list

    def set_cent_freq_list(self, cent_freq_list):
        self.cent_freq_list = cent_freq_list
        self.epy_block_0.cent_freqs = self.cent_freq_list

    def get_cent_freq(self):
        return self.cent_freq

    def set_cent_freq(self, cent_freq):
        self.cent_freq = cent_freq
        self.analog_sig_source_x_0.set_frequency(self.cent_freq)
        self.epy_block_0.cent_freq = self.cent_freq




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
