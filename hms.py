#!/usr/bin/python

import sys

def secs2hms(secs):
    mins = secs / 60.0
    if mins < 1.0:
        return "%.1fs" % secs
    hrs = mins / 60.0
    if hrs < 1.0:
        return "%.1fm" % mins
    return "%.1fh" % hrs

if __name__ == "__main__":
    did_something = False    
    for arg in sys.argv[1:]:
        print secs2hms(float(arg))
        did_something = True
    if not did_something:
        for line in sys.stdin:
            out_tokens = []
            for token in line.split():
                try:
                    out_tokens.append(secs2hms(float(token)))
                except:
                    out_tokens.append(token)
            print ' '.join(out_tokens)
