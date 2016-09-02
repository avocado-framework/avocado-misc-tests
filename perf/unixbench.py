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
# Author: Santhosh G <santhog4@linux.vnet.ibm.com>
# Copyright: 2016 IBM
#
# Based on code mostly written by:
# Author : John Admanski <jadmanski@google.com>
# copyright : 2008 Google

import os
import re
from avocado import Test
from avocado import main
from avocado.utils import process
from avocado.utils import build
from avocado.utils import git
from avocado.utils.software_manager import SoftwareManager
from avocado.utils import distro
from avocado.core import data_dir


class unixbench(Test):
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
        git.get_repo('https://github.com/kdlucas/byte-unixbench.git',
                     destination_dir=self.srcdir)
        os.chdir(self.srcdir + '/UnixBench')
        makefile_patch = 'patch -p1 < %s' % (os.path.join(
            self.datadir, 'Makefile.patch'))
        process.run(makefile_patch, shell=True)
        os.chdir(self.srcdir + '/UnixBench')
        build.make(self.srcdir + '/UnixBench')

    def test(self):
        self.tmpdir = data_dir.get_tmp_dir()
        stepsecs = self.params.get('stepsecs', default='')
        args = self.params.get('args', default='')
        vars = ''
        if stepsecs:
            # change time per subtest from unixbench's defaults of
            #   10 secs for small tests, 30 secs for bigger tests
            vars = ' systime=%i looper=%i seconds=%i'\
                   ' dhrytime=%i arithtime=%i' \
                   % ((stepsecs,) * 5)
        os.chdir(self.srcdir + '/UnixBench')
        process.system(vars + ' ./Run ' + args, shell=True)
        report_path = os.path.join(self.logdir, 'stdout')
        self.report_data = open(report_path).readlines()

    def check_for_error(self, words):
        l = len(words)
        if l >= 3 and words[-3:l] == ['no', 'measured', 'results']:
            # found a problem so record it in err string
            key = '_'.join(words[1:-3])
            if self.err is None:
                self.err = key
            else:
                self.err = self.err + " " + key
            return True
        else:
            return False

    def tearDown(self):
        self.err = None
        keyval = {}
        parse_flag = False
        result_flag = False
        for line in self.report_data:
            if "BYTE UNIX Benchmarks" in line:
                result_flag = 1
            if "Dhrystone" in line and result_flag:
                parse_flag = True
            if parse_flag:
                if len(line.split()) == 0:
                    break
                words = line.split()
                # look for problems first
                if self.check_for_error(words):
                    continue

                # we should make sure that there are at least
                # 6 guys before we start accessing the array
                if len(words) >= 6:
                    key = '_'.join(words[0:-6])
                    key = re.sub('\W', '', key)
                    value = words[-6]
                    keyval[key] = value
            else:
                continue
        for line in self.report_data:
            if 'System Benchmarks Index Score' in line:
                keyval['score'] = line.split()[-1]
                break

        if self.err is not None:
            self.error('Error Has been Occured \n %s' % self.err)
        else:
            self.log.info('System Benchmarks Index Score is %s \n'
                          'Please check logs for full stats\n'
                          % keyval['score'])
