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

TEST_SCENARIO="ofpathname tool"

# Printing log header
print_header

# ofpathname translates the device name between logical name and Open Firmware name 
exec_cmd "ofpathname -h" 
exec_cmd "ofpathname -V" 
disk_name=`df -h | egrep '(s|v)da[1-8]' | tail -1 | cut -d' ' -f1`
exec_cmd "ofpathname $disk_name"
of_name=`ofpathname $disk_name`
exec_cmd "ofpathname -l $of_name" 

exit $IS_FAILED
