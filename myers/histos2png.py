#!/usr/bin/env python3

from __future__ import print_function
from __future__ import with_statement

import ast, datetime, itertools, operator, sys
import png # pip install pypng

# Color or greyscale (deprecated).
greyscale = False

COLORS = 1 if greyscale else 3

# One data point every PERIOD minutes.
PERIOD = 3

# left margin, graph 1, mid margin, graph 2, right margin
LM = 15  # 1 + 5 + 2 + 5 + 2
G1 = 120
MM = 16
G2 = 108
RM = 15

TOPMARGIN = 10   # 1 + 7 + 2
BOTTOMMARGIN = 2

DIGIT_WIDTH = 5   # except 1: width=3
DIGIT_HEIGHT = 7

digits = [
    [(0,1,1,1,0),
     (1,0,0,0,1),
     (1,0,0,0,1),
     (1,0,0,0,1),
     (1,0,0,0,1),
     (1,0,0,0,1),
     (0,1,1,1,0)],
    [(0,1,0),
     (1,1,0),
     (0,1,0),
     (0,1,0),
     (0,1,0),
     (0,1,0),
     (1,1,1)],
    [(0,1,1,1,0),
     (1,0,0,0,1),
     (0,0,0,0,1),
     (0,0,1,1,0),
     (0,1,0,0,0),
     (1,0,0,0,0),
     (1,1,1,1,1)],
    [(0,1,1,1,0),
     (1,0,0,0,1),
     (0,0,0,0,1),
     (0,0,1,1,0),
     (0,0,0,0,1),
     (1,0,0,0,1),
     (0,1,1,1,0)],
    [(0,0,0,1,0),
     (0,0,1,1,0),
     (0,1,0,1,0),
     (1,0,0,1,0),
     (1,1,1,1,1),
     (0,0,0,1,0),
     (0,0,0,1,0)],
    [(1,1,1,1,1),
     (1,0,0,0,0),
     (1,1,1,1,0),
     (0,0,0,0,1),
     (0,0,0,0,1),
     (1,0,0,0,1),
     (0,1,1,1,0)],
    [(0,1,1,1,0),
     (1,0,0,0,0),
     (1,0,0,0,0),
     (1,1,1,1,0),
     (1,0,0,0,1),
     (1,0,0,0,1),
     (0,1,1,1,0)],
    [(1,1,1,1,1),
     (0,0,0,0,1),
     (0,0,0,0,1),
     (0,0,0,1,0),
     (0,0,0,1,0),
     (0,0,1,0,0),
     (0,0,1,0,0)],
    [(0,1,1,1,0),
     (1,0,0,0,1),
     (1,0,0,0,1),
     (0,1,1,1,0),
     (1,0,0,0,1),
     (1,0,0,0,1),
     (0,1,1,1,0)],
    [(0,1,1,1,0),
     (1,0,0,0,1),
     (1,0,0,0,1),
     (0,1,1,1,0),
     (0,0,0,0,1),
     (0,0,0,0,1),
     (0,1,1,1,0)],
    ]

class Histo(object):
    def __init__(self, line):
        date, speed, direc = ast.literal_eval(line)[0]
        self.dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.speed = speed
        self.direc = direc

    def rowno(self):
        """ Row number == which interval of the day? """
        return self.dt.hour * (60 // PERIOD) + self.dt.minute // PERIOD

def add_vgrid(row):
    if greyscale:
        row[LM  + 31] = 128
        row[LM  + 61] = 128
        row[LM  + 91] = 128
    else:
        row[LM*3 + 93]  = row[LM*3 + 94]  = row[LM*3 + 95] = 128
        row[LM*3 + 183] = row[LM*3 + 184] = row[LM*3 + 185] = 128
        row[LM*3 + 273] = row[LM*3 + 274] = row[LM*3 + 275] = 128

def add_hgrid(row):
    for i in range(LM * COLORS, (LM+G1) * COLORS):
        row[i] = 128

def blank_row():
    return ((LM + G1 + MM + G2 + RM) * COLORS) * [255]

def new_row(quadrant):
    if greyscale:
        row = (LM + G1 + MM + G2 + RM) * [255]
    else:
        if quadrant == 6:
            row = list(itertools.chain(LM * [255, 255, 255],
                                       31 * [192, 255, 255],
                                       30 * [192, 255, 192],
                                       30 * [255, 255, 192],
                                       29 * [255, 192, 192],
                                       MM * [255, 255, 255],
                                       G2 * [224, 224, 224],
                                       RM * [255, 255, 255],
                                       ))
        elif quadrant == 12:
            row = list(itertools.chain(LM * [255, 255, 255],
                                       31 * [224, 255, 255],
                                       30 * [224, 255, 224],
                                       30 * [255, 255, 224],
                                       29 * [255, 224, 224],
                                       MM * [255, 255, 255],
                                       G2 * [240, 240, 240],
                                       RM * [255, 255, 255],
                                       ))
        else: # 0 and 18
            row = list(itertools.chain(LM * [255, 255, 255],
                                       31 * [192, 224, 224],
                                       30 * [192, 224, 192],
                                       30 * [224, 224, 192],
                                       29 * [224, 192, 192],
                                       MM * [255, 255, 255],
                                       G2 * [208, 208, 208],
                                       RM * [255, 255, 255],
                                       ))
    add_vgrid(row)
    return row

absence_row = {
    0  : new_row(0),
    6  : new_row(6),
    12 : new_row(12),
    18 : new_row(18),
}

def grey_or_white(row, idx):
    if row[idx] == row[idx+1] and row[idx] == row[idx+2]:
        return row[idx];
    else:
        return 255

def put_pixels(row, speed, pop, maxpop, is_hour):
    val = 192 - (192 * pop) // maxpop
    col = LM * COLORS + speed * 3 * COLORS # 3 pixels per speed
    if greyscale:
        prev = 255 if col == 0 else row[col-1]
        row[col] = (val + prev) // 2
        row[col+1] = val
        row[col+2] = val
        if speed < 39:
            row[col+3] = (val + 255) // 2
    else:
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

def histo_to_row(h, quadrant):
    row = new_row(quadrant)
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

def row2quadrant(rowno):
    return (rowno * PERIOD) // (6 * 60) * 6


def rows_from_file(filename, nrows):
    # Header
    for i in range(TOPMARGIN):
        yield blank_row()
    # Main Graph
    cur = 0
    quadrant = 0
    for h in histos_from_file(filename):
        rowno = h.rowno()
        if rowno < cur:
            print("Skipping", h.dt)
            continue
        while cur < rowno:
            yield absence_row[row2quadrant(cur)]
            cur += 1
            if cur == nrows:
                break
        row = histo_to_row(h, row2quadrant(rowno))
        yield row
        cur += 1
        if cur == nrows:
            break
    while cur < nrows:
        yield absence_row[row2quadrant(cur)]
        cur += 1
    # Footer
    for i in range(BOTTOMMARGIN):
        yield blank_row()

def histos_file_to_png(filename):
    # widht = 40 mph * 3 pixels each
    # height = 1 row per 5 minutes, 24 hrs = 288
    if filename.endswith(".txt"):
        outfilename = filename[:-4] + ".png"
    else:
        outfilename = filename + ".png"
    with open(outfilename, "wb") as f:
        nrows = 60*24//PERIOD
        w = png.Writer(LM + G1 + MM + G2 + RM,
                       TOPMARGIN + nrows + BOTTOMMARGIN,
                       greyscale = greyscale)
        w.write(f, rows_from_file(filename, nrows))

if __name__ == "__main__":
    for f in sys.argv[1:]:
        histos_file_to_png(f)
