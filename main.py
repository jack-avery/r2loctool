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
        # create the window
        self.root = tk.Tk()
        self.root.geometry('480x280')
        self.root.title(f"r2loctool {version}")
        self.root.configure(bg="#222222")
        self.root.resizable(0, 0)

        # build UI
        self.folder_path = tk.StringVar()

        # folder browse button
        self.folder_button = tk.Button(
            text="Browse...", command=self.get_folder, bg="#222222", fg="white")
        self.folder_button.pack(anchor=tk.W, side=tk.TOP)

        # folder display label
        self.folder_label = tk.Label(
            master=self.root, textvariable=self.folder_path, bg="#222222", fg="white")
        self.folder_label.pack(anchor=tk.W, side=tk.TOP)

        # logging info box for user notification
        self.infobox = tk.Listbox(self.root, bg="#222222", fg="white")
        self.infobox.pack(fill=tk.BOTH, expand=1, side=tk.TOP)

        # build the start and restore buttons but do not embed them for now.
        self.go = tk.Button(
            text="Start", command=self.process, bg="#004400", fg="white")
        self.res = tk.Button(
            text="Restore", command=self.restore, bg="#000044", fg="white")

        # open window and inform user to select a directory
        self.log("Please select your Risk of Rain 2 directory.")
        tk.mainloop()

    def get_folder(self):
        """
        Open a folder query dialogue and check if it's valid and whether backups exist.
        """
        # get folder
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)

        # validate it is a real RoR2 directory (basic validation)
        if len(ROR2_PATH_RE.findall(self.folder_path.get())) != 0:
            self.log("Valid directory selected.")
            self.langroot = f"{self.folder_path.get()}/Risk of Rain 2_Data/StreamingAssets/Language"
            self.langs = os.listdir(self.langroot)
            self.log(
                f"Found folders for {len(self.langs)} langs: {', '.join(self.langs)}")

            # pack the "start" button
            self.go.pack(side=tk.TOP, fill=tk.X)

            # check for backups in the folders
            for lang in self.langs:
                if os.path.exists(f"{self.langroot}/{lang}/b_Items.txt"):
                    # if a backup is found, inform the user and pack the "restore" button
                    self.log(
                        "Existing backups have been found. Click 'Restore' to restore them.")
                    self.res.pack(side=tk.TOP, fill=tk.X)
                    break

        else:
            # if the user changes the directory and it's now invalid, unpack the "start" and "restore" buttons
            self.go.pack_forget()
            self.res.pack_forget()
            self.log("Invalid directory.")

    def perform(self, type: str):
        """
        Perform a workflow.

        `"process"` will replace PICKUP data with DESC data from the logbook.

        `"restore"` will restore from a backup file generated by `r2loctool`.
        """
        match type:
            case "process":
                func = self.process_perfile
            case "restore":
                func = self.restore_perfile

        # destroy UI and inform user the process is beginning
        self.go.destroy()
        self.folder_button.destroy()
        self.res.destroy()
        self.log("")
        self.log("Beginning...")

        for lang in self.langs:
            self.log("")
            self.log(f"Working on {lang}...")

            workdir = f"{self.langroot}/{lang}"

            for params in file_meta:
                datafile = f"{workdir}/{params['file']}"
                backfile = f"{workdir}/b_{params['file']}"

                func(params, datafile, backfile)

            self.log(f"{lang} completed!")

        # inform the user the workflow has completed and app is safe to close.
        self.log("")
        self.log("----------------------------------------")
        self.log("All done! You can now close this window.")

    def restore(self):
        """
        Begin the restoration workflow, restoring from backups.

        This should only ever be possible if a backup exists.

        See `get_folder()`.
        """
        self.perform("restore")

    def process(self):
        """
        Begin the normal pickup replacement workflow.
        """
        self.perform("process")

    def restore_perfile(self, params, datafile: str, backfile: str):
        """
        Restore from a backup for either Equipment or Items.
        """
        # try to read backup... skip if can't.
        try:
            with open(backfile, 'r') as file:
                self.log(f"Reading b_{params['file']}...")
                backup = file.readlines()
        except FileNotFoundError:
            self.log(
                f"Could not find b_{params['file']}, skipping...")
            return

        # write backup to localization file
        self.log(f"Writing to {params['file']}...")
        with open(datafile, 'w') as file:
            file.writelines(backup)

        # remove redundant backup and inform user file completed.
        self.log("Removing now redundant backup...")
        os.remove(backfile)
        self.log(f"{params['file']} completed successfully.")

    def process_perfile(self, params: str, datafile: str, backfile: str):
        """
        Replace pickup tooltip data for either Equipment or Items.
        """
        # try to read... skip if can't.
        try:
            with open(datafile, 'r') as file:
                self.log(f"Reading {params['file']}...")
                data = file.readlines()
        except FileNotFoundError:
            self.log(
                f"Could not find {params['file']}, skipping...")
            return

        # remove old backups
        if os.path.isfile(backfile):
            self.log(f"Removing old {params['file']} backup...")
            os.remove(backfile)

        # create a new one
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
                    data[i] = dataDesc.pop(0)
                    dataPick.pop(0)
                except IndexError:
                    break

        # write and inform user file completed
        self.log(f"Writing to {params['file']}...")
        with open(datafile, 'w') as file:
            file.writelines(data)
        self.log(f"{params['file']} completed successfully.")

    def log(self, l: str):
        """
        Log information to the info box and force the view to the bottom.
        """
        self.infobox.insert(tk.END, f"{l}")
        self.infobox.yview(tk.END)


if __name__ == "__main__":
    app = Application()
