#!/usr/bin/env /python3

from __future__ import print_function
from __future__ import with_statement

import cv2 # pip3 install opencv-python
from PIL import Image # pip3 install Pillow
import pillow_heif # pip3 install pillow-heif
import os, sys

pic_stats = True
vid_stats = True

pillow_heif.register_heif_opener()

def verbose(*args, **kwargs):
    print(*args, **kwargs)

def cv2_imgdim(filename):
   img = cv2.imread(filename, 0)
   if img is None:
       return None
   hgt, wid = img.shape[:2]
   dim = f"{wid}x{hgt}"
   return dim

def pillow_imgdim(filename):
   img = Image.open(filename)
   if img is None:
       return None
   dim = f"{img.width}x{img.height}"
   return dim

# Textual summary of video dimensions
dimsum = {
  (4096, 2160): "4k",     # DCI 4k
  (3840, 2160): "4k",     # UHD 4k
  (2688, 1512): "2.7k",    # "4MP" (Mavic Air 2)
# (1920, 1440): "1440p-4:3",
  (1920, 1080): "1080p",  # "1080p" / "fhd"  ~~ TODO: use "10p" ?
  (1280, 720):  "720p",   # "720p" / "hd"   ~~ TODO: use "7p"  ?
}

# IMPORTANT: this does not check that the input is a valid video, so may return
# legit-looking values for non-video files.
def vidstats(filename):
    v = cv2.VideoCapture(filename)
    if not v.isOpened():
        print("VIDEO NOT OPENED", filename)
        return None, None

    # Duration = frame_count / fps
    # Other SO suggestions don't seem to get correct results.
    # NOTE: not fully verified that this is always accurate.
    frame_count = v.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = v.get(cv2.CAP_PROP_FPS)
    totsecs = round(frame_count / fps)
    secs = totsecs % 60
    dur = ":%02d" % secs
    totmins = int(totsecs / 60)
    if totmins:
        mins = totmins % 60
        hrs = int(totmins / 60)
        if hrs:
            dur = ("%d:%02d" % (hrs, mins)) + dur # prepend hrs:mins
        else:
            dur = str(mins) + dur # prepend mins

    # Dimensions: summarized as "1080p" etc.
    width  = round(v.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = round(v.get(cv2.CAP_PROP_FRAME_HEIGHT))
    dim = dimsum.get((width, height), None)
    if dim is None:
        dim = f"{width}x{height}"
        # TODO: iPhone live photo is 1920x1440 - skip warning
        # NOTE: live photo loop is variable
        # TODO: output '*' after unusual dimensions?
        print("WARNING: unusual video dimensions:", dim, filename)
    # Append fps if not 29 or 30 (TODO: record 24 and 25 still?)
    if round(fps) not in (29, 30):
        dim += "/{}fps".format(round(fps))

    return dim, dur

def probefile(filename):
    size = None
    dim = None
    dur = None

    # file size
    size = os.stat(filename).st_size

    # TODO: .wav, .mp3, etc.

    ext = os.path.splitext(filename)[1].lower()
    if ext in (".mp4", ".m4v", ".mov"):
        # video stats.
        # NOTE: cv2.VideoCapture can't determine file format, and will succeed
        #       even for text files, so we must filter by extension.
        if vid_stats:
            dim, dur = vidstats(filename) # May be None, None
    elif ext in (".gif", ".jpg", ".jpeg", ".png"):
        # picture stats: dimension only
        # TODO?: .cv2 = canon raw format (e.g. 2023/12-09-icb-ford/raw/)
        if pic_stats:
            dim = cv2_imgdim(filename)
    elif ext in (".heic"):
        if pic_stats:
            dim = pillow_imgdim(filename)
    elif ext in (".mp3", ".m4a", ".wav"):
        # TODO .aac also
        pass
    elif ext not in (".sh", ".txt", ".TXT"):            
        print("WARNING: skipping file", filename)

    return size, dim, dur 

def normname(dirname, filename):
    joined = os.path.join(dirname, filename)
    if os.name == 'nt':
        return joined.replace('\\', '/')
    else:
        return joined

def fmtline(size, dim, dur, filepath, file):
    mb = size / 1024 / 1024 # Size in MB
    if dim is None:
        dim = ""
    if dur is None:
        dur = ""
    print(f"{mb: 7.1f}M", # 1234.5M  
          f"{dim:12s}",  # 1080p/240fps
          f"{dur:>7s}",   # 1:23:45
          filepath, file=file)

def do_arg(arg):
    if not os.path.isdir(arg):
        print("ERROR: expecting directory:", arg)
        return False
    parts = list(filter(bool, os.path.split(arg)))
    if len(parts) != 1:
        print("ERROR: subdir not supported:", arg)
        return False
    basename = parts[0] # Note: may differ from arg in trailing /
    if basename.startswith('.'):
        print("SANITY: skipping arg starting with dot:", arg)
        return False
    txtname = basename + '.txt'
    if os.path.exists(txtname):
        # TODO: support merge?
        i = input("EXISTS (" + txtname + "): *[s]kip, [a]ppend, [q]uit? ")
        if i == 'q':
            raise # Lazy escape - FIXME?
        if i != 'a':
            return False
    num_entries = 0
    with open(txtname, 'a') as fp:
        for dirpath, dirnames, filenames in os.walk(basename):
            dirnames.sort() # does this force sorted traversal?
            for filename in sorted(filenames):
                filepath = normname(dirpath, filename)
                size, dim, dur = probefile(filepath)
                fmtline(size, dim, dur, filepath, file=fp)
                num_entries += 1
    verbose(num_entries, txtname)
    return True

usage = """
USAGE: pix-summarize [-p] dir1 dir2/ ...

Writes output to dir1.txt, dir2.txt ...

Arguments may include trailing slash,
but cannot be a nested directory (e.g., dir1/dir2),
as it's unclear where the output should go.

Option -p skips pic status, useful for just "ls" sizing.
"""

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == '-p':
        print("-p: disabling pic status")
        pic_stats = False
        args = args[1:]
    if not args:
        print(usage)
        sys.exit(1)
    num_ok = 0
    num_fail = 0
    for arg in args:
        if do_arg(arg):
            num_ok += 1
        else:
            num_fail += 1
    print("Success:", num_ok)
    if num_fail:
        print("FAILED:", num_fail)
    sys.exit(num_fail)

