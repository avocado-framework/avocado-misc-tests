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
# Author: Nosheen Pathan <nopathan@linux.vnet.ibm.com>

# Based on code by
#   Author: Lucas Meneghel Rodrigues <lmr@redhat.com>
#   Author: Yiqiao Pu <ypu@redhat.com>
#   Author: Jiří Župka <jzupka@redhat.com>
#   Author: Martin J. Bligh <mbligh@google.com>
#   Author: John Admanski <jadmanski@google.com>
#   Author: Mihai Rusu <dizzy@google.com>
#   Author: Scott Zawalski <scottz@google.com>
#   Copyright: 2009-2015  Red Hat, Inc
#   Copyright: 2013  Red Hat, Inc
#   Copyright: 2012  Red Hat, Inc
#   Copyright: 2007-2010  Google, Inc
#   Copyright: 2010  Google, Inc
#   Copyright: 2009 Google, Inc
#   Copyright: 2008 Google, Inc

import os
import shutil

from avocado import Test
from avocado import main
from avocado.utils import memory
from avocado.utils import disk
from avocado.utils import process
from avocado.utils import build
from avocado.utils.software_manager import SoftwareManager


class Disktest(Test):

    """
    Avocado module for disktest.
    Pattern test of the disk, using unique signatures for each block and each
    iteration of the test. Designed to check for data corruption issues in the
    disk and disk controller.
    It writes 50MB/s of 500KB size ops.
    """
    version = 2

    def setUp(self):
        """
        Verifies if we have gcc to compile disktest.
        :param disks: Directory (usually mountpoints) to be passed to the test.
                      Directory gets created if not existing
        :param gigabytes: Disk space that will be used for the test to run.
        :param chunk_mb: Size of the portion of the disk used to run the test.
                        Cannot be larger than the total amount of free RAM.
        :param source: name of the source file located in deps path
        :param make: name of the makefile file located in deps path
        """
        softm = SoftwareManager()
        if not softm.check_installed("gcc") and not softm.install("gcc"):
            self.error('Gcc is needed for the test to be run')

        self.disks = self.params.get('disks', default=self.workdir)
        self.gigabytes = self.params.get('gigabytes', default=None)
        self.chunk_mb = self.params.get('chunk_mb', default=None)
        source = self.params.get('source', default='disktest.c')
        makefile = self.params.get('make', default='Makefile')
        c_file = os.path.join(self.datadir, source)
        c_file_name = os.path.basename(c_file)
        make_file = os.path.join(self.datadir, makefile)
        make_file_name = os.path.basename(make_file)
        dest_c_file = os.path.join(self.srcdir, c_file_name)
        dest_m_file = os.path.join(self.srcdir, make_file_name)
        shutil.copy(c_file, dest_c_file)
        shutil.copy(make_file, dest_m_file)
        self.memory_mb = memory.memtotal() / 1024 / 8
        os.chdir(self.srcdir)
        build.make(self.srcdir)

    def one_disk_chunk(self, disks, chunk):
        """
        Tests one part of the disk by spawning a disktest instance.
        :param disks: Directory (usually a mountpoint).
        :param chunk: Portion of the disk used.
        """
        self.log.info("Testing %d MB files on %s in %d MB memory, chunk %s",
                      self.chunk_mb, disks, self.memory_mb, chunk)
        logfile = os.path.join(self.outputdir, "log.txt")
        cmd = ("%s/disktest -m %d -f %s/testfile.%d -i -S >>%s 2>&1" %
               (self.srcdir, self.chunk_mb, disks, chunk, logfile))
        self.log.debug("Running '%s'", cmd)

        proc = process.get_sub_process_klass(cmd)(cmd, shell=True)
        proc.start()
        proc.poll()
        proc.wait()
        return proc

    def test(self):
        """
        Runs one iteration of disktest.

        """
        os.chdir(self.srcdir)
        if self.chunk_mb is None:
            self.chunk_mb = memory.memtotal() / 1024 / 8
        if self.gigabytes is None:
            free = 100  # cap it at 100GB by default
            if not os.path.isdir(self.disks):
                os.makedirs(self.disks)

            free = min(disk.freespace(self.disks) / 1024 ** 3, free)
            self.gigabytes = free
            self.log.info("Resizing to %s GB", self.gigabytes)

        if self.memory_mb > self.chunk_mb:
            self.error("Too much RAM (%dMB) for this test to work" %
                       self.memory_mb)

        if self.chunk_mb == 0:
            self.chunk_mb = 1
        chunks = (1024 * self.gigabytes) / self.chunk_mb
        self.log.info("Total of disk chunks that will be used: %s", chunks)
        errors = []
        for i in xrange(chunks):
            proc = self.one_disk_chunk(self.disks, i)
            retval = proc.wait()
            if retval != 0:
                errors.append(retval)
        if errors:
            self.fail("Errors from children: %s" % errors)

    def tearDown(self):
        """
        To clean all the testfiles generated
        """
        process.run('rm -rf %s/testfile.*' % self.disks, shell=True)


if __name__ == "__main__":
    main()
