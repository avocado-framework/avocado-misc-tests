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
#
# Copyright: 2016 IBM
# Author: Venkat Rao B <vrbagal1@linux.vnet.ibm.com>

# Blkdiscard  is  used  to  discard  device  sectors.This is useful for
# solid-state drivers (SSDs) and thinly-provisioned storage.

from avocado import Test
from avocado.utils.software_manager import SoftwareManager
from avocado.utils import process
from avocado import main


class Blkdiscard(Test):

    """
    blkdiscard is used to discard device sectors.This is useful for
    solid-state drivers (SSDs) and thinly-provisioned storage.
    """

    def setUp(self):

        """
        Checks if the blkdiscard packages are installed or not.
        """
        smm = SoftwareManager()
        if not smm.check_installed("util-linux"):
            self.skip("blkdiscard is needed for the test to be run")
        self.disk = self.params.get('self.disk', default='/dev/nvme0n1')
        cmd = "blkdiscard -V"
        process.run(cmd)

    def test(self):

        """
        Sectors are dicarded for the different values of OFFSET and LENGTH.
        """
        cmd = "fdisk -l | grep %s | awk '{print $5}' | sed 1q;" % self.disk
        size = process.system_output(cmd, shell=True)
        cmd = "blkdiscard %s -o 0 -v -l %s" % (self.disk, size)
        process.run(cmd, shell=True)
        cmd = "blkdiscard %s -o %s -v -l %s" % (self.disk, size, size)
        cmd = "blkdiscard %s -o 0 -v -l %s" % (self.disk, size)
        cmd = "blkdiscard %s -o %s -v -l 0" % (self.disk, size)
        process.run(cmd)
        for i in xrange(2, 10, 2):
            for j in xrange(2, 10, 2):
                if (int(size) / i) % 4096 == 0 and (int(size) / j) % 4096 == 0:
                    cmd = "blkdiscard %s -o %d -l %d -v" \
                        % (self.disk, int(size) / i, int(size) / j)
                    process.system(cmd, shell=True)
                else:
                    cmd = "blkdiscard %s -o %d -l %d -v" \
                        % (self.disk, int(size) / i, int(size) / j)
                    if process.system(cmd, ignore_status=True,
                                      shell=True) == 0:
                        self.fail("Blkdiscard passed for the values which is, \
                            not aligned to 4096 but actually it should fail")

if __name__ == "__main__":
    main()
