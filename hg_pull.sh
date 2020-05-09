#!/bin/sh

# Pull into the hg clone defined by $SANDBOX,
# update the working directory (sandbox), and
# copy the svn info results stashed for $SB by
# HgSubversion clone defined by $HS_SANDBOX.

echo "\nRefreshing $SANDBOX...\n"

cd $SANDBOX

# Rebasing won't work with uncommitted changes.  Handle two kinds of changes:
# a. unwanted changes in third-party due to builds deleting committed files,
# b. keeper semi-permanent changes applied to sandboxes.

# 1. Simply revert the known unwanted third-party changes.
# In third-party: curl/docs/*, flex/doc/flex.pdf, openssl/tools/c_rehash.bak
echo Reverting unwanted uncommitted changes in third-party...
hg revert --no-exclude third-party/curl third-party/flex third-party/openssl

# 2. "shelve" remaining uncommitted changes (using built-in commands):
# save a patch (to be reapplied after rebasing) and revert all changes.
echo Making a patch with remaining uncommitted changes...
hg diff > patch   # save local changes
if [ -s patch ]   # don't waste time if diff is empty
then
    NANOS=`date +%N`
    echo Backing up patch in patch.$NANOS...
    cp -f patch patch.$NANOS  # back up patch just in case
    hg revert -a --no-backup  # revert local changes (w/o backup .orig files)
fi

# 3. pull into the hg clone defined by $SANDBOX with rebasing of
# local changesets and updating the working directory (sandbox).
echo Pulling with --rebase...
hg pull --rebase

# 4. "unshelve" uncommitted changes, if any (using built-in command import).
if [ -s patch ]
then
    echo Reapplying patch with uncommitted changes...
    hg import --no-commit -v patch
fi

# Copy the svn info results for $SB stashed by HgSubversion clone
# defined by $HS_SANDBOX.  We should probably preserve _$SB in
# filename for switching between branches within hg clones.
cp -p $HS_SANDBOX/svn_info_$SB.txt $SANDBOX/svn_info.txt

echo "\nUpdated $SANDBOX ($SB) to:\n"
cat $SANDBOX/svn_info.txt
