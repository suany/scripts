#!/bin/sh

for X in IMG_E????.HEIC
do if [ ! -e "$X" ]
   then echo "Does not exit: $X"
        break
   fi
   REN=`echo $X | sed -e s/E// -e s/\.HEIC/e.heic/`
   echo mv -i "$X" "$REN"
        mv -i "$X" "$REN"
done
for X in IMG_E????.JPG
do if [ ! -e "$X" ]
   then echo "Does not exit: $X"
        break
   fi
   REN=`echo $X | sed -e s/E// -e s/\.JPG/e.jpg/`
   echo mv -i "$X" "$REN"
        mv -i "$X" "$REN"
done
for X in IMG_E????.MOV
do if [ ! -e "$X" ]
   then echo "Does not exit: $X"
        break
   fi
   REN=`echo $X | sed -e s/E// -e s/\.MOV/e.mov/`
   echo mv -i "$X" "$REN"
        mv -i "$X" "$REN"
done
