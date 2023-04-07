import cv2, os, sys

# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
#
# This version uses OpenCV, which is apparently a lousy tool
# for re-encoding, as it layers poorly on top of ffmpeg.
# In particular, you can't control the output bitrate (aka quality).
#
# See instead PyAV, which is described as decent Pythonic bindings
# for ffmpeg.  Note that there are many lousy Python ffmpeg wrappers
# to avoid.
#
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

WIDTH = 384
HEIGHT = 288
BADCOL = 163

# Produced by passing fourcc=-1 to VideoWriter constructor
SUPPORTED_FOURCC_TAGS = """
fourcc tag 0x7634706d/'mp4v' codec_id 000C
fourcc tag 0x31637661/'avc1' codec_id 001B
fourcc tag 0x33637661/'avc3' codec_id 001B
fourcc tag 0x31766568/'hev1' codec_id 00AD
fourcc tag 0x31637668/'hvc1' codec_id 00AD
fourcc tag 0x7634706d/'mp4v' codec_id 0002
fourcc tag 0x7634706d/'mp4v' codec_id 0001
fourcc tag 0x7634706d/'mp4v' codec_id 0007
fourcc tag 0x7634706d/'mp4v' codec_id 003D
fourcc tag 0x7634706d/'mp4v' codec_id 0058
fourcc tag 0x312d6376/'vc-1' codec_id 0046
fourcc tag 0x63617264/'drac' codec_id 0074
fourcc tag 0x7634706d/'mp4v' codec_id 00A3
fourcc tag 0x39307076/'vp09' codec_id 00A7
fourcc tag 0x31307661/'av01' codec_id 801D
fourcc tag 0x6134706d/'mp4a' codec_id 15002
fourcc tag 0x63616c61/'alac' codec_id 15010
fourcc tag 0x6134706d/'mp4a' codec_id 1502D
fourcc tag 0x6134706d/'mp4a' codec_id 15001
fourcc tag 0x6134706d/'mp4a' codec_id 15000
fourcc tag 0x332d6361/'ac-3' codec_id 15003
fourcc tag 0x332d6365/'ec-3' codec_id 15028
fourcc tag 0x6134706d/'mp4a' codec_id 15004
fourcc tag 0x61706c6d/'mlpa' codec_id 1502C
fourcc tag 0x43614c66/'fLaC' codec_id 1500C
fourcc tag 0x7375704f/'Opus' codec_id 1503C
fourcc tag 0x6134706d/'mp4a' codec_id 15005
fourcc tag 0x6134706d/'mp4a' codec_id 15018
fourcc tag 0x6134706d/'mp4a' codec_id 15803
fourcc tag 0x7334706d/'mp4s' codec_id 17000
fourcc tag 0x67337874/'tx3g' codec_id 17005
fourcc tag 0x646d7067/'gpmd' codec_id 18807
fourcc tag 0x316d686d/'mhm1' codec_id 15817
"""

# mpeg-4 codec = lower q (smaller file)
#FOURCC, OUTEXT = ('mp4v','mp4')

# avc1 = avc3 = h264
# - needs openh264-1.8.0-win64.dll; downloaded and placed alongside.
# - NOTE: output bitrate is 1375, vs 3240 for input
# - NOTE: with missing dll, output was "mp42" with bitrate 2777
FOURCC, OUTEXT = ('avc1','mp4')

def image_edit_frame(frame):
    for y in range(0, HEIGHT-1):
        frame[y, BADCOL] = frame[y+1, BADCOL]
    return frame

def video_incap_to_outfile(in_vcap, outfile):
    # Output specs
    fourcc = cv2.VideoWriter_fourcc(*FOURCC)
    fps = 25
 
    if not in_vcap.isOpened():
        print("ERROR: input video capture not opened")
        return False
    # First frame: handle specially
    ret, frame = in_vcap.read()
    if not ret:
        print("ERROR: input video capture read failed")
        return False
    if frame.shape != (HEIGHT, WIDTH, 3):
        print("ERROR: input video shape not supported", frame.shape)
        return False

    outvid = cv2.VideoWriter(outfile, fourcc, fps, (WIDTH, HEIGHT))
    # XXX: trying to change bitrate - DOES NOT WORK
    #outvid.set(cv2.VIDEOWRITER_PROP_QUALITY, 80)
    frameno = 0
    while in_vcap.isOpened():
        ret, frame = in_vcap.read()
        if not ret:
            break
        frameno += 1
        frame = image_edit_frame(frame)
        outvid.write(frame)
    print("Frames processed:", frameno, "seconds:" + str(frameno/fps))
    outvid.release()
    return True

def video_edit_frames(infile, outfile):
    in_vcap = cv2.VideoCapture(infile)
    video_incap_to_outfile(in_vcap, outfile)
    in_vcap.release()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        infile = sys.argv[1]
        outfile = sys.argv[2]
    elif len(sys.argv) == 2:
        infile = sys.argv[1]
        base, ext = os.path.splitext(infile)
        outfile = base + "-adj-" + FOURCC + "." + OUTEXT
    else:
        print("USAGE: thermapp-video-adjust infile outfile")
        sys.exit(1)
    if not os.path.exists(infile):
        print("ERROR: infile does not exist:", infile)
        sys.exit(1)
    if os.path.exists(outfile):
        print("WARNING: outfile exists:", outfile)
        if not input("Overwrite? [y/N]") in ('y', 'Y'):
            sys.exit(1)
    video_edit_frames(infile, outfile)
