from model.hardware.mso5104.pyMSO5104 import pyMSO5104
import os
from time import sleep
from numpy import array, random

from model.data.WaveformDataList import WaveformData
from model.inversion.CosFit import CosFit
from model.Logger import Logger


# User Inpur Code Section
# Folder location for saving recorded data
folder = r'Samples/H3C/S11T/Waveforms'

# Frequency list for with the resistivity measurement is required
f = array([0.1, 0.2, 0.4, 0.6, 0.8,
           1, 2, 4, 6, 8,
           10, 20, 40, 60, 80,
           100, 200, 400, 600, 800,
           1000, 2000, 4000, 6000, 8000,
           10000])

# List of frequency at which the waveform must be centered on the oscilloscope
cf = array([1, 4, 10, 40, 100, 400, 1000, 4000, 10000])

# No. of repeat readings for each frequency in the frequency list
# This is averaged before recording into Excel File
avg = array([1, 1, 1, 1, 1,
             1, 1, 2, 2, 2,
             4, 4, 4, 4, 4,
             8, 8, 8, 8, 8,
             8, 8, 8, 8, 8,
             8])

# No. of frequency sweep required
sub = ['a', 'b', 'c']
sub_index = [0, 1, 2]


# Main Code Starts
def float_equal(f1, f2, df):
    if f2 - df < f1 < f2 + df:
        return True
    else:
        return False

def get_waveforms(channels, tol=20):
    v = []
    n = len(channels)
    mso.trigger_single()
    mso.wait_for_trigger()
    t = mso.get_x_axis()
    for i in range(n):
        v.append(mso.record_waveform(channels[i]))

    pa = []
    for i in range(n):
        e = 1E6
        y = v[i]
        p = []
        iter = 0
        while e > tol:
            cs = CosFit(t, y)
            p = cs.get_parameter()
            if p[0] < 0.1:
                e = 1E6
            else:
                e = cs.get_error(p)
            iter += 1
            if iter > 100:
                iter = 0
                mso.trigger_single()
                mso.wait_for_trigger()
                t = mso.get_x_axis()
                v = []
                for j in range(n):
                    v.append(mso.record_waveform(channels[j]))
            y = v[i] + (random.rand(len(t))-0.5)*0.2
        pa.append(p)
    return pa

def center_waveforms(channels, tol=10):
    n = len(channels)
    pa = get_waveforms(channels)
    for i in range(n):
        p = pa[i]
        logger.InfoLog("Center Waveform " + "Channel {0} ".format(channels[i]) + "{0:.4f}, {1:.4f}, {2:.4f}, {3:.4f}".format(p[0], p[1], p[2], p[3]))
        if channels[i] == 3:
            mso.set_y_scale(channels[i], p[0] / 2)
        else:
            mso.set_y_scale(channels[i], p[0] / 3)
        mso.set_y_offset(channels[i], -p[3])

logger = Logger()
logger.setDefaultTitle("DataAcquire")

yscale = [0.3, 1, 1, 1]
cur_res_int = 0
sleep(1)

mso = pyMSO5104()
mso.open_instrument()
mso.setup_channel(1, 0, '1', 'DC')
mso.setup_channel(2, 0, '1', 'DC')
mso.setup_channel(3, 0, '1', 'DC')
mso.setup_channel(4, 0, '1', 'DC')
mso.set_y_scale(1, yscale[0])
mso.set_y_scale(2, yscale[1])
mso.set_y_scale(3, yscale[2])
mso.set_y_scale(4, yscale[3])
mso.set_y_offset(1, 0)
mso.set_y_offset(2, 0)
mso.set_y_offset(3, 0)
mso.set_y_offset(4, 0)
mso.setup_trigger('SING', '0', 'POS')
mso.setup_waveform_generator('SIN', '2', '0')
a = [0]


f = f[::-1]
avg = avg[::-1]
cf = cf[::-1]
cur_res = 1000
average_readings = 1
wft = 1E-3
mset = False
n = len(f)

for jsub in sub_index:
    lfi = 0
    lf = cf[0]
    for i in range(n):
        if os.path.exists(os.path.join(folder, "{0:0.1f}{1}".format(f[i], sub[jsub])) + ".xlsx"):
            if f[i] == lf:
                lfi += 1
                if lfi < len(cf):
                    lf = cf[lfi]
            continue

        average_readings = avg[i]

        sleep(0.5)
        mso.set_waveform_generator_frequency(f[i])
        mso.set_x_scale(1/f[i], 0)

        if f[i] >= 100:
            if not mset:
                mset = True
                mso.run()
                sleep(0.5)
                mso.set_mem_depth('10k')
                mso.stop()
        else:
            if mset:
                mset = False
                mso.run()
                sleep(0.5)
                mso.set_mem_depth('AUTO')
                mso.stop()


        logger.InfoLog("Frequency Requested {0:.2f}".format(f[i]))

        if f[i] == lf:
            lfi += 1
            if lfi < len(cf):
                lf = cf[lfi]
            center_waveforms([2, 3, 4])

        mso.trigger_single()
        mso.wait_for_trigger()

        x = mso.get_x_axis()
        y = mso.record_average_waveform([1, 2, 3, 4], average_readings)

        cs = CosFit(x, y[0])
        p1 = cs.get_parameter()
        freq_1 = p1[1]
        inv_err_1 = cs.get_error(p1)

        cs = CosFit(x, y[3])
        p2 = cs.get_parameter()
        freq_2 = p2[1]
        inv_err_2 = cs.get_error(p2)
        vr = p1[0]/p2[0]
        pd = p1[2]-p2[2]

        logger.InfoLog("CosFit Inversion Error: {0:.2f}, {1:.2f}".format(inv_err_1, inv_err_2))
        logger.InfoLog("Frequency = {0:0.2f}, {1:0.2f}, {2:0.2f}".format(f[i], freq_1, freq_2))
        logger.InfoLog("Voltage Ratio = {0:0.2f}, Phase Difference = {1:0.2f} mRad, average = {2}".format(vr, pd * 1000, average_readings))

        while (not float_equal(freq_1, freq_2, wft*(freq_1+freq_2)/2)):
            logger.WarningLog("Waveform Frequency not within tolerance. ReTriggering")

            mso.trigger_single()
            mso.wait_for_trigger()

            x = mso.get_x_axis()
            y = mso.record_average_waveform([1, 2, 3, 4], average_readings)

            cs = CosFit(x, y[0])
            p1 = cs.get_parameter()
            freq_1 = p1[1]
            inv_err_1 = cs.get_error(p1)

            cs = CosFit(x, y[3])
            p2 = cs.get_parameter()
            freq_2 = p2[1]
            inv_err_2 = cs.get_error(p2)
            vr = p1[0] / p2[0]
            pd = p1[2] - p2[2]

            logger.InfoLog("CosFit Inversion Error: {0:.2f}, {1:.2f}".format(inv_err_1, inv_err_2))
            logger.InfoLog("Frequency = {0:0.2f}, {1:0.2f}, {2:0.2f}".format(f[i], freq_1, freq_2))
            logger.InfoLog("Voltage Ratio = {0:0.2f}, Phase Difference = {1:0.2f} mRad".format(vr, pd * 1000))

        wfd = WaveformData()
        wfd.set_data(f[i], x, y, cur_res, cur_res_int)
        wfd.save_data(os.path.join(folder, "{0:0.1f}{1}".format(f[i], sub[jsub])))
mso.close()

