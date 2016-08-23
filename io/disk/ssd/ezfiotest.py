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
# Author: Narasimhan V <sim@linux.vnet.ibm.com>


"""
This test script is intended to give a block-level based overview of
SSD performance.
"""

import os
from avocado import Test
from avocado import main
from avocado.utils import build
from avocado.utils import process
import avocado.utils.git as git


class EzfioTest(Test):

    """
    This test script is intended to give a block-level based overview of
    SSD performance. Uses FIO to perform the actual IO tests.
    Places the output files in avocado test's outputdir.

    :param device: Name of the ssd block device
    """

    def setUp(self):
        """
        Build 'fio and ezfio'.
        """
        fio_path = os.path.join(self.srcdir, 'fio')
        fio_link = 'https://github.com/axboe/fio.git'
        git.get_repo(fio_link, destination_dir=fio_path)
        build.make(fio_path, make='./configure')
        build.make(fio_path)
        build.make(fio_path, extra_args='install')
        self.ezfio_path = os.path.join(self.srcdir, 'ezfio')
        ezfio_link = 'https://github.com/earlephilhower/ezfio.git'
        git.get_repo(ezfio_link, destination_dir=self.ezfio_path)
        self.device = self.params.get('device', default='/dev/nvme0n1')
        self.utilization = self.params.get('utilization', default='100')
        self.cwd = os.getcwd()

    def test(self):
        """
        Performs ezfio test on the block device'.
        """
        os.chdir(self.ezfio_path)
        cmd = './ezfio.py -d %s -o %s -u %s --yes' \
            % (self.device, self.outputdir, self.utilization)
        process.run(cmd, shell=True)

    def tearDown(self):
        """
        Clean up
        """
        os.chdir(self.cwd)


if __name__ == "__main__":
    main()
