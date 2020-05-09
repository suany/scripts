#!/usr/bin/python

# :g/&#233;/s//\&eacute;/g
# :g/&#237;/s//\&iacute;/g

import os, re, subprocess, sys

do_execute = True
verbose = True
start_index = 0

# TODO: batch call to exiftool!
#
# convert foo.jpg -resize 800x800 sfoo.jpg
#  - dim = upper bound
#
# 'exiftool', '-tagsFromFile', fromfile, tofile
#
# 'exiftool', '-S', '-DateTimeOriginal', filename
#  --> see if empty

def exif(filename, keys):
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
        print "  %s -> %s" % (k,v)

def print_bydate(thelist):
    bydate = dict()
    index = start_index
    for (timestamp, descr) in thelist:
        index += 10
        try:
            mmdd = timestamp[5:10].replace(':','-')
        except:
            mmdd = 'NODATE'
        bydate.setdefault(mmdd, list())
        bydate[mmdd] += [str(index)]
    aslist = list(bydate.iteritems())
    aslist.sort(key = (lambda l:l[0]))
    for (mmdd, entries) in aslist:
        print '  "%s" => new si(' % mmdd
        print '    "%s", "", array(' % mmdd
        start = 0
        num_entries = len(entries)
        while start < num_entries:
            end = start + 10
            if end < num_entries:
                chunk = entries[start:end]
            else:
                chunk = entries[start:]
            print '        ' + ', '.join(chunk) + ','
            start = end
        print '    )),'

def print_thelist(thelist):
    index = start_index
    for (timestamp, descr) in thelist:
        index += 10
        print "%7d => %s" % (index, descr)

thelist = []

def myscrub(string):
    if not string:
        return ""
    return string.replace('"', '&quot;'
                         ).decode('utf-8'
                         ).encode('ascii', 'xmlcharrefreplace')

def process_sourcefile(dirname, filename):

    global thelist

    if len(thelist) % 10 == 0:
        print >> sys.stderr, ' ', len(thelist),
        if len(thelist) % 100 == 0:
            print >> sys.stderr
        sys.stderr.flush()

    filepath = os.path.join(dirname, filename)
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
     ) = exif(filepath, ['DateTimeOriginal',
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
    model_abbrev = 'XXX_None'
    if model == 'DMC-LX7':
        model_abbrev = 'lx'
    elif model == 'Canon EOS 7D':
        model_abbrev = '7d'
    elif model == 'Canon EOS 350D DIGITAL':
        model_abbrev = 'axel'
    elif model == 'iPhone 5s':
        model_abbrev = '5s'

    mytitle = ""
    mycaption = ""
    if objectname:
        mytitle = objectname
    if caption:
        if mytitle:
            mycaption = caption
        else:
            mytitle = caption
    mycaption = ", ".join(
                     filter(None,
                            [mycaption, sublocation, city, state, country]))

    if model_abbrev == 'axel':
        if mycaption:
            mycaption += "<br/>"
        mycaption += "<i>(photo by Axel Schult)</i>"

    thelist += [(timestamp,
                 'new ii("%s", %s, %s, "%s", "%s", "%s"),' % (
                     filepath.replace('\\','/'),
                     imagewidth, imageheight,
                     myscrub(mytitle), myscrub(mycaption), model_abbrev,
                     ))]

def process_dir(dirname, process_file):
    for fname in os.listdir(dirname):
        if fname == '.svn' or fname == '.git':
            continue
        fullpath = os.path.join(dirname, fname)
        if os.path.isfile(fullpath):
            process_file(dirname, fname)
        elif os.path.isdir(fullpath):
            process_dir(fullpath, process_file)

if __name__ == "__main__":
    sources = []
    for arg in sys.argv[1:]:
        if arg.startswith('s='):
            start_index = int(arg[2:])
            continue
        if arg == '-e':
            do_execute = True
            continue
        if arg == '-n':
            do_execute = False
            continue
        if arg == '-q':
            verbose = False
            continue
        if arg == '-v':
            verbose = True
            continue
        sources += [arg]

    print >> sys.stderr, 'Start index = ' + str(start_index)

    for source in sources:
        if os.path.isdir(source):
            print >> sys.stderr, 'Source dir: ' + source
            sys.stderr.flush()
            if do_execute:
                process_dir(source, process_sourcefile)
            continue
        if os.path.isfile(source):
            print >> sys.stderr, 'Source file: ' + source
            sys.stderr.flush()
            if do_execute:
                process_sourcefile(os.path.dirname(source),
                                   os.path.basename(source))
            continue
        raise Exception("Unrecognized source %s" % source)

    thelist.sort(key = (lambda l:l[0]))

    print_bydate(thelist)

    print_thelist(thelist)
