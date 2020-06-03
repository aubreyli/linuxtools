"""
obtain function duration
--------------------------
sudo trace-cmd record -p function_graph -l select_task_rq_fair -- sleep 1
sudo trace-cmd report

Author: Aubrey Li

Ver: 2016-07-04
"""
from struct import *
import numpy as np
import sys,time,getopt
import os
import os.path
import math
from code import *

def obtain_log(logfile):
    count = 0
    lat = []
    ofile=open(logfile,'r')
    for line in ofile.readlines():
        ele = line.replace('+', '').replace('!','').strip().split()
        if len(ele) < 8:
            continue
        print(ele)
        lat.append(float(ele[4]))
        count+=1
    ofile.close()
    return np.mean(lat),np.std(lat), count

if __name__ == "__main__":
    avg, std, count = obtain_log("funcgraph.log")
    print(avg, std, count/192.0)
