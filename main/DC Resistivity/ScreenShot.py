from model.hardware.mso5104.pyMSO5104 import pyMSO5104

file_path = r'Samples/A2B/S11T/DC_Resistivity.bmp'

mso = pyMSO5104()
mso.open_instrument()

file = open(file_path, 'wb')
file.write(bytes(mso.get_screenshot()))
file.close()

mso.close()