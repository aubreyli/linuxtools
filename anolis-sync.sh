# keep main-stream cloud-kernel up to date
cd /home/aubrey/anolis/cloud-kernel
git checkout devel-5.10
git pull > /home/aubrey/anolis-pull-`date +%Y-%m-%d`.log 2>&1

cd /home/aubrey/anolis/intel-kernel
#sync up intel-kernel master branch with linux-stable master branch
git checkout master
git pull /home/aubrey/work/linux-stable master >> /home/aubrey/anolis-pull-`date +%Y-%m-%d`.log 2>&1
git push >> /home/aubrey/anolis-pull-`date +%Y-%m-%d`.log 2>&1

#sync up intel-kernel anck-devel-5.10 branch with cloud-kernel devel-5.10 branch
git checkout anck-devel-5.10
git pull /home/aubrey/anolis/cloud-kernel devel-5.10 >> /home/aubrey/anolis-pull-`date +%Y-%m-%d`.log 2>&1
git push >> /home/aubrey/anolis-pull-`date +%Y-%m-%d`.log 2>&1
