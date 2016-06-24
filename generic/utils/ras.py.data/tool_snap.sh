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

TEST_SCENARIO="snap tool"

# Printing log header
print_header

# snap tool collects the log and saves it as tar file
exec_cmd "snap" 
tar -xf snap*
rm -rf snap*
rm -rf ibmsupt*
exec_cmd "snap -h" 
exec_cmd "snap -a" 
rm -rf snap*
exec_cmd "snap -d /tmp/ibmibm"
tar -xf snap*
rm -rf ibmibm
rm -rf snap* 
exec_cmd "snap -o mysnap.tar.gz" 
rm -rf mysnap.tar.gz
exec_cmd "snap -t" 
rm -rf snap* 
exec_cmd "snap -v" 
rm -rf snap*

exit $IS_FAILED
