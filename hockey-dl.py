#!/usr/bin/python3
from __future__ import print_function
from __future__ import with_statement
import os
import urllib.request
from datetime import datetime

# ref https://stackoverflow.com/questions/33713084/download-link-for-google-spreadsheets-csv-export-with-multiple-sheets

DOC_KEY = "1KSGk-EbkXGWFUAMsRAsxo2BDrBx3c_DoYziibktN-Xo"
SH_NAME = "Schedule"
SH_ID = "1969887782"

def get_url1():
    # This is a more powerful/complex gviz API, see SO link above.
    # But for some reason, out:csv output has some first column cells empty.

    # other options:
    #   tqx=out:json
    #   range=A1:C99
    url = (f"https://docs.google.com/spreadsheets/d/{DOC_KEY}/gviz/tq?" +
           f"tqx=out:csv&sheet={SH_NAME}&headers=0")
    print("URL:", url)
    return url

def get_url2():
    # Simpler export URL.
    url = (f"https://docs.google.com/spreadsheets/d/{DOC_KEY}/export?" +
           f"format=csv&id={DOC_KEY}&gid={SH_ID}")
    print("URL:", url)
    return url

def do_download():
    url = get_url2()
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

