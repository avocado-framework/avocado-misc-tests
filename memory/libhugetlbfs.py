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
# Author: Santhosh G <santhog4@linux.vnet.ibm.com>
#
# Based on code by:
# Author: Yao Fei Zhu <walkinair@cn.ibm.com>
# copyright : 2006 IBM
# https://github.com/autotest/autotest-client-tests/tree/master/libhugetlbfs

import os
import glob
from avocado import Test
from avocado import main
from avocado.utils import process
from avocado.utils import build
from avocado.utils import kernel
from avocado.utils import memory
from avocado.utils import git
from avocado.utils.software_manager import SoftwareManager
from avocado.utils import distro


class libhugetlbfs(Test):
    def setUp(self):
        # Check for root permission
        if os.geteuid() != 0:
            exit("You need to have root privileges to run this script."
                 "\nPlease try again, using 'sudo'. Exiting.")
        # Check for basic utilities
        sm = SoftwareManager()
        detected_distro = distro.detect()
        if not sm.check_installed("gcc") and not sm.install("gcc"):
            self.error('Gcc is needed for the test to be run')
        if not sm.check_installed("make") and not sm.install("make"):
            self.error('make is needed for the test to be run')
        if detected_distro.name == "SuSE":
            if not sm.check_installed("git-core") and not sm.install("git-"
                                                                     "core"):
                self.error('git is needed for the test to be run')
        else:
            if not sm.check_installed("git") and not sm.install("git"):
                self.error('git is needed for the test to be run')

        kernel.check_version("2.6.16")
        if detected_distro.name == "Ubuntu":
            op = glob.glob("/usr/lib/*/libpthread.a")
        else:
            op = glob.glob("/usr/lib*/libpthread.a")

        if not op:
            self.error("libpthread.a is required!!!"
                       "\nTry installing glibc-static")

        # Get arguments:
        self.hugetlbfs_dir = self.params.get('hugetlbfs_dir', default=None)
        pages_requested = self.params.get('pages_requested',
                                          default=20)

        # Check hugepages:
        pages_available = 0
        if os.path.exists('/proc/sys/vm/nr_hugepages'):
            Hugepages_support = process.system_output('cat /proc/meminfo',
                                                      verbose=False,
                                                      shell=True)
            if 'HugePages_' not in Hugepages_support:
                self.error("No Hugepages Configured")
            memory.set_num_huge_pages(pages_requested)
            pages_available = memory.get_num_huge_pages()
        else:
            self.error("Kernel does not support hugepages")

        # Check no of hugepages :
        if pages_available < pages_requested:
            self.error('%d pages available, < %d pages requested'
                       % pages_available, pages_requested)

        # Check if hugetlbfs is mounted
        cmd_result = process.run('grep hugetlbfs /proc/mounts', verbose=False)
        if not cmd_result:
            if not self.hugetlbfs_dir:
                self.hugetlbfs_dir = os.path.join(self.tmpdir, 'hugetlbfs')
                os.makedirs(self.hugetlbfs_dir)
            process.system('mount -t hugetlbfs none %s' % self.hugetlbfs_dir)

        data_dir = os.path.abspath(self.datadir)
        git.get_repo('https://github.com/libhugetlbfs/libhugetlbfs.git',
                     destination_dir=self.srcdir)
        os.chdir(self.srcdir)
        patch = self.params.get('patch', default='elflink.patch')
        process.run('patch -p1 < %s' % data_dir + '/' + patch, shell=True)
        build.make(self.srcdir, extra_args='BUILDTYPE=NATIVEONLY')

    def test(self):
        os.chdir(self.srcdir)
        build.make(self.srcdir, extra_args='BUILDTYPE=NATIVEONLY check')

    def tearDown(self):
        if self.hugetlbfs_dir:
            process.system('umount %s' % self.hugetlbfs_dir)

if __name__ == "__main__":
    main()
