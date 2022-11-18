#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Interference
# Author: alysemjones
# GNU Radio version: 3.9.6.0-rc1

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np



from gnuradio import qtgui

class interference(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Interference", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Interference")
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

        self.settings = Qt.QSettings("GNU Radio", "interference")

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
        self.wide_samp_rate = wide_samp_rate = 8e6/8
        self.num_channels = num_channels = 8
        self.signal_samp_rate = signal_samp_rate = wide_samp_rate/num_channels
        self.cent_freq_list = cent_freq_list = np.linspace(-wide_samp_rate/2+signal_samp_rate/2, wide_samp_rate/2-signal_samp_rate/2, num_channels)
        self.int_freq = int_freq = cent_freq_list[3]

        ##################################################
        # Blocks
        ##################################################
        self.digital_psk_mod_0_0 = digital.psk.psk_mod(
            constellation_points=8,
            mod_code="gray",
            differential=True,
            samples_per_symbol=num_channels*4,
            excess_bw=0.001,
            verbose=False,
            log=False)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_c(wide_samp_rate, analog.GR_COS_WAVE, int_freq, 2, 0, 0)
        self.analog_random_source_x_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 100))), True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self, 'int_freq'), (self.analog_sig_source_x_0_0_0, 'cmd'))
        self.connect((self.analog_random_source_x_0_0, 0), (self.digital_psk_mod_0_0, 0))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_multiply_xx_1, 0), (self, 0))
        self.connect((self.digital_psk_mod_0_0, 0), (self.blocks_multiply_xx_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "interference")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_wide_samp_rate(self):
        return self.wide_samp_rate

    def set_wide_samp_rate(self, wide_samp_rate):
        self.wide_samp_rate = wide_samp_rate
        self.set_cent_freq_list(np.linspace(-self.wide_samp_rate/2+self.signal_samp_rate/2, self.wide_samp_rate/2-self.signal_samp_rate/2, self.num_channels))
        self.set_signal_samp_rate(self.wide_samp_rate/self.num_channels)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.wide_samp_rate)

    def get_num_channels(self):
        return self.num_channels

    def set_num_channels(self, num_channels):
        self.num_channels = num_channels
        self.set_cent_freq_list(np.linspace(-self.wide_samp_rate/2+self.signal_samp_rate/2, self.wide_samp_rate/2-self.signal_samp_rate/2, self.num_channels))
        self.set_signal_samp_rate(self.wide_samp_rate/self.num_channels)

    def get_signal_samp_rate(self):
        return self.signal_samp_rate

    def set_signal_samp_rate(self, signal_samp_rate):
        self.signal_samp_rate = signal_samp_rate
        self.set_cent_freq_list(np.linspace(-self.wide_samp_rate/2+self.signal_samp_rate/2, self.wide_samp_rate/2-self.signal_samp_rate/2, self.num_channels))

    def get_cent_freq_list(self):
        return self.cent_freq_list

    def set_cent_freq_list(self, cent_freq_list):
        self.cent_freq_list = cent_freq_list
        self.set_int_freq(self.cent_freq_list[3])

    def get_int_freq(self):
        return self.int_freq

    def set_int_freq(self, int_freq):
        self.int_freq = int_freq
        self.analog_sig_source_x_0_0_0.set_frequency(self.int_freq)




def main(top_block_cls=interference, options=None):

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
