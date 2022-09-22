#!/bin/sh

# Input: video file
# Output: text file with video name plus .txt suffix

for X in "$@"
do if [ -e "$X.txt" ]
   then echo "SKIPPING (file exists): $X.txt"
        continue
   fi
   DUR=`ffprobe.exe "$X" 2>&1 | fgrep Duration: | cut -f1 -d. | cut -f2- -d:`
   if [ -z "$DUR" ]
   then echo "SKIPPING (no duration): $X.txt"
        continue
   fi
   SIZ=`stat --printf="%s" "$X"`
   printf "%12s %15s   $X\n" "$DUR" "$SIZ" > "$X.txt"
done
