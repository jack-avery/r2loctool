## r2loctool

**[Download Latest (.exe)](https://github.com/jack-avery/r2loctool/releases/latest/download/r2loctool.exe)**

**r2loctool** is a utility program for the video game **Risk of Rain 2** (by Hopoo Games) to replace the pickup tooltips with the more informative entries from the logbook, **no mod loader (e.g. r2modman) required.**

![r2loctool](https://user-images.githubusercontent.com/47289484/184267034-0ad2ba86-0953-4d41-8db3-70842ffe32b1.jpg)

## Usage
1. Download and open **r2loctool.exe**.
2. Use the `Browse` button to find your Risk of Rain 2 folder.
> This normally looks something like `[...]/steamapps/common/Risk of Rain 2`<br/>
> You can find this directory for your installation under `Risk of Rain 2` -> `Properties` -> `Local Files` -> `Browse...` 
3. Press `Start` to replace the pickup tooltips.

The program will inform you when the process is complete and the app is safe to close.

## Restoring the Original Pickup Tooltips
As of `v1.2.0`, **r2loctool** comes with its' own primitive backup system, but if that doesn't work, I recommend you:
### Verify integrity of game files
1. Right click on Risk of Rain 2 in your Steam library
2. Click on Properties
3. Click on "Local Files" on the left
4. Click "Verify integrity of game files..."

## Building
Requires **[Python 3.11](https://www.python.org/downloads/)** or later.

1. Install `pyinstaller`
```
python -m pip install pyinstaller
```
2. Run `pyinstaller --onefile -n r2loctool --clean --noconsole main.py`
