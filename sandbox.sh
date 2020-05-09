#!/bin/sh

# Ambient variables:
export SANDBOX SY_SANDBOX_LABEL SY_SANDBOX_TILDE
#SY_IDA_HOMES_INITIALIZED: IDA_*_HOME initialization, see sy_ida_init
export IDA_PRO_VERSION IDA_HOME
export SY_ADDL_LABELS # psdk, ppc/arm, etc., 
#SY_ALIAS_GCC_PREFIX SY_SOURCERY_PROCESSOR SY_SOURCERY_PATH
NOTITLE=false

# Push cygwin paths to the end of the search path
# This is to avoid conflicts with vc "link".
push_cyg_path () {
   PATH_NOCYG=`echo $PATH \
             | tr : '\n' \
             | grep -v -e "^/usr/local/bin$" \
                       -e "^/usr/bin$"       \
                       -e "^/bin$"           \
                       -e "^/usr/X11R6/bin$" \
             | tr '\n' : \
             | sed -e 's/:$//'`

   PATH="${PATH_NOCYG}:/usr/local/bin:/usr/bin:/bin:/usr/X11R6/bin"
}

sy_process_sandbox () {
  case "$1" in
    admin) SY_SANDBOX_LABEL=admin
           SANDBOX=
           SY_SANDBOX_TILDE=
           ;;
    nocs) SY_SANDBOX_LABEL=nocs
          SANDBOX=
          SY_SANDBOX_TILDE=
          ;;
    "") SY_SANDBOX_LABEL=
        SANDBOX=
        SY_SANDBOX_TILDE=
        ;;
    /*) SY_SANDBOX_LABEL=`basename "$1"`
        SANDBOX="$1"
        SY_SANDBOX_TILDE="$1"
        ;;
    *) SY_SANDBOX_LABEL="$1"
       SANDBOX="${HOME}/${SY_SANDBOX_LABEL}"
       SY_SANDBOX_TILDE="~/${SY_SANDBOX_LABEL}"
       ;;
  esac

  if [ -n "${SANDBOX}" -a ! -d "${SANDBOX}" ]
  then echo WARNING: does not exist: "${SANDBOX}"
  fi

  # This is used by (Alexey's) hg_pull and svn_pull
  export SB=`basename "${SANDBOX}"`

  if [ -n "${ADDL_PATHS}" ]
  then PATH="${PATH}:${ADDL_PATHS}"
  fi
  export PATH
}

sy_ida_init () {
  if [ "${SY_IDA_HOMES_INITIALIZED}" = 1 ]
  then return
  fi
  export SY_IDA_HOMES_INITIALIZED=1
  if [ "${OS}" = "Windows_NT" ]
  then IDA_INSTALL_ROOT="`cygpath -am "${PROGRAMFILES}"`/DataRescue"
       export IDA45_HOME="${IDA_INSTALL_ROOT}/IDA Pro 4.5"
       export IDA46_HOME="${IDA_INSTALL_ROOT}/IDA Pro 4.6"
       export IDA461_HOME="${IDA_INSTALL_ROOT}/IDA Pro 4.61"
       export IDA47_HOME="${IDA_INSTALL_ROOT}/IDA Pro 4.7"
       export IDA48_HOME="${IDA_INSTALL_ROOT}/IDA Pro 4.8"
       export IDA49_HOME="${IDA_INSTALL_ROOT}/IDA Pro 4.9"
       export IDA491_HOME="${IDA_INSTALL_ROOT}/IDA Pro 4.9.1"
       export IDA49f_HOME="${IDA_INSTALL_ROOT}/IDA Free 4.9"
       export IDA50_HOME="${IDA_INSTALL_ROOT}/IDA Pro 5.0"
       export IDA51_HOME="${IDA_INSTALL_ROOT}/IDA Pro 5.1"
       export IDA52_HOME="${IDA_INSTALL_ROOT}/IDA Pro 5.2"
       export IDA53_HOME="${IDA_INSTALL_ROOT}/IDA Pro 5.3"
       export IDA55_HOME="${IDA_INSTALL_ROOT}/IDA Pro 5.5"
       export IDA56_HOME="${IDA_INSTALL_ROOT}/IDA Pro 5.6"
       export IDA57_HOME="${IDA_INSTALL_ROOT}/IDA Pro 5.7"
       export IDA60_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.0"
       export IDA601_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.0.1"
       export IDA61_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.1"
       export IDA62_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.2"
       export IDA63_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.3"
       export IDA64_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.4"
       export IDA64SP_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.4SP"
       export IDA65_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.5"
       export IDA65SP_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.5SP"
       export IDA66_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.6"
       export IDA67_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.7"
       export IDA68_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.8"
  else IDA_INSTALL_ROOT=/usr/local/idapro
       export IDA55_HOME="${IDA_INSTALL_ROOT}/idapro_5.5/idaadv"
       export IDA56_HOME="${IDA_INSTALL_ROOT}/idapro_5.6/idaadv"
       export IDA57_HOME="${IDA_INSTALL_ROOT}/idapro_5.7/idaadv"
       export IDA60_HOME="${IDA_INSTALL_ROOT}/idapro_6.0/ida"
       export IDA601_HOME="${IDA_INSTALL_ROOT}/idapro_6.0.1/ida"
       export IDA61_HOME="${IDA_INSTALL_ROOT}/idapro_6.1/ida"
       export IDA62_HOME="${IDA_INSTALL_ROOT}/idapro_6.2/ida"
       export IDA63_HOME="${IDA_INSTALL_ROOT}/idapro_6.3/ida"
       export IDA64_HOME="${IDA_INSTALL_ROOT}/idapro_6.4/ida"
       export IDA64SP_HOME="${IDA_INSTALL_ROOT}/idapro_6.4SP/ida"
       export IDA65_HOME="${IDA_INSTALL_ROOT}/idapro_6.5/ida"
       export IDA65SP_HOME="${IDA_INSTALL_ROOT}/idapro_6.5SP/ida"
       export IDA66_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.6"
       export IDA67_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.7"
       export IDA68_HOME="${IDA_INSTALL_ROOT}/IDA Pro 6.8"
  fi
}

sy_process_ida () {
  sy_ida_init
  case "$1" in
     ""|0|00)
          IDA_HOME=
          IDA_PRO_VERSION=
          ;;
     45|4.5)
          IDA_HOME="${IDA45_HOME}"
          IDA_PRO_VERSION=4.5
          ;;
     46|4.6)
          IDA_HOME="${IDA46_HOME}"
          IDA_PRO_VERSION=4.6
          ;;
     461|4.61)
          IDA_HOME="${IDA461_HOME}"
          IDA_PRO_VERSION=4.61
          ;;
     47|4.7)
          IDA_HOME="${IDA47_HOME}"
          IDA_PRO_VERSION=4.7
          ;;
     48|4.8)
          IDA_HOME="${IDA48_HOME}"
          IDA_PRO_VERSION=4.8
          ;;
     49|4.9)
          IDA_HOME="${IDA49_HOME}"
          IDA_PRO_VERSION=4.9
          ;;
     491|4.9.1)
          IDA_HOME="${IDA491_HOME}"
          IDA_PRO_VERSION=4.9.1
          ;;
     49f|4.9f)
          IDA_HOME="${IDA49f_HOME}"
          IDA_PRO_VERSION=4.9f
          ;;
     50|5.0)
          IDA_HOME="${IDA50_HOME}"
          IDA_PRO_VERSION=5.0
          ;;
     51|5.1)
          IDA_HOME="${IDA51_HOME}"
          IDA_PRO_VERSION=5.1
          ;;
     52|5.2)
          IDA_HOME="${IDA52_HOME}"
          IDA_PRO_VERSION=5.2
          ;;
     53|5.3)
          IDA_HOME="${IDA53_HOME}"
          IDA_PRO_VERSION=5.3
          ;;
     55|5.5)
          IDA_HOME="${IDA55_HOME}"
          IDA_PRO_VERSION=5.5
          ;;
     56|5.6)
          IDA_HOME="${IDA56_HOME}"
          IDA_PRO_VERSION=5.6
          ;;
     57|5.7)
          IDA_HOME="${IDA57_HOME}"
          IDA_PRO_VERSION=5.7
          ;;
     60|6.0)
          IDA_HOME="${IDA60_HOME}"
          IDA_PRO_VERSION=6.0
          ;;
     601|6.0.1)
          IDA_HOME="${IDA601_HOME}"
          IDA_PRO_VERSION=6.0.1
          ;;
     61|6.1)
          IDA_HOME="${IDA61_HOME}"
          IDA_PRO_VERSION=6.1
          ;;
     62|6.2)
          IDA_HOME="${IDA62_HOME}"
          IDA_PRO_VERSION=6.2
          ;;
     63|6.3)
          IDA_HOME="${IDA63_HOME}"
          IDA_PRO_VERSION=6.3
          ;;
     64|6.4)
          IDA_HOME="${IDA64_HOME}"
          IDA_PRO_VERSION=6.4
          ;;
     64SP|64sp|6.4SP|6.4sp|641|6.41)
          IDA_HOME="${IDA64SP_HOME}"
          IDA_PRO_VERSION=6.4SP
          ;;
     65|6.5)
          IDA_HOME="${IDA65_HOME}"
          IDA_PRO_VERSION=6.5
          ;;
     65SP|65sp|6.5SP|6.5sp|651|6.51)
          IDA_HOME="${IDA65SP_HOME}"
          IDA_PRO_VERSION=6.5SP
          ;;
     66|6.6)
          IDA_HOME="${IDA66_HOME}"
          IDA_PRO_VERSION=6.6
          ;;
     67|6.7)
          IDA_HOME="${IDA67_HOME}"
          IDA_PRO_VERSION=6.7
          ;;
     68|6.8)
          IDA_HOME="${IDA68_HOME}"
          IDA_PRO_VERSION=6.8
          ;;
     *) return 1 ;;
  esac
  return 0
}

# Arguments are passed to fgrep -v.
remove_from_path () {
  PATH=`echo $PATH \
      | tr : '\n' \
      | fgrep -v "$@" \
      | tr '\n' : \
      | sed -e 's/:$//'`
}

sy_win_python_path () {
  if [ "${OS}" != "Windows_NT" ]
  then return 1
  fi
  case "$1" in
    py25|py26|py27)
      PYVER=`echo $1 | cut -c2-` ;;
    25|26|27)
      PYVER=$1 ;;
    *) return 1 ;;
  esac
  PYPATH="/cygdrive/c/Python$PYVER"
  if [ ! -d "${PYPATH}" ]
  then echo "Error: python path not found: ${PYPATH}"
       return 1
  fi
  remove_from_path -e python -e Python
  PATH="${PYPATH}:${PATH}"
  export PATH
}

sy_sourcery_arm () {

  export SY_SOURCERY_PROCESSOR=arm

  # NOTE: eabi == Embedded ABI
  case `/bin/hostname` in
    cub) # On cub: linux-gnueabi is installed here.
         ARMPATH="/usr/local/CodeSourcery/bin.arm-none-linux-gnueabi"
         PATH="${ARMPATH}:${PATH}"
         export SY_SOURCERY_PATH="${ARMPATH}"
         ;;
    meacham)
         # This is for meacham (Windows)
         export SY_ALIAS_GCC_PREFIX=arm-none-eabi
         # NOTE: already in PATH on meacham:
         # /cygdrive/c/Program Files (x86)/CodeSourcery/Sourcery G++ Lite/
         ;;
    *) SY_SOURCERY_PROCESSOR=ARM_SETUP_INCOMPLETE
       ;;
  esac
}

# Process arguments (all optional) to set the various environment variables
while [ -n "$*" ]
do case "$1" in
     sb=*) sy_process_sandbox `echo "$1" | cut -c4-` ;;
     ida=*) if ! sy_process_ida `echo "$1" | cut -c5-`
            then echo "Warning: invalid IDA version: $1"
            fi
            ;;
     isa=*) export ISA=`echo "$1" | cut -c5-` ;;
     isa=) unset ISA ;;
     py=*) if ! sy_win_python_path `echo "$1" | cut -c4-`
           then echo "Warning: invalid python version: $1"
           fi
           ;;
     push_cyg_path) push_cyg_path ;;
     arm) sy_sourcery_arm
          # swyx-tests Makefile variable:
          export ISA=arm
# For poky, see
#/u4/TARBALLS/neptune/vet-yocto/sdk/environment-setup-armv7a-poky-linux-gnueabi
          ;;
     bc) CYGPROGRAMFILES=`cygpath -a "$PROGRAMFILES"`
         TURBO_C_PATH=`cygpath -a "c:/Program Files/Borland/BDS/4.0/Bin"`
         PATH="${PATH}:${TURBO_C_PATH}"
         ;;
     defida) # Use current default IDA version
             sy_process_ida 6.5SP
             ;;
     linux) # NOTE: i686 for Linux-GNU
            export SY_ALIAS_GCC_PREFIX=i686-pc-linux-gnu
            export SY_SOURCERY_PROCESSOR=linux
            ;;
     nopy) remove_from_path -e python -e Python
           ;;
     nosourcery)
          export SY_SOURCERY_PROCESSOR=
          if [ -n "${SY_ALIAS_GCC_PREFIX}" ]
          then export SY_ALIAS_GCC_PREFIX=
               unalias addr2line ar as c++ c++filt cpp g++ gcc gcov gdb gprof
               unalias ld nm objcopy objdump ranlib readelf size strings strip
          fi
          if [ -n "${SY_SOURCERY_PATH}" ]
          then remove_from_path -e "${SY_SOURCERY_PATH}"
               export SY_SOURCERY_PATH=
          fi
          ;;
     notitle) NOTITLE=true
              title "no title"
              ;;
     ppc) # NOTE: for Linux-GNU (EABI version also available if needed)
          export SY_ALIAS_GCC_PREFIX=powerpc-linux-gnu
          export SY_SOURCERY_PROCESSOR=ppc
          export ISA=ppc
          ;;
     todo) NOTITLE=true
           title "TODO"
           ;;
     *) # For backward compatibility - any other argument is first checked
        # against ida version, then treated as sandbox id.
        sy_process_ida "$1" || sy_process_sandbox "$1"
        #echo "Unrecognized argument $1. Press enter to quit."
        #read whatever
        #exit 1
        ;;
   esac
   shift
done

# CodeSourcery GCC alises
if [ -n "${SY_ALIAS_GCC_PREFIX}" ]
then
   alias addr2line=${SY_ALIAS_GCC_PREFIX}-addr2line
   alias ar=${SY_ALIAS_GCC_PREFIX}-ar
   alias as=${SY_ALIAS_GCC_PREFIX}-as
   alias c++=${SY_ALIAS_GCC_PREFIX}-c++
   alias c++filt=${SY_ALIAS_GCC_PREFIX}-c++filt
   alias cpp=${SY_ALIAS_GCC_PREFIX}-cpp
   alias g++=${SY_ALIAS_GCC_PREFIX}-g++
   alias gcc=${SY_ALIAS_GCC_PREFIX}-gcc
   alias gcov=${SY_ALIAS_GCC_PREFIX}-gcov
   alias gdb=${SY_ALIAS_GCC_PREFIX}-gdb
   alias gprof=${SY_ALIAS_GCC_PREFIX}-gprof
   alias ld=${SY_ALIAS_GCC_PREFIX}-ld
   alias nm=${SY_ALIAS_GCC_PREFIX}-nm
   alias objcopy=${SY_ALIAS_GCC_PREFIX}-objcopy
   alias objdump=${SY_ALIAS_GCC_PREFIX}-objdump
   alias ranlib=${SY_ALIAS_GCC_PREFIX}-ranlib
   alias readelf=${SY_ALIAS_GCC_PREFIX}-readelf
   alias size=${SY_ALIAS_GCC_PREFIX}-size
   alias strings=${SY_ALIAS_GCC_PREFIX}-strings
   alias strip=${SY_ALIAS_GCC_PREFIX}-strip
fi

# Set PS1

if [ "$TERM" = screen ]
then SUANSCREEN_NAME=" ["`echo ${STY} | cut -f2 -d.`"]"
else SUANSCREEN_NAME=
fi

HOSTNAME1=`hostname | cut -c1`

PARENTHETIC=
TITLE_PREFIX=
HOST_PREFIX=

# In .bashrc, I set "ulimit -c 0" to avoid big swyx coredumps.
# However, cso-tests insists on >=3GB of coredumps, so it must run in a special
# shell.  The following warning will hopefully prevent me from running anything
# else from such a shell.
ULIMIT_C=`ulimit -c`
if [ "${ULIMIT_C}" != 0 ]
then TITLE_PREFIX="*CORE_ULIMIT=${ULIMIT_C}*"
fi

if [ -n "{SY_SANDBOX_LABEL}" ]
then TITLE_PREFIX="${TITLE_PREFIX}${SY_SANDBOX_LABEL}: "
fi

if [ -n "${IDA_PRO_VERSION}" ]
then PARENTHETIC="${PARENTHETIC} IDA ${IDA_PRO_VERSION}"
fi
if [ -n "${ISA}" ]
then PARENTHETIC="${PARENTHETIC} ISA=${ISA}"
fi
if [ -n "${SY_SOURCERY_PROCESSOR}" ]
then PARENTHETIC="${PARENTHETIC} sourcery=${SY_SOURCERY_PROCESSOR}"
fi
PARENTHETIC="${PARENTHETIC} ${SY_ADDL_LABELS}"

if [ -n "`echo ${PARENTHETIC}`" ]
then PARENTHETIC=" (`echo ${PARENTHETIC}`)"
fi

if [ -n "${SANDBOX}" ]
then WD_COLOR='`if echo "\w" | fgrep -q '\"${SY_SANDBOX_TILDE}\"'; then echo 2; else echo 3; fi`'
else WD_COLOR=2
fi

TITLE=
if ! ${NOTITLE}
then TITLE_TEXT="${TITLE_PREFIX}"'\W @ \h'"${SUANSCREEN_NAME}${PARENTHETIC}"
     TITLE='\[\033]0;'"${TITLE_TEXT}"'\007\]'
fi
export PS1="${TITLE}"'\[\033[33m\]'${HOST_PREFIX}'\[\033[3'"${WD_COLOR}"'m\]\w>\[\033[0m\]'

# (\033 = escape)
# (\007 = ctrl-G)
#
# DOS window title
#  \033]0;title\007
#
# ANSI sequences
# - colors(C):
#   0-black
#   1-red
#   2-green
#   3-yellow
#   4-blue
#   5-magenta
#   6-cyan
#   7-white
#  - \033[3Cm]      normal foreground
#  - \033[1;3Cm]    bold foreground
#  - \033[4Cm]      background
#  - \033[0m        reset all previous text attrs
#  - \033[1m        bold/bright text
#  - \033[2m        bold off (not reliable; use [0m
#  - \033[4m        underline, or blue
#  - \033[5m        blink, or bright background
#  - \033[7m        reversed text
#  - \033[8m        invisible text
#
# - cursor positions
#  - \033[r;cH      Position cursor at row r and column c
#  - \033[nA        Move cursor n rows up
#  - \033[nB        Move cursor n rows down
#  - \033[nC        Move cursor n columns forward (right)
#  - \033[nD        Move cursor n columns back (left)
#  - \033[6n        Show current cursor position
#  - \033[s         Save current cursor position
#  - \033[u         Restore previously stored cursor position
#
