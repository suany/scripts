#!/usr/bin/env python3

from __future__ import print_function

from datetime import date, timedelta
import copy

def usage():
    print("""
Usage: weekend.py [days] year[-]month[[-]day]
E.g.:
    weekend.py 2025 03              - show weekends starting March 2025
    weekend.py 2025-03-08           - show weekends starting March 8, 2025
    weekend.py 2025-03-08 Mon Thu   - show mon/thu starting March 8, 2025
    """)

def fail(msg):
    print("Error:", msg)
    usage()
    sys.exit(1)

DAYS_OF_WEEK = {
   "mon" : 0, "tue" : 1, "wed" : 2, "thu" : 3, "fri" : 4, "sat" : 5, "sun" : 6,
}

if __name__ == "__main__":
    import sys

    incl_days = set()
    yr = None
    mo = None
    dy = None
    for arg in sys.argv[1:]:
        dayno = DAYS_OF_WEEK.get(arg[:3].lower(), None)
        if dayno is not None:
            incl_days.add(dayno)
            continue
        if yr is None:
            ymd = arg.split('-', 3)
            yr = int(ymd[0])
            if len(ymd) >= 2:
                mo = int(ymd[1])
            if len(ymd) == 3:
                dy = int(ymd[2])
            if len(ymd) > 3:
                fail("Error: too many hyphens")
            continue
        if mo is None:
            mo = int(arg)
            continue
        if dy is None:
            dy = int(arg)
            continue
        fail("Error: too many args")
    if yr is None or mo is None:
        fail("Error: year / month not specified")
    if dy is None:
        dy = 1 # Default day = 1
    if not incl_days:
        incl_days.add(5) # Default to weekend (Sat and Sun)
        incl_days.add(6)

    d0 = date(yr, mo, dy)
    d = copy.copy(d0)
    while d - d0 < timedelta(days=128):
        if d.weekday() in incl_days:
            print(d.strftime("%a %Y-%m-%d"))
        d += timedelta(days = 1)
