#!/usr/bin/env python

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

import os
import commands
from avocado import Test
from avocado import main
from avocado.utils import process
from avocado.utils.software_manager import SoftwareManager


class RASTools(Test):

    '''
    This script executes the scripts listed in mux.yaml which inturn validates RAS tools.
    Command to run:
    avocado run ras.py --multiplex ras.py.data/mux.yaml
    '''

    def setUp(self):
        if os.geteuid() != 0:
            exit("You need to have root privileges to run this script."
                 "\nPlease try again, using 'sudo'. Exiting.")
        architecture = commands.getoutput("arch")
        if "ppc" not in architecture:
            self.skip("supported only on Power platform")
        sm = SoftwareManager()
        for package in ("ppc64-diag", "powerpc-utils", "lsvpd"):
            if not sm.check_installed(package) and not sm.install(package):
                self.error("Fail to install %s required for this test." % package)

    def test(self):
        script_to_run = self.params.get("script", default=None)
        tool_to_run = self.params.get("tool", default=None)
        log_dir = os.path.join(self.datadir, 'log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        command_to_run = (self.datadir + '/' + script_to_run + ' ' +
                          '>>' + ' ' + self.datadir + '/log/output.txt' + ' ' + '2>&1')
        cmd_result = process.run(command_to_run, ignore_status=True)
        self.log.info(cmd_result)
        if cmd_result.exit_status == 0:
            self.log.info("RAS check %s is successful" % tool_to_run)
        else:
            self.fail("RAS check %s failed" % tool_to_run)

if __name__ == "__main__":
    main()
