## r2loctool

Risk of Rain 2 utility to replace the basic pickup tooltips with the more informative entries from the logbook.

Requires Python 3.10 or later.

## Building
1. Install `pyinstaller`
```
python -m pip install pyinstaller
```
2. Run `pyinstaller --onefile -n r2loctool --clean --noconsole main.py`

## todo
- Detect when a version change has occurred, and do not recover from backup before acting