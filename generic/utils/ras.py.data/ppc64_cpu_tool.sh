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

TEST_SCENARIO="ppc64_cpu tool"

# Printing log header
print_header

# ppc64_cpu is used to set cpu options
exec_cmd "ppc64_cpu --smt"
exec_cmd "ppc64_cpu --smt=8"
exec_cmd "ppc64_cpu --smt"
exec_cmd "ppc64_cpu --smt=4"
exec_cmd "ppc64_cpu --smt"
exec_cmd "ppc64_cpu --smt=off"
exec_cmd "ppc64_cpu --smt"
exec_cmd "ppc64_cpu --smt=on"
exec_cmd "ppc64_cpu --smt"
exec_cmd "ppc64_cpu --cores-present"
exec_cmd "ppc64_cpu --cores-on"
exec_cmd "ppc64_cpu --dscr"
exec_cmd "ppc64_cpu --dscr=1"
exec_cmd "ppc64_cpu --dscr"
exec_cmd "ppc64_cpu --dscr=0"
exec_cmd "ppc64_cpu --smt-snooze-delay"
exec_cmd "ppc64_cpu --smt-snooze-delay=200"
exec_cmd "ppc64_cpu --smt-snooze-delay"
exec_cmd "ppc64_cpu --smt-snooze-delay=100"
exec_cmd "ppc64_cpu --run-mode"
exec_cmd "ppc64_cpu --subcores-per-core"

exit $IS_FAILED
