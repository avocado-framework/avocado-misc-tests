#!/bin/bash

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: 2016 IBM
# Author: Harsha Thyagaraja <harshkid@linux.vnet.ibm.com>

CONFIG_FILE="$AVOCADO_TEST_DATADIR"/config
DRIVER=`lspci -k | grep -iw "Kernel driver in use" | cut -d ':' -f2 | sort | uniq`

module_load() {
    echo "Reloading driver $1"
    modprobe $1
    if [ $? != 0 ]; then
        echo "Failed to load driver module $1"
        break;
    fi
    echo
}


module_unload() {
    for i in $(cat $CONFIG_FILE | grep "$1=" | awk -F'=' '{print $2}'); do
        module_unload $i
        if [ $? != 0 ]; then
            return
        fi
    done
    echo "Unloaded driver $1"
    rmmod $1
    if [ $? != 0 ]; then
        echo "Failed to unload driver module $i"
        break;
    fi
}


for driver in $DRIVER; do
    echo "Starting driver module load/unload test for $driver"
    echo
    for j in $(seq 1 100) ; do
        module_unload $driver
        # Sleep for 5s to allow the module unload to complete
        sleep 5
        module_load $driver
        # Sleep for 5s to allow the module load to complete
        sleep 5
    done
    echo "Finished driver module load/unload test for $driver"
    echo
done
