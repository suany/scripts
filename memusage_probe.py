# NOTE: this is unsound, mainly because /proc/<pid>/stat can't reliably
#       delineate the executable name if it contains spaces.

def _usage(errmsg):
    print errmsg
    print "Usage: memusage_probe <period> <pid> <outfile> [<project-descr>]"
    print "  Writes memory usage information every <period> seconds"
    print "  for process <pid> to file <outfile>."
    print "  Optional <project-descr> arguments are just echoed as a comment."
    return 1

def _writeln(outfile, line):
    fp = open(outfile, 'a')
    fp.write(line + "\n")
    fp.close()

def memusage_probe(period, pid, outfile, descr = None):
    if period <= 0:
        return _usage("Invalid period: " + str(period))
    summary_line = ("memusage_probe period=" + str(period) + "s, pid="
                    + str(pid) + ((" : " + descr) if descr else ""))
    _writeln(outfile, "{ begin " + summary_line)
    import os, time
    while True:
        try:
            statf = open(os.path.join('/proc', str(pid), 'stat'))
        except IOError as err:
            break
        stats = statf.read().split()
        statf.close()
        vmbytes = int(stats[22])
        vmmb = int(round(float(vmbytes) / (1024*1024)))
        statline = (time.asctime() + "\t" + str(vmmb) + " M")
        _writeln(outfile, statline)
        time.sleep(period)

    _writeln(outfile, "} end " + summary_line)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        sys.exit(_usage("Not enough arguments"))
    memusage_probe(
        int(sys.argv[1]),
        int(sys.argv[2]),
        sys.argv[3],
        sys.argv[4] if len(sys.argv) > 4 else None,
        )
