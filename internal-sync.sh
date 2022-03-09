TODAY=`date +%Y-%m-%d`
LOGFILE=/home/aubrey/intel-kernel-$TODAY.log
EMAIL=aubrey.li@intel.com

cd /home/aubrey/work/intel-kernel
#sync up internal intel-kernel master branch with linux-stable linux-5.10.y branch
git checkout master
echo "intel-kernel stable master branch result:" > $LOGFILE 2>&1
echo "=========================================" >>  $LOGFILE 2>&1
git pull /home/aubrey/work/linux-stable linux-5.10.y >> $LOGFILE 2>&1
git push >> $LOGFILE 2>&1
echo "\n" >>  $LOGFILE 2>&1

#sync up intel-kernel anck-devel-5.10 branch with cloud-kernel devel-5.10 branch
git checkout anck-devel-5.10
echo "intel-kernel devel-5.10 branch result:" >> $LOGFILE 2>&1
echo "=========================================" >>  $LOGFILE 2>&1
git pull /home/aubrey/anolis/cloud-kernel devel-5.10 >> $LOGFILE 2>&1
git push >> $LOGFILE 2>&1
echo "\n" >>  $LOGFILE 2>&1

git checkout linux-next
echo "intel-kernel linux-next branch result:" >> $LOGFILE 2>&1
echo "=========================================" >>  $LOGFILE 2>&1
git pull /home/aubrey/anolis/cloud-kernel linux-next >> $LOGFILE 2>&1
git push >> $LOGFILE 2>&1
echo "\n" >>  $LOGFILE 2>&1

cat $LOGFILE | mutt -s "[Intel-kernel]: $TODAY update" $EMAIL
rm $LOGFILE
