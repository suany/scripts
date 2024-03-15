#!/bin/sh

# SY NOTE: suffix case matters, I think, sort of...
#  - input mp4 output mp4 --> re-encode!
#  - input mp4 output mp4 --> copy frames only (faster)!
#  -> *HOWEVER*, output are identical

# DRONE 24fps -> 30fps (speed up 20%):
# ffmpeg -itsscale 0.8 -i input -c copy output

# Crop from 4096 x 2160 (5D4)
# -filter:v "crop=1920:1080:1088:540"
#       max "crop=1920:1080:2174:1080"
# -filter:v "crop=1280:720:1408:720"
#       max "crop=1280:720:2816:1440"
# -vb 14M
# -pix_fmt yuv420p
# # Quality; used to do 24M, looks like 14M good enough?
# # yuv: IMPORTANT for emulsio/mplayer (eos default 422) - 4k only
#
# -vf scale=1920:1080
#
# 4k->1080p:
# -filter:v "scale=2048:1080,crop=1920:1080:64:0"
#
# -r 29.97
#
# Fns: if(lt(n\,10)\,100\,100+n*.1) <-- must escape commas for -filter:v
#
# Online TL;DR:
#   When sampling down: Use Lanczos or Spline filtering.
#   When sampling up: Use Bicubic or Lanczos filtering.
# -sws_flags lanczos (default =  bicubic)
# -vf scale=1920x1080:flags=lanczos
#
# *FIXME*: output y is 1072 instead of 1080, even for crop! Dunno why!

# JPG/jpg capture: -q:v 2 (quality, 2 best, 2-5 recommended)
# ffmpeg -ss <> -i input.mp4 -t <> -q:v 2 "out-%03d.jpg"

# REVERSE video
# Input:      181M
# Output 14M:  78M
# Output 20M: 110M
# Output 24M: 131M
reverse () {
  ffmpeg -i $1 -vf reverse -vb 24M $2
}

# Scaling from 4096:2160 and cropping to 1920:1080-- smallest decimal delta
#
#           scale       center     bot-right  tot error x&y
#  50.00% - 4096:2160   1088:540   2176:1080  err 0.0
#  52.50% - 3901:2057   991:489    1981:977   err 0.2
#  53.60% - 3821:2015   951:468    1901:935   err 0.2
#  54.60% - 3751:1978   916:449    1831:898   err 0.1
#  55.50% - 3690:1946   885:433    1770:866   err 0.1
#  56.70% - 3612:1905   846:413    1692:825   err 0.2
#  58.00% - 3531:1862   806:391    1611:782   err 0.1
#  60.20% - 3402:1794   741:357    1482:714   err 0.0
#  61.50% - 3330:1756   705:338    1410:676   err 0.2
#  62.90% - 3256:1717   668:319    1336:637   err 0.0
#  63.90% - 3205:1690   643:305    1285:610   err 0.1
#  64.40% - 3180:1677   630:299    1260:597   err 0.1
#  65.10% - 3146:1659   613:290    1226:579   err 0.1
#  66.30% - 3089:1629   585:275    1169:549   err 0.1
#  67.50% - 3034:1600   557:260    1114:520   err 0.1
#  68.70% - 2981:1572   531:246    1061:492   err 0.1
#  69.90% - 2930:1545   505:233    1010:465   err 0.2
#  70.50% - 2905:1532   493:226    985:452    err 0.1
#  71.43% - 2867:1512   474:216    947:432    err 0.2
#  72.73% - 2816:1485   448:203    896:405    err 0.2
#  74.23% - 2759:1455   420:188    839:375    err 0.1
#  75.10% - 2727:1438   404:179    807:358    err 0.1
#  76.70% - 2670:1408   375:164    750:328    err 0.2
#  77.60% - 2639:1392   360:156    719:312    err 0.4
#  78.95% - 2594:1368   337:144    674:288    err 0.1
#  80.60% - 2541:1340   311:130    621:260    err 0.1
#  81.50% - 2513:1325   297:123    593:245    err 0.3
#  82.95% - 2469:1302   275:111    549:222    err 0.1
#  83.90% - 2441:1287   261:104    521:207    err 0.2
#  85.30% - 2401:1266   241:93     481:186    err 0.2
#  86.20% - 2376:1253   228:87     456:173    err 0.2
#  87.30% - 2346:1237   213:79     426:157    err 0.2
#  88.74% - 2308:1217   194:69     388:137    err 0.2
#  89.70% - 2283:1204   182:62     363:124    err 0.2
#  90.90% - 2253:1188   167:54     333:108    err 0.1
#  92.30% - 2219:1170   150:45     299:90     err 0.2
#  93.90% - 2181:1150   131:35     261:70     err 0.2
#  94.90% - 2158:1138   119:29     238:58     err 0.1
#  96.10% - 2131:1124   106:22     211:44     err 0.3
#  97.20% - 2107:1111   94:16      187:31     err 0.1


# TRIM BUT KEEP AUDIO IN SYNC:
#  ffmpeg -ss keyframe -i input [-t duration] -c copy output
# (with -i input -ss keyframe, audio still out of sync, somehow;
#  guessing that -ss first forces that start, -i first will start at
#  next video keyframe and next audio keyframe, which don't line up)

# (ss before i to go to start at next keyframe)
#ffmpeg -ss HH:MM:SS.000 -i in.mp4 [-t HH:MM:SS.000] -c copy out.mp4

# Slow motion (from grouse)
# TODO: must figure out how to stretch audio to match
# ffmpeg -ss 11 -i 4329-good.mov -t 17 -c copy -an tmp4329-noaudio.mov
# (Note: audio is not stretched here)
# ffmpeg -r 15 -i tmp4329-noaudio.mov -filter:v "crop=1280:720:320:180" \
#      -vb 24M 4329slow15-grouse.mov
#
# Slow motion (from hairy woodpecker)
# -r 15: 15 fps (~= 59fps/4)
# - video 4x slower
# - audio .25 speed; atempo only supports 0.5, so thread it
# --> output audio is very strange
#ffmpeg -i tmp-8100.mov -r 15 \
#  -filter_complex \
#  "[0:v]setpts=4.0*PTS[v];[0:a]atempo=0.5,atempo=0.5[a]" \
#  -map "[v]" -map "[a]" slo8100.mov

# Change fps without slomo
# -filter:v fps=fps=30 -vb 24M

####################################################

# $1 = number part
# $2 = descr part
# input filename = clip$1$2.mov
# output filename = ${1}s$2.mov
slomo () {
ffmpeg -i clip$1$2.mov \
   -r 15 \
   -filter_complex "[0:v]setpts=4.0*PTS[v];[0:a]atempo=0.5,atempo=0.5[a]" \
   -map "[v]" -map "[a]" \
   ${1}s$2-waudio.mov
ffmpeg -i ${1}s$2-waudio.mov -c copy -an ${1}s$2.mov
ffmpeg -i clip$1$2.mov -vn -acodec copy clip$1$2.wav
}

# XXX from 5d4 4k video, .wav not accepted by audacity.
# XXX but can open mov directly in audacity.
# $1 base
audio_extract () {
ffmpeg -i $1.mov -vn -acodec copy $1.wav
}

# After audacity
audio_merge () {
ffmpeg -i $1.mov -i $1.wav \
  -c copy -map 0:v:0 -map 1:a:0 \
  $1-saudio.mov
}

# $1 = output
# $2* = inputs
concat () {
  catlist=catlist-$$.txt
  outfile=$1
  shift
  while [ -n "$1" ]
  do echo "file '$1'" >> "$catlist"
     shift
  done
  ffmpeg -f concat -i $catlist -codec copy "$outfile"
  rm -f "$catlist"
}

set -ex

################
# MOVING CROP
################

# done
remove_audio () {
ffmpeg -i xzzz.mp4 -c copy -an czzz.mp4
}

# simple crops (SoloShot)
# -filter:v "crop=1280:720:320:180"
#       max "crop=1280:720:640:360"
# -vb 24M   # to improve quality == bitrate (iphone seems to use 14M)
# (-pix_fmt yuv420p - IMPORTANT for emulsio/mplayer from eos, todo soloshot?)
# -r 29.97  # downsample soloshot for facebook
# note: SoloShot is 59.94; -> 29.97 looks good
#                          -> 24 looks jumpy
simple_crops () {
ffmpeg -i zzz.mp4 -filter:v "crop=1280:720:320:180" \
       -vb 24M -r 29.97 czzz.mp4
}

cat > /dev/null <<XXXXXXXXXXXX_NOT_DONE

NOTES

XXXXXXXXXXXX_NOT_DONE

##################
# STEP 1

# SY NOTE: duration should be up to pts for frame before keyframe.
# [A to B-1][B to C-1], ...
# Previously, doing [A to B][B to C] caused flicker at boundary (double frame).
# Note: one SO answer used dts; pts seems to work well enough.  What's the
# difference?
# Note 2: using B-1's pts _may_ be causing some dropped time? hard to tell...
# TODO: awk into more readable form?
dump_keyframes () {
  ffprobe -select_streams v \
          -show_frames \
          -show_entries frame=pkt_pts_time,key_frame \
          $1 | fgrep -B 3 -A 1 key_frame=1 > $1.keyframes.txt
}

todo_dump_keyframes () {
dump_keyframes 02-clewstart.mp4
}

##################
# STEP 2

to_hms () { # Not necessary
  echo | python <<EOF
s = $1 % 60
tm = $1 / 60
m = tm % 60
h = tm / 60
print "%02d:%02d:%02d" % (h,m,s)
EOF
}

dotrim_hms () { # Not necessary
  dur=`echo $2 - $1 | bc -l`
  ss=`to_hms $1`
  t=`to_hms $dur`
  ffmpeg -ss $ss -i $INFILE -t $t -c copy $3
}

dotrim () { # Note: >60s ok
  dur=`echo $2 - $1 | bc -l`
  ffmpeg -ss $1 -i $INFILE -t $dur -c copy $3
}

dotrim_end () {
  ffmpeg -ss 00:00:$1 -i $INFILE -c copy $2
}

todo_zzz_trim () {
INFILE=zzz.mp4
dotrim  0.000000  6.246000 seg-zzz-1.mp4

dotrim  0.000000 29.769500 audio-zzz.mp4
}


##################
# STEP 3 -- easiest if stdout piped to file
# SY NOTE: this works well on meacham:
# ffprobe version N-83975-g6c4665d Copyright (c) 2007-2017 the FFmpeg developers
# SY NOTE: the numbers differ on my laptop:
# (TODO: what version?)
count_frames () {
  # -v error: hides version output
  # -count_frames
  # -select_streams - video stream only
  # -show_entries - show only # read frames
  # -of - output format
  ffprobe -v error -count_frames -select_streams v:0 \
          -show_entries stream=nb_read_frames \
          -of default=nokey=1:noprint_wrappers=1 \
          $1
  echo $1
  echo $1 | sed -e 's/seg/crop/'
}

set -ex

todo_count () {
count_frames seg-zzz-1.mp4
count_frames seg-zzz-2.mp4
}
#todo_count > counts.txt

##################
# STEP 5

# from 1920x1080
# centered: ffmpeg -i in.mov -filter:v "crop=1280:720:320:180" \
#                  -vb 24M -r 29.97 out.mov

todo_zzz_crop () {
# n=120
ffmpeg -i seg-zzz-1.mp4 -filter:v "crop=1280:720:320:180" \
       -vb 24M -r 29.97 crop-zzz-1.mp4
}


##################
# STEP 6

done_zzz_cat () {
cat > catlist.txt <<EOF
file 'crop-zzz-1.mp4'
file 'crop-zzz-2.mp4'
EOF
ffmpeg -f concat -i catlist.txt -codec copy xzzz.mp4
}


##################
# STEP 7: resync audio (if desired)

# $1 input video
# $2 input audio
# $3 output
resync_audio () {
  ffmpeg -i $1 -i $2 -c copy -map 0:v:0 -map 1:a:0 $3
}

todo_resync_audio () {
resync_audio xzzz.mp4 audio-zzz.mp4 czzz.mp4
}

##################
