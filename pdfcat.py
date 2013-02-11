#!/usr/bin/env python

'''Concatenate input pdfs to an output pdf using OS X's built-in PDFKit framework.
   Should work with any recent OS X\'s system Python out of the box.'''

import optparse
import os
import sys
import objc
from Quartz import *

__author__ = 'Ben Nham'
__license__ = 'WTFPL'

parser = optparse.OptionParser(usage='pdfcat [-f] 1.pdf 2.pdf 3.pdf ... output.pdf')
parser.add_option('-f', '--force', action='store_true', dest='force', help='force write even if output.pdf exists, or if input pdf can\'t be opened')

options, args = parser.parse_args()

if len(args) < 2:
    parser.error('Must specify at least one input file and one output file.')

dstpath = args[-1]
paths = args[:-1]

if os.path.exists(dstpath) and not options.force:
    parser.error('Bailing since %s already exists. Use -f to force overwrite.' % dstpath)

dstdoc = PDFDocument.alloc().init()

for path in paths:
    doc = PDFDocument.alloc().initWithURL_(NSURL.fileURLWithPath_(path))

    if not doc:
        if not options.force:
            parser.error('Bailing since %s can\'t be opened. Use -f to force creation anyway.' % path)
        else:
            continue
    
    for i in range(doc.pageCount()):
        page = doc.pageAtIndex_(i)
        dstdoc.insertPage_atIndex_(page, dstdoc.pageCount())

dstdoc.writeToFile_(dstpath)
