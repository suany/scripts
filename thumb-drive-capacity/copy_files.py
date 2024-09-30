from __future__ import print_function

"""
black:  60GB ok
silver: 60GB ok
"""

import os, shutil, sys, time

ROOT = "d:\\"

def mkdir_exist_ok(dirname):
    if os.path.exists(dirname):
        assert os.path.isdir(dirname)
    else:
        os.mkdir(dirname)
    return dirname

def make_one_copy(counter):
    srcdir = "d0000"
    dstdir = mkdir_exist_ok(os.path.join(ROOT, "d%04d" % counter))
    print(counter, ":", end="")
    sys.stdout.flush()
    start = time.perf_counter()
    for i in range(1,21):
        srcfile = os.path.join(srcdir, "f%04d.txt" % i)
        assert os.path.exists(srcfile)
        dstfile = os.path.join(dstdir, "d%04df%02d.txt" % (counter, i))
        print(".", end="")
        sys.stdout.flush()
        shutil.copy(srcfile, dstfile)
    elapsed = time.perf_counter() - start
    print(" - %.1fs" % elapsed) # black: 900s (15m)

def do_copy():
    counter = 1
    try:
        while True:
            make_one_copy(counter)
            counter += 1
    except Exception as e:
        print("\nFailed at counter", counter, e)
        # Failed at counter 4 [Errno 22] Invalid argument


if __name__ == "__main__":
    do_copy()
