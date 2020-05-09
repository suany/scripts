#!/bin/sh

# cd to script dir, remember caller dir FWIW
CALLERDIR=`pwd`
SCRIPTDIR_REL=`dirname "$0"`
cd "${SCRIPTDIR_REL}"
SCRIPTDIR=`pwd`

echo "caller=${CALLERDIR}"
echo "scriptdir=${SCRIPTDIR}"
