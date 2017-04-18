#!/bin/bash
CONFIG_FILE="$AVOCADO_TEST_DATADIR"/config
DRIVER=`lspci -k | grep -iw "Kernel driver in use" | cut -d ':' -f2 | sort | uniq`

#Loads the kernel driver modules
module_load() {
    echo "Reloading driver $1"
    modprobe $1
    if [ $? != 0 ]; then
        echo "Failed to load driver module $1"
        break;
    fi
    echo
}

#Unloads the kernel driver modules
module_unload() {
    for i in $(cat $CONFIG_FILE | grep "$1=" | awk -F'=' '{print $2}'); do
        module_unload $i
        if [ $? != 0 ]; then
            echo "Failed to unload driver module $i"
            return
        fi
    done
    echo "Unloaded driver $1"
    rmmod $1
    return
}

#Parses the input and then performs module load/unload 
for driver in $DRIVER; do
    echo "Starting driver module load/unload test for $driver"
    echo
    for j in $(seq 1 100) ; do
            module_unload $driver
            # Sleep for 5s to allow the module load to complete
            module_load $driver
            sleep 5
    done
    echo "Finished driver module load/unload test for $driver"
    echo
done
