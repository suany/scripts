#!/usr/bin/env python3

from __future__ import print_function
from __future__ import with_statement

import ast, datetime, operator, sys
import png # pip install pypng

class Histo(object):
    def __init__(self, line):
        date, speed, direc = ast.literal_eval(line)[0]
        self.dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.speed = speed
        self.direc = direc

    def minute(self):
        return self.dt.hour * 60 + self.dt.minute

def add_vgrid(row):
    row[31] = 128
    row[61] = 128
    row[91] = 128

def add_hgrid(row):
    for i in range(len(row)):
        if row[i] == 255:
            row[i] = 128

def histo_to_row(h):
    row = 120 * [255]
    add_vgrid(row)
    maxpop = max(h.speed, key = operator.itemgetter(1)) [1]
    def put_pixels(speed, pop):
        col = speed * 3
        val = int(255 - (255 * pop)/maxpop)
        row[col+1] = val
        row[col+2] = val
        prev = 255 if col == 0 else row[col-1]
        row[col] = round((val + prev) / 2)
    pop39 = 0
    prev = None
    for speed, pop in h.speed:
        if speed < 39:
            if prev and prev[0]+1 != speed:
                put_pixels(prev[0]+1, 0)
            put_pixels(speed, pop)
            prev = (speed, pop)
        else:
            pop39 += pop
    if pop39:
        put_pixels(39, pop39)
    elif prev is not None:
        put_pixels(prev[0]+1, 0)
    return row

def histos_from_file(filename):
    with open(filename) as f:
        for line in f:
            yield Histo(line)

def rows_from_file(filename, nrows):
    cur = 0
    for h in histos_from_file(filename):
        rowno = h.minute()
        if rowno < cur:
            print("Skipping", h.dt)
            continue
        while cur < rowno:
            yield 120 * [255] # TODO: absence indicator
            cur += 1
            if cur == nrows:
                return
        row = histo_to_row(h)
        if h.dt.minute == 0:
            add_hgrid(row)
        yield row
        cur += 1
        if cur == nrows:
            return
    while cur < nrows:
        yield 120 * [255] # TODO: absence indicator
        cur += 1

def histos_file_to_png(filename):
    # widht = 40 mph * 3 pixels each
    # height = 1 row per minute, 24 hrs
    # TODO height = 1 row per 5 minutes, 24 hrs = 288
    if filename.endswith(".txt"):
        outfilename = filename[:-4] + ".png"
    else:
        outfilename = filename + ".png"
    with open(outfilename, "wb") as f:
        w = png.Writer(120, 1440, greyscale=True)
        w.write(f, rows_from_file(filename, 1440))

if __name__ == "__main__":
    for f in sys.argv[1:]:
        histos_file_to_png(f)
