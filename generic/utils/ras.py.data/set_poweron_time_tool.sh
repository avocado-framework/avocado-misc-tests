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

TEST_SCENARIO="set_poweron_time tool"

# Printing log header
print_header

# set_poweron_time schedules the power on time
exec_cmd "set_poweron_time -m" 
exec_cmd "set_poweron_time -h"
exec_cmd "set_poweron_time -d m2" 
exec_cmd "set_poweron_time -t M6D15h12"

exit $IS_FAILED
