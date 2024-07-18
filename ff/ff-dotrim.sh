# SY dotrim + concat EXPERIMENT:
# end frame - start frame : concat will duplicate one frame
# end frame - start frame - 0.03 : no duplication (0.03 for 30 fps)

# DRONE 24fps -> 30fps (speed up 20%):
# ffmpeg -itsscale 0.8 -i input -c copy output

DONE () { true; }
TODO () { true; }
SKIP () { true; }

# $1 infile
# $2 outfile
# $3 start time
# $4 end time
dotrim () {
  #test -e $1
  #test ! -e $2
  DUR=`echo $4 - $3 | bc -l`
  echo ffmpeg -ss $3 -i $1 -t $DUR -c copy $2
       ffmpeg -ss $3 -i $1 -t $DUR -c copy $2
}

##################################################

set -e

