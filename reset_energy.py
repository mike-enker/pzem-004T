from pzem_tool import PZEM004T

pzem = PZEM004T('/dev/ttyUSB0')

pzem.reset_energy()
