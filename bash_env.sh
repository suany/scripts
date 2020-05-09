#!/bin/sh

# cygwin's bin may not yet be in the path
export PATH="${PATH}:/bin"

SCRIPTDIR=`dirname "$0"`

# Forward to sandbox.sh
. "${SCRIPTDIR}/sandbox.sh" "$@"

# GT assert: development mode, use "break"
export GT_ASSERT=break

exec bash --login -i
