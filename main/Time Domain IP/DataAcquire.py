from model.hardware.mso5104.pyMSO5104 import pyMSO5104
import numpy as np
from model.data.TDIPData import TDIPData

# User Input Code Section
# Number of repeat reading for final average
n = 10
# File name to save the data
filename = "S11_TDIP_1Hz"
# Measuring Resistance
R = 336.2

# Main Code Section
mso = pyMSO5104()
mso.open_instrument()

Va = np.zeros(1000)
Vm = np.zeros(1000)
Vn = np.zeros(1000)
Vb = np.zeros(1000)
for i in range(n):
    mso.trigger_single()
    mso.wait_for_trigger()
    Va += mso.record_waveform(1)
    Vm += mso.record_waveform(2)
    Vn += mso.record_waveform(3)
    Vb += mso.record_waveform(4)
t = mso.get_x_axis()
mso.close()

Va /= n
Vm /= n
Vn /= n
Vb /= n

tdip = TDIPData(R)
tdip.set_data(t, Va, Vm, Vn, Vb)
tdip.save_data_to_file(filename)
