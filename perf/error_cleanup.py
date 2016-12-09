#! /usr/bin/env python

from avocado import Test
from avocado import main


class error_cleanup(Test):
    """
    Raise an exception during cleanup()
    """

    def test(self):
        pass

    def cleanup(self):
        self.NameError("test a bug in cleanup()")


if __name__ == "__main__":
    main()
