ffmpeg -i 7c-vira-chase.mp4 -af volumedetect -f null /dev/null
#--> max 8.9dB

ffmpeg -i 7c-vira-chase.mp4 -af volume=9dB -c:v copy -c:a aac \
         -strict experimental -b:a 192k 7n-vira-chase.mp4


# $1 = input
# $2 = output
scale_recode () {
  FFMPEG=/home/suan/bin/ffmpeg.exe
  $FFMPEG -i "$1" -vf "scale=768x576" \
          -vcodec libx264 -preset slow -tune film -crf 18 -acodec copy $2
}
