# keep main-stream cloud-kernel up to date
TODAY=`date +%Y-%m-%d`
LOGFILE=/home/aubrey/anolis-pull-$TODAY.log
EMAIL=aubrey.li@intel.com

# Function to sync a repository with error handling
sync_branch() {
    local repo_path=$1
    local branch=$2
    local remote=$3
    local remote_name=${4:-"origin"}

    echo "Syncing $repo_path:$branch from $remote_name/$branch..." >> $LOGFILE 2>&1
    echo "========================================" >> $LOGFILE 2>&1

    cd "$repo_path" || return 1

    # Checkout the branch
    if ! git checkout "$branch" >> $LOGFILE 2>&1; then
        echo "ERROR: Failed to checkout $branch" >> $LOGFILE 2>&1
        return 1
    fi

    # Fetch from remote to get latest changes (handles force push)
    if ! git fetch "$remote_name" "$branch" >> $LOGFILE 2>&1; then
        echo "ERROR: Failed to fetch $branch from $remote_name" >> $LOGFILE 2>&1
        return 1
    fi

    # Reset local branch to match remote (handles force push)
    if ! git reset --hard "$remote_name/$branch" >> $LOGFILE 2>&1; then
        echo "ERROR: Failed to reset $branch to $remote_name/$branch" >> $LOGFILE 2>&1
        return 1
    fi

    echo "SUCCESS: $branch synced" >> $LOGFILE 2>&1
    echo "" >> $LOGFILE 2>&1
}

# Initialize log file
> $LOGFILE 2>&1

# Sync cloud-kernel repository
echo "Starting sync of cloud-kernel repository" >> $LOGFILE 2>&1
echo "========================================" >> $LOGFILE 2>&1
echo "" >> $LOGFILE 2>&1

sync_branch "/home/aubrey/anolis/cloud-kernel" "devel-5.10" "origin" "origin"
sync_branch "/home/aubrey/anolis/cloud-kernel" "devel-6.6" "origin" "origin"

echo "" >> $LOGFILE 2>&1
echo "Starting sync of intel-cloud-kernel repository" >> $LOGFILE 2>&1
echo "========================================" >> $LOGFILE 2>&1
echo "" >> $LOGFILE 2>&1

# Sync intel-cloud-kernel repository
sync_branch "/home/aubrey/anolis/intel-cloud-kernel" "devel-5.10" "upstream" "upstream"
sync_branch "/home/aubrey/anolis/intel-cloud-kernel" "devel-6.6" "upstream" "upstream"

# Push synced branches to origin
echo "" >> $LOGFILE 2>&1
echo "Pushing synced branches to origin..." >> $LOGFILE 2>&1
echo "========================================" >> $LOGFILE 2>&1
cd /home/aubrey/anolis/intel-cloud-kernel

git checkout devel-5.10 >> $LOGFILE 2>&1
git push --force-with-lease >> $LOGFILE 2>&1
echo "Pushed devel-5.10" >> $LOGFILE 2>&1

git checkout devel-6.6 >> $LOGFILE 2>&1
git push --force-with-lease >> $LOGFILE 2>&1
echo "Pushed devel-6.6" >> $LOGFILE 2>&1

# Send summary email
cat $LOGFILE | mutt -s "[$(hostname) anolis]: $TODAY update" $EMAIL
rm $LOGFILE
