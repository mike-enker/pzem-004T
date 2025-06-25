import argparse
from pzem_tool import PZEM004T

def main():

    parser = argparse.ArgumentParser(description="PZEM-004T print current values")
    parser.add_argument(
        "-p", "--port", type=str, default="/dev/ttyUSB0",
        help="Serial port for PZEM-004T (e.g. COM3 or /dev/ttyUSB0)"
    )

    args = parser.parse_args()

    pzem = PZEM004T(args.port)

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

if __name__ == "__main__":
    main()

