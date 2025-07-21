@echo off
REG ADD "HKCU\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
setlocal enabledelayedexpansion
chcp 65001 >nul
title portX Console

set "BASEDIR=%~dp0"
set "ENGINEDIR=%BASEDIR%engine"
set "SYSTEMDIR=%BASEDIR%system"
set "CMDMAP=%BASEDIR%commandmap.json"

call :banner

if not exist "%SYSTEMDIR%" mkdir "%SYSTEMDIR%"

set OLD_FILE_COUNT=0
set OLD_FILE_SIZE=0
set OLD_LAST_MOD=0

for %%F in (engine_file_count.txt engine_file_size.txt engine_lastmod.txt) do (
    if exist "%SYSTEMDIR%\%%F" (
        for /f "usebackq delims=" %%a in ("%SYSTEMDIR%\%%F") do set "OLD_%%~nF=%%a"
    )
)

for /f %%C in ('powershell -noprofile -command "(gci -path \"%ENGINEDIR%\" -filter \"*.py\").Count"') do set CUR_FILE_COUNT=%%C
for /f %%S in ('powershell -noprofile -command "(gci -path \"%ENGINEDIR%\" -filter \"*.py\" | measure -property Length -sum).Sum"') do set CUR_FILE_SIZE=%%S
for /f %%T in ('powershell -noprofile -command "(gci -path \"%ENGINEDIR%\" -filter \"*.py\" | sort LastWriteTimeUtc -desc | select -first 1).LastWriteTimeUtc.Ticks"') do set CUR_LAST_MOD=%%T

set UPDATECMD=0
if not "%CUR_FILE_COUNT%"=="%OLD_FILE_COUNT%" set UPDATECMD=1
if not "%CUR_FILE_SIZE%"=="%OLD_FILE_SIZE%" set UPDATECMD=1
if not "%CUR_LAST_MOD%"=="%OLD_LAST_MOD%" set UPDATECMD=1

if "%UPDATECMD%"=="1" (
    call python "%ENGINEDIR%\logmsg.py" info "Scanning commands..."
    python "%BASEDIR%build_command_index.py" >nul 2>"%BASEDIR%scanip_error.txt"
    if errorlevel 1 (
        call python "%ENGINEDIR%\logmsg.py" fail "An error occurred during command scanning. Check the scanip_error.txt file."
    ) else (
        call python "%ENGINEDIR%\logmsg.py" system "Commands have been updated."
        del "%BASEDIR%scanip_error.txt" 2>nul
        echo %CUR_FILE_COUNT% > "%SYSTEMDIR%\engine_file_count.txt"
        echo %CUR_FILE_SIZE% > "%SYSTEMDIR%\engine_file_size.txt"
        echo %CUR_LAST_MOD%  > "%SYSTEMDIR%\engine_lastmod.txt"
    )
) else (
    call python "%ENGINEDIR%\logmsg.py" system "Commands are already up to date."
)

:loop
echo.
for /f "usebackq delims=" %%i in (`powershell -command "Read-Host ' [32m%USERNAME%@%COMPUTERNAME% /[0m'"`) do set "userinput=%%i"

if /i "%userinput%"=="exit" exit
if /i "%userinput%"=="clear" cls & call :banner & goto :loop
if /i "%userinput%"=="cl" cls & call :banner & goto :loop

for /f "tokens=1*" %%A in ("%userinput%") do (
    set "cmd=%%A"
    set "params=%%B"
)

set "cmdfile="
for /f "delims=" %%a in ('powershell -noprofile -command "try { (Get-Content -raw '%CMDMAP%' | ConvertFrom-Json).%cmd% } catch { '' } "') do (
    set "cmdfile=%%a"
)

if "%cmdfile%"=="" (
    call python "%ENGINEDIR%\logmsg.py" fail "Invalid command: '%cmd%'"
    goto :loop
)

if exist "%ENGINEDIR%\%cmdfile%" (
    call python "%ENGINEDIR%\%cmdfile%" %params%
) else (
    call python "%ENGINEDIR%\logmsg.py" fail "File not found: %cmdfile%"
)

goto :loop

:banner
echo [32m
echo.                                       `7MM"""Mq.                      mm    `YMM'   `MP' 
echo.                                         MM   `MM.                     MM      VMb.  ,P   
echo.                                         MM   ,M9  ,pW"Wq.  `7Mb,od8 mmMMmm     `MM.M'    
echo.                                         MMmmdM9  6W'   `Wb   MM' "'   MM         MMb     
echo.                                         MM       8M     M8   MM       MM       ,M'`Mb.   
echo.                                         MM       YA.   ,A9   MM       MM      ,P   `MM.  
echo.                                       .JMML.      `Ybmd9'  .JMML.     `Mbmo .MM:.  .:MMa.
echo [0m
exit /b
