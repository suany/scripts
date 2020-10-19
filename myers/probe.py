#!/usr/bin/env python3

from __future__ import print_function
from __future__ import with_statement

import json, sched, sys, time
import urllib.request
import datetime

def get_data():
    while True:
        try:
            with urllib.request.urlopen(
                    "http://www.employees.org/~wing/cgi/myers-data.txt"
                    ) as f:
                d = json.load(f)
            return d['localtimesecs'], d['windspeedmph'], d['winddir']
        except ConnectionError as e:
            print(e)
            time.sleep(1)
        except json.decoder.JSONDecodeError as e:
            print(e)
            time.sleep(1)
    sample = {
        'windspeedmph-5min-avg': 4.41,
        'windspeedmph-5min-max': 5.95,
        'windspeedmph-10min-avg': 4.32,
        'localtimesecs': '2020-10-17 23:07:58',
        'tempf': 39.1,
        'localdate': 'Oct 17, 2020',
        'windspeedmph': 5.59,
        'baromin': 29.88,
        'winddir-10min-avg': 55.0,
        'humidity': 84.4,
        'winddir': 82.0,
        'windspeedmph-10min-max': 7.09,
        'utc-timesecs': '2020-10-18 03:07:58',
        'myers-data': 'data',
        'windspeedmph-1day-max': 19.48,
        'dewptf': 34.8,
        'winddir-5min-avg': 60.0,
        'windspeedmph-10min-min': 2.41,
        'windspeedmph-5min-min': 2.72,
        'localtime-1day-max': '2020-10-17 14:27:26',
        'localtime': '11:07:58 PM'
    }

def mainloop():
    lastdata = None
    nsame = 0
    while True:
        time0 = time.time()
        curdata = get_data()
        if lastdata != curdata:
            lastdata = curdata
            nsame = 0
            yield curdata
        else:
            nsame += 1
            if nsame > 10:
                print("Same", nsame, "times")
        elapsed = time.time() - time0
        if elapsed < 0.8:
            time.sleep(0.8 - elapsed)

class Histo(object):
    def __init__(self, dtmin):
        self.dtmin = dtmin
        self.speed = dict()
        self.direc = dict()
    def add(self, sp, dn):
        sp_rounded = int(round(sp))
        self.speed[sp_rounded] = self.speed.get(sp_rounded, 0) + 1
        dn_rounded = int(round(dn, -1))
        self.direc[dn_rounded] = self.direc.get(dn_rounded, 0) + 1
    def write(self):
        # py 3.7: datestr = self.dtmin.date.isoformat()
        datestr = self.dtmin.strftime('%Y-%m-%d')
        filename = "myers-histo-" + datestr + ".txt"
        with open(filename, "a") as f:
            dtstr = self.dtmin.strftime('%Y-%m-%d %H:%M:%S')
            speed = [(k, self.speed[k]) for k in sorted(self.speed)]
            direc = [(k, self.direc[k]) for k in sorted(self.direc)]
            print((dtstr, speed, direc), ",", file=f)

_histo_from_data_test = False # TODO temporary
_do_histo = True
_do_log = True

def collect_histo(datagen):
    histos = []
    for data in datagen():
        if _do_log:
            date = data[0].split()[0]
            with open("myers-data-" + date + ".txt", "a") as f:
                print(data, ",", file=f)
        if _do_histo:
            # py 3.7: dt = datetime.datetime.fromisoformat(data[0])
            dt = datetime.datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')
            dt_rounded = dt.replace(second=0)
            if not histos or histos[-1].dtmin != dt_rounded:
                histos.append(Histo(dt_rounded))
                if len(histos) > 10:
                    histo0 = histos.pop(0)
                    histo0.write()
            histos[-1].add(data[1], data[2])

if __name__ == "__main__":
    if _histo_from_data_test:
        import ast
        # TODO cmdline support
        with open("test.txt") as f:
            def linegen():
                for line in f:
                    yield ast.literal_eval(line)[0]
            collect_histo(linegen)
    else:
        collect_histo(mainloop)
