import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

def setup(root):
    # Folder selection
    folder_path = tk.StringVar()
    tk.Label(root, text="Addon Folder:").pack(anchor='w')
    folder_frame = tk.Frame(root)
    folder_frame.pack(fill='x')
    folder_entry = tk.Entry(folder_frame, textvariable=folder_path, width=30)
    folder_entry.pack(side='left', fill='x', expand=True)
    tk.Button(folder_frame, text="Browse", command=lambda: select_folder(folder_path)).pack(side='right')

    # Name Input
    tk.Label(root, text="Name:").pack(anchor='w')
    name_entry = tk.Entry(root)
    name_entry.pack(fill='x')

    # Version Dropdowns
    tk.Label(root, text="Version:").pack(anchor='w')
    version_frame = tk.Frame(root)
    version_frame.pack()

    version_vars = [tk.StringVar(value='0') for _ in range(3)]
    version_menus = []
    for var in version_vars:
        menu = tk.OptionMenu(version_frame, var, *map(str, range(10)))
        menu.pack(side='left')
        version_menus.append(menu)

    # Checkboxes
    options = {"Include Dependencies": tk.BooleanVar(), "Optimize": tk.BooleanVar()}
    tk.Label(root, text="Options:").pack(anchor='w')
    for option, var in options.items():
        tk.Checkbutton(root, text=option, variable=var).pack(anchor='w')

    # Listbox with checkboxes
    tk.Label(root, text="Additional Options:").pack(anchor='w')
    listbox = tk.Listbox(root, selectmode='multiple')
    listbox.pack(fill='both', expand=True)
    for item in ["Option A", "Option B", "Option C"]:
        listbox.insert('end', item)

    # Build Button
    tk.Button(root, text="Build", command=lambda: build(version_vars)).pack(pady=10)

########################•########################
"""                 CALLBACKS                 """
########################•########################

def select_folder(folder_path):
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)


def build(version_vars):
    version = "{} . {} . {}".format(*[var.get() for var in version_vars])
    messagebox.showinfo("Build", f"Extension build process started!\nVersion: {version}")

########################•########################
"""                APPLICATION                """
########################•########################

APP_NAME = "Blender Extension Creator"
APP_WIDTH = 400
APP_HEIGHT = 800

if __name__ == "__main__":
    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry(f"{int(APP_WIDTH)}x{int(APP_HEIGHT)}")
    setup(root)
    root.mainloop()
