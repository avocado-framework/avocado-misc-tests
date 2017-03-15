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

echo "===============Executing ofpathname tool test==============="

# ofpathname translates the device name between logical name and Open Firmware name 
run_cmd "ofpathname -h" 
run_cmd "ofpathname -V" 
disk_name=`df -h | egrep '(s|v)da[1-8]' | tail -1 | cut -d' ' -f1`
run_cmd "ofpathname $disk_name"
of_name=`ofpathname $disk_name`
run_cmd "ofpathname -l $of_name" 

exit $FAIL_FLAG
