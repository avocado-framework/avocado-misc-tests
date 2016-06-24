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

CURRENT_DIR=`pwd`
TMP_LOG="$CURRENT_DIR/ras.py.data/log/tmp.log"

# Initializing variable to determine script result
IS_FAILED=0

# Function to execute the command passed and return the exit code
exec_cmd ()
{   echo "Output of the command \"$1\":"
    eval $1 1>&2 >$TMP_LOG
    EXIT_CODE=$?
    cat $TMP_LOG 
    rm -f $TMP_LOG

    if [ $EXIT_CODE != 0 ]; then
        echo "ERROR: Command \"$1\" ended abnormally with exit code $EXIT_CODE. Please verify." 
        IS_FAILED=1
    fi

    return $EXIT_CODE
}

# Function to print header with tool name
print_header ()
{
cat << TEXT 
********************************************************************************
* RAS Testcase: $TEST_SCENARIO
* Date: $(date +'%d/%m/%y %H:%M')
********************************************************************************
TEXT

return 0
}
