#!/usr/bin/python

import os, sys

#----------------------------------------------------
class MyError(Exception):
    def __str__(self):
        return "\n" + self.args[0] + """

Usage: leaf.py pids [kill[1][=timelimit|process]]
                    [-cwd]
                    [-v(erbose)]
                    [-q(uiet)]
                    [-t(ree)]
                    [-a(ll)]

Reports the leaves of the process trees rooted at the given pids.
You can use the pseudo-pid value of 1 for the root of the process tree.

Other options:
 kill: Kill orphans
 kill=n,kill1=n: Leaves whose age is >= n seconds will be killed (0 kills all
                 leaves); kill1 will only kill the first matching process.
 kill=proc,kill1=proc: Kill leaves named proc (0=kill all, 1=kill first match)
 -a(ll):  Don't exclude processes. By default, excludes memusage_probe.
 -t(ree): Print the process tree (diagnostic output).
 -cwd:    Print the cwd of each process.
        """

#----------------------------------------------------
def proc_stats(pid):
    """
Read /proc/<pid>/stat and split it into an array, recognizing that the second
token '(process name)' may contain spaces and parens, etc.!
Return None to indicate the stat file (thus the process) doesn't exist.
    """
    try:
        stats_line = open(os.path.join('/proc', str(pid), 'stat')).read()
    except IOError as err:
        return None
    rparen = stats_line.rfind(') ')
    if rparen == -1:
        raise MyError("no rparen in /proc/%s/stat" % pid)
    stats_front = stats_line[:rparen+1]
    stats_back = stats_line[rparen+2:]
    stats = stats_front.split(' ', 1) + stats_back.split(' ')
    # Sanity: check that the 'state' field looks legit:
    #  - man proc claims state is one of "RSDZTW"
    #  - 't' was observed on cub
    #  - 'I' observed on riddle2, not in man page
    if not stats[2] in ['R','S','D','Z','T','t','I']:
        raise MyError("unrecognized status (%s) in /proc/%s/stat" %
                      (stats[2], pid))
    return stats

#----------------------------------------------------
def psppid(pid):
    """
Return the parent pid for the given pid, both as ints.
    """
    # Return the fourth token from /proc/N/stat.
    stats = proc_stats(pid)
    if stats is None: # e.g., <defunct> on cygwin
        return 1      # or return 0?
    ppid = stats[3]
    # NOTE: /proc/N/ppid seems to be a cygwin thing.
    #ppid = open(os.path.join('/proc', str(pid), 'ppid')).read().split()[0]
    return int(ppid)

#----------------------------------------------------
def pstree(exclude):
    """
Collect the process tree, returning two dictionaries:
  children: parent_pid -> list(child_pid)
  parent: child_pid -> parent_pid
Argument exclude gives a list of process names (strings) to exclude.
    """
    children = dict()
    parent = dict()
    for item in os.listdir('/proc'):
        if not item.isdigit():
            continue
        ipid = int(item)

        stats = proc_stats(ipid)
        if stats is None: # e.g., <defunct> on cygwin
            ippid = 1     # or 0?
        else:
            name = stats[1][1:-1] # exclude leading and trailing parens
            if name in exclude:
                continue
            ippid = int(stats[3])

        parent[ipid] = ippid
        if not ippid in children:
            children[ippid] = list()
        children[ippid].append(ipid)
    return (children,parent)

#----------------------------------------------------
def normalize_roots(roots, children, parent):
    """
Eliminate redundant roots.
Filter out roots that are not active processes.
    """
    alive = set()
    for root in roots:
        if root != 1 and not root in parent:
            print "Warning: pid %s not found. Continuing..." % root
            continue
        alive.add(root)
    
    for root in set(alive):
        par = parent.get(root)
        while par is not None:
            if par in alive:
                alive.remove(root)
                break
            par = parent.get(par)
    return list(alive)

#----------------------------------------------------
def psleaves(roots, children, parent):
    """
Find the leaves of the process tree(s) starting at the given roots,
traversing the given children/parent dictionaries.
    """
    pending = list(roots)
    leaves = set()
    while pending:
        cur = pending.pop() # NOTE: reverse order (more efficient?)
        if not cur in children:
            leaves.add(cur)
            continue
        pending.extend(children[cur])
    return leaves

#----------------------------------------------------
def psprint_tree(roots, children, parent):
    """
Print the process tree(s) starting at the given roots,
traversing the given children/parent dictionaries.
    """
    def rprint(pid, level):
        stats = proc_stats(pid)
        if stats is None:
            name = "<orphan>"
        else:
            name = stats[1]
        print "%s-%s %s" % ((level * 4) * ' ', pid, name)
        for child in children.get(pid,[]):
            rprint(child, level + 1)
    for root in roots:
        rprint(root, 0)

#----------------------------------------------------
# Note: proc manpage says starttime is in jiffies.
# Empirically that seems to be the same as sysconf(_SC_CLK_TCK).
# TODO: Confirm that this is so!

def now_in_jiffies():
    return proc_stats(os.getpid())[21]

def psage(pids, verbose=False):
    """
Return a tuple of two lists:
 list 1: a list of pids for which stat failed, indicative of orphanage.
 list 2: a list of tuples (age, pid, comm) sorted by age in descending order,
         where age is the age of the process in seconds, and comm is its
         command string.
    """
    jnow = now_in_jiffies()
    sc_clk_tck = os.sysconf('SC_CLK_TCK')

    out1_orphans = []
    out2_ages = []
    for pid in pids:
        stats = proc_stats(pid)
        if stats is None:
            print "Orphan found (%d)" % pid
            out1_orphans.append(pid)
            continue
        comm = stats[1]
        starttime = stats[21]
        elapsed_s = (int(jnow) - int(starttime)) / sc_clk_tck
        out2_ages.append((elapsed_s, pid, comm))
        if verbose:
            print "Pid %s elapsed %s secs (%s - %s / %s)" % (
                   pid, elapsed_s, starttime, jnow, sc_clk_tck)
    out2_ages.sort(lambda t1, t2: cmp(t2, t1)) # Sort descending
    return (out1_orphans, out2_ages)

#----------------------------------------------------
def pscmdline(pid):
    """
Return the command line for the given process.
    """
    try:
        cmdline = open(os.path.join('/proc', str(pid), 'cmdline')
                      ).read().strip('\0').split('\0')
        return cmdline
    except IOError as err:
        return str(err)

def pscwd(pid):
    """
Return the working directory of the given process.
    """
    return os.readlink(os.path.join('/proc', str(pid), 'cwd'))

#----------------------------------------------------
def pskill(pid):
    """
Kill the process, return true if successful.
    """
    import signal, time
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(2) # Give kill a chance to percolate
        if not os.path.exists(os.path.join('/proc', str(pid))):
            print "Kill(%s, SIGTERM) succeeded" % pid
            return True
    except OSError as err:
        print "Kill(%s, SIGTERM): %s" % (pid, err)
        return False
    print "Kill(%s, SIGTERM) failed" % pid
    try:
        os.kill(pid, signal.SIGKILL)
        time.sleep(2) # Give kill a chance to percolate
        if not os.path.exists(os.path.join('/proc', str(pid))):
            print "Kill(%s, SIGKILL) succeeded" % pid
            return False
    except OSError as err:
        print "Kill(%s, SIGKILL): %s" % (pid, err)
        return False
    print "Kill(%s, SIGKILL) failed - giving up!" % pid
    return False

#----------------------------------------------------
#----------------------------------------------------

def process_roots(roots, exclude, kill=0, timelimit=-1, target=None,
                  print_cwd=False, print_tree=False, verbose=False):
    """
roots = list (non-empty)
exclude = set
kill: 0=no, 1=limit, -1=unlimited
    """

    if sys.platform == 'win32':
        raise Exception("This doesn't work with windows python (try cygwin?)")

    if not roots:
        raise MyError("No roots specified")

    (children,parent) = pstree(exclude)

    roots = normalize_roots(roots, children, parent)

    if verbose:
        print "normalized roots = %s" % roots

    # Print tree if requested
    if print_tree:
        psprint_tree(roots, children, parent)

    leaves = psleaves(roots, children, parent)

    if verbose:
        print "leaves = %s" % leaves

    #for leaf in leaves:
    #    check_ps_age(leaf, int(timelimit), kill)

    (orphaned_leaves, aged_leaves) = psage(leaves, verbose=verbose)

    if verbose or not kill:
        for pid in orphaned_leaves:
            print "Orphan %s" % pid
        for (age, pid, comm) in aged_leaves:
            pretty_age = ""
            if int(age) > 90:
                nmin = float(age)/60.0
                if nmin < 90:
                    pretty_age = " (%.1f m)" % nmin
                else:
                    pretty_age = " (%.1f h)" % (nmin/60.0)
            print "Pid %s %s age %s s%s" % (pid, comm, age, pretty_age)
            if print_cwd:
                print "\tcwd: " + pscwd(pid)

    killed = []
    if kill:
        # First try orphans and their parents
        for pid in orphaned_leaves:
            if pskill(pid): # Not expected to succeed, as orphans are elusive
                killed.append(pid)
                continue
            ppid = psppid(pid)
            if ppid == 1:
                print "Orphan %s has been killed before, skipping..." % pid
                continue
            # Kill ancestor of orphan until successful
            while True:
                if pskill(ppid):
                    killed.append(ppid)
                    break
                ppid = psppid(ppid)
                if ppid == 1:
                    print "Ancestral slaughter of orphan %s failed." % pid
                    break

        # Only continue if no orphans killed
        if not killed and (timelimit >= 0 or target is not None):
            for (age, pid, comm) in aged_leaves:
                do_kill = False
                if timelimit >= 0 and age >= timelimit:
                    do_kill = True
                    print "Pid %s %s elapsed %ss exceeds timelimit %ss." % (
                          pid, comm, age, timelimit)
                elif target is not None and ('(' + target + ')') == comm:
                    do_kill = True
                    print "Pid %s %s matches target %s." % (
                          pid, comm, target)
                if not do_kill:
                    continue

                print "Cmdline: %s" % pscmdline(pid)
                print "Cwd: " + pscwd(pid)

                # This is probably SCons, which isn't easily killed gracefully
                if sys.platform == 'cygwin' and comm == 'python':
                    print "Looks like SCons - can't kill."
                    break

                print "Killing..."
                if pskill(pid):
                    killed.append(pid)
                    if kill == 1: # TODO: enforce other limits
                        break
    return killed

def swyx_excludes():
    """
    Processes to exclude when finding SWYX leaves.
    """
    exclude = set() # processes to exclude (their children are also excluded)

    # Standard exclusions
    # TODO: on cygwin, exclude also dwwin, etc.?
    exclude.add('memusage_probe')
    #exclude.add('memusage_probe.exe') #??
    return exclude

#----------------------------------------------------
if __name__ == "__main__":
    verbose = False
    print_tree = False
    print_cwd = False
    kill = 0
    timelimit = -1
    target = None
    roots = []
    exclude = swyx_excludes()

    for arg in sys.argv[1:]:
        kv = arg.split('=',1)
        if len(kv) == 2:
            key = kv[0].lower()
            if key == 'kill':
                kill = -1
                try:
                    timelimit = int(kv[1])
                except ValueError:
                    timelimit = -1
                    target = kv[1]
                continue
            if key == 'kill1':
                kill = 1
                try:
                    timelimit = int(kv[1])
                except ValueError:
                    timelimit = -1
                    target = kv[1]
                continue
            raise MyError("Unrecognized argument %s" % arg)
        if arg == 'kill':
            kill = -1
            timelimit = -1 # Only kill orphans
            continue
        if arg == 'kill1':
            kill = 1
            timelimit = -1 # Only kill orphans
            continue
        if arg == '-a' or arg == '-all':
            exclude = set() # no exclusions
            continue
        if arg == '-cwd':
            print_cwd = True
            continue
        if arg == '-q' or arg == '-quiet':
            verbose = False
            continue
        if arg == '-t' or arg == '-tree':
            print_tree = True
            continue
        if arg == '-v' or arg == '-verbose':
            verbose = True
            continue
        if arg.isdigit():
            roots.append(int(arg))
            continue
        raise MyError("Unrecognized argument %s" % arg)

    killed = process_roots(roots, exclude, kill, timelimit, target,
                           print_cwd, print_tree, verbose)
    rv = 0
    if kill:
        rv = not killed
    sys.exit(rv)
