#!/usr/bin/env python
#
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
# Author:Praveen K Pandey <praveen@linux.vnet.ibm.com>
#

import os

from avocado import Test
from avocado import main
from avocado.utils import process, build, git
from avocado.utils.software_manager import SoftwareManager


class Perfmon(Test):

    """
    performance monitoring on Linux : test  perf_events on Linux
    """

    def setUp(self):

        # Check for basic utilities
        smm = SoftwareManager()
        smm = SoftwareManager()

        for package in ("gcc", "make"):
            if not smm.check_installed(package) and not smm.install(package):
                self.error(
                    "Fail to install %s required for this test." % package)

        git.get_repo('git://perfmon2.git.sourceforge.net/gitroot'
                     '/perfmon2/libpfm4', destination_dir=self.srcdir)

        os.chdir(self.srcdir)

        build.make('.')

    def test(self):

        out = process.system_output('%s ' % os.path.join(
            self.srcdir, 'tests/validate'))
        if 'fail' in out:
            self.error("test failed:check manually")


if __name__ == "__main__":
    main()
