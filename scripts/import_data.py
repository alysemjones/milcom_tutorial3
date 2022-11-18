import numpy as np
import sys
import matplotlib.pyplot as plt
import nitime.utils as utils
import nitime.timeseries as ts
import nitime.viz as viz

def signaltonoise(a, axis=0, ddof=0):
	"""
	The signal-to-noise ratio of the input data.
	Returns the signal-to-noise ratio of `a`, here defined as the mean
	divided by the standard deviation.
	Parameters
	----------
	a : array_like
	    An array_like object containing the sample data.
	axis : int or None, optional
	    Axis along which to operate. Default is 0. If None, compute over
	    the whole array `a`.
	ddof : int, optional
	    Degrees of freedom correction for standard deviation. Default is 0.
	Returns
	-------
	s2n : ndarray
	    The mean to standard deviation ratio(s) along `axis`, or 0 where the
	    standard deviation is 0.
	"""
	a = np.asanyarray(a)
	m = a.mean(axis)
	sd = a.std(axis=axis, ddof=ddof)
	return np.where(sd == 0, 0, m/sd)

x = np.fromfile('data/rx_sig_low.dat',dtype=np.complex64)
dat = x[0::2] + 1j*x[1::2]
print(signaltonoise(dat))

t = np.arange(len(dat))
#plt.specgram(dat,Fs=1e6)
plt.plot(t,dat)
#manager = plt.get_current_fig_manager()
#manager.full_screen_toggle()
plt.show()
