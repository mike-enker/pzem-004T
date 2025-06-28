#!/bin/bash

lsusb | grep PL2303 
if [ $? != 0 ];
then
    echo PZEM USB device not found
    exit -1
fi

# has to run elevated to read USB (?)
# assumes proper sudoers config
if [ $(whoami) != root ];
then 
    sudo "$0" "$@"
    exit $?
fi

echo Running as: $(whoami)

DEV=/dev/$(dmesg | grep "pl2303 converter now attached to tty" | tail -1 | awk '{print $NF}')
if [ ! -e $DEV ]; 
then 
    echo Device not found: $DEV
    exit -2
fi

echo Device found: $DEV

cd "$HOME"/src/pzem
. pzem_env/bin/activate

CSV="$HOME/logs/pzem_log.csv"
LOG="$HOME/logs/pzem_log.out"
echo Starting logger at $(date) >> $LOG

python ./run_pzem_logger.py -i 0 -o $CSV -p "$DEV" -a >> $LOG 2>&1 &

echo pzem logger started, see output in $CSV, log in $LOG
