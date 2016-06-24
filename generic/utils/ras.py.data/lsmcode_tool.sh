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

TEST_SCENARIO="lsmcode tool"

# Printing log header
print_header

# lsmcode provides FW version information
exec_cmd "lsmcode"
exec_cmd "lsmcode -A"
exec_cmd "lsmcode -v"
exec_cmd "lsmcode -D"
path=`find / -iname vpd.db`

if [ "$path" != "" ]; then
    cp $path /root
    exec_cmd "lsmcode --path=/root/vpd.db"
    rm -rf /root/vpd.db
    file=`find / -iname vpd.*.gz | head -1`
    exec_cmd "lsmcode --zip=$file"
fi

exit $IS_FAILED
