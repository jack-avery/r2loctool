import fnmatch,os,sys

# recover from backups before running again (may cause issues)
for backup in ["Items","Equipment"]:
    if os.path.isfile(os.path.join(f"b_{backup}.txt")):
        with open(f"b_{backup}.txt",'r') as back:
            with open(f"{backup}.txt",'w') as file:
                file.writelines(back.readlines())

# allow manual reversion
if '-r' in sys.argv:
    input('Original files recovered. You may now close this window.')
    sys.exit(0)

# define metadata for each file to perform replacements on
meta = [
    {
        "file": "Items.txt",
        "pre": "ITEM"
    },
    {
        "file": "Equipment.txt",
        "pre": "EQUIPMENT"
    }
]

# for both items and equipment...
for params in meta:
    with open(params["file"],'r') as file:
        items=file.readlines()

    # create a backup
    with open(f"b_{params['file']}",'w') as backupfile:
        backupfile.writelines(items)
    
    # grab all of the valid lines
    itemPick = fnmatch.filter(items,f"*{params['pre']}_*_PICKUP*")
    itemDesc = fnmatch.filter(items,f"*{params['pre']}_*_DESC*")

    # replace "_DESC" for each logbook entry with "_PICKUP"
    for i, item in enumerate(itemDesc):
        itemDesc[i]=item.replace("DESC","PICKUP")

    # replace each "_PICKUP" with the new line
    for i, item in enumerate(items):
        if item in itemPick:
            try:
                items[i] = itemDesc[0]
            except IndexError:
                break

            itemDesc = itemDesc[1:]
            itemPick = itemPick[1:]

    with open(params["file"],'w') as file:
        file.writelines(items)

    print(f"{params['file']} completed successfully")

print("Backups are present at b_(filename), you can recover this at any time by running this script with the -r parameter.")
input("Delete the backups and re-validate if there has been an update since you last ran this")