#!/usr/bin/env python3

from __future__ import print_function

from datetime import date, timedelta

if __name__ == "__main__":
    import sys
    date1 = date.fromisoformat(sys.argv[1])
    date2 = date.fromisoformat(sys.argv[2])
    assert date1 < date2
    while date1 <= date2:
        print(date1.strftime("%a %Y-%m-%d"))
        date1 += timedelta(days = 1)
