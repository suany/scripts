@echo off

set SANDBOX=C:\cygwin\home\testbot\testbox\

set WSDK71=%SANDBOX%win32-fetcher\wsdk71\
set VSINSTALLDIR=%WSDK71%msvs10\
set VS100COMNTOOLS=%VSINSTALLDIR%Common7\Tools\
set VCINSTALLDIR=%VSINSTALLDIR%VC\
set DevEnvDir=%VSINSTALLDIR%Common7\IDE\

rem NOTE: this will check the registry, which we probably won't have set
rem call "%VS100COMNTOOLS%vsvars32.bat" > nul

set PATH=%VSINSTALLDIR%Common7\Tools;%PATH%
set PATH=%VCINSTALLDIR%BIN;%PATH%
set PATH=%DevEnvDir%;%PATH%

set INCLUDE=%VCINSTALLDIR%INCLUDE;%INCLUDE%
set LIB=%VCINSTALLDIR%LIB;%LIB%
set LIBPATH=%VCINSTALLDIR%LIB;%LIBPATH%

C:\cygwin\bin\rxvt.exe -saveLines 3000 -geometry 80x60 -bg black -fg white -font Terminal -e bash --login -i
