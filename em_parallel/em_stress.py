#!/usr/bin/env python

import os
import subprocess
import re
from avocado import Test
from avocado import main



class em_stress(Test):
    def setUp(self):
        architecture = os.uname()[4]
        if "ppc" not in architecture:
            self.skip('supported only on Power platform')
        file = os.uname()[2]
        filename = "/boot/config-%s" %file
        for line in open(filename,'r'):
            if re.search('CONFIG_POWERNV_CPUFREQ',line):
                line1 = line.split('=')[1]
                if str(line1).strip() == 'm':
                    self.log.info("Dynamically loadable")
                else:
                    self.skip('Module not loadable,Skipping this test')
 

    def test(self):
        error_count = 0
        cpu_hotplug = os.path.join(self.datadir, 'cpu_hotplug.py')
        load = os.path.join(self.datadir, 'load.py')
        list1 = [cpu_hotplug, load] 
        processes = {}
        try:
            for cmd in list1:
                cmd1 = "python %s" % cmd
                p = subprocess.Popen(cmd1, shell = True)
                processes[cmd] = p
            for key,value in processes.items():
                P,rc = value.communicate()[0],value.returncode
                if rc!= 0:
                    error_count += 1
                    self.log.info("The test %s failed with return code %d" % (key,rc))
        except Exception as e:
            self.error("Unexpected error :" + e.message)

        if error_count!= 0:
            self.fail('The test failed with errors')

if __name__ == "__main__":
    main()
