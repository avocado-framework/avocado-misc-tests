Tests the network driver and interface with 'ethtool' command.
Different parameters are specified in Parameters section of multiplexer file.
Interfaces are specified in Interfaces section of multiplexer file.

Requirements:
-------------
For all specified interfaces, configuration file for that interface needs
to be updated, so that 'ifup/ifdown <interface>' configures the interface.

Input Needed (in multiplexer file):
-----------------------------------
Interfaces  -   Specify all the interfaces for which the test needs to be run.

