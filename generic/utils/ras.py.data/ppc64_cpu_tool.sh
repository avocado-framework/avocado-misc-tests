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

echo "===============Executing ppc64_cpu tool test==============="

# ppc64_cpu is used to set cpu options
run_cmd "ppc64_cpu --smt"
run_cmd "ppc64_cpu --smt=8"
run_cmd "ppc64_cpu --smt"
run_cmd "ppc64_cpu --smt=4"
run_cmd "ppc64_cpu --smt"
run_cmd "ppc64_cpu --smt=off"
run_cmd "ppc64_cpu --smt"
run_cmd "ppc64_cpu --smt=on"
run_cmd "ppc64_cpu --smt"
run_cmd "ppc64_cpu --cores-present"
run_cmd "ppc64_cpu --cores-on"
run_cmd "ppc64_cpu --dscr"
run_cmd "ppc64_cpu --dscr=1"
run_cmd "ppc64_cpu --dscr"
run_cmd "ppc64_cpu --dscr=0"
run_cmd "ppc64_cpu --smt-snooze-delay"
run_cmd "ppc64_cpu --smt-snooze-delay=200"
run_cmd "ppc64_cpu --smt-snooze-delay"
run_cmd "ppc64_cpu --smt-snooze-delay=100"
run_cmd "ppc64_cpu --run-mode"
run_cmd "ppc64_cpu --subcores-per-core"

exit $FAIL_FLAG
