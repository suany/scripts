#!/usr/bin/python

import os, subprocess

skip_svn = True
skip_git = True
run_vi = False # FIXME: doesn't work (tty issue)

ans = []

for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        if filename.startswith(".") and filename.endswith(".swp"):
            editfile = os.path.join(dirpath, filename[1:-4])
            print editfile
            ans += [editfile]
    if skip_svn:
        try: dirnames.remove(".svn")
        except ValueError: pass
    if skip_git:
        try: dirnames.remove(".git")
        except ValueError: pass

if ans and run_vi:
    subprocess.Popen(['vi', '-o'] + ans)
