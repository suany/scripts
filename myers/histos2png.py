#!/usr/bin/env python3

from __future__ import print_function
from __future__ import with_statement

import ast, datetime, itertools, operator, sys
import png # pip install pypng

greyscale = False

class Histo(object):
    def __init__(self, line):
        date, speed, direc = ast.literal_eval(line)[0]
        self.dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.speed = speed
        self.direc = direc

    def rowno(self):
        """ Row number == which 5-minute interval of the day? """
        return self.dt.hour * 12 + self.dt.minute // 5

def add_vgrid(row):
    if greyscale:
        row[31] = 128
        row[61] = 128
        row[91] = 128
    else:
        row[93] = row[94] = row[95] = 128
        row[183] = row[184] = row[185] = 128
        row[273] = row[274] = row[275] = 128

def add_hgrid(row):
    for i in range(len(row)):
        row[i] = 128

def new_row():
    if greyscale:
        row = 120 * [255]
    else:
        row = list(itertools.chain(31 * [192, 255, 255],
                                   30 * [192, 255, 192],
                                   30 * [255, 255, 192],
                                   29 * [255, 192, 192],
                                   ))
    add_vgrid(row)
    return row

_absence_row = None
def absence_row():
    global _absence_row
    if _absence_row is None:
        _absence_row = new_row()
        add_vgrid(_absence_row)
    return _absence_row

def grey_or_white(row, idx):
    if row[idx] == row[idx+1] and row[idx] == row[idx+2]:
        return row[idx];
    else:
        return 255

def put_pixels(row, speed, pop, maxpop, is_hour):
    val = 192 - (192 * pop) // maxpop
    if greyscale:
        col = speed * 3
        prev = 255 if col == 0 else row[col-1]
        row[col] = (val + prev) // 2
        row[col+1] = val
        row[col+2] = val
        if speed < 39:
            row[col+3] = (val + 255) // 2
    else:
        col = speed * 3 * 3 # 3 pixels per speed, 3 colors per pixel
        if is_hour or col == 0:
            row[col + 0] = row[col + 1] = row[col + 2] = val
        else:
            prev = grey_or_white(row, col-3)
            row[col + 0] = row[col + 1] = row[col + 2] = (val + prev) // 2
        row[col + 3] = row[col + 4] = row[col + 5] = val
        row[col + 6] = row[col + 7] = row[col + 8] = val
        if speed < 39:
            # NOTE: should probably skip if is_hour, but this seems to give
            #       a useful end marker.
            row[col + 9] = row[col + 10] = row[col + 11] = (val + 255) // 2

def histo_to_row(h):
    row = new_row()
    if h.dt.minute == 0:
        add_hgrid(row)
    maxpop = max(h.speed, key = operator.itemgetter(1))[1]
    pop39 = 0
    for speed, pop in h.speed:
        if speed < 39:
            put_pixels(row, speed, pop, maxpop, h.dt.minute == 0)
        else:
            pop39 += pop
    if pop39:
        put_pixels(row, 39, pop39, maxpop, h.dt.minute == 0)
    return row

def histos_from_file(filename):
    with open(filename) as f:
        for line in f:
            yield Histo(line)

def rows_from_file(filename, nrows):
    cur = 0
    for h in histos_from_file(filename):
        rowno = h.rowno()
        if rowno < cur:
            print("Skipping", h.dt)
            continue
        while cur < rowno:
            yield absence_row()
            cur += 1
            if cur == nrows:
                return
        row = histo_to_row(h)
        yield row
        cur += 1
        if cur == nrows:
            return
    while cur < nrows:
        yield absence_row()
        cur += 1

def histos_file_to_png(filename):
    # widht = 40 mph * 3 pixels each
    # height = 1 row per 5 minutes, 24 hrs = 288
    if filename.endswith(".txt"):
        outfilename = filename[:-4] + ".png"
    else:
        outfilename = filename + ".png"
    with open(outfilename, "wb") as f:
        w = png.Writer(120, 288, greyscale = greyscale)
        w.write(f, rows_from_file(filename, 288))

if __name__ == "__main__":
    for f in sys.argv[1:]:
        histos_file_to_png(f)
