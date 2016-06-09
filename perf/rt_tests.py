#!/usr/bin/env python

import os
from avocado import Test
from avocado import main
from avocado.utils import build
from avocado.utils import process
from avocado.utils import git
from avocado.utils.software_manager import SoftwareManager
from avocado.utils import distro


class rt_tests(Test):

    def setUp(self):
        # Check for root permission
        if os.geteuid() != 0:
            exit("You need to have root privileges to run this script."
                 "\nPlease try again, using 'sudo'. Exiting.")
        # Check for basic utilities
        sm = SoftwareManager()
        detected_distro = distro.detect()
        deps = ['gcc', 'git', 'make']
        for package in deps:
            if package == 'git' and detected_distro.name == "SuSE":
                package = 'git-core'
            if not sm.check_installed(package) and not sm.install(package):
                self.error(package + ' is needed for the test to be run')
        if detected_distro.name == "Ubuntu":
            if not sm.check_installed("build-essential") and not \
                     sm.install("build-essential"):
                self.error('build-essential is needed for the test to be run')
            if not sm.check_installed("libnuma-dev") and not \
                    sm.install("libnuma-dev"):
                self.error('libnuma-dev is needed for the test to be run')

        if detected_distro.name == "redhat":
            if not sm.check_installed("numactl-devel") and not \
                                      sm.install("numactl-devel"):
                self.error('numactl-devel is needed for the test to be run')
        data_dir = os.path.abspath(self.datadir)
        git.get_repo('git://git.kernel.org/pub/scm/utils/rt-tests/'
                     'rt-tests.git', destination_dir=self.srcdir)
        os.chdir(self.srcdir)
        build.make(self.srcdir)

    def test(self):
        test_to_run = self.params.get('test_to_run', default='signaltest')
        args = self.params.get('args', default='-t 10 -l 100000')
        process.system('./' + test_to_run + ' ' + args)

if __name__ == "__main__":
    main()
