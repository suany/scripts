#!/usr/bin/python3
from __future__ import print_function
from __future__ import with_statement
import os
import urllib.request
from datetime import datetime

DOC_KEY = "1KSGk-EbkXGWFUAMsRAsxo2BDrBx3c_DoYziibktN-Xo"
SH_NAME = "Schedule"
SH_ID = "1969887782"

def get_url():
    url = (f"https://docs.google.com/spreadsheets/d/{DOC_KEY}/export?" +
           f"format=csv&id={DOC_KEY}&gid={SH_ID}")
    print("URL:", url)
    return url

def do_download():
    url = get_url()
    today = datetime.today().strftime('%Y-%m-%d')
    outfile = f"schedule-{today}.csv"
    print("OUTFILE:", outfile)
    if os.path.exists(outfile):
        print("ERROR: FILE EXISTS")
        return False
    urllib.request.urlretrieve(url, outfile)
    return True

if __name__ == "__main__":
    do_download()

