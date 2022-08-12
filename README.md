## r2loctool

[Download latest (.exe)](https://github.com/jack-avery/r2loctool/releases/latest/download/r2loctool.exe)

Risk of Rain 2 utility to replace the basic pickup tooltips with the more informative entries from the logbook.

## Reverting the Changes
As of `v1.2.0`, **r2loctool** comes with its' own primitive backup system, but if that doesn't work, I recommend you:
### Verify integrity of game files
1. Right click on Risk of Rain 2 in your Steam library
2. Click on Properties
3. Click on "Local Files" on the left
4. Click "Verify integrity of game files..."

## Building
Requires Python 3.10 or later.

1. Install `pyinstaller`
```
python -m pip install pyinstaller
```
2. Run `pyinstaller --onefile -n r2loctool --clean --noconsole main.py`