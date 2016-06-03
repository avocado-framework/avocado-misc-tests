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
# Author: Harish <harisrir@linux.vnet.ibm.com>
#
# Based on the code by:
#
# Copyright: 2012 Intra2net
# Author: Plamen Dimitrov (plamen.dimitrov@intra2net.com)

"""
Test that automatically takes shapshots from existing logical volumes
or creates them using a given policy.

For details about the policy see below.
"""

from avocado import Test
from avocado import main
from avocado.utils import lv_utils


class Lvsetup(Test):

    """
    Test class for creating logical volumes.
    """

    def test(self):
        """
        General logical volume setup.

        The main part of the lvm setup checks whether the provided volume group
        exists and if not, creates one from the ramdisk. It then creates a
        logical volume if there is no logical volume, takes a snapshot from the
        logical if there is logical volume but no snapshot, and merges with the
        snapshot if both the snapshot and the logical volume are present.
        """
        # if no virtual group is defined create one based on ramdisk
        disk = self.params.get('disk', default=None)
        vg_name = self.params.get('vg_name', default='avocado_vg')
        if disk:
            vg_name = vg_name + '_' + disk.split('/')[-1]
        lv_name = self.params.get('lv_name', default='avocado_lv')
        lv_size = self.params.get('lv_size', default='1G')
        lv_snapshot_name = self.params.get(
            'lv_snapshot_name', default='avocado_sn')
        lv_snapshot_size = self.params.get('lv_snapshot_size', default='1G')
        ramdisk_vg_size = self.params.get('ramdisk_vg_size', default='10000')
        ramdisk_basedir = self.params.get('ramdisk_basedir', default='/tmp')
        ramdisk_sparse_filename = self.params.get(
            'ramdisk_sparse_filename', default='virtual_hdd')
        override_flag = self.params.get('override_flag', default=0)

        if not lv_utils.vg_check(vg_name):
            lv_utils.vg_ramdisk(disk, vg_name, ramdisk_vg_size,
                                ramdisk_basedir,
                                ramdisk_sparse_filename)
        # if no snapshot is defined start fresh logical volume
        if override_flag == 1 and lv_utils.lv_check(vg_name, lv_name):
            lv_utils.lv_remove(vg_name, lv_name)
            lv_utils.lv_create(vg_name, lv_name, lv_size)
        elif override_flag == -1 and lv_utils.lv_check(vg_name, lv_name):
            lv_utils.lv_remove(vg_name, lv_name)
        else:
            # perform normal check policy
            if (lv_utils.lv_check(vg_name, lv_snapshot_name) and
                    lv_utils.lv_check(vg_name, lv_name)):
                lv_utils.lv_revert(vg_name, lv_name, lv_snapshot_name)
                lv_utils.lv_take_snapshot(vg_name, lv_name,
                                          lv_snapshot_name,
                                          lv_snapshot_size)

            elif (lv_utils.lv_check(vg_name, lv_snapshot_name) and
                  not lv_utils.lv_check(vg_name, lv_name)):
                raise Exception("Snapshot origin not found")

            elif (not lv_utils.lv_check(vg_name, lv_snapshot_name) and
                  lv_utils.lv_check(vg_name, lv_name)):
                lv_utils.lv_take_snapshot(vg_name, lv_name,
                                          lv_snapshot_name,
                                          lv_snapshot_size)

            else:
                lv_utils.lv_create(vg_name, lv_name, lv_size)

if __name__ == "__main__":
    main()
