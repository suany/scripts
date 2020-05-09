#!/usr/bin/python

# Render an expression containing parens in a tree form.
# NOTE: This version differs from paren.py in that it tries to output lines
# sooner rather than collect everything in memory before outputting everything
# at the end.  However, this version is MUCH slower -- apparently due having
# to keep and manipulate LONG_LINES in memory (where paren.py processes
# individual tokens on the fly and collects much shorter output lines).
# Thus, this version should be considered ABANDONED.

import sys

# Compresses succession of open-parens into one line
do_compression = True

partner = { '(': ')',
            '<': '>',
            '[': ']',
            '{': '}',
          }

LEFT_PAREN = -1
NOT_PAREN = 0
RIGHT_PAREN = 1

def classify(c):
    if c in [ '(', '<', '[', '{', ]:
        return LEFT_PAREN
    if c in [ ')', '>', ']', '}', ]:
        return RIGHT_PAREN
    return NOT_PAREN

#---------------------------------------
# Buffered input with unget

# TODO: wrap this somehow into a buffered input object?
infile = sys.stdin

# Note: a simpler implementation just needs ungetbuf, updating it as
# we go.  This was suspected to be a reason for the LONG_LINES slowdown
# described above, so we keep a fixed ungetbuf and maintain an index to
# it.  This is still slower, however, than paren.py.

ungetbuf = ''
ungetbuf_ptr = 0
def my_fgetc():
    global infile
    global ungetbuf
    global ungetbuf_ptr
    if ungetbuf:
        tmp = ungetbuf[ungetbuf_ptr]
        ungetbuf_ptr += 1
        if ungetbuf_ptr >= len(ungetbuf):
            ungetbuf = ''
            ungetbuf_ptr = 0
        return tmp
    return infile.read(1)

def my_unget(s):
    global ungetbuf
    global ungetbuf_ptr
    ungetbuf = s + ungetbuf[ungetbuf_ptr:]
    ungetbuf_ptr = 0

def my_readline():
    global infile
    global ungetbuf
    global ungetbuf_ptr
    if ungetbuf:
        # Assumes ungetbuf is an entire line (no intervening \n)
        tmp = ungetbuf[ungetbuf_ptr:]
        ungetbuf = ''
        ungetbuf_ptr = 0
        return tmp
    return infile.readline()

#---------------------------------------

def scan_next_token():
    c = my_fgetc()
    if not c:
        return (None, None)
    while c.isspace():
        c = my_fgetc()
        if not c:
            return (None, None)

    tclass = classify(c)
    if tclass != NOT_PAREN:
        return (c, tclass)

    out = c

    while True:
        c = my_fgetc()
        if not c or c.isspace():
            return (out, NOT_PAREN)
        if classify(c) != NOT_PAREN:
            my_unget(c)
            return (out, NOT_PAREN)
        out += c

outlines = []

# TODO: don't have to remember the whole thing
def append_indented_line(indent, s):
    global outlines
    # Compression
    if (do_compression and
        outlines and
        outlines[-1] and
        classify(outlines[-1][-1]) == LEFT_PAREN):
        # unindented
        outlines[-1] += " " + s
    else:
        outlines += [(indent * '  ') + s]


def append_vertical(terms, indent):
    for term in terms:
        append_indented_line(indent, term)

def append_horizontal(terms, indent):
    out = ''
    for term in terms:
        out += " " + term
    if out:
        out = out[1:]
    append_indented_line(indent, out)

def print_vertical(terms):
    for term in terms:
        print term

def treeify_sexpr():
    global outlines
    curterm = []
    horizontal = True
    stack = []
    rv = False

    while True:
        token, tclass = scan_next_token()
        if not token:
            rv = False
            break

        if tclass == LEFT_PAREN:
            append_vertical(curterm, len(stack))
            append_indented_line(len(stack), token)
            curterm = []
            stack += [partner[token[0]]]
            horizontal = True
            continue
        if tclass == RIGHT_PAREN:
            if not stack:
                sys.stderr.write("WARNING: bottom of stack: %s\n" % token)
                rv = True
                break
            else:
                top = stack[0]
                if top == token[0]:
                    del stack[0]
                else:
                    sys.stderr.write(
                            "WARNING: stack mismatch '%s' and '%s'\n" %
                            (top, token[0]))
                    # Note: the following is a half-assed way to treat
                    # the non-matching token like a non-paren, useful
                    # in practice for handling a non-paren '>', for
                    # example.  We live with a linebreak after the
                    # non-matching token, however.
                    if curterm:
                        curterm[-1] += token
                    else:
                        curterm += [token]
                    continue

            if horizontal:
                curterm += [token]
                append_horizontal(curterm, len(stack)+1)
            else:
                append_vertical(curterm, len(stack)+1)
                append_indented_line(len(stack), token)
            curterm = []
            horizontal = False
            if not stack:
                rv = True
                break
            continue
        #else:
        curterm += [token]

    if curterm:
        outlines += ["LEFTOVER:"]
        append_horizontal(curterm, 0)
    print_vertical(outlines)
    outlines = []
    return rv

#---------------------------------------

def echo_til_paren():
    while True:
        line = my_readline()
        if not line:
            return False
        for i in range(len(line)):
            tclass = classify(line[i])
            if tclass == LEFT_PAREN:
                if i > 0:
                    print line[0:i] # NOTE: adds newline
                my_unget(line[i:])
                return True
            if tclass == RIGHT_PAREN:
                sys.stderr.write("WARNING: unmatched %s\n" % line[i])
        print line,

def treeify_file(inf):
    global infile
    infile = inf
    while echo_til_paren() and treeify_sexpr():
        pass

treeify_file(sys.stdin)
