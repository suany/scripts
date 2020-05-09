import re

def myscrub(s):
    s = re.sub('&([AEIOUaeiou])(acute|grave|circ);', '\\1', s)
    s = s.replace('&ntilde;', 'n'
        ).replace('&amp;', '_'
        ).replace('&quot;', ''
        ).replace('&#250;', 'u' # &uacute;
        ).replace('&#233;', 'e' # &eacute;
        ).replace('&#237;', 'i' # &iacute;
        )
    if s.find('&') != -1:
        raise Exception("Unprocessed & in %s" % s)
    s = '_'.join([''.join(filter(str.isalnum, list(token)))
                  for token in s.split()])
    return s

def list2dict(thelist):
    thedict = dict()
    for record in thelist:
        timestamp = record[3]
        if not re.match(
             '201[0-9]:[01][0-9]:[0123][0-9] [012][0-9]:[0-9][0-9]:[0-9][0-9]',
             timestamp):
            raise Exception("Funny timestamp: %s" % timestamp)
        ymd = timestamp[:10]
        thedict.setdefault(ymd, []).append(record)
    return thedict

def sortrec(lhs, rhs):
    return cmp(lhs[3], rhs[3])

def do_process(thedict):
  for ymd,records in thedict.iteritems():
    records.sort(sortrec)
    ndigits = len(str(len(records)))
    index = 0
    for record in records:
        index += 1
        name = record[0]
        source = record[1] # filename or NO_SOURCE
        camera = record[2] # lx,7d,5s,XXX_None
        timestamp = record[3]
        width = record[4]
        height = record[5]
        title = record[6]
        caption = record[7]

        (dim1,dim2) = (width,height) if width > height else (height,width)
        if dim1 <= 950:
            sz = 's'
        elif dim1 < 1500:
            sz = 'c'
        elif dim1 < 2000:
            sz = ''
        elif dim1 <= 2100:
            sz = 'w'
        else:
            sz = 'XXX'
            print "# wid=%u hgt=%d" % (width, height)

        mmdd = timestamp[5:10].replace(':','-')
        yymmdd = timestamp[:10].replace(':','-')
        time = timestamp[11:]
        tscrub = myscrub(title)

        newtitle = (sz + mmdd +
                         '-' + str(index).zfill(ndigits) +
                         '-' + camera +
                         '-' + tscrub + ".jpg")

        # TODO: check for duplication without sz

        print "# " + yymmdd + " " + time
        print "mv -i %s %s" % (name, newtitle)

if __name__ == "__main__":
    import sys
    execfile(sys.argv[1])
    thedict = list2dict(thelist)
    do_process(thedict)
