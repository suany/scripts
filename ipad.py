#!/usr/bin/python

from __future__ import print_function
from __future__ import with_statement

"""
TODO: width/height

from PIL import Image
im=Image.open(filepath)
im.size # (width,height) tuple

--> use pillow
--> also has exif (and iptc?) support

"""

# TODO lessons from 2013 iteration
# -- collect list: second granularity not good enough for fast shutter
# -- if no match found in dest, may be from iPhone
# TODO lessons from antarc
# -- when processing source, exclude timestamp None -- probably not images
# -- dest is .\FOO -- easy to s&r, tho

# :g/&#233;/s//\&eacute;/g
# :g/&#237;/s//\&iacute;/g

import os, re, subprocess, sys
from exif import Image
from iptcinfo3 import IPTCInfo

do_execute = True
use_exiftool = False # old exiftool version

#############################################################
# From stack overflow
import struct
import imghdr

def test_jpeg(h, f):
    # SOI APP2 + ICC_PROFILE
    if h[0:4] == '\xff\xd8\xff\xe2' and h[6:17] == b'ICC_PROFILE':
        #/**/print("A")
        return 'jpeg'
    # SOI APP14 + Adobe
    if h[0:4] == '\xff\xd8\xff\xee' and h[6:11] == b'Adobe':
        return 'jpeg'
    # SOI DQT
    if h[0:4] == '\xff\xd8\xff\xdb':
        return 'jpeg'
imghdr.tests.append(test_jpeg)

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        what = imghdr.what(None, head)
        if what == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif what == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif what == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf or ftype in (0xc4, 0xc8, 0xcc):
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

#############################################################


# TODO: batch call to exiftool!
#
# convert foo.jpg -resize 800x800 sfoo.jpg
#  - dim = upper bound
#
# 'exiftool', '-tagsFromFile', fromfile, tofile
#
# 'exiftool', '-S', '-DateTimeOriginal', filename
#  --> see if empty

def exifkeys(filename, keys):
    with open(filename, "rb") as f:
        img = Image(f)
    return tuple(getattr(img, key, None) for key in keys)

def iptckeys(filename, keys):
    info = IPTCInfo(filename)
    def infoget(info, key):
        try:
            return info[key]
        except KeyError:
            return None
    return tuple(infoget(info, key) for key in keys)

def lookup_via_exiftool(filename, keys):
    " Old: using exiftool "
    # -S = very short
    p = subprocess.Popen(['exiftool', '-S'] +
                         ['-' + k for k in keys] +
                         [filename],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         )
    (out,err) = p.communicate()
    kvdict = dict()
    for line in out.split('\n'):
        if line:
            (key,val) = line.rstrip().split(': ', 1)
            kvdict[key] = val
    return tuple(kvdict.get(key) for key in keys)

def print_dict(dict):
    for k,v in dict.iteritems():
        print("  %s -> %s" % (k,v))

sourcedict = dict()

def process_sourcefile(dirname, filename):
    global sourcedict
    filepath = os.path.join(dirname, filename)
    if use_exiftool:
        (timestamp,) = exifkeys(filepath, ['DateTimeOriginal'])
    else:
        (timestamp,) = exifkeys(filepath, ['datetime_original'])
    if sourcedict.has_key(timestamp):
        print("# Duplicate timestamp %s: %s and %s" % (
                        timestamp, sourcedict[timestamp], filename))
        sourcedict[timestamp] += '*'
        return False
    sourcedict[timestamp] = filename
    return True
    #if re.match("IMG_[0-9]{4}.JPG", filename):
    #    imgno = filename[4:-4]
    #    sourcedict[timestamp] = imgno
    #    return True
    #if re.match("P[0-9]{7}.JPG", filename):
    #    imgno = filename[4:-4]
    #    sourcedict[timestamp] = imgno + 'x'
    #    return True
    #print "# Warning: unhandled source %s, assumed iPhone" % filepath
    #sourcedict[timestamp] = 'iPhone'
    #return False

def myscrub(instr):
    if not instr:
        return ""
    def no_b_wrapper(s):
        # SY: this is a workaround for bytes/str confusion, which may or may
        #     not be due to an iptc bug?
        # Looks like somewhere we are getting a string surrounded literally by
        # "b''" or 'b""'.
        if len(s) < 3:
            return s
        elif s.startswith("b'") and s.endswith("'"):
            return s[2:-1]
        elif s.startswith('b"') and s.endswith('"'):
            return s[2:-1]
        else:
            return s
    ascstr = str(instr.decode('utf-8').encode('ascii', 'xmlcharrefreplace'))
    no_b = no_b_wrapper(ascstr)
    return no_b.replace('"', '&quot;')

def process_destfile(dirname, filename):
    filepath = os.path.join(dirname, filename)
    if use_exiftool:
        (timestamp,
         imagewidth,
         imageheight,
         objectname,
         caption,
         city,
         sublocation,
         state,
         country,
         model,
         ) = lookup_via_exiftool(
                    filepath,
                    ['DateTimeOriginal',
                     'ImageWidth',
                     'ImageHeight',
                     'ObjectName', # Pgene Title
                     'Caption-Abstract', #Pgene caption, Windows title
                     #'Category',
                     #'Keywords', #Pgene, Windows
                     'City',
                     'Sub-location',
                     'Province-State',
                     'Country-PrimaryLocationName', # Country
                     #'By-line', # Pgene Author's Name
                     'Model',
                     ])
    else:
        imagewidth, imageheight = get_image_size(filepath)
        timestamp, model = exifkeys(filepath, ['datetime_original', 'model'])
        (objectname,
         caption,
         city,
         sublocation,
         state,
         country,
         ) = iptckeys(filepath,
                      ['object name', # Pgene Title
                       'caption/abstract',
                       #'category',
                       #'keywords',
                       'city',
                       'sub-location',
                       'province/state',
                       #'country/primary location code',
                       'country/primary location name',
                       #'by-line',
                       #'by-line title',
                       ])
# exif 'Model',
    model_abbrev = 'XXX_None'
    if model == 'DMC-LX5':
        model_abbrev = 'lx5'
    elif model == 'DMC-LX7':
        model_abbrev = 'lx'
    elif model == 'Canon EOS 7D':
        model_abbrev = '7d'
    elif model == 'Canon EOS 350D DIGITAL':
        model_abbrev = 'axel'
    elif model == 'iPhone 5s':
        model_abbrev = '5s'


    sourcefile = sourcedict.get(timestamp, 'NO_SOURCE')
    #if not sourcedict.has_key(timestamp):
    #    print "# Warning: no match %s timestamp %s" % (filepath, timestamp)
    #    return
    mytitle = ""
    mycaption = ""
    if objectname:
        mytitle = objectname
    if caption:
        if mytitle:
            mycaption = caption
        else:
            mytitle = caption
    shortlist = list(filter(None,
                            [mycaption, city, sublocation, state, country]))
    scrubbed = list(map(myscrub, shortlist))
    mycaption = ", ".join(scrubbed)
    print("    ['%s', '%s', '%s', '%s', %s, %s, \"%s\", \"%s\"]," % (
               filepath,
               sourcefile,
               model_abbrev,
               timestamp,
               imagewidth,
               imageheight,
               myscrub(mytitle),
               mycaption,
               ))

def process_dir(dirname, process_file):
    for fname in os.listdir(dirname):
        fullpath = os.path.join(dirname, fname)
        if not fname.endswith(".JPG") and not fname.endswith(".jpg"):
            print("Skipping", fullpath)
            continue
        if os.path.isfile(fullpath):
            process_file(dirname, fname)
        elif os.path.isdir(fullpath):
            process_dir(fullpath, process_file)

if __name__ == "__main__":
    sources = []
    dests = []
    srcmode = False
    for arg in sys.argv[1:]:
        if arg == '-e':
            do_execute = True
            continue
        if arg == '-n':
            do_execute = False
            continue
        if arg == '-src':
            srcmode = True
            continue
        if arg == '-dst':
            srcmode = False
            continue
        if srcmode:
            sources += [arg]
        else:
            dests += [arg]
    print('thelist = [')
    for source in sources:
        if os.path.isdir(source):
            print('Source dir:', source, file=sys.stderr)
            if do_execute:
                process_dir(source, process_sourcefile)
            continue
        if os.path.isfile(source):
            print('Source file:', source, file=sys.stderr)
            if do_execute:
                process_sourcefile(os.path.dirname(source),
                                   os.path.basename(source))
            continue
        raise Exception("Unrecognized source %s" % source)
    for dest in dests:
        if os.path.isdir(dest):
            print('Dest dir:', dest, file=sys.stderr)
            if do_execute:
                process_dir(dest, process_destfile)
            continue
        if os.path.isfile(dest):
            print('Dest file:', dest, file=sys.stderr)
            if do_execute:
                process_destfile(os.path.dirname(dest),
                                 os.path.basename(dest))
            continue
        raise Exception("Unrecognized dest %s" % dest)
    print('] # end thelist')
