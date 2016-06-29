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
# Author: Praveen K Pandey <praveen@linux.vnet.ibm.com>
#
# Based on code by Martin Bligh <mbligh@google.com>
#   copyright: 2006 Google
#   https://github.com/autotest/autotest-client-tests/tree/master/fsfuzzer

import os

from avocado import Test
from avocado import main
from avocado.utils import archive
from avocado.utils import process
from avocado.utils import build
from avocado.utils.software_manager import SoftwareManager


class Fsfuzzer(Test):

    """
    fsfuzzer is a file system fuzzer tool. This test simply runs fsfuzzer
    Fuzzing is slang for fault injection via random inputs. The goal is to
    find bugs in software without reading code or designing detailed test
    cases.
       fsfuzz will inject random errors into the files systems
       mounted. Evidently it has found many errors in many systems.
    """

    def setUp(self):
        '''
        Build fsfuzzer
        Source:
        http://people.redhat.com/sgrubb/files/fsfuzzer-0.7.tar.gz
        '''
        sm = SoftwareManager()
        if not sm.check_installed("gcc") and not sm.install("gcc"):
            self.error("Gcc is needed for the test to be run")
        tarball = self.fetch_asset('http://people.redhat.com'
                                   '/sgrubb/files/fsfuzzer-0.7.tar.gz')
        data_dir = os.path.abspath(self.datadir)
        archive.extract(tarball, self.srcdir)
        version = os.path.basename(tarball.split('.tar.')[0])
        self.srcdir = os.path.join(self.srcdir, version)

        # Patch for fsfuzzer
        patch = self.params.get(
            'patch', default='fstestfix.patch')
        patch_1 = self.params.get(
            'patch', default='ppc64leconfig_guess.patch')
        patch_2 = self.params.get(
            'patch', default='attrfix.patch')
        patch_3 = self.params.get(
            'patch', default='fsfuzz_fix.patch')
        os.chdir(self.srcdir)
        p1 = 'patch -p1 < %s/%s' % (data_dir, patch)
        p2 = 'patch -p1 < %s/%s' % (data_dir, patch_1)
        p3 = 'patch -p1 < %s/%s' % (data_dir, patch_2)
        p4 = 'patch -p1 < %s/%s' % (data_dir, patch_3)

        process.run(p1, shell=True)
        process.run(p2, shell=True)
        process.run(p3, shell=True)
        process.run(p4, shell=True)
        process.run('[ -x configure ] && ./configure', shell=True)

        build.make(self.srcdir)

    def test(self):

        args = self.params.get('fstype', default='')

        process.system(self.srcdir + '/fsfuzz ' + args, sudo=True)

if __name__ == "__main__":
    main()
