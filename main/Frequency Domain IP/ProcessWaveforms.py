from model.inversion.CosFit import CosFit
from model.data.WaveformDataList import WaveformData
from model.data.FitData import FitData
from model.Logger import Logger

import os
import numpy as np

# User Input Code Section
# Folder location recorded waveform data
folder = "Samples/H3C/S11T/Waveforms"


# Main Code Starts from Here
logger = Logger()
logger.setDefaultTitle("ProcessWaveform")

def get_pse(t, v, etol=20):
    y = v
    cs = CosFit(t, y)
    p = cs.get_parameter()
    e = cs.get_error(p)
    return p, cs.get_series(t, p), e

files = os.listdir(folder)
sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))
fd = FitData(2)
for file in sorted_files:
    if file.endswith('.xlsx'):
        wf = WaveformData()
        wf.load_data(os.path.join(folder, file))

        logger.InfoLog("Processing {0}".format(file))

        t = wf.get_time()
        v = wf.get_v(0)
        p0, s0, e0 = get_pse(t, v)

        t = wf.get_time()
        v = wf.get_v(1)
        p1, s1, e1 = get_pse(t, v)

        t = wf.get_time()
        v = wf.get_v(2)
        p2, s2, e2 = get_pse(t, v)

        t = wf.get_time()
        v = wf.get_v(3)
        p3, s3, e3 = get_pse(t, v)

        p = [p0, p1, p2, p3]
        err = [e0, e1, e2, e3]

        n = len(p)
        for i in range(n):
            fd.append_data_from_array(i, p[i], err[i])

fd.save_data(folder)