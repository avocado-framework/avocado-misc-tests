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
# Author: Pooja B Surya <pooja@linux.vnet.ibm.com>

import os
import re

from avocado import Test
from avocado import main
from avocado.utils import process
from avocado.utils import git
from avocado.utils.software_manager import SoftwareManager
from avocado.utils import distro


class Oprofile(Test):

    def setUp(self):
        # Check for basic utilities
        sm = SoftwareManager()
        detected_distro = distro.detect()
        deps = ['git', 'oprofile', 'dejagnu', 'expect']
        if detected_distro.name == "Suse":
            deps.append("git-core")
        else:
            deps.append("git")
        if detected_distro.name == "Ubuntu":
            deps.append("libxml2-utils")
            deps.append("tclsh")
        for package in deps:
            if not sm.check_installed(package) and not sm.install(package):
                self.error(package + ' is needed for the test to be run')
        if detected_distro.name == "SuSE":
            if not (os.path.exists("/usr/bin/oprofiled") and
                    ("/usr/bin/runtest")):
                self.skip("Need oprofile and dejagnu packages to run test")
        git.get_repo('git://oprofile.git.sourceforge.net/gitroot/oprofile/'
                     'oprofile-tests', destination_dir=self.srcdir)
        os.chdir(self.srcdir)
        os.chdir("testsuite/")

    def test(self):
        result = process.system('runtest --tool oprofile', ignore_status=True,
                                sudo=True)
        pattern = re.compile("FAIL")
        for i, line in enumerate(open('oprofile.sum')):
            for match in re.finditer(pattern, line):
                self.fail("Oprofile tests failed")

if __name__ == "__main__":
    main()
