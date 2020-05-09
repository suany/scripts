@echo off

::::::::::::::::::::::::::::::::::::::::::::::::::::
:: "GLOBAL" variables to pass to sandbox.sh
::::::::::::::::::::::::::::::::::::::::::::::::::::
set SY_ADDL_LABELS=
:: Additional lables to put in title (apart from sandbox and IDA version)

::::::::::::::::::::::::::::::::::::::::::::::::::::
:: "LOCAL" variables
::::::::::::::::::::::::::::::::::::::::::::::::::::
:: IMPORTANT: reset these local variables below before calling rxvt.
:: NOTE: cannot use setlocal because we are calling batch files to
::       set "global" variables.
set scriptdir=%~dp0
set rxvt_args=
set sandbox=
set font='Lucida Console-14'
set geometry=80x50
set addl_args=
set ddk_ver=
set ddk_env=chk
set ddk_os=wxp


goto skip
:error_case
  echo ERROR %errorlevel%
  pause
  exit 1
:skip

:do_args

:: -- Visual Studio options --
if "%1" == "vc6" (
  set rxvt_args=%rxvt_args% -fg #ff9999
  set addl_args=%addl_args% push_cyg_path
  set SY_ADDL_LABELS=%SY_ADDL_LABELS% vc6
  call "%PROGRAMFILES%\Microsoft Visual Studio\VC98\Bin\VCVARS32.BAT" > nul
  ::if errorlevel 1 goto error_case
  shift
  goto do_args
)
if "%1" == "vc7" (
  set rxvt_args=%rxvt_args% -fg #66ff66
  set addl_args=%addl_args% push_cyg_path
  set SY_ADDL_LABELS=%SY_ADDL_LABELS% vc7
  call "%VS71COMNTOOLS%vsvars32.bat" > nul
  ::if errorlevel 1 goto error_case
  shift
  goto do_args
)
if "%1" == "vc8" (
  set rxvt_args=%rxvt_args% -fg #cccccc
  set addl_args=%addl_args% push_cyg_path
  set SY_ADDL_LABELS=%SY_ADDL_LABELS% vc8
  call "%VS80COMNTOOLS%vsvars32.bat" > nul
  ::if errorlevel 1 goto error_case
  shift
  goto do_args
)
if "%1" == "vc10" (
  set rxvt_args=%rxvt_args% -fg #cccccc
  set addl_args=%addl_args% push_cyg_path
  set SY_ADDL_LABELS=%SY_ADDL_LABELS% vc10
  call "%VS100COMNTOOLS%vsvars32.bat" > nul
  ::if errorlevel 1 goto error_case
  shift
  goto do_args
)
if "%1" == "psdk2003r2" (
  call "%PROGRAMFILES%\Microsoft Platform SDK for Windows Server 2003 R2\SetEnv.Cmd" > nul
  shift
  goto do_args
)
if "%1" == "vc9" (
  set rxvt_args=%rxvt_args% -fg #9999ff
  set addl_args=%addl_args% push_cyg_path
  set SY_ADDL_LABELS=%SY_ADDL_LABELS% vc9
  call "%VS90COMNTOOLS%vsvars32.bat" > nul
  ::if errorlevel 1 goto error_case
  shift
  goto do_args
)
if "%1" == "x64" (
  set rxvt_args=%rxvt_args% -fg #66ffff
  set addl_args=%addl_args% push_cyg_path
  set SY_ADDL_LABELS=%SY_ADDL_LABELS% x64
  call "%PROGRAMFILES%\Microsoft Platform SDK for Windows Server 2003 R2\SetEnv.Cmd" /XP64 /RETAIL > nul
  ::if errorlevel 1 goto error_case
  shift
  goto do_args
)

if "%1" == "arm" (
  set rxvt_args=%rxvt_args% -fg #66ffff
  set addl_args=%addl_args% arm
  shift
  goto do_args
)

if "%1" == "linux" (
  set rxvt_args=%rxvt_args% -fg #66ffff
  set addl_args=%addl_args% linux
  shift
  goto do_args
)

if "%1" == "ppc" (
  set rxvt_args=%rxvt_args% -fg #66ffff
  set addl_args=%addl_args% ppc
  shift
  goto do_args
)

:: -- WinDDK-related options --
:: WinDDK version
if "%1" == "3790" (
  set ddk_ver=3790.1830
  shift
  goto do_args
)
if "%1" == "6000" (
  set ddk_ver=6000
  shift
  goto do_args
)
:: WinDDK environment
if "%1" == "chk" (
  set ddk_env=chk
  shift
  goto do_args
)
if "%1" == "fre" (
  set ddk_env=fre
  shift
  goto do_args
)
:: WinDDK OS
if "%1" == "wxp" (
  set ddk_os=wxp
  shift
  goto do_args
)
if "%1" == "w2k" (
  set ddk_os=w2k
  shift
  goto do_args
)

:: -- Sandbox tags/colors --
if "%1" == "admin" (
  set rxvt_args=%rxvt_args% -fg #99ffcc -bg #663300
  set sandbox=admin
  shift
  goto do_args
)
if "%1" == "nocs" (
  set rxvt_args=%rxvt_args% -bg #402020
  set sandbox=nocs
  shift
  goto do_args
)
if "%1" == "blue" (
  set rxvt_args=%rxvt_args% -bg #000040
  set sandbox=blue
  shift
  goto do_args
)
if "%1" == "brown" (
  set rxvt_args=%rxvt_args% -bg #402000
  set sandbox=brown
  shift
  goto do_args
)
if "%1" == "debug" (
  set rxvt_args=%rxvt_args% -bg #000040
  set sandbox=debug
  shift
  goto do_args
)
if "%1" == "green" (
  set rxvt_args=%rxvt_args% -bg #003000
  set sandbox=green
  shift
  goto do_args
)
if "%1" == "purple" (
  set rxvt_args=%rxvt_args% -bg #400040
  set sandbox=purple
  shift
  goto do_args
)
if "%1" == "red" (
  set rxvt_args=%rxvt_args% -bg #660000
  set sandbox=red
  shift
  goto do_args
)
if "%1" == "release" (
  set rxvt_args=%rxvt_args% -bg #660000
  set sandbox=release
  shift
  goto do_args
)
:: call sandbox/setenv.cmd if available
:: findstr == windows version of grep
if "%1" == "setenv" (
  findstr /b "set " c:\cygwin\home\%username%\%sandbox%\setenv.cmd > c:\temp\rxvt_setenv.bat
  if errorlevel 1 (
    set SY_ADDL_LABELS=%SY_ADDL_LABELS% SETENV FAILED
  ) else (
    call c:\temp\rxvt_setenv.bat > nul
    set SY_ADDL_LABELS=%SY_ADDL_LABELS% setenv[vc10]
  )
  shift
  goto do_args
)

:: smaller font, larger window.
if "%1" == "lucida" (
  set font='Lucida Console-12'
  set geometry=180x60
  shift
  goto do_args
)

if not "%1" == "" (
  set addl_args=%addl_args% %1
  shift
  goto do_args
)

if "%sandbox%" == "" (
  echo Options include:
  echo   compiler: vc6 vc7 vc8 x64 arm ppc
  echo    sandbox: blue brown debug green purple red release
  echo    ida ver: 00 46 461 47 48 49 491 49f 50 51 52 53 55 56 57
  echo             60 601 61 62 63 64
  echo    ddk ver: 3790 6000
  echo       font: lucida
  pause
  exit 1
)

if "%ddk_ver%" == "" goto skip_ddk
  set rxvt_args=%rxvt_args% -fg #cccc66
  set addl_args=%addl_args% push_cyg_path
  set SY_ADDL_LABELS=%SY_ADDL_LABELS% ddk %ddk_ver% %ddk_env% %ddk_os%
  call c:\WINDDK\%ddk_ver%\bin\setenv.bat c:\WINDDK\%ddk_ver% %ddk_env% %ddk_os%
  ::if errorlevel 1 goto error_case
:skip_ddk

if "%font%" == "" goto skip_font
  set rxvt_args=%rxvt_args% -fn %font%
:skip_font

if "%geometry%" == "" goto skip_geom
  set rxvt_args=%rxvt_args% -geometry %geometry%
:skip_geom

:: Build up rxvt command arguments
set rxvt_cmd_args=%rxvt_args% -e %scriptdir%bash_env.sh %sandbox% %addl_args%
:: Reset local variables below before calling rxvt
set scriptdir=
set rxvt_args=
set sandbox=
set font=
set geometry=
set addl_args=
set ddk_ver=
set ddk_env=
set ddk_os=

:: Call rxvt
C:\cygwin\bin\rxvt.exe %rxvt_cmd_args%

