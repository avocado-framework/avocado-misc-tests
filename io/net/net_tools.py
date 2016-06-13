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
# Author: Basheer K<basheer@linux.vnet.ibm.com>
#
# Based on code by  Hong Bo Peng <penghb@cn.ibm.com>
# copyright: 2003, 2015 IBM Corp

import os
import re
from avocado import Test
from avocado import main
from avocado.core import data_dir
from avocado.utils import process, distro
from avocado.utils.software_manager import SoftwareManager


class net_tools(Test):
    """
    Net_tools class verify the functionality of various network tools.
    hostname: set/get hostname by cmd. Check it with the expected result.
    ifconfig: setup an alias for lo. Check it can be listed.
    netstat: run it with different options. Check the return code.
    arp: run it with different options. Check the return code.
    traceroute,traceroute6: run for localhost. It should report 1 hop.
    route: run it with -n. Check the return code.
    ipmaddr: run it and check the return code.
    iptunnel: create sit1 and check it can be list. Then remove it and
              check it is removed from the list.
    """

    def setUp(self):
        """
        Verify Required tools are installed or not.
        """
        if os.getuid() != 0:
            exit("You need to have root privileges to execute this script. \
                 \nPlease try again, using 'sudo'. Exiting.")
        sm = SoftwareManager()
        self.detected_distro = distro.detect()
        if self.detected_distro.name == "SuSE":
            net_tools = ("net-tools", "traceroute")
        else:
            net_tools = ("net-tools", "hostname", "traceroute")
        for pkg in net_tools:
            if not sm.check_installed(pkg) and not sm.install(pkg):
                self.error("%s package is need to test" % pkg)
        self.ipv6 = False
        if os.path.exists("/proc/net/if_inet6"):
            self.ipv6 = True
        interface_out = process.system_output("ip route show default",
                                              verbose=False,
                                              shell=True)
        search_obj = re.search(
            "default via\s+(\S+)\s+dev\s+(\w+)", interface_out)
        active_iface = search_obj.group(2)
        self.default_router = search_obj.group(1)
        if active_iface is None:
            self.error("can't find active network interface")
        tmpdir = data_dir.get_tmp_dir()
        self.backup_dir = os.path.join(tmpdir, 'net-tools')
        if not os.path.isdir(self.backup_dir):
            os.makedirs(self.backup_dir)
        # Get Hostname
        output = process.run(cmd="hostname", shell=True, verbose=False)
        if output.exit_status != 0:
            self.error("Failed To get hostname\n")
        else:
            if output.stdout is None:
                # set hostname if not set
                if not process.system("hostname localhost.localdomain"):
                    self.error("Failed to set hostname\n")
            process.system("hostname > %s/HOSTNAME" % self.backup_dir,
                           verbose=False,
                           shell=True)

    def test_hostname(self):
        """
        Verify the functionality of the hostname command
        """
        hostname_cmd = "hostname"
        output = process.run(cmd=hostname_cmd, shell=True, verbose=False)
        if output.exit_status != 0 and output.stdout is None:
            self.error("unexpected response from hostname command")

        # Verifying different options provided by hostname
        options_to_verify = self.params.get('hostname_opt', default="f")
        for option in options_to_verify:
            self.log.info("Verifying the hostname -%s option" % option)
            status = process.system("hostname -%s" % option, verbose=False,
                                    shell=True)
            if status != 0:
                self.error(
                    "unexpected response from hostname %s command" %
                    option)

        # Test for setting new hostname using -F option
        process.system(
            "echo 'myhost.my-domain' > %s/MYHOSTNAME" %
            self.backup_dir, verbose=False, shell=True)
        status = process.system("hostname -F %s/MYHOSTNAME" % self.backup_dir,
                                verbose=False,
                                shell=True)
        if status != 0:
            self.error("Failed to change the hostname")
        else:
            output = process.run(
                cmd=hostname_cmd, shell=True, verbose=False)
            if not (re.search("myhost.my-domain", output.stdout)):
                self.error("unexpected response from hostname -F command and \
                                            hostname -F didn't set hostname")
        # Restore hostname
        status = process.system("hostname -F %s/HOSTNAME" % self.backup_dir,
                                verbose=False,
                                shell=True)
        if status != 0:
            self.error(
                "unexpected response trying to restore the hostname \
                from HOSTNAME")

    def test_ifconfig(self):
        """
        Verify the functionality of the ifconfig
        """
        output = process.run(cmd="ifconfig", shell=True, verbose=False)
        if output.exit_status != 0:
            self.error("ifconfig failed")
        if not re.search("Local Loopback", output.stdout):
            self.error("unexpected output of ifconfig")
        if self.ipv6:
            if not re.search("inet6", output.stdout):
                self.error("Did not see IPV6 info")
        # setup and verify an alias interface
        status = process.system("ifconfig lo:1 127.0.0.240  netmask 255.0.0.0",
                                verbose=False,
                                shell=True)
        if status != 0:
            self.error("ifconfig lo:1 failed")
        status = process.system("ifconfig lo:1 down", verbose=False,
                                shell=True)
        if status != 0:
            self.error("ifconfig lo:1 down failed")

    def test_netstat(self):
        """
        Verify the functionality of netstat
        """
        # Verifying different options provided by hostname
        options_to_verify = self.params.get('netstat_opt', default="s")
        for option in options_to_verify:
            self.log.info("Verifying the -%s option of netstat" % option)
            status = process.system("netstat -%s" % option, verbose=False,
                                    shell=True)
            if status != 0:
                self.error("netstat %s failed" % option)

    def test_arp(self):
        """
        Verify the functionality of ARP
        """
        # Test to resolve Mac addr of default gateway router
        process.system("ping -c 2 -w 5 %s" % self.default_router)
        output = process.run(cmd="arp -n", shell=True, verbose=False)
        if not re.search(self.default_router, output.stdout):
            self.error("unexpected response from ping")

    def test_traceroute(self):
        """
        Verify traceroute,traceroute6 functionality.
        """
        output = process.run(cmd="traceroute localhost",
                                 shell=True, verbose=False)
        if output.exit_status != 0:
            self.error("\n traceroute failed")
        no_of_hops = re.search(
            "(\d+)\s+\S+\s*\(127.0.0.1\)",
            output.stdout).group(1)
        # Only one hop is required to get to localhost.
        if (str(no_of_hops) != '1'):
            self.error("traceroute did not show 1 hop for localhost")
        if self.ipv6:
            if self.detected_distro.name == "SuSE":
                output = process.run(cmd="traceroute6 ipv6-localhost",
                                         shell=True, verbose=False)
            elif self.detected_distro.name == "Ubuntu":
                output = process.run(cmd="traceroute6 ip6-localhost",
                                         shell=True, verbose=False)
            else:
                output = process.run(cmd="traceroute6 localhost6",
                                         shell=True, verbose=False)
            if output.exit_status != 0:
                self.error("\n traceroute6 failed")
            no_of_hops = re.search(
                "(\d+)\s+\S+\s*\(::1\)",
                output.stdout).group(1)
            if (str(no_of_hops) != '1'):
                self.error("traceroute6 did not show 1 hop for localhost6")

    def test_route(self):
        """
        Verify the route fuctionality.
        """
        output = process.run(cmd="route -n",
                                 shell=True,
                                 verbose=False)
        if output.exit_status != 0:
            self.error("route cmd failed")
        if self.ipv6:
            output = process.run(cmd="route -A inet6 -n",
                                     shell=True,
                                     verbose=False)
            if output.exit_status != 0:
                self.error("route ipv6 failed")

    def test_ipmaddr(self):
        """
        Verify ipmaddr functionality
        """
        output = process.run(cmd="ipmaddr show dev lo",
                                 shell=True,
                                 verbose=False)
        if output.exit_status != 0:
            self.error("ipmaddr failed to diaplay mcast addr of loop back")
        if self.ipv6:
            output = process.run(cmd="ipmaddr show ipv6 dev lo",
                                     shell=True,
                                     verbose=False)
            if output.exit_status != 0:
                self.error("\n ipmaddr ipv6 failed")

    def test_iptunnel(self):
        """
        Verify iptunnel functionality
        """
        # Note, this messes up dhcp client configurations so is skipped in that
        # case
        output = process.system_output("ps -aef", verbose=False, shell=True)
        if 'dhclient' in output:
            self.log.info("Skipped on dhclient systems")
            return 0
        # add sit1
        status = process.system(
            cmd="iptunnel add sit1 mode sit local 127.0.0.1 ttl 64",
            verbose=False,
            shell=True)
        if status != 0:
            self.error("iptunnel add sit1 failed")
        output = process.run(cmd="iptunnel show",
                                 shell=True,
                                 verbose=False)
        if output.exit_status != 0:
            self.error("iptunnel show failed")
        if not re.search("sit1", output.stdout):
            self.error("iptunnel didn't add sit1")
        # remove sit1
        status = process.system("iptunnel del sit1", verbose=False,
                                shell=True)
        if status != 0:
            self.error("iptunnel del sit1 failed")
        output = process.run(cmd="iptunnel show",
                                 shell=True,
                                 verbose=False)
        if output.exit_status != 0:
            self.error("iptunnel show failed")
        if re.search("sit1", output.stdout):
            self.error("iptunnel didn't remove sit1")

    def teardown(self):
        """
        cleanup function
        """
        if os.path.exists(self.backup_dir):
            process.system("rm -rf %s" % self.backup_dir, verbose=False,
                           shell=True)


if __name__ == "__main__":
    main()
