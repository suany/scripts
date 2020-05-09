#!/usr/bin/python

# NOTE: see bin/src/paren.c, the C source from which this was translated.
# Render an expression containing parens in a tree form.
# NOTE: This was adapted from stree.cpp which only dealt with scheme
#       s-expressions, and did it pretty well.
#       If using this with C++ template expressions, it's slightly less
#       nice (mainly in the handling of commas) but is otherwise quite
#       usable.
# TODO: Add option to treat commas differently/better?
# TODO: flush outlines (the output lines) regularly to reduce memory
#       footprint? -- unless we feel like doing some post-processing
#       to re-collapse lines or adjust indentations
import sys

# Compresses succession of open-parens into one line
do_compression = True

# When outside of any top-level parens, just echo the output.
echo_when_outside = True

partner = { '(': ')',
            '<': '>',
            '[': ']',
            '{': '}',
          }
left_parens = partner.keys()
right_parens = partner.values()

LEFT_PAREN = -1
NOT_PAREN = 0
RIGHT_PAREN = 1

def classify(c):
    if c in left_parens:
        return LEFT_PAREN
    if c in right_parens:
        return RIGHT_PAREN
    return NOT_PAREN

#---------------------------------------
# Buffered input with unget

# TODO: wrap this somehow into a buffered input object?
unget_buffer = []
def my_fgetc():
    if unget_buffer:
        return unget_buffer.pop(0)
    return sys.stdin.read(1)

def my_ungetc(char):
    unget_buffer.extend(char)

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
            my_ungetc(c)
            return (out, NOT_PAREN)
        out += c

#---------------------------------------

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

def process_til_next_paren():
    """
    Scan non-paren characters and pass them through to outlines.
    Return the first left-paren encountered, or None if EOF.
    (Note: right-parens are passed through without warning - FIXME?)
    """
    global outlines
    curline = ''
    while True:
        c = my_fgetc()
        if not c:
            if curline:
                outlines += [curline]
            return (None, None)
        tclass = classify(c)
        if tclass == LEFT_PAREN:
            if curline:
                outlines += [curline]
            return (c, LEFT_PAREN)
        if tclass == RIGHT_PAREN:
            sys.stderr.write("WARNING: unmatched %s\n" % c)
        if c == '\n' or c == '\r':
            if curline:
                outlines += [curline]
                curline = ''
        else:
            curline += c

def treeify_sexpr():
    global outlines
    curterm = []
    horizontal = True
    stack = []

    while True:
        if echo_when_outside and not stack:
            token, tclass = process_til_next_paren()
        else:
            token, tclass = scan_next_token()
        if not token:
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
            continue
        #else:
        curterm += [token]

    if curterm:
        outlines += ["LEFTOVER:"]
        append_horizontal(curterm, 0)
    print_vertical(outlines)


treeify_sexpr()
