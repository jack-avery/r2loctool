## r2loctool

Risk of Rain 2 utility to replace the basic pickup tooltips with the more informative entries from the logbook.

Requires Python 3.10 or later.

## Reverting the Changes
### Verify integrity of game files
1. Right click on Risk of Rain 2 in your Steam library
2. Click on Properties
3. Click on "Local Files" on the left
4. Click "Verify integrity of game files..."

## Building
1. Install `pyinstaller`
```
python -m pip install pyinstaller
```
2. Run `pyinstaller --onefile -n r2loctool --clean --noconsole main.py`

## todo
- Detect when a version change has occurred, and do not recover from backup before acting