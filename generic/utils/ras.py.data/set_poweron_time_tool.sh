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

echo "===============Executing set_poweron_time tool test==============="

# set_poweron_time schedules the power on time
run_cmd "set_poweron_time -m" 
run_cmd "set_poweron_time -h"
run_cmd "set_poweron_time -d m2" 
run_cmd "set_poweron_time -t M6D15h12"

exit $FAIL_FLAG
