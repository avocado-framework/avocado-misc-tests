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

echo "===============Executing lsmcode tool test==============="

# lsmcode provides FW version information
run_cmd "lsmcode"
run_cmd "lsmcode -A"
run_cmd "lsmcode -v"
run_cmd "lsmcode -D"
path=`find / -iname vpd.db`

if [ "$path" != "" ]; then
    cp $path /root
    run_cmd "lsmcode --path=/root/vpd.db"
    rm -rf /root/vpd.db
    file=`find / -iname vpd.*.gz | head -1`
    run_cmd "lsmcode --zip=$file"
fi

exit $FAIL_FLAG
