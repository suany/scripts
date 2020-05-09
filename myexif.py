#!/usr/bin/python

import os, re, subprocess, sys

do_execute = True

# TODO: batch call to exiftool!
#
# 'exiftool', '-tagsFromFile', fromfile, tofile
#
# 'exiftool', '-S', '-DateTimeOriginal', filename
#  --> see if empty

def has_exif(filename):
    p = subprocess.Popen(['exiftool', '-S', '-DateTimeOriginal', filename],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         )
    (out,err) = p.communicate()
    return bool(out)

sources = {}
dests = {}

def print_dict(dict):
    for k,v in dict.iteritems():
        print "  %s -> %s" % (k,v)

def add_source(imgno, filename):
    if has_exif(filename):
        global sources
        if imgno in sources:
            raise Exception("Duplicate entry for %s: %s and %s" % (
                            imgno, sources[imgno], filename))
        sources.update({ imgno : filename })
    else:
        print "Warning: No EXIF in %s" % filename

def add_dest(imgno, filename):
    if not has_exif(filename):
        global dests
        val = dests.get(imgno, [])
        val += [filename]
        dests.update({ imgno : val })
    else:
        print "Warning: EXIF already present in %s" % filename

def process_file(dirname, filename):
    if re.match("IMG_[0-9]{4}.JPG", filename):
        imgno = filename[4:-4]
        add_source(imgno, os.path.join(dirname, filename))
        return True
    if re.match("P[0-9]{7}.JPG", filename):
        imgno = filename[4:-4]
        add_source(imgno, os.path.join(dirname, filename))
        return True
    m = re.search("([0-9]{4}).*jpg", filename)
    if m:
        imgno = m.group(0)
        add_dest(imgno, os.path.join(dirname, filename))
        return True
    return False

def process_dir(dirname):
    for fname in os.listdir(dirname):
        if os.path.isfile(os.path.join(dirname, fname)):
            process_file(dirname, fname)

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg == '-e':
            do_execute = True
            continue
        if arg == '-n':
            do_execute = False
            continue
        if os.path.isdir(arg):
            process_dir(arg)
            continue
        if os.path.isfile(arg):
            if not process_file(os.path.dirname(arg), os.path.basename(arg)):
                raise Exception("Unrecognized file argumnt %s" % arg)
            continue
        raise Exception("Unrecognized argument %s" % arg)
    print "Sources:"
    print_dict(sources)
    print "Dests:"
    print_dict(dests)

