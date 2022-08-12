from tkinter import filedialog
import tkinter as tk
import fnmatch
import re
import os

# regex to compare the directory to to validate it is the RoR2 root folder
ROR2_PATH_RE = re.compile(r"common\/Risk of Rain 2$")
# metadata for each file to perform replacements on
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


class Application:
    def __init__(self):
        self.root = tk.Tk("r2loctool")
        self.root.geometry('480x280')
        self.root.title("r2loctool")
        self.root.configure(bg="#222222")
        self.root.resizable(0, 0)

        # build UI
        self.folder_path = tk.StringVar()

        self.folder_button = tk.Button(
            text="Browse...", command=self.get_folder, bg="#222222", fg="white")
        self.folder_button.pack(anchor=tk.W, side=tk.TOP)

        self.folder_label = tk.Label(
            master=self.root, textvariable=self.folder_path, bg="#222222", fg="white")
        self.folder_label.pack(anchor=tk.W, side=tk.TOP)

        self.infobox = tk.Listbox(self.root, bg="#222222", fg="white")
        self.infobox.pack(fill=tk.BOTH, expand=1, side=tk.TOP)

        # build the go button but do not embed it for now.
        self.go = tk.Button(
            text="Start", command=self.process, bg="#004400", fg="white")

        # build the restore button but do not embed it for now.
        self.res = tk.Button(
            text="Restore", command=self.restore, bg="#000044", fg="white")

        # inform user they must select a directory
        self.log("Please select your Risk of Rain 2 directory.")
        tk.mainloop()

    def get_folder(self):
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)

        # validate it is a real RoR2 directory (basic validation)
        if len(ROR2_PATH_RE.findall(self.folder_path.get())) != 0:
            self.log("Valid directory selected.")
            self.langroot = f"{self.folder_path.get()}/Risk of Rain 2_Data/StreamingAssets/Language"
            self.langs = os.listdir(self.langroot)
            self.log(
                f"Found folders for {len(self.langs)} langs: {', '.join(self.langs)}")

            self.go.pack(side=tk.TOP, fill=tk.X)

            # check for backups in the folders
            for lang in self.langs:
                if os.path.exists(f"{self.langroot}/{lang}/b_Items.txt"):
                    self.log(
                        "Existing backups have been found. Click 'Restore' to restore them.")
                    self.res.pack(side=tk.TOP, fill=tk.X)

                    break

        else:
            self.go.pack_forget()
            self.log("Invalid directory.")

    def restore(self):
        self.go.destroy()
        self.folder_button.destroy()
        self.res.destroy()
        self.log("Beginning...")

        for lang in self.langs:
            self.log("")
            self.log(f"Working on {lang}...")

            for params in meta:
                try:
                    with open(f"{self.langroot}/{lang}/b_{params['file']}", 'r') as file:
                        self.log(f"Reading b_{params['file']}...")
                        backup = file.readlines()
                except FileNotFoundError:
                    self.log(
                        f"Could not find b_{params['file']}, skipping...")
                    break

                self.log(f"Writing to {params['file']}...")
                with open(f"{self.langroot}/{lang}/{params['file']}", 'w') as file:
                    file.writelines(backup)

                self.log("Removing now redundant backup...")
                os.remove(f"{self.langroot}/{lang}/b_{params['file']}")

                self.log(f"{lang} completed")

        self.log("")
        self.log("----------------------------------------")
        self.log("All done! You can now close this window.")

    def process(self):
        self.go.destroy()
        self.folder_button.destroy()
        self.res.destroy()
        self.log("Beginning...")

        for lang in self.langs:
            self.log("")
            self.log(f"Working on {lang}...")
            # for both items and equipment...
            for params in meta:
                try:
                    with open(f"{self.langroot}/{lang}/{params['file']}", 'r') as file:
                        self.log(f"Reading {params['file']}...")
                        items = file.readlines()
                except FileNotFoundError:
                    self.log(
                        f"Could not find {params['file']}, skipping...")
                    break

                # backups
                if os.path.isfile(f"{self.langroot}/{lang}/b_{params['file']}"):
                    self.log(f"Removing old {params['file']} backup...")
                    os.remove(f"{self.langroot}/{lang}/b_{params['file']}")
                self.log(
                    f"Creating a backup {params['file']} before continuing...")
                with open(f"{self.langroot}/{lang}/b_{params['file']}", 'w') as backupfile:
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
                with open(f"{self.langroot}/{lang}/{params['file']}", 'w') as file:
                    file.writelines(items)
                self.log(f"{params['file']} completed successfully.")

                self.log(f"{lang} completed")

        self.log("")
        self.log("----------------------------------------")
        self.log("All done! You can now close this window.")

    def log(self, l: str):
        self.infobox.insert(tk.END, f"{l}")
        self.infobox.yview(tk.END)


if __name__ == "__main__":
    app = Application()
