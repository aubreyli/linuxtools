cd /home/aubrey/work/intel-kernel
#sync up internal intel-kernel master branch with linux-stable linux-5.10.y branch
git checkout master
git pull /home/aubrey/work/linux-stable linux-5.10.y >> /home/aubrey/intel-kernel-`date +%Y-%m-%d`.log 2>&1
git push >> /home/aubrey/intel-kernel-`date +%Y-%m-%d`.log 2>&1

#sync up intel-kernel anck-devel-5.10 branch with cloud-kernel devel-5.10 branch
git checkout anck-devel-5.10
git pull /home/aubrey/anolis/cloud-kernel devel-5.10 >> /home/aubrey/intel-kernel-`date +%Y-%m-%d`.log 2>&1
git push >> /home/aubrey/intel-kernel-`date +%Y-%m-%d`.log 2>&1
