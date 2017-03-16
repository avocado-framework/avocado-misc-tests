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

TEST_SCENARIO="rtas_errd and rtas_dump tools"

# Printing log header
print_header

# rtas_errd adds RTAS events to /var/log/platform and rtas_dump dumps RTAS events
echo "1 - Cleaning servicelog..."
rm -f /var/log/platform

echo "2 - Injecting event"
exec_cmd "/usr/sbin/rtas_errd -d -f ras.py.data/rtas"

echo "5 - Checking if the event was dumped to /var/log/platform"
exec_cmd "cat /var/log/platform"

exec_cmd "/usr/sbin/rtas_errd -d -f ras.py.data/rtas -p ras.py.data/log/myplatformfile -l ras.py.data/log/mylog"
exec_cmd "cat ras.py.data/log/myplatformfile"
exec_cmd "cat ras.py.data/log/mylog"

echo "6 - Verifying rtas_dump command"
exec_cmd "rtas_dump -f ras.py.data/rtas"

echo "7 - Verifying rtas_dump with event number 2302"
exec_cmd "rtas_dump -f ras.py.data/rtas -n 2302"

echo "8 - Verifying rtas_dump with verbose option"
exec_cmd "rtas_dump -f ras.py.data/rtas -v"

echo "9 - Verifying rtas_dump with width 20"
exec_cmd "rtas_dump -f ras.py.data/rtas -w 20"

exit $IS_FAILED
