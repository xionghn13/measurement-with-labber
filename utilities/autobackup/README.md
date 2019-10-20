``autobackup.py`` script in this folder could be used to recursively copy/backup a (source) folder
to another (destination) folder:
```
python autobackup.py --source "C:\User\MyFolder" --destination "Z:\Backup\User\MyFolder"
```

To set up a periodic backup create a ``COMPUTERNAME.bat`` file (to find out computer name run
``hostname`` in the command prompt) with the job. To do this you can just copy an existing
``.bat`` file and edit the pathes to ``python.exe``, ``autobackup.py``, the source, and
destination folders accordingly. Then open Windows Task Scheduler and set up a simple
periodic task following the instructions therein.

Method 2: run autobackup.batch file