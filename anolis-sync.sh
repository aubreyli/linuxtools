# keep main-stream cloud-kernel up to date
TODAY=`date +%Y-%m-%d`
LOGFILE=/home/aubrey/anolis-pull-$TODAY.log
EMAIL=aubrey.li@intel.com

cd /home/aubrey/anolis/cloud-kernel
git checkout devel-5.10
#git reset --hard e2d133180bbc28a48316e67a003796885580b087 #v5.10.9
echo "Cloud-kernel devel-5.10 branch result:" > $LOGFILE 2>&1
echo "======================================" >>  $LOGFILE 2>&1
git pull >> $LOGFILE 2>&1
echo "\n" >>  $LOGFILE 2>&1

git checkout linux-next
#git reset --hard 528cecfa5af09631f0589efe9eacbd543c8c9db1 #v5.16.10
echo "Cloud-kernel linux-next branch result:" >> $LOGFILE 2>&1
echo "======================================" >> $LOGFILE 2>&1
git pull >> $LOGFILE 2>&1
echo "\n" >>  $LOGFILE 2>&1

cd /home/aubrey/anolis/intel-cloud-kernel
#sync up intel-kernel master branch with linux-stable master branch
git checkout devel-5.10
echo "Intel-cloud-kernel devel-5.10 branch result:" >> $LOGFILE 2>&1
echo "============================================" >> $LOGFILE 2>&1
git pull upstream devel-5.10 >> $LOGFILE 2>&1
git push >> $LOGFILE 2>&1
echo "\n" >>  $LOGFILE 2>&1

git checkout linux-next
echo "Intel-cloud-kernel devel-5.10 branch result:" >> $LOGFILE 2>&1
echo "============================================" >> $LOGFILE 2>&1
git pull upstream linux-next >> $LOGFILE 2>&1
git push >> $LOGFILE 2>&1
echo "\n" >>  $LOGFILE 2>&1

cat $LOGFILE | mutt -s "[anolis]: $TODAY update" $EMAIL
rm $LOGFILE
