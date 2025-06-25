from pzem_tool import PZEM004T

pzem = PZEM004T('/dev/ttyUSB0')

try:
    data = pzem.get_measurements()
    print("PZEM-004T Readings:")

    print(f"  Voltage:        {data['voltage']} V")
    print(f"  Current:        {data['current']} A")
    print(f"  Power:          {data['power']} W")
    print(f"  Energy:         {data['energy']} Wh")
    print(f"  Frequency:      {data['frequency']} Hz")
    print(f"  Power Factor:   {data['power_factor']}")
    print(f"  Alarm Active:   {'YES' if data['alarm'] else 'Nope'}")

finally:
    pzem.close()

