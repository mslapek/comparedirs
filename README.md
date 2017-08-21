# Directory compare

Python library/utility to compare directories contents by file names.

## Contents

Module `comparedirs.py` contains class `CompareDirs`, which performs directory
comparison. File `cmpdir.py` is shell interface for that class.

## Basic usage

To compare directories `/books` and `/media/ebksd`, invoke:

```sh
python3 cmpdir.py /books /media/ebksd
```

Sample output:

```
Directory /books:
<< Statistics/ESLII.pdf
<< Statistics/site/index.html
Directory /media/ebksd:
>> System Volume Information/IndexerVolumeGuid
```

Notice, that the comparison is performed *only by filename*.

## Usage

```
usage: cmpdir.py [-h] [--ignore-list IGNORE_LIST] [--copy-dir1-to-dir2] [-y]
                 dir1 dir2

positional arguments:
  dir1                  path to first directory
  dir2                  path to second directory

optional arguments:
  -h, --help            show this help message and exit
  --ignore-list IGNORE_LIST
                        path to file with ignore list
  --copy-dir1-to-dir2   perform copy of missing files from first directory to
                        second directory
  -y, --assumeyes       assume yes; assume that the answer to any question
                        which would be asked is yes
```

### Ignore list

*Ignore list* is text file, where each line is [glob pattern]. For instance,
if `ignore_list.txt` is:

```
System Volume Information/*
*.html
```

Then the sample output is following:

```
Directory /books:
<< Statistics/ESLII.pdf
```

### Copy directory contents

Copies missing files from first directory to second. Asks for confirmation
unless `--assumeyes` is on.

## Motivation

This utility might be used to keep two directories in sync. It might be for
instance music library or book library locally on computer and on a external
device.

For example, under Windows one can create BAT file to keep synchronized
local library and SD card of e-book reader.

```bat
@echo off
python comparedirs/cmpdir.py C:\Books E:\ --ignore-list C:\ignore_list.txt --copy-dir1-to-dir2
pause
```

SD card can be determined also by volume label, such as EBKSD
([reference a volume drive by label on SO]).

```bat
@echo off
for /f %%D in ('wmic volume get DriveLetter^, Label ^| find "EBKSD"') do set ebksd=%%D
python comparedirs/cmpdir.py C:\Books %ebksd% --ignore-list C:\ignore_list.txt --copy-dir1-to-dir2
pause
```

[glob pattern]: https://en.wikipedia.org/wiki/Glob_%28programming%29
[reference a volume drive by label on SO]: https://stackoverflow.com/questions/9065280/reference-a-volume-drive-by-label