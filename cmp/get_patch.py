"""
Gaussian HMM of stock data
--------------------------
This script trained Gaussian HMM on SH510300 price data.

Author: Aubrey Li

Ver: 2016-07-04
"""
import sys,time,getopt
import os

debug = 1

curr_dir = os.getcwd()
patch_dir = os.path.join(curr_dir, "backport")

def format_upstream(ele, commit_id):
    if 'commit' in ele:
        if len(ele) < 3:
            print("xxxxxxxx error: {}".format(patch))
        if len(ele) == 3:
            if (len(ele[1]) != 40 or len(ele[2]) != 9):
		print("xxxxxxxx error: {} - {}".format(patch, ele))
            print(ele)
	    commit_id = ele[1]

def check_format(patch):
    flag_upstream = 0
    pf = open(patch_file,'r')
    for line in pf.readlines():
        ele = line.strip().split()
        format_upstream(ele)
    pf.close()

def obtain_commit_id(patch):
    commit_id = ''
    pf = open(patch,'r')
    for line in pf.readlines():
        ele = line.strip().split()
        if 'commit' in ele:
            if len(ele) < 3:
                print("xxxxxxxx error: {}".format(patch))
            if len(ele) == 3:
                if (len(ele[1]) != 40 or len(ele[2]) != 9):
                    print("xxxxxxxx error: {} - {}".format(patch, ele))
                commit_id = ele[1]
    pf.close()
    return commit_id

def obtain_patch(patch):
    pf = open(patch_file,'r')
    for line in pf.readlines():
        ele = line.strip().split()
    pf.close()

if __name__ == "__main__":

    for patch in os.listdir(patch_dir):
        if os.path.isdir(patch):
            continue
        if debug:
            print("processing {}".format(patch))
        patch_file = os.path.join(patch_dir, patch)
	commit_id = obtain_commit_id(patch_file)
	print(commit_id)
	obtain_patch(patch_file)

