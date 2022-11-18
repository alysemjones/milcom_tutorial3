import numpy
from math import sqrt

fft_len = 64
active_carriers = list(range(6, 6+26)) + list(range(1+6+26, 1+6+26+26))

bpsk = {0: sqrt(2), 1: -sqrt(2)}
sw1 = [bpsk[numpy.random.randint(2)]  if x in active_carriers and x % 2 else 0 for x in range(fft_len)]

bpsk = {0: 1, 1: -1}
sw2 = [bpsk[numpy.random.randint(2)] if x in active_carriers else 0 for x in range(fft_len)]
sw2[0] = 0j

print(sw1)
print('\n')
print(sw2)
