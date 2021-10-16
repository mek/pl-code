https://www.pitcherlist.com/pitcher-list-data-camp-personal-data-warehouse/

Statcaset Data Importer
* src/pl1.py
```
usage: pl1.py [-h] --year YEAR [--batter BATTER] [--pitcher PITCHER]

Statcast data importer.

optional arguments:
  -h, --help         show this help message and exit
  --year YEAR        Year to import.
  --batter BATTER    Batter to import.
  --pitcher PITCHER  Pitcher to import.
```
BUGS:
 * outputs to current working directory.
 * Both pitcher and batter into are written into the same file name.
 * Should be a better way to give pitcher/batter info.

