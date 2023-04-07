import cv2, os, sys

WIDTH = 384
HEIGHT = 288
BADCOL = 163

#FOURCC, OUTEXT = ('mp4v','mp4') # mpeg-4 codec = lower q (smaller file)
FOURCC, OUTEXT = ('avc1','mp4') # h264 = better q (larger file also)

def image_edit_frame(frame):
    for y in range(0, HEIGHT-1):
        frame[y, BADCOL] = frame[y+1, BADCOL]
    return frame

def video_incap_to_outfile(in_vcap, outfile):
    # Output specs
    # TODO: better codec?
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
        outfile = base + "-adj." + OUTEXT
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
