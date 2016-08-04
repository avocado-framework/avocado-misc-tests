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
# Author:Abdul Haleem <abdhalee@in.ibm.com>
#        Praveen K Pandey <praveen@linux.vnet.ibm.com>
#

import os
import time

from avocado import Test
from avocado import main
from avocado.utils import process


class Rcutorture(Test):

    """
    CONFIG_RCU_TORTURE_TEST enables an intense torture test of the RCU
    infratructure. It creates an rcutorture kernel module that can be
    loaded to run a torture test.
    """

    def setUp(self):
        """
        Verifies if CONFIG_RCU_TORTURE_TEST is enabled
        """
        self.results = []
        self.log.info("Check if CONFIG_RCU_TORTURE_TEST is enabled\n")
        ret = os.system(
            'cat /boot/config* | grep CONFIG_RCU_TORTURE_TEST=m')
        if ret != 0:
            self.log.info("CONFIG_RCU_TORTURE_TEST is not set in .config !!\n")
            sys.exit(0)
        self.log.info("Check rcutorture module is loaded\n")
        cmd = os.system('lsmod | grep rcutorture')
        if cmd == 0:
            self.log.info("module already loaded\n")
            process.system('rmmod rcutorture')

    def cpus_toggle(self):
        """
        Toggle CPUS online and offline
        """
        cmd = "lscpu | grep 'CPU(s):' |head -1| awk '{ print $2 }'"
        totalcpus = os.system(cmd)
        full_count = int(totalcpus) - 1
        half_count = int(totalcpus) / 2 - 1
        shalf_count = int(totalcpus) / 2
        fcpu = "0 - "  "%s" % half_count
        scpu = "%s - %s" % (shalf_count, full_count)

        self.log.info("Online all cpus %s", totalcpus)
        for cpu in range(0, full_count):
            online = 'echo 1 > /sys/devices/system/cpu/cpu%s/online' % cpu
            process.system(online)
        time.sleep(10)

        self.log.info("Offline all cpus 0 - %s\n", full_count)
        for cpu in range(0, full_count):
            offline = 'echo 0 > /sys/devices/system/cpu/cpu%s/online' % cpu
            process.system(offline)
        time.sleep(10)

        self.log.info("Online all cpus 0 - %s\n", full_count)
        for cpu in range(0, full_count):
            online = 'echo 1 > /sys/devices/system/cpu/cpu%s/online' % cpu
            process.system(online)

        self.log.info(
            "Offline and online first half cpus %s\n", fcpu)
        for cpu in range(0, half_count):
            offline = 'echo 0 > /sys/devices/system/cpu/cpu%s/online' % cpu
            processs.system(offline)
            time.sleep(10)
            online = 'echo 1 > /sys/devices/system/cpu/cpu%s/online' % cpu
            process.system(online)

        self.log.info("Offline and online second half cpus %s\n", scpu)
        for cpu in range(shalf_count, full_count):
            offline = 'echo 0 > /sys/devices/system/cpu/cpu%s/online' % cpu
            process.system(offline)
            time.sleep(10)
            online = 'echo 1 > /sys/devices/system/cpu/cpu%s/online' % cpu
            process.system(online)

    def test(self):
        """
        Runs rcutorture test for specified time.
        """
        seconds = 15
        os.chdir(self.logdir)
        process.system('modprobe rcutorture')
        self.cpus_toggle()
        time.sleep(seconds)
        self.cpus_toggle()
        process.system('rmmod rcutorture')
        cmd = 'dmesg | grep "rcu-torture: Reader"'
        res = os.system(cmd)
        self.results = str(res).splitlines()

        """
        Runs log ananlysis on the dmesg logs
        Checks for know bugs
        """
        pipe1 = [r for r in self.results if "!!! Reader Pipe:" in r]
        if len(pipe1) != 0:
            self.error('\nBUG: grace-period failure !')
            sys.exit(0)

        pipe2 = [r for r in self.results if "Reader Pipe" in r]
        for p in pipe2:
            nmiss = p.split(" ")[7]
            if int(nmiss):
                self.error('\nBUG: rcutorture tests failed !')

        batch = [s for s in self.results if "Reader Batch" in s]
        for b in batch:
            nmiss = b.split(" ")[7]
            if int(nmiss):
                self.log.info("\nWarning: near mis failure !!")

if __name__ == "__main__":
    main()
