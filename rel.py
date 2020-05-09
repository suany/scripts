#!/usr/bin/python

import os, sys

def relpath(dir1, dir2=os.curdir, dirsep='/', pardir='..'):
    # Special case
    if dir2 == '/':
        return dir1
    dir1_split = os.path.abspath(dir1).split(os.sep)
    dir2_split = os.path.abspath(dir2).split(os.sep)
    if os.name == 'nt' and dir1_split[0] != dir2_split[0]:
        raise OSError('relpath error')
    i = 0
    while i < min(len(dir1_split), len(dir2_split)):
        if dir1_split[i] != dir2_split[i]:
            break;
        i += 1
    if i == 1: # This means the two paths have no common root directory
        return dir1
    rel_split = [pardir] * (len(dir2_split)-i) + dir1_split[i:]
    return dirsep.join(rel_split)

if __name__ == "__main__":                                    
    new_args = [relpath(arg) for arg in sys.argv[1:]]
    #for arg in new_args:
    #    print arg,
    import subprocess
    subprocess.Popen(new_args)
