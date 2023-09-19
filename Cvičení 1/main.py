import numpy as np
import matplotlib.pyplot as plt
import struct
with open('data/cv01_dobryden.wav', 'rb') as f:
    # head
    data = f.read(4)
    A1 = struct.unpack('i', f.read(4))[0]
    WAVE = f.read(4)
    FMT = f.read(4)
    FORMAT = f.read(4)
    COMPRESSION = f.read(2)
    COMPRESSION = f.read(2)
    VF = struct.unpack('i', f.read(4))[0]
    PB = f.read(4)
    VB = f.read(2)
    VV = f.read(2)
    DATA = f.read(4)
    A2 = struct.unpack('i', f.read(4))[0]

    print(VF, WAVE, FMT)
    # data
    SIG = np.zeros(A2)
    for i in range(0, A2):
        SIG[i] = struct.unpack('B', f.read(1))[0]

t = np.arange(A2).astype(float)/VF
plt.plot(t, SIG)
plt.xlabel('t[s]')
plt.ylabel('A[-]')
plt.show()
