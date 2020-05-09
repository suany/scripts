#!/usr/bin/env python
"""
Example from online:

I have a scanned pdf file which has scanned two pages on one virtual page (page
in pdf file).

Is there a script that can convert this pdf file with normal pages (one page
from book = one page in pdf file)?

This script converts stdin to stdout.

"""

import copy, sys
from pyPdf import PdfFileWriter, PdfFileReader
input = PdfFileReader(sys.stdin)
output = PdfFileWriter()

for p in [input.getPage(i) for i in range(0,input.getNumPages())]:
    q = copy.copy(p)
    (w, h) = p.mediaBox.upperRight
    p.mediaBox.upperRight = (w/2, h)
    q.mediaBox.upperLeft = (w/2, h)
    output.addPage(p)
    output.addPage(q)

output.write(sys.stdout)
