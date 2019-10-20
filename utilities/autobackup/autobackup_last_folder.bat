
@ECHO OFF >NUL
SETLOCAL enableextensions disabledelayedexpansion
set "fromFolder=C:\SC Lab\GitHubRepositories\measurement-with-labber\utilities\autobackup\test_folder\BF temp"
rem my debug setting set "fromFolder=D:\path"
for /F "tokens=*" %%f in ('dir /B /S /A:D "%fromFolder%\*.*"') do (
	set "mydir=%%~ff"
	set "last=%%~nxf"
	
)
echo %mydir%

for /L %%n in (1,0,10) do (

	for /F "tokens=*" %%f in ('dir /B /S /A:D "%fromFolder%\*.*"') do (
	set "mydir=%%~ff"
	set "last=%%~nxf"	
	)
	echo %mydir%
	robocopy  "%mydir%" "C:\SC Lab\GitHubRepositories\measurement-with-labber\utilities\autobackup\test_folder\BF temp_2" /e /xo /ndl /njh
	ping 127.0.0.1 -n 6 > nul
	REM wait for 5 sec
)

@ENDLOCAL
goto :eof