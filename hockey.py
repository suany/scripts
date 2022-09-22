from __future__ import print_function
from __future__ import with_statement
import csv, difflib, sys
from datetime import datetime, timedelta

TEAMS = set(['A', 'B', 'C', 'D', 'E'])
verbose = False

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
        if colkey2colno is None: # Process header
            colkey2colno = process_header(row)
            continue
        date = row[colkey2colno['Date']]
        assert date
        time = row[colkey2colno['Time']]
        assert time
        team1 = row[colkey2colno['Team 1']]
        team2 = row[colkey2colno['Team 2']]
        if team1 in ['Playoffs', 'Championship']:
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
    year = 2022 if month >= 9 else 2023
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

def gcal_tuple(date, time, descr):
    gdate1, gtime1, gdate2, gtime2 = normalize_date_time(
        date, time, timedelta(minutes=75))
    return [descr, gdate1, gtime1, gdate2, gtime2]

def filter_team_schedules(schedule, playoffs):
    team_schedules = dict([(team, []) for team in TEAMS])
    for date, time, team1, team2 in schedule:
        entry = gcal_tuple(date, time, 'Hockey ' + team1 + ' vs ' + team2)
        team_schedules[team1].append(entry)
        team_schedules[team2].append(entry)
    for date, time, descr in playoffs:
        for team in team_schedules:
            team_schedules[team].append(
                gcal_tuple(date, time, 'Hockey ' + descr))
    return team_schedules

def process_schedule(csvfile):
    schedule, playoffs = read_csvfile(csvfile)
    if verbose:
        for row in schedule:
            print(row)
        for row in playoffs:
            print(row)
    team_schedules = filter_team_schedules(schedule, playoffs)
    for team, schedule in team_schedules.items():
        outfilename = 'team-' + team + '.csv'
        with open(outfilename, 'w') as ofp:
            writer = csv.writer(ofp)
            writer.writerow(gcal_header())
            for entry in schedule:
                writer.writerow(entry)
        print("Wrote", outfilename)

def compare_schedules(csv1, csv2):
    schedule1, playoffs1 = read_csvfile(csv1)
    schedule2, playoffs2 = read_csvfile(csv2)
    ok1 = compare_lists(schedule1, schedule2)
    ok2 = compare_lists(playoffs1, playoffs2)
    return ok1 + ok2

if __name__ == "__main__":
    csv1 = None
    csv2 = None
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            if arg == '-v':
                verbose = True
                continue
            print("Unrecognized option", arg)
            sys.exit(1)
        if not csv1:
            csv1 = arg
            continue
        if not csv2:
            csv2 = arg
            continue
        print("Too many arguments")
        sys.exit(1)
    if not csv1:
        print("Usage: hockey.py csvfile [csvfile2]")
        sys.exit(1)
    if not csv2:
        process_schedule(csv1)
    else:
        rv = compare_schedules(csv1, csv2)
        sys.exit(rv)