#!/bin/bash

lsusb | grep PL2303
if [ $? != 0 ];
then
    echo PZEM USB device not found
    exit 255
fi

# has to run elevated to read USB (?)
# assumes proper sudoers config
if [ "$(whoami)" != root ];
then 
    sudo "$0" "$HOME" "$@"
    exit $?
fi

echo "Running as: $(whoami)"
if [ "$#" -lt 1 ]; then
    echo "Don't run a root directly."
    exit 254
fi

USER_HOME=$1
echo "USER_HOME=$USER_HOME"

DEV=/dev/$(dmesg | grep "pl2303 converter now attached to tty" | tail -1 | awk '{print $NF}')
if [ ! -e "$DEV" ];
then 
    echo "Device not found: $DEV"
    exit 254
fi

echo "Device found: $DEV"

cd "$USER_HOME"/src/pzem || exit 255
. pzem_env/bin/activate

CSV="$USER_HOME/logs/pzem_log.csv"
LOG="$USER_HOME/logs/pzem_log.out"
echo "Starting logger at $(date)" >> "$LOG"

python ./run_pzem_logger.py -i 0 -o "$CSV" -p "$DEV" -a >> "$LOG" 2>&1 &

echo pzem logger started, see output in "$CSV", log in "$LOG"
