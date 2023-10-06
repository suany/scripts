#!/usr/bin/python3
"""
Usage:
  hockey.py -d

    Download to schedule-{date}.csv, then process per below.

  hockey.py csvfile

    Read schedule, output team-#.csv one for each team.

  hockey.py csvfile1 csvfile2

    Compare two schedules, output diffs.

  Options:
    -c  clobber (overwrite .csv file without checking or backing up)
    -v  verbose
"""

from __future__ import print_function
from __future__ import with_statement
import csv, difflib, os, sys
from datetime import datetime, timedelta
import urllib.request

# Google sheet document key and ID for "Schedule" sheet.
DOC_KEY = "1KSGk-EbkXGWFUAMsRAsxo2BDrBx3c_DoYziibktN-Xo"
SCHED_GID = "1969887782"

TEAMS = {'A': "Black Sheep",
         'B': "Diane's (blue)",
         'C': "Orcutt (gold)",
         'D': "Mansour's (white)",
         'E': "Instant Replay (red)",
         'F': "MBA Outlaws (gray)",
         }
# Google sheet download only has month/day, not year
YEAR1 = 2023
YEAR2 = 2024

# Commandline Options: -c -d -v
clobber = False
download = False
verbose = False

DAYS = {'Sunday'    : 0,
        'Monday'    : 1,
        'Tuesday'   : 2,
        'Wednesday' : 3,
        'Thursday'  : 4,
        'Friday'    : 5,
        'Saturday'  : 6,
        }

class TimeHisto(object):
    " Histograms across days, times, and time slots, for a given team. "
    def __init__(self):
        self.day_histo = dict()
        self.time_histo = dict()
        self.slot_histo = dict()
    def add(self, day, time):
        time = time.split(' ', 1)[0] # Strip off " pm EDT"
        self.day_histo[day] = self.day_histo.get(day, 0) + 1
        self.time_histo[time] = self.time_histo.get(time, 0) + 1
        self.slot_histo[(day, time)] = self.slot_histo.get((day, time), 0) + 1

class TeamSummary(object):
    """
    List of double-header dates, and dictionary of matchup counts.
    The latter is used to check that each team plays each other team
    about the same number of games.
    """
    def __init__(self):
        self.double_headers = []
        self.matchups = dict([(t, 0) for t in TEAMS])

def print_summaries(team_summaries, ofp):
    for team in sorted(team_summaries):
        summary = team_summaries[team]
        print("Double Headers", team, ":", summary.double_headers, file = ofp)
    teams = sorted(TEAMS)
    print("Matchups:", ' '.join(("%4s" % t) for t in teams), file = ofp)
    for team in sorted(team_summaries):
        summary = team_summaries[team]
        print("Team %-4s" % team, 
              ' '.join(("%4d" % summary.matchups[t]) for t in teams),
              file = ofp)

def time_pad(time):
    ' Given time like "7:00" or "10:00", if hour is one digit, prepend " ". '
    return ' ' + time if len(time.split(':',1)[0]) == 1 else time

def day_time_abbrev(day_time):
    """
    Abbreviate the given day+time pair, e.g. "S7" for Sunday 7:XXpm.
    Use "R" for Thursday.
    """
    day = 'R' if day_time[0].startswith('Thu') else day_time[0][0]
    hr = day_time[1].split(':', 1)[0]
    assert len(hr) in [1, 2]
    if len(hr) == 1: # e.g., " S7"
        return ' ' + day + hr
    else:            # e.g., "S10"
        assert len(hr) == 2
        return day + hr

def print_team_histos(team_histos, ofp):
    " Print histograms across days, times, and time slots, for all team. "
    # First collect universe of days, times, slots
    for histo in team_histos.values():
        days = list(histo.day_histo.keys())
        times = list(histo.time_histo.keys())
        slots = list(histo.slot_histo.keys())
    days.sort(key = lambda day : DAYS[day])
    times.sort(key = time_pad)
    slots.sort(key = lambda dt : (DAYS[dt[0]], time_pad(dt[1])))
    teams = sorted(team_histos.keys())
    # Print Days
    header = "Days " + ' '.join(day[:3] for day in days)
    print(header, file = ofp)
    for team in teams:
        assert len(team) == 1
        tname = " " + team + "   "
        cnts = [("%3d" % team_histos[team].day_histo[day]) for day in days]
        print(tname + ' '.join(cnts), file = ofp)
    # Print Times
    header = "Times " + ' '.join(time_pad(time) for time in times)
    print(header, file = ofp)
    for team in teams:
        assert len(team) == 1
        tname = " " + team + "    "
        cnts = [("%5d" % team_histos[team].time_histo[time]) for time in times]
        print(tname + ' '.join(cnts), file = ofp)
    # Print Slots
    header = "Slots " + '  '.join(day_time_abbrev(slot) for slot in slots)
    print(header, file = ofp)
    for team in teams:
        assert len(team) == 1
        tname = " " + team + "    "
        cnts = [("%3d" % team_histos[team].slot_histo[slot]) for slot in slots]
        print(tname + '  '.join(cnts), file = ofp)

def process_header(row):
    colkey2colno = dict()
    for colno, entry in enumerate(row):
        if entry.startswith('\xef\xbb\xbf'): # UTF-8 BOM
            entry = entry[3:]
        colkey2colno[entry] = colno
    for expected in ['Date', 'Time', 'Team 1', 'Team 2']:
        if not expected in colkey2colno:
            assert False
    return colkey2colno

def csv_reader_to_schedule(reader):
    colkey2colno = None
    schedule = []
    playoffs = []
    for row in reader:
        if colkey2colno is None: # Find header
            if row[0] != 'Date':
                continue
            colkey2colno = process_header(row)
            continue
        date = row[colkey2colno['Date']]
        assert date
        time = row[colkey2colno['Time']]
        assert time
        team1 = row[colkey2colno['Team 1']]
        team2 = row[colkey2colno['Team 2']]
        if team1 in ['Playoffs', 'Championship', 'Finals']:
            assert not team2
            playoffs.append([date, time, team1])
            continue
        if not team1 in TEAMS:
            assert not team2 in TEAMS
            if verbose:
                print('# excluded:', team1, team2, file=sys.stderr)
            continue
        assert team2 in TEAMS
        schedule.append([date, time, team1, team2])
    assert schedule
    return schedule, playoffs

def read_csvfile(csvfile):
    with open(csvfile) as fp:
        return csv_reader_to_schedule(csv.reader(fp))

def compare_lists(tuplist1, tuplist2):
    strlist1 = ['\t'.join(row)+'\n' for row in tuplist1]
    strlist2 = ['\t'.join(row)+'\n' for row in tuplist2]
    ndiff = 0
    for line in difflib.ndiff(strlist1, strlist2):
        if line.startswith('  '):
            continue
        print(line, end='')
        ndiff += 1
    return ndiff

def normalize_date_time(date, time, delta):
    # date format is "Sunday, 9/18"
    smonth,sday = date.split(', ', 1)[1].split('/', 1)
    month = int(smonth)
    day = int(sday)
    assert month >= 1 and month <= 12
    assert day >= 1 and day <= 31
    year = YEAR1 if month >= 9 else YEAR2
    # time format is "7:15 pm EDT"
    hrmin, ampm, edt = time.split()
    assert ampm == 'pm'
    assert edt == 'EDT'
    shour,sminute = hrmin.split(':', 1)
    hour = int(shour)
    minute = int(sminute)
    assert hour >= 1 and hour <= 12
    assert minute >= 0 and minute <= 59
    # Create start and end datetime objects
    dt1 = datetime(year, month, day, hour+12, minute)
    dt2 = dt1 + delta
    return (datetime.strftime(dt1, "%Y-%m-%d"),
            datetime.strftime(dt1, "%I:%M %p"),
            datetime.strftime(dt2, "%Y-%m-%d"),
            datetime.strftime(dt2, "%I:%M %p"),
            )

def gcal_header():
    return ["Subject", "Start Date", "Start Time", "End Date", "End Time"]

def sched_tuple(date, time, team1, team2):
    gdate1, gtime1, gdate2, gtime2 = normalize_date_time(
        date, time, timedelta(minutes=75))
    return [team1, team2, gdate1, gtime1, gdate2, gtime2]

def filter_team_schedules(schedule, playoffs):
    team_schedules = dict([(team, []) for team in TEAMS])
    team_histos = dict([(team, TimeHisto()) for team in TEAMS])
    for date, time, team1, team2 in schedule:
        entry = sched_tuple(date, time, team1, team2)
        team_schedules[team1].append(entry)
        team_schedules[team2].append(entry)
        day = date.split(',', 1)[0]
        assert day in DAYS
        team_histos[team1].add(day, time)
        team_histos[team2].add(day, time)
    for date, time, descr in playoffs:
        for team in team_schedules:
            team_schedules[team].append(
                sched_tuple(date, time, descr, None))
    return team_schedules, team_histos

def mvbak(basename, ext):
    if clobber:
        return None
    if not os.path.exists(basename + ext):
        return None
    cnt = 1
    while os.path.exists(basename + ("-%03d" % cnt) + ext):
        cnt += 1
    bakname = basename + ("-%03d" % cnt) + ext
    os.rename(basename + ext, bakname)
    return bakname

def write_team_schedule(team, schedule):
    basename = 'team-' + team
    ext =  '.csv'
    bakname = mvbak(basename, ext)
    summary = TeamSummary() # double headers, matchups
    with open(basename + ext, 'w') as ofp:
        writer = csv.writer(ofp)
        writer.writerow(gcal_header())
        prev_date = None
        for entry in schedule:
            team1 = entry[0]
            team2 = entry[1]
            if team2 is None:
                descr = "Hockey " + team1 # "Playoffs/Championship"
            else:
                opponent = team1 if team == team2 else team2
                descr = "Hockey vs " + TEAMS[opponent]
                summary.matchups[opponent] += 1
                # collect double headers
                date = entry[2]
                time = entry[3]
                if date == prev_date:
                    summary.double_headers.append(date)
                prev_date = date
            gcal_row = [descr] + entry[2:]
            writer.writerow(gcal_row)
    if bakname:
        print("Backed up", bakname, "; ", end="")
    print("Wrote", basename + ext, "; rows (incl playoffs):", len(schedule))
    return summary

def get_summary_file_name(csvfile):
    " Rename schedule*.csv to summary*.txt, or as close as it can get "
    nosuf = csvfile.rsplit(".", 1)[0] # Note: keeps root if no dot
    if nosuf.startswith("schedule-"):
        root = nosuf.split("-", 1)[1]
    else:
        root = nosuf
    return "summary-" + root + ".txt"

def process_schedule(csvfile):
    schedule, playoffs = read_csvfile(csvfile)
    if verbose:
        for row in schedule:
            print(row)
        for row in playoffs:
            print(row)
    team_schedules, team_histos = filter_team_schedules(schedule, playoffs)
    team_summaries = dict()
    for team in sorted(team_schedules):
        summary = write_team_schedule(team, team_schedules[team])
        team_summaries[team] = summary
    summfile = get_summary_file_name(csvfile)
    with open(summfile, 'w') as summary_fp:
        print_team_histos(team_histos, summary_fp)
        print_summaries(team_summaries, summary_fp)
    # echo summary to stdout
    with open(summfile) as fp:
        print(fp.read(), end="")

def compare_schedules(csv1, csv2):
    schedule1, playoffs1 = read_csvfile(csv1)
    schedule2, playoffs2 = read_csvfile(csv2)
    ok1 = compare_lists(schedule1, schedule2)
    ok2 = compare_lists(playoffs1, playoffs2)
    return ok1 + ok2

def get_url():
    url = (f"https://docs.google.com/spreadsheets/d/{DOC_KEY}/export?" +
           f"format=csv&id={DOC_KEY}&gid={SCHED_GID}")
    print("URL:", url)
    return url

def do_download():
    url = get_url()
    today = datetime.today().strftime('%Y-%m-%d')
    basename = f"schedule-{today}"
    ext = ".csv"
    bakname = mvbak(basename, ext)
    if bakname:
        print("Backed up", bakname)
    outfile = basename + ext
    print("OUTFILE:", outfile)
    urllib.request.urlretrieve(url, outfile)
    return outfile

if __name__ == "__main__":
    csv1 = None
    csv2 = None
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            if arg == '-':
                print("Malformed arg -")
                sys.exit(1)
            for c in arg[1:]:
                if c == 'c':
                    clobber = True
                    continue
                if c == 'd':
                    download = True
                    continue
                if c == 'v':
                    verbose = True
                    continue
                print("Unrecognized option", c, "in", arg)
                sys.exit(1)
            continue
        if not csv1:
            csv1 = arg
            continue
        if not csv2:
            csv2 = arg
            continue
        print("Too many arguments")
        sys.exit(1)
    if not csv1 and not download:
        print(__doc__)
        sys.exit(1)
    if download:
        assert not csv1
        outfile = do_download()
        assert outfile is not None
        process_schedule(outfile)
    elif not csv2:
        process_schedule(csv1)
    else:
        rv = compare_schedules(csv1, csv2)
        sys.exit(rv)
