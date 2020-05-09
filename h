#!/bin/sh
######################################################################
if [ "$1" ]
then if [ "$1" = "vi" ]
     then vi $0
     else awk "BEGIN {x=0} /^#[^ ]/ {x=0} /^# ?$1/ {x=1} {if(x)print}" < $0
     fi
else tail +12 $0
fi
exit
######################################################################

#ascii:+-0-1-2-3--4-5-6-7----8-9-a-b--c-d-e-f-+---+---
 32|x20|   ! " #  $ % & '    ( ) * +  , - . / |x2f| 47
 48|x30| 0 1 2 3  4 5 6 7    8 9 : ;  < = > ? |x3f| 63
 64|x40| @ A B C  D E F G    H I J K  L M N O |x4f| 79
 80|x50| P Q R S  T U V W    X Y Z [  \ ] ^ _ |x5f| 95
 96|x60| ` a b c  d e f g    h i j k  l m n o |x6f|111
112|x70| p q r s  t u v w    x y z {  | } ~   |x7f|127
---+---+-0-1-2-3--4-5-6-7----8-9-a-b--c-d-e-f-+---+---
160|xa0|   ¡ ¢ £  ¤ ¥ ¦ §    ¨ © ª «  ¬ ­ ® ¯ |xaf|175
176|xb0| ° ± ² ³  ´ µ ¶ ·    ¸ ¹ º »  ¼ ½ ¾ ¿ |xbf|191
192|xc0| À Á Â Ã  Ä Å Æ Ç    È É Ê Ë  Ì Í Î Ï |xcf|207
208|xd0| Ð Ñ Ò Ó  Ô Õ Ö ×    Ø Ù Ú Û  Ü Ý Þ ß |xdf|223
224|xe0| à á â ã  ä å æ ç    è é ê ë  ì í î ï |xef|239
240|xf0| ð ñ ò ó  ô õ ö ÷    ø ù ú û  ü ý þ ÿ |xff|255
---+---+-0-1-2-3--4-5-6-7----8-9-a-b--c-d-e-f-+---+---

#apt-get
# source libc6   # no need su, fetches into wd

#aiff to m4a
# ffmpeg aiff to 

    # constant bit-rate (CBR) -- nah
 x  ffmpeg -i $X.aiff -c:a aac -b:a 160k $X-c.m4a

    # variable bit-rate (VBR) -- generally better (2=quality)
 *  ffmpeg -i $X.aiff -c:a aac -q:a 2 $X-v.m4a


#aslr
Disable for one process: setarch `uname -m` -R /bin/bash

#bash
# set -o vi|emacs

alt-f/alt-b: skip words

c-r: history

#cols
# columns
         1         2         3         4         5         6         7         8
12345678901234567890123456789012345678901234567890123456789012345678901234567890

#configure --prefix=<target> CFLAGS="-g -O2"

#ctype
# isalpha etc.
Valid range is -1(EOF) and [0,255]
Underrun happens when passing in, e.g., -2.
for char c: isalpha((unsigned char) c);
for int i = getchar(); // precisely the valid range
    isalpha(i); --> ok
    isalpha((unsigned char)c); --> BAD (EOF -> 255)

#cygpath ->
# readlink -f

#cygwin
# bash cr/lf problem
stable: 3.1-6
or try: 3.1-9 but put "shopt -s igncr" in .bashrc
 (partial solution; doesn't work if invoked as "sh")
 (FMI: http://cygwin.com/ml/cygwin-announce/2006-10/msg00000.html)

#cygwin
# passwd
mkpasswd -l -d > /etc/passwd
mkgroup  -l -d > /etc/group

#cygwin
# rebaseall
- to resolve fork errors:
  - kill all cyg processes
  - c:\cygwin\bin\dash -c /usr/bin/rebaseall
    (or ash)

#cygwin install
ctags
gmake
netcat
patch
psmisc: pstree
sharutils: uuencode
subversion
time
!cvs!

#cygwin
# bash
# complete (smart completion)
Disable in bash: shopt -u progcomp
    (re-enable): shopt -s progcomp
To leave it on, but eliminate rules: complete -r
(Just "complete" to see current settings).

Directory expansion: shopt -s direxpand (starting >= 4.2.29, not on gem,cub)


#cl:
cl /c /Fa[assembly-file-name]
cl /FAcs -> output assembly in .cod file
cl /Fe[exe-file-name]
parallel builds: cl /MP (new in VC9, undoc in VC8)
# vcbuild: cl /M<x> for <x> parallel builds
# masm: ml /Fl -> listing

#cleanup
# du
/cygdrive/c/Documents and Settings/suan/Local Settings/Temp


#codesourcery
# sourcery
# ppc: powerpc-linux-gnu-gcc
# arm: arm-none-eabi-gcc
  in c:/Program Files/CodeSourcery/Sourcery G++ Lite/bin

#cpp -H        // shows includes
# gcc -Wp,-H   // shows includes

#cpu
# cores
windows:
  wmic cpu get DeviceID,NumberOfCores,NumberOfLogicalProcessors
  wmic cpu get /Format:List


#ctags
# tags
# vim
ctags -R                     -> output "tags" file in working directory
.vimrc    set tags=tags;/    -> recurse up to look for "tags" file
vi        :tag foo
          ctrl-]
          :tselect foo       -> choose from multiple
          :tags              -> list window history

          :set nu(mber)      -> line numbers, :set nu! to disable

#cygcheck -cd
cygcheck -c cygwin


#docker
- needs Linux 3.10.0 or newer (colden ok, cub no)
- colden:
  - see sy-docker (aws)
  - also, aliased 'dr'
- NOTE: docker uses space on /var/lib by default (on oak, at least)

#dos
# batch files

%1    The normal parameter.
%~f1  Expands %1 to a fully qualified pathname.
      If you passed only a filename from the current directory,
      this parameter would also expand to the drive or directory.
%~d1  Extracts the drive letter from %1.
%~p1  Extracts the path from %1.
%~n1  Extracts the filename from %1, without the extension.
%~x1  Extracts the file extension from %1.
%~s1  Changes the n and x options’ meanings to reference the short name.
      You would therefore use %~sn1 for the short filename and %~sx1
      for the short extension.

%~dp1 Expands %1 to a drive letter and path only.
%~sp1 For short path.
%~nx1 Expands %1 to a filename and extension only.

if not defined foo ()
if errorlevel N ()  == if [ $? >= N ]
if exist <filename> ()
for %%a in (1 2 3) do @echo %%a
for /l %%a in (1,1,10) do @echo %%a

#dot:
dot -Tgif < input > output
    -Tcmapx = imagemap: digraph G {
                          URL="...";
                          command [URL="..."];
                          command -> output [URL="..."];
                        }
rankdir = LR

# zgrv viewer: use svg format

#escape sequences:
# title:
DOS window title:  \033]0;title\007
  (\033 = escape) (\007 = ctrl-G)

#ansi
# escape sequences:
# colors(C):   (\033 = escape)
   0-black   ([30mblack[0m)
   1-red     ([31mred[0m)
   2-green   ([32mgreen[0m)
   3-yellow  ([33myellow[0m)
   4-blue    ([34mblue[0m)
   5-magenta ([35mmagenta[0m)
   6-cyan    ([36mcyan[0m)
   7-white   ([37mwhite[0m)
  \033[3Cm]     normal foreground
  \033[1;3Cm]   bold foreground
  \033[4Cm]     background
  \033[0m       reset all previous text attrs
  \033[1m       bold/bright text
  \033[2m       bold off (not reliable; use [0m
  \033[4m       underline, or blue
  \033[5m       blink, or bright background
  \033[7m       reversed text
  \033[8m       invisible text

#ansi
# escape sequences:
# cursor positions:    (\033 = escape)
  \033[r;cH     Position cursor at row r and column c
  \033[nA       Move cursor n rows up
  \033[nB       Move cursor n rows down
  \033[nC       Move cursor n columns forward (right)
  \033[nD       Move cursor n columns back (left)
  \033[6n       Show current cursor position
  \033[s        Save current cursor position
  \033[u        Restore previously stored cursor position


#exif facebook panorama
(did not work:)
exif -c --ifd=0 -t Make --set-value=Apple -o output1.jpg input.jpg
exif -c --ifd=0 -t Model --set-value="iPhone 5s" -o output2.jpg output1.jpg


#ffmpeg -ss HH:MM:SS.000 -i in.mp4 [-ss 0] [-t HH:MM:SS.000] -c copy out.mp4
# order matters:
#   -i -ss: slower -- SY: audio timing off!
#   -ss -i: faster -- SY: finds nearest keyframe
#   -ss -i -ss: input and output start time
# -ss = start
# -t = duration
# -to = end (newer feature -- not available with -ss -i)
# -c = codec
# -c copy equiv to: -vcodec copy -acodec copy

# TODO: try segments:
#
#  ffmpeg -i <input> -f segments -c copy -reset_timestamps 1 -map 0 out%06d.mp4
# -rest_timestamps: meant to ease playback of generated segments
# -map 0: all streams (default 1st vid and 1st aud, which is normally enough)


# mts to mov
Lossless
--------
1. Works, but Emulsio doesn't like

  ffmpeg -i step-falls.mts -vcodec copy -ab 128000 -f mov step-falls.mov

2. About same as above? (file size almost the same!)

  ffmpeg -i input.mts -c:v copy -c:a aac -strict experimental -b:a 128k out.mp4

Re-encoding
-----------

  ffmpeg -i input.mts -vcodec libx264 -crf 10 -ab 128000 -vf "yadif" output.mp4

  crf: smaller=higher quality, 0=lossless
       - 10:4x larger, but pretty good quality
       - 20:about same size, but visibly worse

  yadif: deinterlace
    (TODO: experiment with this? maybe emulsio doesn't like interlaced?)
    (-ilme: force interlace?)

  (online instruction: -acodec ac3 ==> result is no audio)

# crop                     "crop=1920:1080:1088:540"       #from 4096x2160
ffmpeg -i in.mov -filter:v "crop=1280:720:320:180" out.mov #from 1920x1080
                           "crop=1024:576:448:252"         #from 1920x1080
                           "crop=1024:576:128:72"          #from 1280x720
       -vb 24M           # to improve quality
       -pix_fmt yuv420p  # IMPORTANT for emulsio and other players
                         # (EOS default 422 seems to confuse them)
       -r 29.97 # downsample for facebook
                # note: SoloShot is 59.94; -> 29.97 looks good
                #                          -> 24 looks jumpy
                # historical fps's are:
                #  24: movies (NTSC: 23.976)
                #  25: Europe (50Hz power)
                #  30: US (60Hz power) (NTSC: 29.970)
                #  60: 2x30 (NTSC: 59.940 <- SoloShot)

# scale: -vf scale=1920:108 (plus -vb 24M -pix_fmt yuv420p)

# transpose: -filter:v "transpose=1,crop=1280:720:320:180"

#gcc -mno-cygwin
#gcc -H ~= cl /showIncludes
#gcc -Wa,-al=<asm_output>

__GNUC__
__GNUC_MINOR__
__GNUC_PATCHLEVEL__

Fewer warnings:
 #pragma GCC system_header

#gcc
# ld/collect2 -m elf_i386
# collect2 -m elf_i386

#gcc
# LC_ALL=C
Avoids special characters in error/warning output.

# ppc little endian
gcc -Wa,-le


#gdb
finish = step out of
next = step over
step = step into
set print object on     # print derived type info from vtable
set env LD_LIBRARY_PATH = y

conditional break point:
(gdb) cond 1 x==y       # 1 == breakpoint number

(gdb) set $mystr = "foo"
(gdb) cond 1 strcmp ( $mystr, s ) == 0

(gdb) print (char[6])*0x1234

# stack: dump the stack
(gdb) x/100x $sp

LOGGING:
set logging redirect on
set logging file <filename>
define hook-stop # only prints on stop, though (e.g., after stepi 100)
 info registers
end

Examing core:
maintenance info sections

# asm
ni/si = assembly
x/i $pc = show asm;  x/3i = show three instrs
display/i $pc = display asm at each break/step

# break at very start: use "starti" for gdb >= 8.1, else this hack:
b *0  // set breakpoint at illegal address 0
run   // triggers error setting breakpoint above
disas  or  x/i $pc  // see where you are (prolly _dlstart)
(don't forget to disable the bad breakpoint from step 1)

# gdbtui (gdb -tui) == curses UI
C-x s = single-key mode
layout asm = assembly

# add-symbol-file <blah.so> 0x<base-ea>
On MVEE with libtwithcer, base-ea is the end-ea of preceding .so
(for normal .so, that is same as so's first ea)

#git
# bundle
cd repo && git bundle create /tmp/bundle-name --all

#git branch workflow
new branch xxx:   git checkout -b xxx --track (== branch [--track] && checkout)
commits, then
push new branch:  [xxx] git push -u origin xxx
           then:  [xxx] git push origin HEAD

rebase:           [xxx] git rebase origin/master
then force push:  [xxx] git push origin HEAD --force-with-lease
                        # checks for unexpected commits; else -f/--force

before merge req: [xxx] git checkout -b yyy --track
after merge:      [yyy] git rebase origin/master
if interference:  [yyy] git checkout -b zzz --track
                  [zzz] git --no-pager rebase -i yyy^

delete branch:    git push origin --delete xxx
                  git branch -d xxx

#git
info/status:
  list (recursive): git ls-tree --full-tree -r --name-only HEAD
  log = git dump NNN
  new local files: git ls-files --others --directory
  origin = git remote show [origin] / git config --get remote.origin.url
           git remote -v
  tree: git log --graph
  clean: git clean -x -d [-f]
         -x: also clean git-ignored files
         -d: delete directories too
         -e patt: exclude pattern
         -n: dry-run
         -f: required to actually do it (unless git configured otherwise)

branch: checkout existing remote:
        git fetch [origin [BNAME]]       # origin optional with git > 1.6.6
        git checkout -b BNAME origin/BNAME

diff branches:
  git diff [--name-status] branch1..branch2 [-- file1 file2]
  -> three dots: branch1...branch2: changes since branch point
  ==> A..B:  history(B) minus history(A)   ==   ^A B
  ==> A...B: (history(A) U history(B)) minus (history(A) intersect history(B))

show commit:
  git format-patch -1 HEAD|<sha> 
  git diff <sha>^1 <sha>

interactive rebase: git rebase -i HEAD~n  # n=last n commits to inspect
 - drop (or remove line)
 - squash/fixup -- former combines commit msgs, latter deletes

git cherry-pick b354cd7 ==opposite of== git revert b354cd7
git cherry-pick h1^..h2 # h1>=range>=h2 (note the "^", else h1>range>=h2)

pull -r --- NEVER JUST "git pull"  (r=rebase)
pull --rebase=preserve: preserve merges (-> git rebase -p)

rebase (eschulte): git pull -r -X ours
 -r=rebase
 -X=merge strategy
or: git fetch -r

rename branch:
  git branch -m old_name new_name
  git push origin :old_name new_name
  git push origin -u new_name

revert:
 - everything: git reset
 - one file: git checkout [HEAD] [--] file1 file2
   -- is for clarity in case file1 conflicts with git command
 - path (e.g., tsl/cir): git checkout HEAD -- path

#git
# stash save 'description message'
# stash apply stash@{0}  # 0th=top, 1, 2...
# stash show    [stash@{N}]     (list)
# stash show -p                 (diff)

#google
# cpuprof (cpuprof=1, default)
# hprof   (hprof=1, default but disabled in overnite)
# profiler
SWYX_CPU_PROF='phase=/outfile'
third-party/google-perftools/src/pprof --pdf /path2binary /outfile > out.pdf

CPUPROFILE_REALTIME=1      # vs. CPU type. not recommended by google?
CPUPROFILE_FREQUENCY=50    # hertz: default 100; 50 good for short pgms;
                           #        smaller to avoid int overflow.

#binary
# hex
# xxd
# vim hex (xxd)
:%! xxd
:%! xxd -r

#ipad
# iphone
# itunes backup
$APPDATA/Apple Computer/MobileSync/Backup
where
  APPDATA=/cygdrive/c/Users/suan/AppData/Roaming

#dns flush
# ipconfig /flushdns

#link
# ppc
# ld -EL -o foo.elf foo.o 
(EL=little-endian)

#msdev:
msdev x86fe.dsw
  /MAKE "x86plugin - Win32 Debug"
[ /CLEAN | /REBUILD ]
  /OUT outfile.txt

dsp/plg:
 when building x.dsp, see x.plg for log file!

#net use drive: \\computer\directory [password|?]
  ?          - prompt for password (not needed if password is required)
  /SAVEPW:NO - don't save password in password-list file!
               (password-list cached in .pwl file)
# sshd
  net start sshd
  net stop sshd

#cvs (colby)
  (mkdir ~/CVS/CVSROOT)(setenv CVSROOT ~/CVS)-or-(cvs -d ~/CVS ...)
  cd new-module-dir
  cvs import proj-name vendor-tag release-tag
  -> imports files in *current* dir-tree into new project called proj-name
  -> vendor/release-tag need to be different (e.g. vYY-MM-DD/rYY-MM-DD)
     (use GrammaTech/start?)
  cvs checkout proj-name
  -> create new working copy
  cvs update
     -A reset sticky tags

#idag help

__IDA_VERSION__ (>=5.1)
python: idc.Eval("\"x\" + __IDA_VERSION__")[1:] 


#lncs:
# pstops '4:0L@.95(24cm,-3cm)+1L@.95(24cm,10cm),2R@.95(-2.5cm,31cm)+3R@.95(-2.5cm,18cm)'

#makefile:
$(addsuffix .c, $(STEMS))

 # Hack approach to figure out where this Makefile is located.
 # NOTE: This only works if this file is included from
 # subdirectories of the current directory!
THIS_MAKEFILE_PATH = $(shell ( \
                        while ! grep -F XXX_FOO_BAR_DUMMY_STRING_YYY Makefile.decomp > /dev/null 2>&1 ; \
                        do cd .. ; \
                           pwd | grep '^/*$$' > /dev/null 2>&1 && exit 1 ; \
                        done ; \
                        cygpath -am . ; \
                      ))

ifeq ($(THIS_MAKEFILE_PATH),)
$(error You can only include Makefile.decomp from a subdirectory)
endif

#java:
java -Xms64m -Xmx256m
starting/max heap size (m=mb, k=kb)

# jar:
jar tf file.jar     #list     (or jar t [files] < file.jar)
jar xf file.jar     #extract  (or jar x [files] < file.jar)
java -jar file.jar  #runs app specified by 'Main-Class' manifest

#keyboard
# caps lock
# remap
REGEDIT4

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layout]
"Scancode Map"=hex:00,00,00,00,00,00,00,00,02,00,00,00,1d,e0,3a,00,3a,00,1d,e0,00,00,00,00 

00,00,00,00, // header 1
00,00,00,00, // header 2
02,00,00,00, // header 3: number of mappings (incl null terminator)
1d,e0,3a,00, // 3a (caps lock) -> e01d (right ctrl)
3a,00,1d,e0, // e01d () -> 3a (caps lock)
00,00,00,00  // null terminator

--> must reboot <--


#kill:
taskkill /pid n /f  # /f=force
tskill              # problem: killed process returns 0!
tasklist
taskmgr (gui)
taskman (cmd line? or tray startup?)

# tasklist:
 /V       to show all columns (e.g. cputime)
 /FO CSV  to output csv
 /M       show dll info (or, e.g., /m cygwin1.dll)

# pslist (from sysinternals.com)
 -m   memory-oriented information
 -t   process tree

# pstree -Alp
 -A = ascii
 -l = long lines
 -p = pids


#macho
# otool or nm   on   hedges or lime
otool -l    # sections etc
otool -ttV  # approx objdump

#nonascii
# vim nonascii : /[^ -~]

#patch -p0 --binary < filename
 --binary: to handle CRLF issues
 --dry-run: see if any problems

#pdf select pages 3-4
pdftk A=input.pdf cat A3-4 output output.pdf

#perf
# flame graph
# FlameGraph
NOTE: our perf versions are old and don't support useful things like --children

> perf record -F 99 -a -g -- cmd
--> -F=frequency(Hz)
--> -a=all processes: omit to just record cmd (and children?)
--> need sudo to get necessary data, so:
    > sudo perf record -F 99 -a -g -- su suan
    --> run command in that shell (will need to re-establish envvars)

> perf script | ~/FlameGraph/stackcollapse-perf.pl > out.perf-folded
--> ~/FlameGraph from https://github.com/brendangregg/FlameGraph

> perf report -n
--> summary, but top-level count doesn't include childen
    (want --children support from new versions, default in even newer versions)

> python ~/scripts/sy-perf-children.py < out.perf-folded
--> counts samples including children (towards perf report --children)

> ~/FlameGraph/flamegraph.pl out.perf-folded > out.svg


#port: which process is listening?
Windows: netstat -a -b (-n = skip nslookup, faster)


#pytest
# tempdir = C:\temp

#python
import inspect
print '\n'.join(["%s---%s" % (x,y) for x,y in inspect.getmembers(XXX)])

#python
# class
Definitely init class in __init__ instead of inline, because:
    class Foo():
        foo = dict()
means ALL INSTANCES of Foo will share the same dict!

#qemu third-party/qemu
# arm: ./configure --target-list=arm-linux-user --cxx=g++ --prefix=<destdir>

(see ~/scripts/qarm)

run: bin/qemu-arm -cpu cortex-a8 <path-to-arm-exe> 
dynamic: pass to qemu-arm:
-L /usr/local/CodeSourcery/Sourcery_CodeBench_Lite_for_ARM_GNU_Linux/arm-none-linux-gnueabi/libc
(in which it can find /lib/ld-linux.so.3, etc.)

#rpm extract:
  cd where_you_want_to_be
  rpm2cpio RPM_file | cpio -idv

#readelf -W/--wide

#reboot
# boot
Windows last reboot: net statistics server
Windows shutdown: shutdown -r  # restart (-f = force -- implied after 30 s)
Linux: last reboot

#rpath: chrpath -d (delete), -l (list)

#rundll32
# cmdline windows
rundll32.exe user.exe,ExitWindows
rundll32.exe shell32.dll,SHExitWindowsEx n
 where n is 0:logoff 1:shutdown 2:reboot 4:force 8:poweroff

#rsync
local: rsync -av
remote: rsync -azLe ssh user@host:/path ...
  -a     = archive
  -z     = compress during transmission
  -L     = expand soft links by copying linked file
  -e ssh = specify remote login method
  -v     = verbose
  -n/--dry-run
source/ <- trailing slash important, ~equivalent to source/*

#admin
# runas /user:Administrator <command>

#rxvt
# fonts
xfontsel xlsfonts
/usr/share/fonts/misc/fonts.alias


#scp
scp foo http@www:/home/http/www/foo

#screen -e '^\\\' bash --login -i
 (default command is ^a, overriden to ^\ with above -e change)
 detach: ^\-d
 scrollback/copy: ^\-[ (spacebar to copy)
 paste: ^\-]
 screen -d -r
  --> automatically finds one to reattach
  --> -D -R to create new if none found
  --> screen -list   -- do this before reattaching
http://www.emacswiki.org/emacs/GnuScreen

#shutdown (windows)
 -s shutdown
 -r restart
 -a abort
Default timeout = 30 seconds.


#sort -u = sort -unique
# LC_ALL=C -- to get traditional sort instead of locale-specific (ignores _)
              (also, gcc output excludes special characters)

#special chars
/[^0-9a-zA-Z !"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~]
grep --color='auto' -P -n "[\x80-\xFF]"


#stk
Show trace of file loading:
  (define *load-verbose* #t)

# copy-file
(define (copy-file infname outfname)
   (let ((inf (open-file infname "rb"))
         (outf (open-file outfname "wb")))
     (copy-port inf outf)
     (close-port outf)
     (close-port inf)))

# sleep
(define (sleep n)
  (while (> n 0) (let ((x 1000000))
                   (while (> x 0) (set! x (- x 1)))
                   (set! n (- n 1)))))

#strace
  -o<outfile>       # else -> stderr
  -fF               # follow forked proceses
  -e trace=execve   # limit traced funcs
  -e trace=file     # == trace=open,stat,chmod,unlink...
  -e trace=process  # == trace=fork,wait,...
  -s4000            # string buffer limit (default 32)
  -i                # print EIP


#svn propset svn:executable \* *.exe *.bat *.sh
 svn propset -F .cvsignore svn:ignore .

#svnadmin dump [--incremental -r X:Y] repo > file
# svnadmin load repo < file (after svnadmin create repo, if needed)


#tar
Archive: tar cvf[z] output.tar[.Z] input_path
Extract: tar xvf[z] file.tar[.Z]
List:    tar t[v]f[z] file.tar[.Z]
bzip2 = j


# uw
pts membership suan

#mangle
# demangle
# unmangle
undname /show_flags
undname -f (cl)
c++filt (gcc)
ld --no-demangle

#vc
# return value
$ReturnValue in watch window

#vim http://rayninfo.co.uk/vimtips.html
syntax on       - enable syntax highlighting
set ft=scheme   - set filetype to "scheme"
set runtimepath - see path in which vim files are read
let loaded_matchparen=1 - disable paren-match highlighting (can be slow!)

macro record: qq...q    run: @q

help modeline: embed settings in "  vim:xxx

z=fold: zo(open) zc(close) zf(create) zd(delete) zM/zR(open/close all)
foldmethod/fdm:
  set fdm=indent  (e.g., python)
  set fdm=syntax  (e.g., c/cpp, behavior already defined)
  set fdm=marker  foldmarker = {{{ }}}

case insensitive search: /\cfoo (\C for case sensitive)

source indentation: '='
format paragraph: gqap (gqj for one line, etc.)

window
 C-W x : exchange current window with next
 C-W s : split, new viewport
 C-W = : equal size windows

word wrap:
:set linebreak   " wrap at breakat characters
:set showbreak=> " mark beginning of broken lines (will be colored).
                   (Future: may support A,B, with A at EOL, B at start of next
(also...
 :set wrap        " do wrapping (on by default)
 :set nolist      " list disables wrapping (off by default)
)

#sort
# vim
:sort n
:sort /patt to ignore/ (e.g. for column 2: /^.*\t/)

#vagrant scp <localpath> [vm_name]:<destpath>
2016-07-20:colden> vagrant plugin install vagrant-scp
Installed the plugin 'vagrant-scp (0.5.7)'!

Machine exists: unclear if either is right:
 Option 1: Remove ~/.vagrant.d
 Option 2: vboxmanage list vms
           vboxmanage unregistervm <name> --delete


#wc -L = length of longest line


#which
# where
# type

 # Use this until getting used to using type:
function which() { builtin type "$@"; }
function where() { builtin type -a "$@"; }


#windows update
wmic qfe list full /format:htable (not yet successfully tested)

#wsurf
WINDSURFING-L-REQUEST@cornell.edu
 "join"
 "leave"

http://www.cit.cornell.edu/computer/elist/lyris/join.html

#zip
-x "*/.svn/*" -x "*/_svn/*" -x "*/CSURF.FILES/*"

