#!/bin/sh

for X in "$@"
do DUR=`ffprobe.exe "$X" 2>&1 | fgrep Duration: | cut -f1 -d. | cut -f2- -d:`
   SIZ=`stat --printf="%s" "$X"`
   printf "%12s %15s   $X\n" "$DUR" "$SIZ"
done
