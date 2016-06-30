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

FAIL_FLAG=0

# Function to execute the command

run_cmd()
{   echo "Output of command \"$1\":"
    echo "==============================="
    eval $1 

    if [ $? != 0 ]; then
        FAIL_FLAG=1
    fi
    
    return 0
}
