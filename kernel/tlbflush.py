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
import shutil
import json

from avocado import Test
from avocado import main
from avocado.utils import process
from avocado.utils.software_manager import SoftwareManager


class Tlbflush(Test):

    """
    This is a macrobenchmark for TLB flush range testing.
    """

    def setUp(self):

        self.tlbflush_max_entries = self.params.get('entries', default=200)
        self.tlbflush_iteration = self.params.get('iterations', default=50)
        self.nr_threads = self.params.get('nr_threads', default=50)

        # Check for basic utilities

        smm = SoftwareManager()

        if not smm.check_installed("gcc") and not smm.install("gcc"):
            self.error(
                "Fail to install %s required for this test." % package)

        data_dir = os.path.abspath(self.datadir)

        shutil.copyfile(os.path.join(data_dir, 'tlbflush.c'),
                        os.path.join(self.srcdir, 'tlbflush.c'))

        os.chdir(self.srcdir)
        os.system('cp tlbflush.c /root/pp/tlbflush.c')
        tlbflush_patch = 'patch -p1 < %s' % (
            os.path.join(data_dir, 'tlbflush.patch'))

        process.run(tlbflush_patch, shell=True)
        cmd = 'gcc -DFILE_SIZE=$((128*1048576)) -g -O2 tlbflush.c \
               -lpthread -o tlbflush'
        process.run(cmd, shell=True)

    def set_value(self):

        self.perf_json = [{}]
        self.nr_entries = 100

        for ite in range(1, self.tlbflush_iteration):
            # Select a range of entries to randomly select from.
            # This is to ensure an evenish spread of entries to
            # be tested

            nr_section = ite % 8
            ranges = self.tlbflush_max_entries / 8
            min_entries = ranges * nr_section + 1
            max_entries = min_entries + ranges
            if self.nr_entries > max_entries:
                self.nr_entries = max_entries

            out = self.run()
            self.perf_json.append({'Test time' + str(ite): out})

        output_path = os.path.join(self.outputdir, "perf.json")
        json.dump(self.perf_json, open(output_path, "w"))

    def run(self):
        out = process.system_output('%s ' % os.path.join(
            self.srcdir, 'tlbflush'), '-n ' + str(self.nr_entries) +
            ' -t' + str(self.nr_threads))

        return out

    def test(self):

        # call test function
        self.set_value()


if __name__ == "__main__":
    main()
