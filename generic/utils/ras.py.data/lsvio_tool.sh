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

TEST_SCENARIO="lsvio tool"

# Printing log header
print_header

# lsvio lists the virtual I/O adopters and devices
exec_cmd "lsvio -h"
exec_cmd "lsvio -v"
exec_cmd "lsvio -s"
exec_cmd "lsvio -e"
exec_cmd "lsvio -d"

exit $IS_FAILED
