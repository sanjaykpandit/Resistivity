import visa
from time import sleep
from numpy import array, arange, linspace, ndarray
from model.Logger import Logger

from typing import Iterable

from model.data.WaveformDataList import WaveformData
from model.inversion.__CosFit import CosFit

class pyMSO5104:
    def __init__(self):

        self.mso5104 = None
        self.device_info = ''
        self.logger = Logger()
        self.logger.setDefaultTitle("model.hardware.mso5104.pyMSO5104")

    @staticmethod
    def instrument_available():
        instrument_address = r"TCPIP::10.106.118.100::INSTR"
        resource_manager = visa.ResourceManager()
        try:
            mso5104 = resource_manager.open_resource(instrument_address)
            mso5104.query('*IDN?')
            mso5104.close()
            return True
        except visa.VisaIOError:
            return False

    def open_instrument(self):
        instrument_address = r"TCPIP::10.106.118.100::INSTR"
        resource_manager = visa.ResourceManager()
        try:
            self.mso5104 = resource_manager.open_resource(instrument_address)
            self.logger.InfoLog(self.mso5104.query("*IDN?"))
            self.mso5104.timeout = 25000
            return True
        except visa.VisaIOError:
            self.mso5104 = None
            return False

    def close(self):
        self.mso5104.close()

    def set_mem_depth(self, depth: str):
        self.mso5104.write(':ACQ:MDEP ' + depth)

    def run(self):
        self.mso5104.write(':RUN')

    def stop(self):
        self.mso5104.write(':RUN')

    def get_screenshot(self):
        return self.mso5104.query_binary_values(':DISP:DATA?', datatype='B', is_big_endian=True)

    def setup_channel(self, channel: int, offset: float, probeAttn: str, coupling: str):
        if 1 <= channel <= 4:
            command_list = [':CHAN' + str(channel) + ':DISP ON',
                            ':CHAN' + str(channel) + ':COUP ' + coupling,
                            ':CHAN' + str(channel) + ':OFFS ' + str(offset),
                            ':CHAN' + str(channel) + ':PROB ' + probeAttn]
            for command in command_list:
                self.mso5104.write(command)

    def setup_trigger(self, sweep: str, level: str, edge_slope: str):
        command_list = [':TRIG:MODE EDGE',
                        ':TRIG:SWE ' + sweep,
                        ':TRIG:EDGE:SLOP ' + edge_slope,
                        ':TRIG:EDGE:LEV ' + level]
        for command in command_list:
            self.mso5104.write(command)

    def setup_waveform_generator(self, function: str, voltage_level: str, offset: str):
        command_list = [':SOUR1:OUTP 1',
                        ':SOUR1:FUNC ' + function,
                        ':SOUR1:VOLT ' + voltage_level,
                        ':SOUR1:VOLT:OFFS ' + offset]
        for command in command_list:
            self.mso5104.write(command)

    def set_waveform_generator_frequency(self, frequency: float):
        self.mso5104.write(':SOUR1:FREQ ' + str(frequency))

    def get_waveform_generator_frequency(self):
        return float(self.mso5104.query(':SOUR1:FREQ?'))

    def set_measure_source_channel(self, channel: int):
        self.mso5104.write(':MEAS:SOUR CHAN' + str(channel))

    def get_measured_frequency(self, channel: int):
        self.mso5104.write(':MEAS:SOUR CHAN' + str(channel))
        try:
            f = float(self.mso5104.query(':MEAS:FREQ?'))
        except visa.VisaIOError:
            return -1
        return f

    def get_measured_amplitude(self, channel: int):
        self.mso5104.write(':MEAS:SOUR CHAN' + str(channel))
        try:
            a = float(self.mso5104.query(':MEAS:VPP?')) / 2.0
        except visa.VisaIOError:
            return -1
        return a

    def trigger_single(self):
        self.mso5104.write(':TRIG:SWE SING')

    def set_x_scale(self, scale: float, offset: float):
        command_list = [':TIM:MAIN:SCAL ' + str(scale),
                        ':TIM:MAIN:OFFS ' + str(offset)]
        for command in command_list:
            self.mso5104.write(command)

    def set_y_scale(self, channel: int, scale: float):
        self.mso5104.write(':CHAN' + str(channel) + ':SCAL ' + "{0:0.4f}".format(scale))

    def set_y_offset(self, channel:int, offset: float):
        self.mso5104.write(':CHAN' + str(channel) + ':OFFS ' + "{0:0.4f}".format(offset))

    def record_waveform(self, channel):
        if 1 <= channel <= 4:
            command_list = [':WAV:SOUR CHAN' + str(channel),
                            ':WAV:MODE NORM',
                            ':WAV:FORM BYTE']
            for command in command_list:
                self.mso5104.write(command)

            y = self.mso5104.query_binary_values(':WAV:DATA?', datatype='B', is_big_endian=True)
            y_increment = float(self.mso5104.query(':WAV:YINC?'))
            y_reference = int(self.mso5104.query(':WAV:YREF?'))
            y_origin = float(self.mso5104.query(':WAV:YOR?'))

            y = array(y)
            y = y - y_reference - y_origin
            y = y * y_increment
            return y

    def record_average_waveform(self, channels: Iterable, num_average: int = 1) -> ndarray:
        y = []
        for i in range(num_average):
            for channel in channels:
                if i == 0:
                    y.append(self.record_waveform(channel))
                else:
                    y[channel-1] += self.record_waveform(channel)
            if num_average > 1:
                sleep(0.1)
                self.trigger_single()
                self.wait_for_trigger()

        for c in channels:
            y[c-1] = y[c-1] / num_average

        return array(y)

    def get_x_axis(self):
        x_increment = float(self.mso5104.query(':WAV:XINC?'))
        x = arange(1000)*x_increment
        return x

    def trigger_status(self):
        return self.mso5104.query(':TRIG:STAT?').strip()

    def wait_for_trigger(self):
        while self.trigger_status() != 'STOP':
            sleep(0.5)
            continue
