#!/bin/sh

# This script probes THEFILE every PERIOD seconds to see if it has changed.
# If it hasn't, a snapshot of THEFILE is stashed away, and information is
# logged and echoed.

# The file to probe: $1
if [ "$1" -a -e "$1" ]
then THEFILE="$1"
else echo "Usage: $0 <filename>"
     exit 1
fi

# Probe frequency, in seconds
PERIOD=600

# This is the output log of this probe
PROBE_OUTLOG=probe.log

# This defines additional actions to perform each time a delay is detected.
addl_action () {
  grep '^:' memusage.log | tail -10 >> $PROBE_OUTLOG
}

#####################################################

echo Probing "$THEFILE" every "$PERIOD" seconds.

#####################################################

LASTFILE="${THEFILE}.last"
LASTTIME=`date`

while sleep $PERIOD
do if [ -e "$LASTFILE" ]
   then if cmp "$THEFILE" "$LASTFILE" > /dev/null
        then NOW=`date +%s`
             TIMESTAMP=`date -r "${THEFILE}" +%s`
             ELAPSED=`expr \( ${NOW} - ${TIMESTAMP} \) / 60`
             echo Silent for $ELAPSED min
             echo Silent for $ELAPSED min: `date` >> $PROBE_OUTLOG
             addl_action
             cp -p "$THEFILE" "${THEFILE}-`date +%F-%H.%M.%S`"
        fi
   fi
   cp -p "$THEFILE" "$LASTFILE"
done
