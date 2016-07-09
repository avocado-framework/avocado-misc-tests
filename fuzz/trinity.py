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
# Author: Praveen K Pandey <praveen@linux.vnet.ibm.com>
#

import os
import re

from avocado import Test
from avocado import main
from avocado.utils import archive, build, process
from avocado.utils.software_manager import SoftwareManager


class Trinity(Test):

    """
    This testsuite test  syscall by calling syscall
    with random system call and varying number of args
    """

    def setUp(self):
        '''
        Build Trinity
        Source:
        https://github.com/kernelslacker/trinity
        '''

        process.run('useradd  trinity', sudo=True)

        smm = SoftwareManager()

        for package in ("gcc", "make"):
            if not smm.check_installed(package) and not smm.install(package):
                self.error(
                    "Fail to install %s required for this test." % package)

        locations = ["https://github.com/kernelslacker/trinity/archive/"
                     "master.zip"]
        tarball = self.fetch_asset("trinity.zip", locations=locations)
        archive.extract(tarball, self.srcdir)
        self.srcdir = os.path.join(self.srcdir, 'trinity-master')

        os.chdir(self.srcdir)

        process.run('chmod -R  +x ' + self.srcdir)
        process.run('./configure', shell=True)
        build.make('.')

    def test(self):
        '''
        Trinity need to run as non root user
        '''
        args = self.params.get('runarg', default='-x madasive ')

        process.system('su - trinity -c " %s  %s  %s"' %
                       (os.path.join(self.srcdir, 'trinity'), args, '-N 100000'),
                       shell=True)

        dmesg = process.system_output('dmesg')

        # verify if system having issue after fuzzer run

        match = re.search(r'unhandled', dmesg, re.M | re.I)
        if match:
            self.log.info("Testcase failure as segfault")
        match = re.search(r'Call Trace:', dmesg, re.M | re.I)
        if match:
            self.log.info("some call traces seen please check")

    def tearDown(self):

        process.system('userdel trinity', sudo=True)

if __name__ == "__main__":
    main()
