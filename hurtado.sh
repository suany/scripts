#!/bin/sh

# Recommended on Linux only.
# Requires avconv or ffmpeg.
#

#BASE=http://people.mbi.ohio-state.edu/hurtado.10/US_Composite_Radar
BASE=http://www.pauljhurtado.com/US_Composite_Radar/

DATE=`date --date=yesterday +%Y-%-m-%-d`
START=
START=uscomp37.gif
END=uscomp115.gif

FILENAMES_FILE=${BASE}/filenames.txt
THRU_7ET="\
	uscomp1.gif \
	uscomp4.gif \
	uscomp7.gif \
	uscomp10.gif \
	uscomp13.gif \
	uscomp16.gif \
	uscomp19.gif \
	uscomp22.gif \
	uscomp25.gif \
	uscomp28.gif \
	"
CORE_NIGHT="\
	uscomp31.gif \
	uscomp34.gif \
	uscomp37.gif \
	uscomp40.gif \
	uscomp43.gif \
	uscomp46.gif \
	uscomp49.gif \
	uscomp52.gif \
	uscomp55.gif \
	uscomp58.gif \
	uscomp61.gif \
	uscomp64.gif \
	uscomp67.gif \
	uscomp70.gif \
	uscomp73.gif \
	uscomp76.gif \
	uscomp79.gif \
	uscomp82.gif \
	uscomp85.gif \
	uscomp88.gif \
	uscomp91.gif \
	uscomp94.gif \
	uscomp97.gif \
	uscomp100.gif \
	uscomp103.gif \
	uscomp106.gif \
	uscomp109.gif \
	uscomp112.gif \
	uscomp115.gif \
	"
PAST_6PT="\
	uscomp118.gif \
	uscomp121.gif \
	uscomp124.gif \
	uscomp127.gif \
	uscomp130.gif \
	uscomp133.gif \
	uscomp136.gif \
	uscomp139.gif \
	uscomp142.gif \
	"

#FILENAMES="${THRU_7ET} ${CORE_NIGHT} ${PAST_6PT}"
FILENAMES="${CORE_NIGHT}"


do_clean () {
  rm -f *.gif
}

do_download () {

  URLS=
  for FILE in ${FILENAMES}
  do if [ -e ${FILE} ]
     then echo "WARNING: ${FILE} exists, skipping..."
          continue
     fi
     URL=${BASE}/${DATE}/$FILE
     URLS="${URLS} ${URL}"
  done

  if [ -n "${URLS}" ]
  then wget --no-verbose ${URLS}
  fi
}

do_link () {
  I=0
  for FILE in ${FILENAMES}
  do if [ -n "${START}" ]
     then if [ "${START}" != "${FILE}" ]
          then continue
          else START=
          fi
     fi
     ln -s ${FILE} img${I}.gif
     I=`expr $I + 1`
     #ln -s ${FILE} img${I}.gif
     #I=`expr $I + 1`
     #ln -s ${FILE} img${I}.gif
     #I=`expr $I + 1`
     #ln -s ${FILE} img${I}.gif
     #I=`expr $I + 1`
  done
}

# avconv -codecs

#   Audio codec : aac
#   Audio bitrate : 128kb/s
#   Video codec : mpeg4
#   Video bitrate : 1200kb/s
#   Video size : 320px par 180px

#  input
#  -acodec aac
#  -ab 128kb
#  -vcodec mpeg4
#  -b 1200kb
#  -mbd 2
#  -flags +4mv+trell
#  -aic 2
#  -cmp 2
#  -subcmp 2
#  -s 320x180
#  -title X

# iPad: H.264 up to 1080p 30fps
# m4v, mp4, mov
#
#  -vcodec libx264
#  -vcodec h264
#

do_mpeg4 () {

  # TODO: -r 4 -- 4 frames per second, doesn't work
  avconv -f image2 -i "img%d.gif" -vcodec mpeg4 ${DATE}.mp4
}

do_gif () {

# NOTE: can do gif with this, but output is unnecessarily enormous!
#
#  avconv -f image2 -i "img%d.gif" -pix_fmt rgb24 ${DATE}.gif
#

#  -delay in milliseconds
#

  echo "convert -delay 50 ${FILENAMES} -loop 1 ${DATE}.gif"
        convert -delay 50 ${FILENAMES} -loop 1 ${DATE}.gif
}

echo DATE = ${DATE}
echo START = ${START}
echo steps: dl=download ln=link mp4=mpeg4 gif=animated gif

while [ -n "$1" ]
do case "$1" in
      clean) do_clean ;;
      dl) do_download ;;
      ln) do_link ;; # for mpeg4 -- screw this
      mp4) do_mpeg4 ;;
      gif) do_gif ;;
      ????-*-*) DATE="$1"
                echo DATE = ${DATE}
                ;;
   esac
   shift
done

