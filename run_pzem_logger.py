import csv
import time
import argparse
from datetime import datetime
from pzem_tool import PZEM004T
import signal
import sys

def shutdown(sig, frame, f=None):
    print("Received SIGINT, shutting down gracefully...")
    if f is not None:
        f.close()
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="PZEM-004T Data Logger")
    parser.add_argument(
        "-o", "--output", type=str, default="pzem_log.csv",
        help="Output CSV file path"
    )
    parser.add_argument(
        "-i", "--interval", type=float, default=1.0,
        help="Polling interval in seconds (e.g. 1.0)"
    )
    parser.add_argument(
        "-p", "--port", type=str, default="/dev/ttyUSB0",
        help="Serial port for PZEM-004T (e.g. COM3 or /dev/ttyUSB0)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output") 
    parser.add_argument("-a", "--append", action="store_true", help="Append to the log file")

    args = parser.parse_args()

    pzem = PZEM004T(args.port)

    mode = 'a' if args.append else 'w'

    with open(args.output, mode, newline='') as f:
        writer = csv.writer(f)
        if not args.append:
            writer.writerow(['timestamp', 'voltage', 'current', 'frequency'])

        signal.signal(signal.SIGINT, lambda sig,frame: shutdown(sig,frame,pzem))

        try:
            while True:
                data = pzem.get_measurements()
                now = datetime.now().isoformat()
                writer.writerow([now, data['voltage'], data['current'], data['frequency']])
                f.flush()
                if args.verbose:
                    print(f"[{now}] V={data['voltage']}V  I={data['current']}A  F={data['frequency']}Hz")
                time.sleep(args.interval)

        except KeyboardInterrupt:
            print("\nLogging stopped by Ctrl+C.")
        finally:
            pzem.close()

if __name__ == "__main__":
    main()

