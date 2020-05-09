#!/usr/bin/env python
#
# USAGE: feed input of perf script | ~/FlameGraph/stackcollapse-perf.pl
# To summarize functions of interest, populate target_fns below.
# (NOTE: current summaries are noisy and less than ideal; more tweaks and
#        cleanups needed).

from __future__ import print_function
from __future__ import with_statement

import sys

do_histo = True
target_fns = ['nast_get_field'] # functions to summarize

full_histo = dict()

# Histogram of call-strings.
num_stacktraces = 0
upstream_stacks_forward = dict()
upstream_stacks_backward = dict()
downstream_stacks = dict()

def add_stack(stacks, stack, count):
    ''' Add given stack to the stacks dictionary (representing the tree) '''
    d = stacks
    for fn in stack:
        d = d.setdefault(fn, dict())
    d.setdefault('#', 0)
    d['#'] += count
    
def process_line(line):
    global full_histo
    global num_stacktraces
    global upstream_stacks_forward
    global upstream_stacks_backward
    global downstream_stacks
    sstack, scount = line.rsplit(None, 1)
    count = int(scount)
    stack = sstack.split(';')
    if do_histo:
        for fn in stack:
            full_histo.setdefault(fn, 0)
            full_histo[fn] += count
    for target_fn in target_fns:
        try:
            i = stack.index(target_fn)
            num_stacktraces += 1
            bef = stack[:i+1]
            aft = stack[i:]
            add_stack(upstream_stacks_forward, bef, count)
            bef.reverse()
            add_stack(upstream_stacks_backward, bef, count)
            add_stack(downstream_stacks, aft, count)
        except ValueError:
            pass


def print_histo(histo):
    for k,v in histo.iteritems():
        print(v,k)

def print_stacks(d, count = 0, prefix = []):
    this_count = d.get('#', 0)
    count += this_count
    if this_count:
        print(count, this_count, ';'.join(prefix))
    for k,v in d.iteritems():
        if k != '#' and k != '##':
            print_stacks(v, count, prefix + [k])

def print_tree(d, level = 0):
    if level == 0: # Top-level only
        print(d['##'], '(toplevel)')
    level += 1
    indent = level * '- '
    for k,v in d.iteritems():
        if k != '#' and k != '##':
            print(indent, v['##'], k)
            print_tree(v, level)

def propagate_counts(d):
    assert not '##' in d
    sub_counts = 0
    for k,v in d.iteritems():
        if k != '#':
            sub_counts += propagate_counts(v)
    this_count = d.get('#', 0)
    d['##'] = this_count + sub_counts
    return this_count + sub_counts

def collect_caller_histo(histo, d, prefix = []):
    this_count = d.get('#', 0)
    if this_count:
        for i in prefix:
            histo.setdefault(i, 0)
            histo[i] += this_count
    for k,v in d.iteritems():
        if k != '#' and k != '##':
            collect_caller_histo(histo, v, prefix + [k])

if __name__ == '__main__':
    for line in sys.stdin:
        process_line(line)
    if do_histo:
        print("{ Histogram")
        print_histo(full_histo)
        print("} Histogram")
    if target_fns:
        print("# Stacktraces:", num_stacktraces)
        # Histogram of unique calling contexts -- probably too sparse
        print("{ Backward")
        print_stacks(upstream_stacks_backward)
        print("} Backward")
        print("{ Forward")
        print_stacks(upstream_stacks_forward)
        print("} Forward")
        print("{ Tree")
        propagate_counts(upstream_stacks_forward)
        print_tree(upstream_stacks_forward)
        print("} Tree")
        # Histogram of functions in calling contexts
        # -- recursive contexts will be counted multiple times per call-string
        print("{ Callers")
        caller_histo = dict()
        collect_caller_histo(caller_histo, upstream_stacks_backward)
        print_histo(caller_histo)
        print("} Callers")
        # Histogram of call stacks downstream from targets
        print("{ Downstream")
        print_stacks(downstream_stacks)
        print("} Downstream")
