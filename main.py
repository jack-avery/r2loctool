from tkinter import filedialog
import tkinter as tk
import fnmatch
import os
import time


class Application:
    def __init__(self):
        self.root = tk.Tk("r2loctool")
        self.root.geometry('480x240')
        self.root.title("r2loctool")
        self.root.resizable(0, 0)

        # build UI
        self.folder_path = tk.StringVar()

        self.folder_button = tk.Button(
            text="Browse...", command=self.get_folder)
        self.folder_button.pack(anchor=tk.W, side=tk.TOP)

        self.folder_label = tk.Label(
            master=self.root, textvariable=self.folder_path)
        self.folder_label.pack(anchor=tk.W, side=tk.TOP)

        self.infobox = tk.Listbox(self.root)
        self.infobox.pack(fill=tk.BOTH, expand=1, side=tk.TOP)

        # build the go button but do not embed it for now.
        self.go = tk.Button(text="Start", command=self.process)

        # inform user they must select a directory
        self.log("Please select your Risk of Rain 2 directory.")
        tk.mainloop()

    def get_folder(self):
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)

        # validate it is a real RoR2 directory (basic validation)
        if "common/Risk of Rain 2" in self.folder_path.get():
            self.log(
                "Valid directory selected. Click 'Start' to start the process.")
            self.go.pack(side=tk.TOP, fill=tk.X)

    def process(self):
        self.go.destroy()
        self.folder_button.destroy()

        self.log("Beginning...")
        self.log("Refreshing from backup if exists...")
        for backup in ["Items", "Equipment"]:
            if os.path.isfile(os.path.join(f"{self.folder_path.get()}/Risk of Rain 2_Data/StreamingAssets/Language/en/b_{backup}.txt")):
                with open(f"{self.folder_path.get()}/Risk of Rain 2_Data/StreamingAssets/Language/en/b_{backup}.txt", 'r') as back:
                    with open(f"{self.folder_path.get()}/Risk of Rain 2_Data/StreamingAssets/Language/en/{backup}.txt", 'w') as file:
                        file.writelines(back.readlines())

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
            self.log(f"Reading {params['file']}...")
            try:
                with open(f"{self.folder_path.get()}/Risk of Rain 2_Data/StreamingAssets/Language/en/{params['file']}", 'r') as file:
                    items = file.readlines()
            except FileNotFoundError:
                self.log(f"Could not find {params['file']}...")
                break

            # create a backup
            self.log(f"Backing up {params['file']} before continuing...")
            with open(f"{self.folder_path.get()}/Risk of Rain 2_Data/StreamingAssets/Language/en/b_{params['file']}", 'w') as backupfile:
                backupfile.writelines(items)

            # grab all of the valid lines
            self.log(
                f"Finding pickup and description entries for {params['pre']}s...")
            itemPick = fnmatch.filter(items, f"*{params['pre']}_*_PICKUP*")
            itemDesc = fnmatch.filter(items, f"*{params['pre']}_*_DESC*")

            # replace "_DESC" for each logbook entry with "_PICKUP"
            self.log(f"Processing replacements for {params['pre']}s...")
            for i, item in enumerate(itemDesc):
                itemDesc[i] = item.replace("DESC", "PICKUP")

            # replace each "_PICKUP" with the new line
            self.log(f"Replacing {params['pre']}s...")
            for i, item in enumerate(items):
                if item in itemPick:
                    try:
                        items[i] = itemDesc[0]
                    except IndexError:
                        break

                    itemDesc = itemDesc[1:]
                    itemPick = itemPick[1:]

            self.log(f"Writing to {params['file']}...")
            with open(f"{self.folder_path.get()}/Risk of Rain 2_Data/StreamingAssets/Language/en/{params['file']}", 'w') as file:
                file.writelines(items)

            self.log(f"{params['file']} completed successfully.")

        self.log("All done! You can now close this window.")

    def log(self, l: str):
        self.infobox.insert(tk.END, f"{l}")
        self.infobox.yview(tk.END)


if __name__ == "__main__":
    app = Application()
