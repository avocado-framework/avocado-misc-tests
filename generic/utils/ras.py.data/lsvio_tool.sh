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

echo "===============Executing lsvio tool test==============="

# lsvio lists the virtual I/O adopters and devices
run_cmd "lsvio -h"
run_cmd "lsvio -v"
run_cmd "lsvio -s"
run_cmd "lsvio -e"
run_cmd "lsvio -d"

exit $FAIL_FLAG
