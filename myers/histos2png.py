#!/usr/bin/env python3

from __future__ import print_function
from __future__ import with_statement

import ast, datetime, itertools, operator, sys
import png # pip install pypng

# Color or greyscale (deprecated).
greyscale = False

def ncolors():
    return 1 if greyscale else 3

# One data point every PERIOD minutes.
PERIOD = 3

# Horizontal pixels per point
HPX = 3

# left margin, graph 1, mid margin, graph 2, right margin
LM = 15  # 1 + 5 + 2 + 5 + 2
G1 = 120
MM = 16
G2 = 108
RM = 15

# Direction to start graph
DIR0 = 50

#Looking South:
# - 145 = eastern reach (will be shadowed)
# - 157.5 = SSW (= line of shadow)
# - 165 - center of reach
# - 180 = S (= western reach)
#Looking NW:
# - 290 - western reach
# - 292.5 = WNW
# - 305 - center of reach
# - 315 = NW
DE = (140-DIR0) // 10 * HPX
DS = (180-140) // 10 * HPX
DSW = (290-180) // 10 * HPX
DNW = (320-290) // 10 * HPX
DN = (360-320+DIR0) // 10 * HPX
assert G2 == DE + DS + DSW + DNW + DN

PALETTE = {
    "b" : (0, 0, 0),
    "g" : (128, 255, 128),
    "l" : (0, 0, 255),
    "r" : (255, 128, 128),
    "w" : (255, 255, 255),
}
PALETTEGS = {
    "b" : (0),
    "g" : (64),
    "l" : (128),
    "r" : (192),
    "w" : (255),
}


DIGIT_WIDTH = 5
DIGIT_HEIGHT = 7

DIGITS = [
    ["wbbbw",
     "bwwwb",
     "bwwwb",
     "bwwwb",
     "bwwwb",
     "bwwwb",
     "wbbbw",],
    ["wwbww",
     "wbbww",
     "wwbww",
     "wwbww",
     "wwbww",
     "wwbww",
     "wbbbw",],
    ["wbbbw",
     "bwwwb",
     "wwwwb",
     "wwbbw",
     "wbwww",
     "bwwww",
     "bbbbb",],
    ["wbbbw",
     "bwwwb",
     "wwwwb",
     "wwbbw",
     "wwwwb",
     "bwwwb",
     "wbbbw",],
    ["wwwbw",
     "wwbbw",
     "wbwbw",
     "bwwbw",
     "bbbbb",
     "wwwbw",
     "wwwbw",],
    ["bbbbb",
     "bwwww",
     "bbbbw",
     "wwwwb",
     "wwwwb",
     "bwwwb",
     "wbbbw",],
    ["wbbbw",
     "bwwww",
     "bwwww",
     "bbbbw",
     "bwwwb",
     "bwwwb",
     "wbbbw",],
    ["bbbbb",
     "wwwwb",
     "wwwwb",
     "wwwbw",
     "wwwbw",
     "wwbww",
     "wwbww",],
    ["wbbbw",
     "bwwwb",
     "bwwwb",
     "wbbbw",
     "bwwwb",
     "bwwwb",
     "wbbbw",],
    ["wbbbw",
     "bwwwb",
     "bwwwb",
     "wbbbw",
     "wwwwb",
     "wwwwb",
     "wbbbw",],
    ]

def put_digit_row(row, pixel, colors):
    palette = PALETTEGS if greyscale else PALETTE
    for i, c in enumerate(colors):
        for j, val in enumerate(PALETTE[c]):
            row[(pixel + i) * ncolors() + j] = val

############################################################################

# w=0xffffff
# b=0x000000
# Split into 70-character segments for readability.
X_KEY_NROWS = 11
X_KEY = [
    ["wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbwwwbbbwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbwwbwwwbwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbwwbwwwbwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbwwbwwwbwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbwwbwwwbwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbwwbwwwbwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbbwwbbbwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
    ],
    ["wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwbbbwwwbbbwwwwwwwwwwwwwwwwwwwwwbbbwwwbbbwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wbwwwbwbwwwbwwwwwwwwwwwwwwwwwwwbwwwbwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwbwbwwwbwwwwwwwwwwwwwwwwwwwwwwwbwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwbbwwbwwwbwwwwwwwwwwwwwwwwwwwwbbbwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwbwwwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwbwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wbwwwwwbwwwbwwwwwwwwwwwwwwwwwwwbwwwbwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wbbbbbwwbbbwwwwwwwwwwwwwwwwwwwwwbbbwwwbbbwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
    ],
    ["wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwbbbbbwwwwwwwwwwwwwwwwwwwwwwwbbbbwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwbwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwbwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwbbbbbwwwwwwwwwwwwwwwwwwwwwwwbbbwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwbbbbbwwwwwwwwwwwwwwwwwwwwwwbbbbwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
    ],
    ["wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwbwwwwwbwwwwwwwwwwwwwwwwwwwwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwbwwwwwbwwwwwwwwwwwwwwwwwwwwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwbwwbwwbwwwwwwwwwwwwwwwwwwwwwbbwwbwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwbwbwbwwwwwwwwwwwwwwwwwwwwwwbwbwbwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwbwbwbwwwwwwwwwwwwwwwwwwwwwwbwwbbwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwbwbwbwwwwwwwwwwwwwwwwwwwwwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwbwbwwwwwwwwwwwwwwwwwwwwwwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
    ],
    ]

LEGEND_NROWS = 13
LEGEND = [
    ["wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
    ],
    ["wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwbwwwwwbwwbbbbwwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwbbwwwbbwwbwwwbwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwbwbwbwbwwbwwwbwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwbwwbwwbwwbbbbwwwbbbbbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwbwwwwwbwwbwwwwwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwbwwwwwbwwbwwwwwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwbwwwwwbwwbwwwwwwbwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
     "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
    ],
    ["wwwwwwwwwwwwwwggggggggggggggggggggwwwllllllllllllllllllllllllllllwww",
     "wwwwwwwwwwwwwwggggggggggggggggggggwwwllllllllllllllllllllllllllllwww",
     "wwwwwwwwwwwwwwggggggggggggggggggggwwwllllllllllllllllllllllllllllwww",
     "wwwwwwwwwwwwwwgggggbgggggbbbbbggggwwwlllllwwwllllllllwllwwwwwllllwww",
     "wwwwwwwwwwwwwwggggbbgggggggggbggggwwwllllwlllwllllllwwllwllllllllwww",
     "wwwwwwwwwwwwwwgggggbgggggggggbggggwwwllllwlllwlllllllwllwwwwlllllwww",
     "wwwwwwwwwwwwwwgggggbggbbbgggbgggggwwwlllllwwwlllwwwllwllllllwllllwww",
     "wwwwwwwwwwwwwwgggggbggggggggbgggggwwwllllwlllwlllllllwllllllwllllwww",
     "wwwwwwwwwwwwwwgggggbgggggggbggggggwwwllllwlllwlllllllwllwlllwllllwww",
     "wwwwwwwwwwwwwwggggbbbggggggbggggggwwwlllllwwwlllllllwwwllwwwlllllwww",
     "wwwwwwwwwwwwwwggggggggggggggggggggwwwllllllllllllllllllllllllllllwww",
     "wwwwwwwwwwwwwwggggggggggggggggggggwwwllllllllllllllllllllllllllllwww",
     "wwwwwwwwwwwwwwggggggggggggggggggggwwwllllllllllllllllllllllllllllwww",
    ],
    ["bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbwwwrrrrrrrrrrrrrrrrrrrrrrrwwwwwwwwww",
     "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbwwwrrrrrrrrrrrrrrrrrrrrrrrwwwwwwwwww",
     "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbwwwrrrrrrrrrrrrrrrrrrrrrrrwwwwwwwwww",
     "bbbbbwbbbwwwbbbbbbbbwwwbbbbwwwbbbbbwwwrrrrrbbbrrrrrbrrrrrrrrrwwwwwwwwww",
     "bbbbwwbbwbbbbbbbbbbwbbbwbbwbbbwbbbbwwwrrrrbrrrbrrrbbrrrrrrrrrwwwwwwwwww",
     "bbbbbwbbwbbbbbbwwwbbbbbwbbbbbbwbbbbwwwrrrrrrrrbrrbrbrrrrrrrrrwwwwwwwwww",
     "bbbbbwbbwwwwbbbbbbbbbwwbbbbbwwbbbbbwwwrrrrrrbbrrbrrbrrbbbrrrrwwwwwwwwww",
     "bbbbbwbbwbbbwbbbbbbbwbbbbbbbbbwbbbbwwwrrrrrbrrrrbbbbbrrrrrrrrwwwwwwwwww",
     "bbbbbwbbwbbbwbbbbbbwbbbbbbwbbbwbbbbwwwrrrrbrrrrrrrrbrrrrrrrrrwwwwwwwwww",
     "bbbbwwwbbwwwbbbbbbbwwwwwbbbwwwbbbbbwwwrrrrbbbbbrrrrbrrrrrrrrrwwwwwwwwww",
     "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbwwwrrrrrrrrrrrrrrrrrrrrrrrwwwwwwwwww",
     "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbwwwrrrrrrrrrrrrrrrrrrrrrrrwwwwwwwwww",
     "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbwwwrrrrrrrrrrrrrrrrrrrrrrrwwwwwwwwww",
    ],
    ]


def gen_pixels_for_row(pixels, rowno):
    palette = PALETTEGS if greyscale else PALETTE
    for segment in pixels:
        for c in segment[rowno]:
            for v in palette[c]:
                yield v

def x_key_rows():
    for i in range(X_KEY_NROWS):
        yield list(gen_pixels_for_row(X_KEY, i))

def legend_rows():
    for i in range(LEGEND_NROWS):
        yield list(gen_pixels_for_row(LEGEND, i))

############################################################################

class Histo(object):
    def __init__(self, line):
        date, speed, direc = ast.literal_eval(line)[0]
        self.dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.speed = speed
        self.direc = direc

    def rowno(self):
        """ Row number == which interval of the day? """
        return self.dt.hour * (60 // PERIOD) + self.dt.minute // PERIOD

def direc2col(direc):
    return ((LM+G1+MM) * ncolors()
            + ((direc - DIR0) % 360 // 10) * HPX * ncolors())

def add_vgrid(row):
    if greyscale:
        row[LM + 31] = 128
        row[LM + 61] = 128
        row[LM + 91] = 128
    else:
        def init_gray_pixel(idx):
            row[idx] = row[idx+1] = row[idx+2] = 128
        L1 = LM * 3
        # The +3 chooses the second of three pixels for the point
        init_gray_pixel(L1 +  90 + 3)
        init_gray_pixel(L1 + 180 + 3)
        init_gray_pixel(L1 + 270 + 3)
        init_gray_pixel(direc2col(0) + 3)
        init_gray_pixel(direc2col(90) + 3)
        init_gray_pixel(direc2col(180) + 3)
        init_gray_pixel(direc2col(270) + 3)

def add_hgrid(row):
    for i in range(LM * ncolors(), (LM+G1) * ncolors()):
        row[i] = 128
    for i in range((LM+G1+MM) * ncolors(), (LM+G1+MM+G2) * ncolors()):
        row[i] = 128

def blank_row():
    return ((LM + G1 + MM + G2 + RM) * ncolors()) * [255]

def new_row(quadrant):
    if greyscale:
        row = (LM + G1 + MM + G2 + RM) * [255]
    else:
        if quadrant == 6:
            BADDIR = [208, 207, 208]
            GOODDIR = [224, 224, 255]
            row = list(itertools.chain(LM * [255, 255, 255],
                                       31 * [192, 255, 192],
                                       30 * [192, 255, 255],
                                       30 * [255, 255, 192],
                                       29 * [255, 192, 192],
                                       MM * [255, 255, 255],
                                       DE * BADDIR,
                                       DS * GOODDIR,
                                       DSW * BADDIR,
                                       DNW * GOODDIR,
                                       DN * BADDIR,
                                       RM * [255, 255, 255],
                                       ))
        elif quadrant == 12:
            BADDIR = [224, 223, 224]
            GOODDIR = [240, 240, 255]
            row = list(itertools.chain(LM * [255, 255, 255],
                                       31 * [224, 255, 224],
                                       30 * [224, 255, 255],
                                       30 * [255, 255, 224],
                                       29 * [255, 224, 224],
                                       MM * [255, 255, 255],
                                       DE * BADDIR,
                                       DS * GOODDIR,
                                       DSW * BADDIR,
                                       DNW * GOODDIR,
                                       DN * BADDIR,
                                       RM * [255, 255, 255],
                                       ))
        else: # 0 and 18
            # Hack: BADDIR is slightly off-grey to evade grey_or_white
            BADDIR = [192, 191, 192]
            GOODDIR = [208, 208, 255]
            row = list(itertools.chain(LM * [255, 255, 255],
                                       31 * [192, 224, 192],
                                       30 * [192, 224, 224],
                                       30 * [224, 224, 192],
                                       29 * [224, 192, 192],
                                       MM * [255, 255, 255],
                                       DE * BADDIR,
                                       DS * GOODDIR,
                                       DSW * BADDIR,
                                       DNW * GOODDIR,
                                       DN * BADDIR,
                                       RM * [255, 255, 255],
                                       ))
    add_vgrid(row)
    return row

def grey_or_white(row, idx):
    if row[idx] == row[idx+1] and row[idx] == row[idx+2]:
        return row[idx];
    else:
        return 255

def put_pixels(row, col, pop, maxpop, is_hour, shade=(0,0,0), is_final=False):
    if pop > maxpop:
        pop = maxpop # Saturation possible if > 39mph
    val = 192 - (192 * pop) // maxpop
    if greyscale:
        prev = 255 if col == 0 else row[col-1]
        row[col] = (val + prev) // 2
        row[col+1] = val
        row[col+2] = val
        if not is_final:
            row[col+3] = (val + 255) // 2
    else:
        def put_rgb(idx, val):
            row[col + idx + 0] = 255 if shade[0] else val
            row[col + idx + 1] = 255 if shade[1] else val
            row[col + idx + 2] = 255 if shade[2] else val

        if is_hour or col == 0:
            put_rgb(0, val)
        else:
            prev = grey_or_white(row, col-3)
            put_rgb(0, (val + prev) // 2)
        put_rgb(3, val)
        put_rgb(6, val)
        if not is_final:
            # NOTE: should probably skip if is_hour, but this seems to give
            #       a useful end marker.
            put_rgb(9, (val + 255) // 2)

def speed2col(speed):
    return LM * ncolors() + speed * HPX * ncolors()

def write_speed(h, row):
    maxpop = max(h.speed, key = operator.itemgetter(1))[1]
    is_hour = h.dt.minute == 0
    pop39 = 0
    for speed, pop in h.speed:
        if speed < 39:
            put_pixels(row, speed2col(speed), pop, maxpop, is_hour)
        else:
            pop39 += pop
    if pop39:
        put_pixels(row, speed2col(39), pop39, maxpop, is_hour, is_final = True)

def percentile75(speed):
    """ speed at 75th percentile """
    tot = sum(sp * pop for sp, pop in speed)
    thresh = tot * 3 // 4
    accum = 0
    for sp, pop in speed:
        accum += sp * pop
        if accum > thresh:
            return sp
    assert False

def write_direction(h, row):
    maxpop = max(h.direc, key = operator.itemgetter(1))[1]
    is_hour = h.dt.minute == 0
    speed75 = percentile75(h.speed)
    if speed75 < 8:
        shade = (0,1,0)
    elif speed75 < 16:
        shade = (0,0,1)
    elif speed75 < 24:
        shade = (0,0,0)
    else:
        shade = (1,0,0)
    # Loop 1: dir0 to 360
    for direc, pop in h.direc:
        if direc < DIR0:
            continue
        put_pixels(row, direc2col(direc), pop, maxpop, is_hour, shade)
    # Loop 2: 0 to dir0
    for direc, pop in h.direc:
        if direc >= DIR0:
            break
        put_pixels(row, direc2col(direc), pop, maxpop, is_hour, shade,
                   direc == DIR0 - 10)

def histo_to_row(h, quadrant):
    row = new_row(quadrant)
    if h.dt.minute == 0:
        add_hgrid(row)
    write_speed(h, row)
    write_direction(h, row)
    return row

def histos_from_file(filename):
    with open(filename) as f:
        for line in f:
            yield Histo(line)

def row2quadrant(rowno):
    return (rowno * PERIOD) // (6 * 60) * 6

def add_y_key(row, rowno):
    adj = rowno + (DIGIT_HEIGHT // 2)
    hour = adj // (60 // PERIOD)
    if hour == 0 or hour == 24:
        return row # skip midnight
    yrow = adj % (60 // PERIOD)
    if yrow >= DIGIT_HEIGHT:
        return row
    hnorm = hour if hour <= 12 else hour - 12
    digit0 = hnorm % 10
    digit1 = hnorm // 10
    if digit1 == 0: # one digit
        # left
        put_digit_row(row, LM-DIGIT_WIDTH-2, DIGITS[digit0][yrow])
        # middle
        put_digit_row(row, LM+G1+MM//2-DIGIT_WIDTH//2, DIGITS[digit0][yrow])
        # right
        put_digit_row(row, LM+G1+MM+G2+2, DIGITS[digit0][yrow])
    else: # two digits
        # left
        put_digit_row(row, LM-(2*DIGIT_WIDTH+2), DIGITS[digit1][yrow])
        put_digit_row(row, LM-DIGIT_WIDTH-2, DIGITS[digit0][yrow])
        # middle
        put_digit_row(row, LM+G1+MM//2-DIGIT_WIDTH, DIGITS[digit1][yrow])
        put_digit_row(row, LM+G1+MM//2, DIGITS[digit0][yrow])
        # right
        put_digit_row(row, LM+G1+MM+G2+2, DIGITS[digit1][yrow])
        put_digit_row(row, LM+G1+MM+G2+2+DIGIT_WIDTH, DIGITS[digit0][yrow])
    return row

def rows_from_file(filename, nrows):
    # Header
    yield from x_key_rows()
    # Main Graph
    cur = 0
    quadrant = 0
    for h in histos_from_file(filename):
        rowno = h.rowno()
        if rowno < cur:
            print("Skipping", h.dt)
            continue
        while cur < rowno:
            row = new_row(row2quadrant(cur))
            yield add_y_key(row, cur)
            cur += 1
            if cur == nrows:
                break
        row = histo_to_row(h, row2quadrant(rowno))
        yield add_y_key(row, rowno)
        cur += 1
        if cur == nrows:
            break
    while cur < nrows:
        row = new_row(row2quadrant(cur))
        yield add_y_key(row, cur)
        cur += 1
    # Footer
    yield from x_key_rows()
    yield from legend_rows()

def histos_file_to_png(filename):
    # width = 40 mph * 3 pixels each
    # height = 1 row per 5 minutes, 24 hrs = 288
    if filename.endswith(".txt"):
        outfilename = filename[:-4] + ".png"
    else:
        outfilename = filename + ".png"
    with open(outfilename, "wb") as f:
        nrows = 60*24//PERIOD
        w = png.Writer(LM + G1 + MM + G2 + RM,
                       X_KEY_NROWS + nrows + X_KEY_NROWS + LEGEND_NROWS,
                       greyscale = greyscale)
        w.write(f, rows_from_file(filename, nrows))

if __name__ == "__main__":
    for f in sys.argv[1:]:
        histos_file_to_png(f)
