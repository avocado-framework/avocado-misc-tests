#!/bin/bash -e

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
# Author: Narasimhan V <sim@linux.vnet.ibm.com>

# Tests the network driver and interface with 'ethtool' command.
# 12 different options of ethtool command are tested for each
# of the interfaces specified in 'config' file

PATH=$(avocado "exec-path"):$PATH

# Install dependencies
if [[ `python -c 'from avocado.utils.software_manager import SoftwareManager; \
    print SoftwareManager().install("ethtool")'` == 'False' ]]
then
    avocado_debug 'Ethtool not installed'
    exit
fi

CONFIG_FILE="$AVOCADO_TEST_DATADIR"/config
interfaces=$(cat $CONFIG_FILE | grep -w "Interfaces" | awk -F'=' '{print $(NF)}')
echo $interfaces

for interface in $interfaces; do
    echo $interface
    ifup $interface
    for command in ifdown ifup; do
        sleep 10
        $command $interface
        sleep 10
        echo "Ethool, $command:"
        output_file=`mktemp`
        echo $output_file
        ethtool ${arg} ${interface} | tee $output_file
        error=$?

        if [ $error == 0 ]; then
            echo "PASS"
        elif grep "Operation not supported" $output_file; then
            echo "PASS (Not supported return:$error)"
        elif grep "no stats available" $output_file; then
            echo "PASS (No stats available return:$error)"
        elif [[ "${arg}" = "-t" && "$command" = "ifdown" ]]; then
            echo "PASS (ethtool -t may fail when iface is down)"
        else
            echo "FAIL (return: $error)"
        fi

        rm -f $output_file
    done
done

