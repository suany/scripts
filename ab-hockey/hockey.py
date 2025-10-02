#!/usr/bin/env python3
"""
Usage:
  hockey.py -d

    Download to schedule-{date}.csv.

  hockey.py file1.csv

    Read full schedule, output team-#.csv one for each team.

  hockey.py file1.csv file2.csv

    Compare two full schedules, output diffs.

  hockey.py file1.ics file2.csv

    Compare one team's ics file with csv file, output diffs.

  Options:
    -b  back up team .csv files before overwriting
    -v  verbose
    -vv very verbose
"""


from __future__ import print_function
from __future__ import with_statement
import csv, difflib, os, sys
import inspect
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import urllib.request # TODO: import requests # pip3 install requests

"""
MBA CONSTRAINTS 2024-25:
  Sundays: prefer 9:30pm
 (Sun 10/13 - Fall Break Begins -- low turnout)
 (Wed 10/16 - Instruction Resumes)
  Sun 11/24 - out of town for Thanksgiving
 (Wed 11/27 - Thanksgiving break begins)
 (Sun 12/01 - After Thanksgiving)
 (Mon 12/09 - Last Day of Instruction)
 (Fri 12/13 - Exams Begin)
 (Sat 12/21 - Exams End)
 (Tue  1/21 - Instruction Begins)
 (Sat  2/15 - Feb Break Begins)
 (Wed  2/19 - Instruction Resumes)
  Sun  2/23 - MBA small Feb break -- turnout ok (for playoffs)
 (Sat  3/29 - Spring Break begins)
"""

## Google sheet document key and ID for 2024-25 "Schedule" sheet
## from roster spreadsheet, which imports from goalie signup
DOC_KEY = "1ttVHnN5RidBciGpv9I9GDgvQnjQ9VYObOI0zsuOd8kY"
SCHED_GID = "1969887782"
# TODO?: switch to "Goalie Signup" sheet? but must deal with newline problems
#DOC_KEY = "1r_muHg9Mhz8O4v2Qo4ziHcTdh_zvFvfhKPZJiFvSyHM"

TEAMS = {'A': "Black Sheep",
         'B': "Diane's Dipsticks (blue)",
         'C': "Orcutt (gold)",
         'D': "Mansour's (white)",
         'E': "Ice Cream Bar (teal)",
         'F': "MBA Instant Replay (red)",
         }
# Google sheet download only has month/day, not year
YEAR1 = 2024
YEAR2 = 2025

ICS_START_DATE = "2024-10-06" # for reading ics file when diffing
#PLAYOFF_PRESUMED_START = "2025-02-23" # usual bracket
PLAYOFF_PRESUMED_START = "2025-02-02" # round robin

# Commandline Options: -b -d -v
backup = False
download = False
verbose = False
very_verbose = False

DAYS = {'Sunday'    : 0,
        'Monday'    : 1,
        'Tuesday'   : 2,
        'Wednesday' : 3,
        'Thursday'  : 4,
        'Friday'    : 5,
        'Saturday'  : 6,
        }

def day_nr(iso_weekday):
    return 0 if iso_weekday == 7 else iso_weekday

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
        # matchups = full, matchups2 = up to PLAYOFF_PRESUMED_START
        self.matchups = dict([(t, 0) for t in TEAMS])
        self.matchups2 = dict([(t, 0) for t in TEAMS])
    def ngames(self):
        return sum(self.matchups.values())
    def ngames2(self):
        return sum(self.matchups2.values())

def print_summaries(team_summaries, ofp):
    for team in sorted(team_summaries):
        summary = team_summaries[team]
        print("Double Headers", team, ":", summary.double_headers, file = ofp)
    teams = sorted(TEAMS)
    print("FULL:", file = ofp)
    print("Matchups:", ' '.join(("%4s" % t) for t in teams), file = ofp)
    for team in sorted(team_summaries):
        summary = team_summaries[team]
        print("  Team %-2s" % team, 
              ' '.join(("%4d" % summary.matchups[t]) for t in teams),
              '    Total', summary.ngames(),
              file = ofp)
    print("EXCL PLAYOFFS STARTING", PLAYOFF_PRESUMED_START, ":", file = ofp)
    print("Matchups:", ' '.join(("%4s" % t) for t in teams), file = ofp)
    for team in sorted(team_summaries):
        summary = team_summaries[team]
        print("  Team %-2s" % team, 
              ' '.join(("%4d" % summary.matchups2[t]) for t in teams),
              '    Total', summary.ngames2(),
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
    days = set()
    times = set()
    slots = set()
    for histo in team_histos.values():
        days = days.union(histo.day_histo.keys())
        times = times.union(histo.time_histo.keys())
        slots = slots.union(histo.slot_histo.keys())
    days = sorted(days, key = lambda day : DAYS[day])
    times = sorted(times, key = time_pad)
    slots = sorted(slots, key = lambda dt : (DAYS[dt[0]], time_pad(dt[1])))
    teams = sorted(team_histos.keys())
    # Print Days
    header = "Days " + ' '.join(day[:3] for day in days)
    print(header, file = ofp)
    for team in teams:
        assert len(team) == 1
        tname = " " + team + "   "
        cnts = [("%3d" % team_histos[team].day_histo.get(day, 0))
                for day in days]
        print(tname + ' '.join(cnts), file = ofp)
    # Print Times
    header = "Times " + ' '.join(time_pad(time) for time in times)
    print(header, file = ofp)
    for team in teams:
        assert len(team) == 1
        tname = " " + team + "    "
        cnts = [("%5d" % team_histos[team].time_histo.get(time, 0))
                for time in times]
        print(tname + ' '.join(cnts), file = ofp)
    # Print Slots
    header = "Slots " + '  '.join(day_time_abbrev(slot) for slot in slots)
    print(header, file = ofp)
    for team in teams:
        assert len(team) == 1
        tname = " " + team + "    "
        cnts = [("%3d" % team_histos[team].slot_histo.get(slot, 0))
                for slot in slots]
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

WEEK1 = 40 # 2024-2025 season, week 1 is week 41
BREAKS = [12,13,19] # 12-13 xmas, 19 super bowl

# Input:
#  - ISO weekno starts on Monday.
#  - ISO weekday is 1=Monday to 7=Sunday.
# Normalize:
#  - Make weekno start on Sunday
#  - Add 52 if YEAR2
#  - Start from week 1
def normalize_weekno(weekno, weekday, year):
    n = weekno
    if weekday == 7:
        n += 1
    if year == YEAR2:
        n += 52
    return n - WEEK1

# Given list of gap weeks, divy up into breaks and non-breaks, return list of
# strings.
def gap_descrs(gap):
    bef = []
    brk = []
    aft = []
    for w in gap:
        if w in BREAKS:
            brk.append(w)
        elif brk:
            aft.append(w)
        else:
            bef.append(w)
    #print(gap, "bef", bef, "brk", brk, "aft", aft)
    def gap_msg(kind, weeks):
        return kind + " " + ','.join("%02d" % w for w in weeks)
    rv = []
    if bef:
        rv.append(gap_msg("GAP", bef))
    if brk:
        rv.append(gap_msg("BREAK", brk))
    if aft:
        rv.append(gap_msg("GAP", aft))
    return rv

class GameTime(object):
    def __init__(self, date, time):
        # date format is "Sunday, 9/18"
        sweekday, sdate = date.split(',', 1)
        smonth, sday = sdate.split('/', 1)
        month = int(smonth)
        day = int(sday)
        assert sweekday in DAYS
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
        # Fields of GameTime object
        self.dt = datetime(year, month, day, hour+12, minute)
        self.sday = sweekday # day of week in string form
        self.stime = time # time in string form
        _year, weekno, weekday = self.dt.isocalendar()
        if day_nr(weekday) != DAYS[sweekday]:
            print("date", date, "time", time)
            assert False
        self.weekno = normalize_weekno(weekno, weekday, year)
    def __str__(self):
        return datetime.strftime(self.dt, "%Y-%m-%d %I:%M %p")
    def sdate(self):
        date = datetime.strftime(self.dt, "%Y-%m-%d")
        return date
    def four_tuple(self):
        date1 = datetime.strftime(self.dt, "%Y-%m-%d")
        time1 = datetime.strftime(self.dt, "%I:%M %p")
        dt2 = self.dt + timedelta(minutes=75)
        date2 = datetime.strftime(dt2, "%Y-%m-%d")
        time2 = datetime.strftime(dt2, "%I:%M %p")
        assert date1 == date2 # Not necessarily true if 10:45pm timeslot!
        return (date1, time1, date2, time2)

def trace(row):
    if very_verbose:
        lineno = inspect.currentframe().f_back.f_lineno
        print("TRACE", lineno, row)

def array_get_or_none(arr, idx):
    try:
        return arr[idx]
    except IndexError:
        return None

def csv_reader_to_schedule(reader):
    colkey2colno = None
    schedule = []
    playoffs = []
    # FIXME: separate loop for finding header?
    for row in reader:
        if colkey2colno is None: # Find header
            if row[0] != 'Date':
                trace(row)
                continue
            colkey2colno = process_header(row)
            trace(row)
            continue
        date = row[colkey2colno['Date']]
        if not date:
            # 1. Line immediately after header in Goalies spreadsheet
            # 2. Trailing entries in Goalies spreadsheet
            trace(row)
            continue
        time = array_get_or_none(row, colkey2colno['Time'])
        team1 = array_get_or_none(row, colkey2colno['Team 1'])
        team2 = array_get_or_none(row, colkey2colno['Team 2'])
        if not time:
            # Blank time rows
            assert not team1
            assert not team2
            trace(row)
            continue
        if team1 is None:
            # No games (e.g. break)
            continue
        gtime = GameTime(date, time)
        if (team1.startswith(('Playoff', 'Scrimmage', 'Semifinal')) or
            team1 in ['5th Place', '3rd Place', 'Championship']
            ):
            assert not team2
            playoffs.append([gtime, team1])
            trace(row)
            continue
        if not team1 in TEAMS:
            assert not team2 in TEAMS
            if verbose:
                print('# excluded:', team1, team2, file=sys.stderr)
            trace(row)
            continue
        assert team2 in TEAMS
        schedule.append([gtime, team1, team2])
    assert schedule
    return schedule, playoffs

def read_csvfile(csvfile):
    with open(csvfile, newline='') as fp:
        return csv_reader_to_schedule(csv.reader(fp))

def strip_prefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return None

class IcsReader(object):
    def __init__(self, fp):
        self.fp = fp
        self.begin_vevent = False
        self.eof = False
    def read_until(self, until_lines):
        while not self.eof:
            line = self.fp.readline()
            if not line:
                self.eof = True
                return
            text = line.rstrip()
            if text in until_lines:
                self.begin_vevent = (text == "BEGIN:VEVENT")
                return
            yield text

def read_ics_vevents(reader):
    while not reader.eof:
        if not reader.begin_vevent:
            reader.read_until("BEGIN:VEVENT")
            if reader.eof:
                return
        e_datetime = None
        e_subject = None
        for line in reader.read_until("END:VEVENT"):
            dtstart = strip_prefix(line, "DTSTART:")
            if dtstart:
                assert not e_datetime
                # Format is YYYYMMDDTHHMMSSZ
                dt0 = datetime.strptime(dtstart, "%Y%m%dT%H%M%SZ")
                e_datetime = dt0.replace(tzinfo=timezone.utc)
                continue
            summary = strip_prefix(line, "SUMMARY:")
            if summary:
                assert not e_subject
                e_subject = summary
                continue
        if reader.eof:
            assert not e_datetime
            assert not e_subject
            return
        yield e_datetime, e_subject

def read_icsfile(icsfile):
    tzinfo = None
    rv = []
    with open(icsfile) as fp:
        # Up to first VEVENT
        reader = IcsReader(fp)
        for line in reader.read_until(["BEGIN:VEVENT", "END:VCALENDAR"]):
            # TODO: skip all this, just hardcode UTC vs New_York difference?
            tzstr = strip_prefix(line, "X-WR-TIMEZONE:")
            if tzstr:
                assert tzstr == "America/New_York"
                tzinfo = ZoneInfo(tzstr) # raises ZoneInfoNotFoundError
                continue
        if verbose:
            print("Time zone:", tzinfo)
        if not tzinfo:
            assert False # TODO: just create one
        for zdatetime, subject in read_ics_vevents(reader):
            # zdatetime is UTC, subject is string description
            ldatetime = zdatetime.astimezone(tz = tzinfo)
            ldate = ldatetime.strftime("%Y-%m-%d")
            if ldate < ICS_START_DATE:
                if verbose:
                    print("Skipping", ldatetime, subject)
                continue
            ltime = ldatetime.strftime("%I:%M %p")
            if not subject:
                print("No subject", ldatetime)
                assert false
                continue
            rv.append([subject, ldate, ltime])
    return sorted(rv, key=lambda x:(x[1], x[2]))

def gcal_header():
    return ["Subject", "Start Date", "Start Time", "End Date", "End Time"]

def csv_reader_to_gcal3(reader):
    " Return list of gcal triples (Subject, Start Date, Start Time) "
    processed_header = False
    rv = []
    header = next(reader)
    assert header == gcal_header()
    for row in reader:
        rv.append(row[0:3])
    return rv

def read_gcal_csvfile(csvfile):
    with open(csvfile, newline='') as fp:
        return csv_reader_to_gcal3(csv.reader(fp))

def stringify_elts(tpl):
    return (str(elt) for elt in tpl)

def compare_lists(tuplist1, tuplist2):
    strlist1 = ['\t'.join(stringify_elts(row))+'\n' for row in tuplist1]
    strlist2 = ['\t'.join(stringify_elts(row))+'\n' for row in tuplist2]
    ndiff = 0
    for line in difflib.ndiff(strlist1, strlist2):
        if line.startswith('  '):
            continue
        print(line, end='')
        ndiff += 1
    return ndiff

def filter_team_schedules(schedule, playoffs):
    team_schedules = dict([(team, []) for team in TEAMS])
    team_histos = dict([(team, TimeHisto()) for team in TEAMS])
    for gtime, team1, team2 in schedule:
        entry = [team1, team2, gtime]
        team_schedules[team1].append(entry)
        team_schedules[team2].append(entry)
        team_histos[team1].add(gtime.sday, gtime.stime)
        team_histos[team2].add(gtime.sday, gtime.stime)
    for gtime, descr in playoffs:
        entry = [descr, None, gtime]
        for team in team_schedules:
            team_schedules[team].append(entry)
    return team_schedules, team_histos

def mvbak(basename, ext):
    filename = basename + ext
    if not backup:
        return None, filename
    if not os.path.exists(basename + ext):
        return None, filename
    cnt = 1
    while os.path.exists(basename + ("-%03d" % cnt) + ext):
        cnt += 1
    bakname = basename + ("-%03d" % cnt) + ext
    os.rename(filename, bakname)
    return bakname, filename

class GapFinder(object):
    def __init__(self):
        self.weekno = None
        self.sday = None
    def process(self, weekno, sday3):
        gap_msgs = []
        if self.weekno is not None:
            assert self.sday is not None
            if self.weekno + 1 < weekno:
                gap = range(self.weekno + 1, weekno)
                gap_msgs = gap_descrs(gap)
        self.weekno = weekno
        self.sday = sday3
        return gap_msgs

def write_team_schedule(team, schedule):
    summary = TeamSummary() # double headers, matchups
    basename = 'team-' + team
    csvbakname, csvname = mvbak(basename, ".csv")
    txtbakname, txtname = mvbak(basename, ".txt")
    with open(csvname, 'w', newline='') as ofp, open(txtname, 'w') as tfp:
        writer = csv.writer(ofp)
        writer.writerow(gcal_header())
        prev_date = None
        gap_finder = GapFinder()
        last_weekno = None
        for entry in schedule:
            team1 = entry[0]
            team2 = entry[1]
            gtime = entry[2]
            if team2 is None:
                opponent = ""
                descr = "Hockey " + team1 # "Playoffs/Championship"
                odescr = team1
            else:
                opponent = team1 if team == team2 else team2
                descr = "Hockey vs " + TEAMS[opponent]
                odescr = TEAMS[opponent]
                summary.matchups[opponent] += 1
                if gtime.sdate() < PLAYOFF_PRESUMED_START:
                    summary.matchups2[opponent] += 1
                # collect double headers
                date = gtime.sdate()
                if date == prev_date:
                    summary.double_headers.append(date)
                prev_date = date
            dtimes = gtime.four_tuple()
            gcal_row = [descr] + list(dtimes)
            writer.writerow(gcal_row)
            gap_msgs = gap_finder.process(gtime.weekno, gtime.sday[:3])
            if gap_msgs:
                print(file=tfp)
                for msg in gap_msgs:
                    print(msg, file=tfp)
            if last_weekno != gtime.weekno:
                if last_weekno is not None:
                    print(file=tfp)
                last_weekno = gtime.weekno
            print("%02d" % gtime.weekno, gtime.sday[:3],
                  dtimes[0], dtimes[1], opponent, odescr,
                  file=tfp)
    if csvbakname:
        print("Backed up", csvbakname, "; ", end="")
    if txtbakname:
        print("Backed up", txtbakname, "; ", end="")
    print("Wrote", csvname, txtname, "; rows (incl playoffs):", len(schedule))
    return summary

def get_summary_file_name(csvfile):
    " Rename schedule*.csv to summary*.txt, or as close as it can get "
    nosuf = csvfile.rsplit(".", 1)[0] # Note: keeps root if no dot
    if nosuf.startswith("schedule-"):
        root = nosuf.split("-", 1)[1]
    else:
        root = nosuf
    return ("summary-" + root, ".txt")

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
    summbase, summext = get_summary_file_name(csvfile)
    bakname, summfile = mvbak(summbase, summext)
    if bakname:
        print("Backed up", bakname)
    with open(summfile, 'w') as summary_fp:
        print_team_histos(team_histos, summary_fp)
        print_summaries(team_summaries, summary_fp)
    # echo summary to stdout
    with open(summfile) as fp:
        print(fp.read(), end="")

def compare_csv_schedules(csv1, csv2):
    schedule1, playoffs1 = read_csvfile(csv1)
    schedule2, playoffs2 = read_csvfile(csv2)
    ok1 = compare_lists(schedule1, schedule2)
    ok2 = compare_lists(playoffs1, playoffs2)
    return ok1 + ok2

def compare_gcal_ics_with_csv(ics, csv):
    gcalsched1 = read_icsfile(ics)
    gcalsched2 = read_gcal_csvfile(csv)
    return compare_lists(gcalsched1, gcalsched2)

def get_url():
    gid = "" if SCHED_GID is None else f"&gid={SCHED_GID}"
    url = (f"https://docs.google.com/spreadsheets/d/{DOC_KEY}/export?" +
           f"format=csv&id={DOC_KEY}" + gid)
    print("URL:", url)
    return url

def do_download():
    url = get_url()
    today = datetime.today().strftime('%Y-%m-%d')
    bakname, outfile = mvbak(f"schedule-{today}", ".csv")
    if bakname:
        print("Backed up", bakname)
    print("OUTFILE:", outfile)
    urllib.request.urlretrieve(url, outfile)
    return outfile

if __name__ == "__main__":
    csv1 = None
    csv2 = None
    ics = None
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
                if c == 'i':
                    clobber = False
                    continue
                if c == 'v':
                    verbose = True
                    continue
                if c == 'vv':
                    very_verbose = True
                    continue
                print("Unrecognized option", c, "in", arg)
                sys.exit(1)
            continue
        if arg.lower().endswith('.csv'):
            if not csv1:
                csv1 = arg
                continue
            if not csv2:
                csv2 = arg
                continue
            print("Too many csv arguments")
            sys.exit(1)
        if arg.lower().endswith('.ics'):
            if not ics:
                ics = arg
                continue
            print("Too many ics arguments")
            sys.exit(1)
        print("Unrecognized arguments")
        sys.exit(1)
    if download:
        assert not csv1 and not ics
        outfile = do_download()
        assert outfile is not None
        #process_schedule(outfile)
        sys.exit(0)
    if ics:
        assert csv1 and not csv2
        print("diff", ics, csv1)
        rv = compare_gcal_ics_with_csv(ics, csv1)
        sys.exit(rv)
    if csv1 and not csv2:
        assert not ics
        process_schedule(csv1)
        sys.exit(0) # TODO: return rv?
    if csv1 and csv2:
        assert not ics
        print("diff", csv1, csv2)
        rv = compare_csv_schedules(csv1, csv2)
        sys.exit(rv)
    #else:
    print(__doc__)
    sys.exit(1)
