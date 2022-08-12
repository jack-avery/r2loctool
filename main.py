###
#   r2loctool
#   Jack Avery 2022
###
import os
import re
import fnmatch
import tkinter as tk
from tkinter import filedialog
version = 'v1.2.2'


# regex to compare the directory to to validate it is the RoR2 root folder
ROR2_PATH_RE = re.compile(r"common\/Risk of Rain 2$")
# metadata for each file to perform replacements on
file_meta = [
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
        self.root.title(f"r2loctool {version}")
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
        """
        Open a folder query dialogue and check if it's valid and whether backups exist.
        """
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
            self.res.pack_forget()
            self.log("Invalid directory.")

    def notify_begin(self):
        """
        Destroy the UI and notify the user that the process is beginning.
        """
        self.go.destroy()
        self.folder_button.destroy()
        self.res.destroy()
        self.log("Beginning...")

    def notify_end(self):
        """
        Notify the user that the workflow has completed and the app is safe to close.
        """
        self.log("")
        self.log("----------------------------------------")
        self.log("All done! You can now close this window.")

    def restore(self):
        """
        Begin the restoration workflow, restoring from backups.

        This should only ever be possible if a backup exists.

        See `get_folder()`.
        """
        self.notify_begin()

        for lang in self.langs:
            self.log("")
            self.log(f"Working on {lang}...")

            workdir = f"{self.langroot}/{lang}"

            for params in file_meta:
                datafile = f"{workdir}/{params['file']}"
                backfile = f"{workdir}/b_{params['file']}"

                try:
                    with open(backfile, 'r') as file:
                        self.log(f"Reading b_{params['file']}...")
                        backup = file.readlines()
                except FileNotFoundError:
                    self.log(
                        f"Could not find b_{params['file']}, skipping...")
                    break

                self.log(f"Writing to {params['file']}...")
                with open(datafile, 'w') as file:
                    file.writelines(backup)

                self.log("Removing now redundant backup...")
                os.remove(backfile)

            self.log(f"{lang} completed!")

        self.notify_end()

    def process(self):
        """
        Begin the normal pickup replacement workflow.
        """
        self.notify_begin()

        for lang in self.langs:
            self.log("")
            self.log(f"Working on {lang}...")

            workdir = f"{self.langroot}/{lang}"

            for params in file_meta:
                datafile = f"{workdir}/{params['file']}"
                backfile = f"{workdir}/b_{params['file']}"

                try:
                    with open(datafile, 'r') as file:
                        self.log(f"Reading {params['file']}...")
                        data = file.readlines()
                except FileNotFoundError:
                    self.log(
                        f"Could not find {params['file']}, skipping...")
                    break

                # backups
                if os.path.isfile(backfile):
                    self.log(f"Removing old {params['file']} backup...")
                    os.remove(backfile)

                self.log(
                    f"Creating a backup {params['file']} before continuing...")
                with open(backfile, 'w') as backup:
                    backup.writelines(data)

                # grab all of the valid lines
                self.log(
                    f"Finding pickup and description entries for {params['pre']}s...")
                dataPick = fnmatch.filter(data, f"*{params['pre']}_*_PICKUP*")
                dataDesc = fnmatch.filter(data, f"*{params['pre']}_*_DESC*")

                # replace "_DESC" for each logbook entry with "_PICKUP"
                self.log(f"Processing replacements for {params['pre']}s...")
                for i, d in enumerate(dataDesc):
                    dataDesc[i] = d.replace("DESC", "PICKUP")

                # replace each "_PICKUP" with the new line
                self.log(f"Replacing {params['pre']}s...")
                for i, d in enumerate(data):
                    if d in dataPick:
                        try:
                            data[i] = dataDesc[0]
                        except IndexError:
                            break

                        dataDesc = dataDesc[1:]
                        dataPick = dataPick[1:]

                self.log(f"Writing to {params['file']}...")
                with open(datafile, 'w') as file:
                    file.writelines(data)
                self.log(f"{params['file']} completed successfully.")

            self.log(f"{lang} completed!")

        self.notify_end()

    def log(self, l: str):
        """
        Log information to the info box and force the view to the bottom.
        """
        self.infobox.insert(tk.END, f"{l}")
        self.infobox.yview(tk.END)


if __name__ == "__main__":
    app = Application()
