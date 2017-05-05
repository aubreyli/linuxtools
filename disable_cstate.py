#!/usr/bin/python

###############################################################
# This program is used to disable c-state thru /sys interface
################################################################


__author__ = "Aubrey Li (aubreylee@gmail.com)"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2017/05/04 10:10:10 $"
__copyright__ = "Copyright (c) 2012 Aubrey Li"
__license__ = "Python"

import sys
import os
import re
import time

cpu_num = 44
cstate_num = 5
cstate_enabled= 2

def disable_cstate():
	for i in range(0, cpu_num):
		for n in range(0, cstate_num):
			if (n != cstate_enabled):
				cmd = "echo 1 > /sys/devices/system/cpu/cpu"+str(i)+"/cpuidle/state"+str(n)+"/disable"
				os.system(cmd)
			cmd = "cat /sys/devices/system/cpu/cpu"+str(i)+"/cpuidle/state"+str(n)+"/name"
			result = os.popen(cmd)
			name = result.read().strip()
			cmd = "cat /sys/devices/system/cpu/cpu"+str(i)+"/cpuidle/state"+str(n)+"/disable"
			result = os.popen(cmd)
			state = result.read().strip()
			info = "cpu"+str(i)+": state"+str(n)+": "+name+": "+state
			print(info)

##############################################
# main()
##############################################
if   __name__  ==  "__main__":
	disable_cstate()
