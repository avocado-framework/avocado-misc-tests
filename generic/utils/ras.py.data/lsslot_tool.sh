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

TEST_SCENARIO="lsslot tool"

# Printing log header
print_header

# lsslot lists the slots based on the option provided 
exec_cmd "lsslot" 
exec_cmd "lsslot -c mem" 
exec_cmd "lsslot -ac pci"
exec_cmd "lsslot -c cpu -b"
exec_cmd "lsslot -c pci -o" 
slot=`lsslot | cut -d' ' -f1 | head -2 | tail -1`
exec_cmd "lsslot -s \"$slot\""

exit $IS_FAILED
