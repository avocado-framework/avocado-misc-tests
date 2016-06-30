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

. ras.py.data/run_cmd_func.sh

echo "===============Executing lsslot tool test==============="

# lsslot lists the slots based on the option provided 
run_cmd "lsslot" 
run_cmd "lsslot -c mem" 
run_cmd "lsslot -ac pci"
run_cmd "lsslot -c cpu -b"
run_cmd "lsslot -c pci -o" 
slot=`lsslot | cut -d' ' -f1 | head -2 | tail -1`
run_cmd "lsslot -s \"$slot\""

exit $FAIL_FLAG
