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

echo "===============Executing nvram tool test==============="

# nvram command retrieves and displays NVRAM data
run_cmd "nvram --help"
run_cmd "nvram --partitions" 
run_cmd "nvram --print-config -p common"  
run_cmd "nvram --dump common --verbose"

exit $FAIL_FLAG
