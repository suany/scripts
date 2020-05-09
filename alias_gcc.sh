#!/bin/sh

# Use this to switch to different platform gcc and binutils
# (from CodeSourcery)
#
if [ -n "${ALIAS_GCC_PREFIX}" ]
then
   alias addr2line=${ALIAS_GCC_PREFIX}-addr2line
   alias ar=${ALIAS_GCC_PREFIX}-ar
   alias as=${ALIAS_GCC_PREFIX}-as
   alias c++=${ALIAS_GCC_PREFIX}-c++
   alias c++filt=${ALIAS_GCC_PREFIX}-c++filt
   alias cpp=${ALIAS_GCC_PREFIX}-cpp
   alias g++=${ALIAS_GCC_PREFIX}-g++
   alias gcc=${ALIAS_GCC_PREFIX}-gcc
   alias gcov=${ALIAS_GCC_PREFIX}-gcov
   alias gdb=${ALIAS_GCC_PREFIX}-gdb
   alias gprof=${ALIAS_GCC_PREFIX}-gprof
   alias ld=${ALIAS_GCC_PREFIX}-ld
   alias nm=${ALIAS_GCC_PREFIX}-nm
   alias objcopy=${ALIAS_GCC_PREFIX}-objcopy
   alias objdump=${ALIAS_GCC_PREFIX}-objdump
   alias ranlib=${ALIAS_GCC_PREFIX}-ranlib
   alias readelf=${ALIAS_GCC_PREFIX}-readelf
   alias size=${ALIAS_GCC_PREFIX}-size
   alias strings=${ALIAS_GCC_PREFIX}-strings
   alias strip=${ALIAS_GCC_PREFIX}-strip
fi
