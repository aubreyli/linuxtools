TODAY=`date +%Y-%m-%d`
LOGFILE=/home/aubrey/intel-kernel-$TODAY.log
EMAIL=aubrey.li@intel.com

cd /home/aubrey/work/os.linux.server.openanolis-kernel/
#sync up intel-kernel devel-5.10 branch with cloud-kernel devel-5.10 branch
git checkout devel-5.10
echo "intel-kernel devel-5.10 branch result:" >> $LOGFILE 2>&1
echo "=========================================" >>  $LOGFILE 2>&1
git pull /home/aubrey/anolis/intel-cloud-kernel devel-5.10 >> $LOGFILE 2>&1
git push >> $LOGFILE 2>&1
echo "\n" >>  $LOGFILE 2>&1

git checkout siov-5.10
echo "intel-kernel siov-5.10 branch result:" >> $LOGFILE 2>&1
echo "=========================================" >>  $LOGFILE 2>&1
git pull /home/aubrey/anolis/intel-cloud-kernel siov-5.10 >> $LOGFILE 2>&1
git push --force >> $LOGFILE 2>&1
echo "\n" >>  $LOGFILE 2>&1

cat $LOGFILE | mutt -s "[Intel-kernel]: $TODAY update" $EMAIL
rm $LOGFILE
