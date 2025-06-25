import argparse
from pzem_tool import PZEM004T

def main():

    parser = argparse.ArgumentParser(description="PZEM-004T energy reset tool")
    parser.add_argument(
        "-p", "--port", type=str, default="/dev/ttyUSB0",
        help="Serial port for PZEM-004T (e.g. COM3 or /dev/ttyUSB0)"
    )

    args = parser.parse_args()

    pzem = PZEM004T(args.port)

    pzem.reset_energy()
    print(f'Energy reset for {args.port}')

if __name__ == "__main__":
    main()

