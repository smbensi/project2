import numpy as np
from scipy import signal

a = np.eye(9)
b = np.ones((3,3))
print(a)
print(b)
c = signal.convolve2d(a,b,mode='same')
print(c)
print(c.shape)