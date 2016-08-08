#!/bin/python
import os
import subprocess



class cpu_hotplug:
	count = 0 
	def func_hot(self):
		cmd = "ls -1 /sys/devices/system/cpu/ | grep ^cpu[0-9][0-9]* |wc -l"
		cpu_list = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(list, err) = cpu_list.communicate()
		for count in range(0,100):
                    for cpus in range(1,(int(list))):
                        cpu="cpu%s" %cpus
			# "cpu" is the list of cpu listed from "/sys/devices/system/cpu" directory , which is used for hot plug/unplugging the cpu
			print("The cpu is %s" %cpu)
			cmd = 'echo 0 > /sys/devices/system/cpu/%s/online' % cpu
			status = os.system(cmd)
			if status != 0:
				print("Error offline cpu %s while running hotplug_1_by_1 ",cpu)
		        else:
                		print("offline'd CPU %s while running hotplug_1_by_1 ",cpu)
			cmd1 = 'echo 1 > /sys/devices/system/cpu/%s/online' % cpu
			status1 = os.system(cmd1)
			if status1 != 0:
				print("Error online cpu %s while running hotplug_1_by_1",cpu)
			else:
				print("Online'd CPU %s while running hotplug_1_by_1 ",cpu)


	
	
hotplug = cpu_hotplug()
hotplug.func_hot()
