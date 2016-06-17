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
Test that automatically takes shapshots from created logical volumes
using a given policy.

For details about the policy see README.
"""
import avocado
from avocado import Test
from avocado import main
from avocado.utils import process
from avocado.utils import lv_utils


class Lvsetup(Test):

    """
    Test class for creating logical volumes.
    """

    def setUp(self):
        """
        Check existence of input PV,VG, LV and snapshots prior to Test.
        """
        self.disk = self.params.get('disk', default=None)
        vg_name = self.params.get('vg_name', default='avocado_vg')
        self.loop = True
        if self.disk:
            vg_name = vg_name + '_' + self.disk.split('/')[-1]
            self.loop = False
        lv_name = self.params.get('lv_name', default='avocado_lv')
        self.lv_size = self.params.get('lv_size', default='1G')
        lv_snapshot_name = self.params.get(
            'lv_snapshot_name', default='avocado_sn')
        self.lv_snapshot_size = self.params.get(
            'lv_snapshot_size', default='1G')
        self.ramdisk_vg_size = self.params.get(
            'ramdisk_vg_size', default='10000')
        self.ramdisk_basedir = self.params.get(
            'ramdisk_basedir', default=self.workdir)
        self.ramdisk_sparse_filename = self.params.get(
            'ramdisk_sparse_filename', default='virtual_hdd')

        if lv_utils.vg_check(vg_name):
            self.skip('Volume group %s already exists' % vg_name)
        self.vg_name = vg_name
        if lv_utils.lv_check(vg_name, lv_name):
            self.skip('Logical Volume %s already exists' % lv_name)
        self.lv_name = lv_name
        if lv_utils.lv_check(vg_name, lv_snapshot_name):
            self.skip('Snapshot %s already exists' % lv_snapshot_name)
        self.lv_snapshot_name = lv_snapshot_name

    @avocado.fail_on(lv_utils.LVException)
    def test(self):
        """
        General logical volume setup.

        A volume group with given name is created in the ramdisk. It then
        creates a logical volume. Takes a snapshot from the logical and
        merges snapshot with the logical volume.
        """

        self.loop_device = lv_utils.vg_ramdisk(self.disk, self.vg_name,
                                               self.ramdisk_vg_size,
                                               self.ramdisk_basedir,
                                               self.ramdisk_sparse_filename)[3]
        lv_utils.lv_create(self.vg_name, self.lv_name, self.lv_size)
        lv_utils.lv_take_snapshot(self.vg_name, self.lv_name,
                                  self.lv_snapshot_name,
                                  self.lv_snapshot_size)
        lv_utils.lv_revert(self.vg_name, self.lv_name, self.lv_snapshot_name)

    def tearDown(self):
        """
        Clear all PV,VG, LV and snapshots created by the test.
        """
        # Remove created VG and unmount from base directory
        if self.vg_name:
            try:
                lv_utils.vg_remove(self.vg_name)
            except process.CmdError:
                self.error("CLEANUP: Cannot remove volume group %s" %
                           self.vg_name)
            try:
                process.run('umount -l %s/%s' %
                            (self.workdir, self.vg_name), sudo=True)
            except process.CmdError:
                self.error("CLEANUP: Cannot unmount %s/%s" %
                           (self.workdir, self.vg_name))

        # Remove the created loop device/PV
        if self.loop:
            try:
                process.run('losetup -d %s' % self.loop_device, sudo=True)
            except process.CmdError:
                self.error(
                    'CLEANUP: Cannot remove created loop device and PV %s'
                    % self.loop_device)
        else:
            try:
                process.run("pvremove %s" % self.loop_device,
                            ignore_status=True, sudo=True)
            except process.CmdError:
                self.error(
                    'CLEANUP: PV %s cannot be removed while cleanup'
                    % self.loop_device)

if __name__ == "__main__":
    main()
