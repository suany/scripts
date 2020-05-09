#!/bin/sh

for SRC in "$@"
do case "$SRC" in
     *.aif) DST=`echo "$SRC" | sed -e 's/.aif$/.m4a/'` ;;
     *.aiff) DST=`echo "$SRC" | sed -e 's/.aiff$/.m4a/'` ;;
     *) echo Error: expecting aif file
        exit 1 ;;
   esac
   
#  ffmpeg -i "$SRC" -f mp3 -acodec libmp31ame -ab 192000 -ar 44100 "$DST.mp3"

#  # constant bit-rate (CBR) -- nah
#  ffmpeg -i "$SRC" -c:a aac -b:a 160k "$DST"

   # variable bit-rate (VBR) -- generally better (2=quality)
   echo ffmpeg -i "$SRC" -c:a aac -q:a 2 "$DST"
   if ! ffmpeg -i "$SRC" -c:a aac -q:a 2 "$DST"
   then echo === FAILED $?
        exit 1
   fi
done
