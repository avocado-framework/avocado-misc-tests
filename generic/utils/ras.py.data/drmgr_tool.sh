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
# Author: Pavithra <pavrampu@linux.vnet.ibm.com>

# Loading common functions
. ras.py.data/common_functions.sh

TEST_SCENARIO="drmgr tool"

# Printing log header
print_header

# drmgr can be used for pci, cpu or memory hotplug
exec_cmd "drmgr -h"
exec_cmd "drmgr -C"
lcpu_count=`lparstat -i | grep "Online Virtual CPUs" | cut -d':' -f2`

if [[ ! -z $lcpu_count ]]; then
    if [ $lcpu_count -ge 2 ]; then
        exec_cmd "drmgr -c cpu -r 1"
        exec_cmd "lparstat"
        exec_cmd "drmgr -c cpu -a 1"
        exec_cmd "lparstat"
    fi
fi

exit $IS_FAILED
