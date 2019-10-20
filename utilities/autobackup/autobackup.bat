@echo off
for /L %%n in (1,0,10) do (
  robocopy  "C:\SC Lab\GitHubRepositories\measurement-with-labber\utilities\autobackup\test_folder\BF temp" "C:\SC Lab\GitHubRepositories\measurement-with-labber\utilities\autobackup\test_folder\BF temp_2" /e /xo /ndl /njh
  ping 127.0.0.1 -n 6 > nul
  REM wait for 5 sec
)
