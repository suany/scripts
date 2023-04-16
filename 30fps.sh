#!/bin/sh

for X in "$@"
do set -ex
   ffmpeg -itsscale 0.8 -i "$X" -c copy "tmp30fps-$X"
done
