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
# Copyright: 2016 IBM.
# Author: Rajashree Rajendran<rajashr7@linux.vnet.ibm.com>

# Based on code by
#   Author: Lucas Meneghel Rodrigues <lmr@redhat.com>
#   Author: Xu Tian <xutian@redhat.com>
#   Author: Jeff Moyer <jmoyer@redhat.com>
#   Author: Dmitry Monakhov <dmonakhov@openvz.org>
#   Copyright: 2008 - 2015 Red Hat, Inc.
#   Copyright: 2013 Red Hat, Inc.
#   Copyright: 2010 Red Hat, Inc.
#   Copyright: 2012 <dmonakhov@openvz.org>
#   https://github.com/autotest/autotest-client-tests/tree/master/tiobench

import os

from avocado import Test
from avocado import main
from avocado.utils import process
from avocado.utils import build
from avocado.utils import git
from avocado.utils import genio
from avocado.utils.software_manager import SoftwareManager


class Tiobench(Test):

    """
    Avocado module for tiobench.
    tiobench is a multi-threaded I/O benchmark.
    It is used to measure file system performance in
    four basic operations: sequential read, random read,
    sequential write, and random write.

    """

    def setUp(self):
        """
        Build tiobench.
        Source:
        https://github.com/mkuoppal/tiobench.git

        """
        s_mngr = SoftwareManager()
        if not s_mngr.check_installed("gcc") and not s_mngr.install("gcc"):
            self.error('Gcc is needed for the test to be run')
        git.get_repo('https://github.com/mkuoppal/tiobench.git',
                     destination_dir=self.srcdir)
        os.chdir(self.srcdir)
        build.make(self.srcdir)

    def test(self):
        """
        Runs two iterations of test.
        :params target: The directory in which to test.
                        Defaults to ., the current directory.
        :params blocks: The blocksize in Bytes to use. Defaults to 4096.
        :params threads: The number of concurrent test threads.
        :params size: The total size in MBytes of the files may use together.
        :params num_runs: This number specifies over how many runs
                          each test should be averaged.
        :params iterations: Number of iterations the test needs to be run.
        """
        target = self.params.get('target', default='/var/tmp')
        blocks = self.params.get('blocks', default=4096)
        threads = self.params.get('threads', default=10)
        size = self.params.get('size', default=1024)
        num_runs = self.params.get('numruns', default=2)
        self.whiteboard = process.system_output('./tiobench.pl --target {}'
                                                '--block={} --threads={}'
                                                '--size={} --numruns={}'
                                                .format(target, blocks,
                                                        threads, size,
                                                        num_runs))
        self.log.info(self.whiteboard)
        whiteboard_file = os.path.join(self.logdir, 'whiteboard')
        genio.write_file(whiteboard_file, self.whiteboard)

if __name__ == "__main__":
    main()
