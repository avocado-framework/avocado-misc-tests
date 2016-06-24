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

TEST_SCENARIO="nvram tool"

# Printing log header
print_header

# nvram command retrieves and displays NVRAM data
exec_cmd "nvram --help"
exec_cmd "nvram --partitions" 
exec_cmd "nvram --print-config -p common"  
exec_cmd "nvram --dump common --verbose"

exit $IS_FAILED
