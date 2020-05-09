#!/bin/sh
#
# Add to your.bashrc:
#
#  alias cdnext='`sh ~/scripts/cdnext_cmd.sh`'
#

THISDIR_ABS=`pwd`
THISDIR=`basename "${THISDIR_ABS}"`
PARENTDIR=`dirname "${THISDIR_ABS}"`
DONEXT=false
for X in `ls "${PARENTDIR}"`
do if ${DONEXT}
   then echo cd "${PARENTDIR}/${X}"
        exit 0
   fi
   if [ "${X}" = "${THISDIR}" ]
   then DONEXT=true
   fi
done

echo echo NO MORE
exit 1
