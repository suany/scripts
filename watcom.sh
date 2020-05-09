#!/bin/sh

#
# See C:/WATCOM/CHANGES.ENV
# 16-bit compiler: wcc/wpp/wcl
#
# TODO: incorporate this into bash_env.sh
#

export WATCOM="C:\\WATCOM"

if [ ! -d "${WATCOM}" ]
then echo "WATCOM installation not found: ${WATCOM}"
fi

export EDPATH="${WATCOM}\\EDDAT"
export WHTMLHELP="${WATCOM}\\BINNT\\HELP"
export WIPFC="${WATCOM}\\WIPFC"

WAT_BINNT=`cygpath -a "${WATCOM}\\BINNT"`
WAT_BINW=`cygpath -a "${WATCOM}\\BINW"`
PATH="${WAT_BINNT}:${WAT_BINW}:${PATH}"

export INCLUDE="${WATCOM}\\H"
INCLUDE="${INCLUDE};${WATCOM}\\H\\NT"
INCLUDE="${INCLUDE};${WATCOM}\\H\\NT\\DIRECTX"
INCLUDE="${INCLUDE};${WATCOM}\\H\\NT\\DDK"

exec bash --login -i
