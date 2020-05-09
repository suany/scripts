#!/usr/bin/python

# Split a file into multiple files at each '^}' delimiter.
# Used in particular to split a dot file generated by swyx.

import sys

if len(sys.argv) != 2:
    print "Expecting one argument (filename)"
    sys.exit(1)


#outprefix = sys.argv[1]
outprefix = "output"
count = 1
outfile = open(outprefix + "-" + str(count) + ".dot", 'w')

infile = open(sys.argv[1], 'r')
for line in infile:
    if outfile.closed:
        if not line.split():
            continue
        count += 1
        outfile = open(outprefix + "-" + str(count) + ".dot", 'w')
    outfile.write(line)
    if line[0] == '}':
        outfile.close()

infile.close()
print "Split into " + str(count) + " files"
