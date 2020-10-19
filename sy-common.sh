#!/bin/sh

# Use this to get a log file name with a four-digit sequence number.
# Usage: filename=`addnum /path/to/prefix. .opt_suffix`
# $1=prefix
# $2=optional suffix
addnum () {
  local last=`ls "$1"[0-9][0-9][0-9][0-9]"$2" 2> /dev/null | tail -1`
  local outfile=
  if [ -z "$last" ]
  then outfile="$1"0001"$2"
  else # NOTE: # and % are bashisms?
       local num=${last#$1}
       num=${num%$2}
       num=`expr ${num} + 1`
       num=`printf %04d ${num}`
       outfile="$1$num$2"
  fi
  if [ -e "$outfile" ]
  then echo "ERROR: exists: $outfile" >&2
       exit 1
  fi
  echo "$outfile"
}

echoargs () {
  for X in "$@"
  do if echo "$X" | grep -e '[^-_/.[:alnum:]]' > /dev/null
     then echo -n " "\""$X"\"
     else echo -n " $X"
     fi
  done
  echo " "
}

# Client can update these (e.g., with options -n, -e)
SY_DO_EXECUTE=true
SY_ECHORUN_FATAL=false

echorun () {
  echoargs "$@"
  if $SY_DO_EXECUTE
  then "$@"
       RV=$?
       if [ $RV != 0 ]
       then echo "===returned $RV"
            if $SY_ECHORUN_FATAL
            then exit $RV
            else return $RV
            fi
       fi
  fi
}

orfail () {
  if ! "$@"
  then echo "***fail $?***"
       echoargs "$@"
       exit 1
  fi
}

# History: used to loop over list and move to bak-<date> (see sy-myriad).
# $1=prefix
# $2=optional suffix
mvbak_datesuf () {
  if [ -z "$1$2" ]
  then echo "ERROR (mvbak_datesuf): empty filename" >&2
       exit 1
  fi
  if [ ! -e "$1$2" ]
  then return # Nothing to back up
  fi
  fdate=`date -r "$1$2" +%F`
  for suf in "" -a -b -c -d -e -f -g -h -i -j \
                -k -l -m -n -o -p -q -r -s -t \
                -u -v -w -x -y -z
  do bakfile="$1-${fdate}${suf}$2"
     if [ ! -e "$bakfile" ]
     then orfail echorun mv "$1$2" "$bakfile"
          return
     fi
  done
  echo "*** Suffix overflow backing up $1$2"
  exit 1
}

# Call this before copying $1 to $2, to check whether we might clobber
# a file.
check_before_copy () {
  SRC="$1"
  DST="$2"
  if [ -d "$DST" ]
  then SRCBASE=`basename "$1"`
       DST="$DST/$SRCBASE"
  fi
  if [ ! -e "$DST" ]
  then return 0  # no dst: ok (destdir existence is responsibility of caller)
  fi
  if [ ! -e "$SRC" ]
  then echo "FATAL: check_before_copy no SRC=$SRC"
       return 1  # or allow this? (since it won't actually clobber)
  fi
  # Return whether src/dst are identical
  cmp "$SRC" "$DST" > /dev/null 2>&1
}
