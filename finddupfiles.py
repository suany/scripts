#!/usr/bin/python

from __future__ import print_function
from __future__ import with_statement

import hashlib, os, sys

def md5sum(path):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()

def process_file(hash2files, path):
    md5 = md5sum(path)
    files = hash2files.get(md5, [])
    files.append(path)
    hash2files[md5] = files

def process_dir(hash2files, dirname):
    for fname in os.listdir(dirname):
        fullpath = os.path.join(dirname, fname)
        if os.path.isfile(fullpath):
            process_file(hash2files, fullpath)
        elif os.path.isdir(fullpath):
            process_dir(hash2files, fullpath)
        else:
            raise Exception("Bad file: " + fullpath)

if __name__ == "__main__":
    hash2files = dict()
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            process_dir(hash2files, arg)
        elif os.path.isfile(arg):
            process_file(hash2files, arg)
        else:
            raise Exception("Bad arg: " + arg)
    for md5, files in hash2files.items():
        if len(files) > 1:
            print(files)
