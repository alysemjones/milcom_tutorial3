import numpy as np
import sys
tx = open('data/tx_bits.dat','rb')
rx = open('data/rx_bits.dat','rb')
b_tx = tx.read()
b_rx = rx.read()
b_tot_tx = ''
b_tot_rx = ''

for i in b_tx:
    i = "{0:08b}".format(i)
    b_tot_tx = b_tot_tx + i

for j in b_rx:
    j = "{0:08b}".format(j)
    b_tot_rx = b_tot_rx + j

print(len(b_tot_tx))
print(len(b_tot_rx))

#print(len(b_tot_tx[0:]))
#print(b_tot_rx)
#b_tot_tx = b_tot_tx[3200:len(b_tot_tx)]
b_tot_tx = b_tot_tx[0:len(b_tot_rx)]
print(len(b_tot_tx))
count = 0
for i in range(len(b_tot_tx)):
    if b_tot_tx[i] != b_tot_rx[i]:
        count += 1

count = count / len(b_tot_tx)
print(count)

