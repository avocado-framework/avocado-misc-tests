This Program loads and unloads the kernel driver modules. For the kernel driver modules that have dependencies, the dependant modules should  be listed in the config file (config). The script takescare of unloading the dependant modules, if any, before unloading the core module. It runs for a total of 100 times as stress.

This script should be run as root.
