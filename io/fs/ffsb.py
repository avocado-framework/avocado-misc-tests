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
# Copyright: 2016 Red Hat, Inc.
# Flexible Filesystem Benchmark (FFSB) is a cross-platform filesystem
#  performance measurement tool
# Ported to Avocado from Kalpana S Shetty(kalshett@linux.vnet.ibm.com)
# source: https://github.com/autotest/autotest-client-tests/tree/master/ffsb

import os
import string
import re
import random
import shutil

from avocado import Test
from avocado import main
from avocado.utils import archive
from avocado.utils import build
from avocado.utils import process


def find_mnt_pt(path):
    """
    Find on which mount point a given path is mounted.

    :param path: Path we want to figure its mount point.
    """
    pth = os.path.abspath(path)
    while not os.path.ismount(pth):
        pth = os.path.dirname(pth)
    return pth


class FFSBTest(Test):

    """
    FFSB is a filesystem performance measurement tool.

    :see: https://sourceforge.net/projects/ffsb/files/

    :param ffsb_tarball: name of the tarball of ffsb suite located in deps path
    :param ffsb_job: profile.cfg, config file used
    """

    version = 1
    params = {}
    tempdirs = []
    bytes = {'K': 1024, 'k': 1024,
             'M': 1048576, 'm': 1048576,
             'G': 1073741824, 'g': 1073741824,
             'T': 1099511627776, 't': 1099511627776}

    def set_ffsb_params(self, usrfl):
        """
        This function checks for the user supplied FFSB profile file
        and validates it against the available resources on the
        guest - currently only disk space validation is supported
        but adjusting the number of threads according to the vcpus
        exported by the qemu-kvm also needs to be added.

        :param usrfl: Path to the user profile file.
        """
        d = {}
        fr = open(usrfl, 'r')
        for line in fr.read().split('\n'):
            p = re.compile(r'\s*\t*\[{1}filesystem(\d+)\]{1}')
            m = p.match(line)
            if m:
                fsno = int(line[m.start(1):m.end(1)])
                d[fsno] = []
            p = re.compile(r'(\s*\t*location)\=(.*)')
            m = p.match(line)
            if m:
                path = line[m.start(2):m.end(2)]
                mntpt = find_mnt_pt(path)
                f = os.statvfs(mntpt)
                avl_dsk_spc = f.f_bfree * f.f_bsize
                avl_dsk_spc *= 0.95
                d[fsno].append(mntpt)
                d[fsno].append(int(avl_dsk_spc))
            p = re.compile(r'(\s*\t*num_files)\=(\d+)')

            m = p.match(line)
            if m:
                usrnumfl = int(line[m.start(2):m.end(2)])
                d[fsno].append(usrnumfl)
            p = re.compile(r'(\s*\t*max_filesize)\=(\d+[kKMmGgTt]?)')
            m = p.match(line)
            if m:
                usrmaxflsz = line[m.start(2):m.end(2)]
                usrmaxflsz = int(usrmaxflsz[0:-1]) * self.bytes[usrmaxflsz[-1]]
                d[fsno].append(usrmaxflsz)
        for k in d.keys():
            while d[k][2] * d[k][3] >= d[k][1]:
                d[k][2] -= 1
            if d[k][2] == 0:
                d[k][2] = 1
                d[k][3] = d[k][1]
            # If the ffsb mount point is on the same file system
            # then use the available disk space after the previous
            # tests
            for k1 in d.keys():
                if d[k1][0] == d[k][0]:
                    d[k1][1] -= (d[k][2] * d[k][3])
        fr.close()
        return d

    def dup_ffsb_profilefl(self):
        """
        Validates the path from the FFSB configuration file, the
        disk space available for the test, warn the user and
        change the file sizes and/or number of files to be used for
        generating the workload according to the available disk space
        on the guest.
        """

        self.usrfl = '%s/%s' % (os.path.split(self.datadir)[0], 'profile.cfg')
        self.sysfl = '%s/%s' % (self.datadir, 'profile.cfg')

        params = self.set_ffsb_params(self.usrfl)

        fsno = 0
        fr = open(self.usrfl, 'r')
        fw = open(self.sysfl, 'w')
        for line in fr.read().split('\n'):
            p = re.compile(r'\s*\t*\[{1}filesystem(\d+)\]{1}')
            m = p.match(line)
            if m:
                fsno = int(line[m.start(1):m.end(1)])
            p = re.compile(r'(\s*\t*location)\=(.*)')
            m = p.match(line)
            if m:
                while True:
                    dirnm = ''.join(random.choice(string.letters)
                                    for i in xrange(9))
                    if line[m.end(2) - 1] == '/':
                        newline = '%s%s' % (line[0:m.end(2)], dirnm)
                        ffsbdir = '%s%s' % (line[m.start(2):m.end(2)], dirnm)
                    else:
                        newline = '%s/%s' % (line[0:m.end(2)], dirnm)
                        ffsbdir = '%s/%s' % (line[m.start(2):m.end(2)], dirnm)
                    self.tempdirs.append(ffsbdir)
                    if os.path.exists(ffsbdir):
                        continue
                    else:
                        os.makedirs(ffsbdir)
                        break
                fw.write(newline + '\n')
                continue
            p = re.compile(r'(\s*\t*num_files)\=(.*)')
            m = p.match(line)
            if m:
                newline = '%s=%s' % (line[0:m.end(1)], str(params[fsno][2]))
                fw.write(newline + '\n')
                continue
            p = re.compile(r'(\s*\t*max_filesize)\=(\d+[kKMmGgTt]?)')
            m = p.match(line)
            if m:
                newline = '%s%s' % (line[0:m.start(2)], str(params[fsno][3]))
                fw.write(newline + '\n')
                continue
            fw.write(line + '\n')
        fr.close()
        fw.close()

    def setUp(self):
        """
        Build 'ffsb'.
        """

        self.update_config('profile.cfg.sample')

        tarball = self.fetch_asset('http://prdownloads.sourceforge.net'
                                   '/ffsb/ffsb-6.0-rc2.tar.bz2')
        data_dir = os.path.abspath(self.datadir)
        archive.extract(tarball, self.srcdir)
        ffsb_version = os.path.basename(tarball.split('.tar.')[0])
        self.srcdir = os.path.join(self.srcdir, ffsb_version)

        patch = self.params.get('patch',
                                default='ffsb-ppc64le-arch-support.patch')

        os.chdir(self.srcdir)
        p1 = 'patch -p1 < %s/%s' % (data_dir, patch)
        process.run(p1, shell=True)
        process.run('[ -x configure ] && ./configure', shell=True)
        build.make(self.srcdir)

    def update_config(self, cfg):
        """
        Update the profile.cfg file.

        :param cfg: Basename of the cfg file, that should be on the
                    test module folder (client/tests/ffsb) or URL of the
                    remote config file.
        """

        filename = os.path.basename(cfg)
        profile_src = os.path.join(self.datadir, filename)
        profile_dst = os.path.join(os.path.dirname(self.datadir),
                                   'profile.cfg')
        shutil.copyfile(profile_src, profile_dst)

    def test(self, cfg=None):
        """
        Runs a single iteration of the FFSB.
        """
        profile_cfg = self.params.get('profile_cfg', default='profile.cfg')
        if cfg is not None:
            self.update_config(cfg)

        self.dup_ffsb_profilefl()

        # Run FFSB using abspath
        cmd = '%s/ffsb %s' % (self.srcdir,
                              os.path.join(self.datadir, profile_cfg))
        print ("FFSB command: %s" % (cmd))
        process.system(cmd)

if __name__ == "__main__":
    main()
