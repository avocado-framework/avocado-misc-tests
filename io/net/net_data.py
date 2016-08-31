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
# Author: Prudhvi Miryala<mprudhvi@linux.vnet.ibm.com>
#

# check the statistics of interface, test big ping
# test lro and gro

import time
import netifaces
from avocado import Test
from avocado.utils.software_manager import SoftwareManager
from avocado.utils import process


class NetDataTest(Test):
    '''
    check the statistics of interface, test big ping
    test lro and gro
    '''
    def setUp(self):
        '''
            To check and install dependencies for the test
        '''
        sm = SoftwareManager()
        network_tools = ("iputils", "ethtool", "net-tools", "openssh-clients")
        for pkg in network_tools:
            if not sm.check_installed(pkg) and not sm.install(pkg):
                self.skip("%s package is need to test" % pkg)
        interfaces = netifaces.interfaces()
        interface = self.params.get("iface")
        if interface not in interfaces:
            self.skip("%s interface is not available" % interface)

    def teststatistics(self):
        '''
         check statistics of interface
        '''
        self.log.info("Statistic incrementer")
        interface = self.params.get("iface")
        peer = self.params.get("peerip")
        rx_cmd = "cat /sys/class/net/%s/statistics/rx_packets" % interface
        tx_cmd = "cat /sys/class/net/%s/statistics/tx_packets" % interface
        rx_stat = int(process.system_output(rx_cmd, shell=True))
        tx_stat = int(process.system_output(tx_cmd, shell=True))
        # flooding ICMP packets to peer system through interface
        tmp = "ping -c 20 -f %s -I %s > /dev/null" % (peer, interface)
        process.system(tmp, shell=True)
        time.sleep(3)
        rx_stat_after = int(process.system_output(rx_cmd, shell=True))
        tx_stat_after = int(process.system_output(tx_cmd, shell=True))
        # check interface working or not
        if (rx_stat >= rx_stat_after) and (tx_stat >= tx_stat_after):
            self.fail("stats not incremented.WRONG with IF %s" % interface)

    def testbigping(self):
        '''
        check with different maximum transfer unit values
        '''
        mtu_list = self.params.get("size_val", default=1500)
        mtu_list = mtu_list.split()
        interface = self.params.get("iface")
        peer = self.params.get("peerip")
        cmd = "\`ifconfig | grep -w -B 1 %s | head -1 | cut -f1 -d' '\`" % peer
        for mtu in mtu_list:
            self.log.info("trying with mtu %s" % (mtu))
            '''
             ping the peer machine with different maximum transfers unit sizes
             and finally set maximum transfer unit size to 1500 Bytes
            '''
            msg = "ssh %s \"ifconfig %s mtu %s\"" % (peer, cmd, mtu)
            process.system(msg, shell=True)
            process.system("ifconfig %s mtu %s" % (interface, mtu), shell=True)
            time.sleep(10)
            mtu = int(mtu) - 28
            cmd_ping = "ping -i 0.1 -c 2 -s %s %s" % (mtu, peer)
            ret = process.system(cmd_ping, shell=True)
            if ret != 0:
                self.fail("bigping test failed")

    def testgro(self):
        '''
        check gro is enabled or not
        '''
        self.log.info("Generic Receive Offload")
        interface = self.params.get("iface")
        peer_ip = self.params.get("peerip")
        ret = process.system("ethtool -K %s gro on" % interface, shell=True)
        if ret == 0:
            ret = process.system("ping -c 1 %s" % peer_ip, shell=True)
            if ret != 0:
                self.fail("gro test failed")
            process.system("ethtool -K %s gro off" % interface, shell=True)
            ret = process.system("ping -c 1 %s" % peer_ip, shell=True)
            if ret != 0:
                self.fail("gro test failed")
        else:
            self.fail("gro test failed")

    def testlro(self):
        '''
        check lro is enabled or not
        '''
        self.log.info("Largest Receive Offload")
        interface = self.params.get("iface")
        peer_ip = self.params.get("peerip")
        if not process.system("ethtool -K %s lro off" % interface, shell=True):
            self.fail("LRO Test failed")
        ret = process.system("ping -c 1 %s" % peer_ip, shell=True)
        if ret != 0:
            self.fail("lro test failed")
            msg = "ethtool -K %s lro on" % interface
            if not process.system(msg, shell=True):
                self.fail("LRO Test failed")
                ret = process.system("ping -c 1 %s" % peer_ip, shell=True)
                if ret != 0:
                    self.fail("lro test failed")


if __name__ == "__main__":
    main()
