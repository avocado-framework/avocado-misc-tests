Tests the network driver and interface with 'ethtool' command.
12 different options of ethtool command are tested for each
of the interfaces specified in 'config' file

Requirements:
-------------
For all specified interfaces, configuration file for that interface needs
to be updated, so that 'ifup/ifdown <interface>' configures the interface.

Input Needed (in 'config' file):
--------------------------------
Interfaces  -   Specify all the interfaces for which the test needs to be run.
                Seperated by spaces

