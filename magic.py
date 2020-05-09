#!/usr/bin/python

import struct, sys

#----------------------------------------------------
def check_magic(filename):
    """
    Return (elf|pe|coff, x86|arm|ppc|x64)
    """
    fp = open(filename, 'rb')
    hdr = fp.read(32)
    if struct.unpack("<I", hdr[:4]) == (0x464C457F,): # LE ELF
        #if hdr[4] == '\x01': # elf32
        #if hdr[4] == '\x02': # elf64
        #if hdr[5] == '\x01': # lsb
        #if hdr[5] == '\x02': # msb
        #et = struct.unpack("<H", hdr[16:18])[0]
        #if et == 1: # rel (obj)
        #if et == 2: # exec (exe)
        #if et == 3: # dyn (so)
        em = struct.unpack("<H", hdr[18:20])[0]
        if em == 3:  # x86
            return ("elf","x86")
        if em == 20: # PPC (21==PPC64)
            return ("elf","ppc")
        if em == 40: # ARM
            return ("elf","arm")
        if em == 62: # x64
            return ("elf","x64")
    #if struct.unpack(">I", hdr[:4]) == (0x7F454C46,): # BE ELF
    # TODO: check PE
    return (None, None)


    for binfile in binfiles:
        (fmt, isa) = check_magic(binfile)
        if isa:
            return isa
    return None

def main(argv):
    if not argv:
        print "No file name given"
        return 1
    for arg in argv:
        ret = check_magic(arg)
        print "%s: %s" % (ret, arg)
    return 0

if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)
