#!/usr/bin/env python3

from __future__ import print_function

from datetime import date, timedelta

if __name__ == "__main__":
    import sys
    yr = int(sys.argv[1])
    mo = int(sys.argv[2])
    mos = 4
    d0 = date(yr, mo, 1)
    d = date(yr, mo, 1)
    while d - d0 < timedelta(days=128):
        if d.weekday() in [5, 6]:
            print(d.strftime("%a %Y-%m-%d"))
        d += timedelta(days = 1)
