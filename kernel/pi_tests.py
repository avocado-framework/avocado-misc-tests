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
# Based on code by Michal Piotrowski <michal.k.k.piotrowski@gmail.com>
#
#  https://github.com/autotest/autotest-client-tests/tree/master/pi_tests

#

import os

from avocado import Test
from avocado import main
from avocado.utils import process
from avocado.utils import build
from avocado.utils.software_manager import SoftwareManager


class Pi_tests(Test):

    """
    The basic premise here is to set up a deadlock scenario and confirm that PI
    mutexes resolve the situation. Three worker threads will be created from the
    main thread: low, medium and high priority threads that use SCHED_FIFO as
    their scheduling policy. The low priority thread claims a mutex and then
    starts "working". The medium priority thread starts and preempts the low
    priority thread. Then the high priority thread runs and attempts to claim
    the mutex owned by the low priority thread. Without priority inheritance,
    this will deadlock the program. With priority inheritance, the low priority
    thread receives a priority boost, finishes it's "work" and releases the mutex,
    which allows the high priority thread to run and finish and then the medium
    priority thread finishes.
    """

    def setUp(self):

        sm = SoftwareManager()
        if not sm.check_installed("gcc") and not sm.install("gcc"):
            self.error("Gcc is needed for the test to be run")

        process.run('tar -xf ' + self.datadir +
                    '/pi_tests.tar.bz2 -C ' + self.srcdir + '/', shell=True)
        self.srcdir = self.srcdir + '/src/'

        build.make(self.srcdir)

    def test(self):

        os.chdir(self.srcdir)
        args = self.params.get('options', default='1 300')
        process.system('./start.sh ' + args)


if __name__ == "__main__":
    main()
