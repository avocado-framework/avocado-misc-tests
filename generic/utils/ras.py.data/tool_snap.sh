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

echo "===============Executing snap tool test==============="

# snap tool collects the log and saves it as tar file
run_cmd "snap" 
tar -xf snap*
rm -rf snap*
rm -rf ibmsupt*
run_cmd "snap -h" 
run_cmd "snap -a" 
rm -rf snap*
run_cmd "snap -d /tmp/ibmibm"
tar -xf snap*
rm -rf ibmibm
rm -rf snap* 
run_cmd "snap -o mysnap.tar.gz" 
rm -rf mysnap.tar.gz
run_cmd "snap -t" 
rm -rf snap* 
run_cmd "snap -v" 
rm -rf snap*

exit $FAIL_FLAG
