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
# Copyright: 2016 Red Hat
# Author: Amador Pahim <apahim@redhat.com>

import fnmatch
import os
import re
import stat
import sys

LICENSE_ITEMS = ["#[ ]{,}This program is free software; you can redistribute "
                 "it and/or modify",
                 "#[ ]{,}it under the terms of the GNU",
                 "#[ ]{,}the Free Software Foundation",
                 "#[ ]{,}Copyright"]


def check_license(license, filename):
    with open(filename, 'r') as f:
        content = f.readlines()

    for item in license:
        match = False
        for line in content:
            if re.search(item, line):
                match = True

        if not match:
            return False

    return True


def is_file_empty(filename):
    if os.stat(filename)[stat.ST_SIZE] == 0:
        return True
    return False

if __name__ == '__main__':
    err = False
    for root, dirname, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.py'):
            path = os.path.join(root, filename)
            if (not is_file_empty(path) and
               not check_license(LICENSE_ITEMS, path)):
                print "%s FAIL" % path
                err = True
    if err:
        sys.exit(1)
