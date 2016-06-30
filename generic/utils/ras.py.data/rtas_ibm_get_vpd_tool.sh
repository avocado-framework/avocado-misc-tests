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

echo "===============Executing rtas_ibm_get_vpd tool test==============="

# rtas_ibm_get_vpd gives vpd data
run_cmd "rtas_ibm_get_vpd >> ras.py.data/log/output"

exit $FAIL_FLAG
