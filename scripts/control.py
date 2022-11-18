import flowgraphs.ofdm_txrx_header as txrx
import time

top_block_cls = txrx.ofdm_txrx_header

tb = top_block_cls()
tb.start()
time.sleep(2)
print(tb.cent_freq)
print(tb.ofdm_rx_hier_0.rx_time)
tb.lock()
tb.cent_freq = 1e6
tb.unlock()
time.sleep(2)
print(tb.cent_freq)
tb.stop()


