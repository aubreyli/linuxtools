#!/usr/bin/python

###############################################################
# This program is used to disable c-state thru /sys interface
# sudo perf-with-kcore record pt_select_task_rq_fair_3 -C0 \
#	 -e intel_pt/cyc/k --filter="filter select_task_rq_fair" \
#	 -- sleep 1
# sudo perf-with-kcore script pt_select_task_rq_fair_3 --itrace=cre \
#	 --ns -Fcomm,time,sym,symoff,dso,addr,flags,callindent > intel_pt.log
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
import numpy as np

skip_header = 3
call_step = 6
return_index = call_step - 1
addr_entry = "ffffffffa3ecf360"
addr_return = "ffffffffa3ec8270"

def function_duration(filename):
	fd = open(filename, 'r')
	count = 0
	lat = []
	for line in fd.readlines():
		item = line.replace('.','')
		item = item.replace(':','').strip().split()
		if addr_entry in item:
			ts_entry = float(item[1])
		if addr_return in line and ts_entry != 0:
			ts_latency = float(item[1]) - ts_entry
			ts_entry = 0
			lat.append(ts_latency)
			count = count + 1
	fd.close()
	return np.mean(lat),np.std(lat), count

##############################################
# main()
##############################################
if   __name__  ==  "__main__":
	avg, std, count = function_duration("intel_pt.log")
	print(round(avg/1000, 5), round(std/1000, 5), count)
