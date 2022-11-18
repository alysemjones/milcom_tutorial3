# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OFDM Transmitter Hierarchical
# Author: Alyse Jones and William "Chris" Headley
# GNU Radio version: 3.10.1.1

from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from math import ceil
from math import floor
from math import log2
from math import sqrt







class ofdm_tx_hier(gr.hier_block2):
    def __init__(self, back_pad=500, cent_freq=0, front_pad=500, signal_samp_rate=1e6/16, wide_samp_rate=20e6):
        gr.hier_block2.__init__(
            self, "OFDM Transmitter Hierarchical",
                gr.io_signature(0, 0, 0),
                gr.io_signature.makev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_char*1]),
        )
        self.message_port_register_hier_in("cent_freq")

        ##################################################
        # Parameters
        ##################################################
        self.back_pad = back_pad
        self.cent_freq = cent_freq
        self.front_pad = front_pad
        self.signal_samp_rate = signal_samp_rate
        self.wide_samp_rate = wide_samp_rate

        ##################################################
        # Variables
        ##################################################
        self.num_guard = num_guard = 11
        self.fft_len = fft_len = 64
        self.pilot_carriers = pilot_carriers = [-21,-7,7,21]
        self.all_carriers = all_carriers = [*range(-int(fft_len/2)+ceil(num_guard/2),0),*range(1,int(fft_len/2)-floor(num_guard/2))]
        self.occupied_carriers = occupied_carriers = [ x for x in all_carriers if x not in set(pilot_carriers)]
        self.cp_len = cp_len = int(fft_len/4)
        self.ofdm_symbol_duration = ofdm_symbol_duration = (1/((1/(fft_len+cp_len))*(signal_samp_rate)))
        self.occupied_carrier_set = occupied_carrier_set = ((occupied_carriers), (occupied_carriers),(occupied_carriers),(occupied_carriers),(occupied_carriers),(occupied_carriers),(occupied_carriers),(occupied_carriers),)
        self.num_pilots = num_pilots = len(pilot_carriers)
        self.num_occupied = num_occupied = len(occupied_carriers)
        self.ifft_time = ifft_time = 1/(signal_samp_rate/fft_len)
        self.training_symbol_time = training_symbol_time = ifft_time/2
        self.pilot_symbols = pilot_symbols = [1.0] * num_pilots
        self.payload_mod = payload_mod = digital.constellation_qpsk()
        self.packet_length_tag_key = packet_length_tag_key = "packet_len"
        self.ofdm_symbol_throughput = ofdm_symbol_throughput = num_occupied*1*(1/2)*1/(ofdm_symbol_duration)
        self.num_payload_symbs = num_payload_symbs = len(occupied_carrier_set)-1
        self.num_header_symbs = num_header_symbs = 1
        self.length_tag_key = length_tag_key = "frame_len"
        self.header_mod = header_mod = digital.constellation_bpsk()
        self.total_throughput = total_throughput = 8*ofdm_symbol_throughput*(140.8e-3)
        self.total_ofdm_symbs = total_ofdm_symbs = num_payload_symbs+num_header_symbs+2
        self.sync_word_1 = sync_word_1 = [0, 0, 0, 0, 0, 0, -1, -1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 0, -1, 1, -1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 0, 0, 0, 0, 0]
        self.sync_word_0 = sync_word_0 = [0, 0, 0, 0, 0, 0, 0, -1.4142135623730951, 0, -1.4142135623730951, 0, 1.4142135623730951, 0, 1.4142135623730951, 0, 1.4142135623730951, 0, -1.4142135623730951, 0, -1.4142135623730951, 0, 1.4142135623730951, 0, 1.4142135623730951, 0, -1.4142135623730951, 0, 1.4142135623730951, 0, 1.4142135623730951, 0, -1.4142135623730951, 0, -1.4142135623730951, 0, -1.4142135623730951, 0, 1.4142135623730951, 0, 1.4142135623730951, 0, 1.4142135623730951, 0, -1.4142135623730951, 0, 1.4142135623730951, 0, 1.4142135623730951, 0, 1.4142135623730951, 0, 1.4142135623730951, 0, -1.4142135623730951, 0, 1.4142135623730951, 0, -1.4142135623730951, 0, 0, 0, 0, 0, 0]
        self.sync_symbol_time = sync_symbol_time = training_symbol_time + 2*ifft_time
        self.sc_spacing = sc_spacing = signal_samp_rate/fft_len
        self.pilot_symbol_set = pilot_symbol_set = ((pilot_symbols),(pilot_symbols),(pilot_symbols),(pilot_symbols),(pilot_symbols),(pilot_symbols),(pilot_symbols),(pilot_symbols),)
        self.pilot_carrier_set = pilot_carrier_set = ((pilot_carriers),(pilot_carriers),(pilot_carriers),(pilot_carriers),(pilot_carriers),(pilot_carriers),(pilot_carriers),(pilot_carriers),)
        self.packet_len_bytes = packet_len_bytes = int(num_payload_symbs*(num_occupied*log2(len(payload_mod.points())))/8)
        self.header_len_bits = header_len_bits = num_header_symbs*num_occupied
        self.header_formatter = header_formatter = digital.packet_header_ofdm([occupied_carriers], n_syms=num_header_symbs, len_tag_key=packet_length_tag_key, frame_len_tag_key=length_tag_key, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False)
        self.guard_interval_time = guard_interval_time = (1/((1/cp_len)*(signal_samp_rate)))

        ##################################################
        # Blocks
        ##################################################
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, signal_samp_rate/wide_samp_rate)
        self.low_pass_filter_0 = filter.interp_fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                wide_samp_rate,
                signal_samp_rate/2,
                0.25*signal_samp_rate/2,
                window.WIN_HAMMING,
                6.76))
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (), True, 1)
        self.digital_packet_headergenerator_bb_0 = digital.packet_headergenerator_bb(header_formatter.base(), packet_length_tag_key)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(
            fft_len,
            fft_len + cp_len,
            0,
            packet_length_tag_key)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc( fft_len, occupied_carrier_set, pilot_carrier_set, pilot_symbol_set, ((sync_word_0),(sync_word_1),), packet_length_tag_key, True)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(header_mod.points(), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(payload_mod.points(), 1)
        self.digital_burst_shaper_xx_0 = digital.burst_shaper_cc(firdes.window(5,10,6.76), front_pad, back_pad, False, "packet_len")
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, packet_length_tag_key, 0)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len_bytes, packet_length_tag_key)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_short*1, (int(front_pad-0.1*front_pad),int(total_ofdm_symbs*(fft_len+cp_len)+0.1*front_pad+0.1*back_pad), int(back_pad-0.1*back_pad)))
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(8, payload_mod.bits_per_symbol(), packet_length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_burst_tagger_0 = blocks.burst_tagger(gr.sizeof_gr_complex)
        self.blocks_burst_tagger_0.set_true_tag('burst_start',True)
        self.blocks_burst_tagger_0.set_false_tag('burst_end',False)
        self.analog_sig_source_x_0 = analog.sig_source_c(wide_samp_rate, analog.GR_COS_WAVE, cent_freq, 1.0, 0, 0.0)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, packet_len_bytes*1000))), True)
        self.analog_const_source_x_0_1 = analog.sig_source_s(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0 = analog.sig_source_s(0, analog.GR_CONST_WAVE, 0, 0, 1)
        self.analog_const_source_x_0 = analog.sig_source_s(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self, 'cent_freq'), (self.analog_sig_source_x_0, 'cmd'))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.analog_const_source_x_0_1, 0), (self.blocks_stream_mux_0, 2))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_burst_tagger_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_burst_tagger_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_packet_headergenerator_bb_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.blocks_burst_tagger_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.digital_burst_shaper_xx_0, 0))
        self.connect((self.digital_packet_headergenerator_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.low_pass_filter_0, 0))


    def get_back_pad(self):
        return self.back_pad

    def set_back_pad(self, back_pad):
        self.back_pad = back_pad

    def get_cent_freq(self):
        return self.cent_freq

    def set_cent_freq(self, cent_freq):
        self.cent_freq = cent_freq
        self.analog_sig_source_x_0.set_frequency(self.cent_freq)

    def get_front_pad(self):
        return self.front_pad

    def set_front_pad(self, front_pad):
        self.front_pad = front_pad

    def get_signal_samp_rate(self):
        return self.signal_samp_rate

    def set_signal_samp_rate(self, signal_samp_rate):
        self.signal_samp_rate = signal_samp_rate
        self.set_guard_interval_time((1/((1/self.cp_len)*(self.signal_samp_rate))))
        self.set_ifft_time(1/(self.signal_samp_rate/self.fft_len))
        self.set_ofdm_symbol_duration((1/((1/(self.fft_len+self.cp_len))*(self.signal_samp_rate))))
        self.set_sc_spacing(self.signal_samp_rate/self.fft_len)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wide_samp_rate, self.signal_samp_rate/2, 0.25*self.signal_samp_rate/2, window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio(self.signal_samp_rate/self.wide_samp_rate)

    def get_wide_samp_rate(self):
        return self.wide_samp_rate

    def set_wide_samp_rate(self, wide_samp_rate):
        self.wide_samp_rate = wide_samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.wide_samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.wide_samp_rate, self.signal_samp_rate/2, 0.25*self.signal_samp_rate/2, window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio(self.signal_samp_rate/self.wide_samp_rate)

    def get_num_guard(self):
        return self.num_guard

    def set_num_guard(self, num_guard):
        self.num_guard = num_guard
        self.set_all_carriers([*range(-int(self.fft_len/2)+ceil(self.num_guard/2),0),*range(1,int(self.fft_len/2)-floor(self.num_guard/2))])

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_all_carriers([*range(-int(self.fft_len/2)+ceil(self.num_guard/2),0),*range(1,int(self.fft_len/2)-floor(self.num_guard/2))])
        self.set_cp_len(int(self.fft_len/4))
        self.set_ifft_time(1/(self.signal_samp_rate/self.fft_len))
        self.set_ofdm_symbol_duration((1/((1/(self.fft_len+self.cp_len))*(self.signal_samp_rate))))
        self.set_sc_spacing(self.signal_samp_rate/self.fft_len)

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers
        self.set_num_pilots(len(self.pilot_carriers))
        self.set_occupied_carriers([ x for x in self.all_carriers if x not in set(self.pilot_carriers)])
        self.set_pilot_carrier_set(((self.pilot_carriers),(self.pilot_carriers),(self.pilot_carriers),(self.pilot_carriers),(self.pilot_carriers),(self.pilot_carriers),(self.pilot_carriers),(self.pilot_carriers),))

    def get_all_carriers(self):
        return self.all_carriers

    def set_all_carriers(self, all_carriers):
        self.all_carriers = all_carriers
        self.set_occupied_carriers([ x for x in self.all_carriers if x not in set(self.pilot_carriers)])

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_header_formatter(digital.packet_header_ofdm([self.occupied_carriers], n_syms=self.num_header_symbs, len_tag_key=self.packet_length_tag_key, frame_len_tag_key=self.length_tag_key, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))
        self.set_num_occupied(len(self.occupied_carriers))
        self.set_occupied_carrier_set(((self.occupied_carriers), (self.occupied_carriers),(self.occupied_carriers),(self.occupied_carriers),(self.occupied_carriers),(self.occupied_carriers),(self.occupied_carriers),(self.occupied_carriers),))

    def get_cp_len(self):
        return self.cp_len

    def set_cp_len(self, cp_len):
        self.cp_len = cp_len
        self.set_guard_interval_time((1/((1/self.cp_len)*(self.signal_samp_rate))))
        self.set_ofdm_symbol_duration((1/((1/(self.fft_len+self.cp_len))*(self.signal_samp_rate))))

    def get_ofdm_symbol_duration(self):
        return self.ofdm_symbol_duration

    def set_ofdm_symbol_duration(self, ofdm_symbol_duration):
        self.ofdm_symbol_duration = ofdm_symbol_duration
        self.set_ofdm_symbol_throughput(self.num_occupied*1*(1/2)*1/(self.ofdm_symbol_duration))

    def get_occupied_carrier_set(self):
        return self.occupied_carrier_set

    def set_occupied_carrier_set(self, occupied_carrier_set):
        self.occupied_carrier_set = occupied_carrier_set
        self.set_num_payload_symbs(len(self.occupied_carrier_set)-1)

    def get_num_pilots(self):
        return self.num_pilots

    def set_num_pilots(self, num_pilots):
        self.num_pilots = num_pilots
        self.set_pilot_symbols([1.0] * self.num_pilots)

    def get_num_occupied(self):
        return self.num_occupied

    def set_num_occupied(self, num_occupied):
        self.num_occupied = num_occupied
        self.set_header_len_bits(self.num_header_symbs*self.num_occupied)
        self.set_ofdm_symbol_throughput(self.num_occupied*1*(1/2)*1/(self.ofdm_symbol_duration))
        self.set_packet_len_bytes(int(self.num_payload_symbs*(self.num_occupied*log2(len(payload_mod.points())))/8))

    def get_ifft_time(self):
        return self.ifft_time

    def set_ifft_time(self, ifft_time):
        self.ifft_time = ifft_time
        self.set_sync_symbol_time(self.training_symbol_time + 2*self.ifft_time)
        self.set_training_symbol_time(self.ifft_time/2)

    def get_training_symbol_time(self):
        return self.training_symbol_time

    def set_training_symbol_time(self, training_symbol_time):
        self.training_symbol_time = training_symbol_time
        self.set_sync_symbol_time(self.training_symbol_time + 2*self.ifft_time)

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols
        self.set_pilot_symbol_set(((self.pilot_symbols),(self.pilot_symbols),(self.pilot_symbols),(self.pilot_symbols),(self.pilot_symbols),(self.pilot_symbols),(self.pilot_symbols),(self.pilot_symbols),))

    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_packet_length_tag_key(self):
        return self.packet_length_tag_key

    def set_packet_length_tag_key(self, packet_length_tag_key):
        self.packet_length_tag_key = packet_length_tag_key
        self.set_header_formatter(digital.packet_header_ofdm([self.occupied_carriers], n_syms=self.num_header_symbs, len_tag_key=self.packet_length_tag_key, frame_len_tag_key=self.length_tag_key, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))

    def get_ofdm_symbol_throughput(self):
        return self.ofdm_symbol_throughput

    def set_ofdm_symbol_throughput(self, ofdm_symbol_throughput):
        self.ofdm_symbol_throughput = ofdm_symbol_throughput
        self.set_total_throughput(8*self.ofdm_symbol_throughput*(140.8e-3))

    def get_num_payload_symbs(self):
        return self.num_payload_symbs

    def set_num_payload_symbs(self, num_payload_symbs):
        self.num_payload_symbs = num_payload_symbs
        self.set_packet_len_bytes(int(self.num_payload_symbs*(self.num_occupied*log2(len(payload_mod.points())))/8))
        self.set_total_ofdm_symbs(self.num_payload_symbs+self.num_header_symbs+2)

    def get_num_header_symbs(self):
        return self.num_header_symbs

    def set_num_header_symbs(self, num_header_symbs):
        self.num_header_symbs = num_header_symbs
        self.set_header_formatter(digital.packet_header_ofdm([self.occupied_carriers], n_syms=self.num_header_symbs, len_tag_key=self.packet_length_tag_key, frame_len_tag_key=self.length_tag_key, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))
        self.set_header_len_bits(self.num_header_symbs*self.num_occupied)
        self.set_total_ofdm_symbs(self.num_payload_symbs+self.num_header_symbs+2)

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key
        self.set_header_formatter(digital.packet_header_ofdm([self.occupied_carriers], n_syms=self.num_header_symbs, len_tag_key=self.packet_length_tag_key, frame_len_tag_key=self.length_tag_key, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))

    def get_header_mod(self):
        return self.header_mod

    def set_header_mod(self, header_mod):
        self.header_mod = header_mod

    def get_total_throughput(self):
        return self.total_throughput

    def set_total_throughput(self, total_throughput):
        self.total_throughput = total_throughput

    def get_total_ofdm_symbs(self):
        return self.total_ofdm_symbs

    def set_total_ofdm_symbs(self, total_ofdm_symbs):
        self.total_ofdm_symbs = total_ofdm_symbs

    def get_sync_word_1(self):
        return self.sync_word_1

    def set_sync_word_1(self, sync_word_1):
        self.sync_word_1 = sync_word_1

    def get_sync_word_0(self):
        return self.sync_word_0

    def set_sync_word_0(self, sync_word_0):
        self.sync_word_0 = sync_word_0

    def get_sync_symbol_time(self):
        return self.sync_symbol_time

    def set_sync_symbol_time(self, sync_symbol_time):
        self.sync_symbol_time = sync_symbol_time

    def get_sc_spacing(self):
        return self.sc_spacing

    def set_sc_spacing(self, sc_spacing):
        self.sc_spacing = sc_spacing

    def get_pilot_symbol_set(self):
        return self.pilot_symbol_set

    def set_pilot_symbol_set(self, pilot_symbol_set):
        self.pilot_symbol_set = pilot_symbol_set

    def get_pilot_carrier_set(self):
        return self.pilot_carrier_set

    def set_pilot_carrier_set(self, pilot_carrier_set):
        self.pilot_carrier_set = pilot_carrier_set

    def get_packet_len_bytes(self):
        return self.packet_len_bytes

    def set_packet_len_bytes(self, packet_len_bytes):
        self.packet_len_bytes = packet_len_bytes
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len_bytes)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len_bytes)

    def get_header_len_bits(self):
        return self.header_len_bits

    def set_header_len_bits(self, header_len_bits):
        self.header_len_bits = header_len_bits

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter

    def get_guard_interval_time(self):
        return self.guard_interval_time

    def set_guard_interval_time(self, guard_interval_time):
        self.guard_interval_time = guard_interval_time

