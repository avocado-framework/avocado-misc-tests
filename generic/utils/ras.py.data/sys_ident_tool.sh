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

TEST_SCENARIO="sys_ident_tool"

# Loading common functions
. ras.py.data/common_functions.sh

# Printing log header
print_header

# sys_ident provides unique system identification information
exec_cmd "sys_ident -p"
exec_cmd "sys_ident -s"

exit $IS_FAILED
