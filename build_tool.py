########################•########################
"""                  IMPORTS                  """
########################•########################

import os
import re
import sys
import shutil
import traceback
import subprocess
import tkinter as tk
from pathlib import Path
from collections.abc import Iterable
from tkinter import filedialog, messagebox

########################•########################
"""                 MENU OPTIONS              """
########################•########################

LICENSES = [
    "SPDX:GPL-3.0-or-later",
    "SPDX:CC0-1.0",
]

EXTENSION_TYPE = [
    "add-on",
    "theme",
]

EXTENSION_TAGS = [
    "3D View",
    "Add Curve",
    "Add Mesh",
    "Animation",
    "Bake",
    "Camera",
    "Compositing",
    "Development",
    "Game Engine",
    "Geometry Nodes",
    "Grease Pencil",
    "Import-Export",
    "Lighting",
    "Material",
    "Modeling",
    "Mesh",
    "Node",
    "Object",
    "Paint",
    "Pipeline",
    "Physics",
    "Render",
    "Rigging",
    "Scene",
    "Sculpt",
    "Sequencer",
    "System",
    "Text Editor",
    "Tracking",
    "User Interface",
    "UV",
]

THEME_TAGS = [
    "Dark",
    "Light",
    "Colorful",
    "Inspired By",
    "Print",
    "Accessibility",
    "High Contrast",
]

PLATFORMS = [
    "windows-x64",
    "macos-arm64",
    "linux-x64",
    "windows-arm64",
    "macos-x64"
]

PERMISSIONS = [
    "files",
    "network",
    "clipboard",
    "camera",
    "microphone",
]

PATH_EXCLUDE_PATTERNS = [
  "__pycache__/",
  "/.git/",
  "/*.zip",
]

########################•########################
"""                 USER DATA                 """
########################•########################

DATA = {
    # --- Directories --- #
    'BLENDER_EXE_PATH'    : "",
    'ADDON_PARENT_DIR'    : None,
    'ADDON_DIR'           : None,
    'BUILD_FOLDER_NAME'   : None,
    'BUILD_DIR'           : None,
    'EXTENSION_FILE_PATH' : None,
    'MANIFEST_FILE_NAME'  : 'blender_manifest.toml',

    # --- Manifest --- #
    'ADDON_NAME'          : None,
    'SCHEMA_VERSION'      : "",
    'ID'                  : "",
    'VERSION'             : "",
    'TAG_LINE'            : "",
    'MAINTAINER'          : "",
    'TYPE'                : "",
    'WEBSITE'             : "",
    'ADDON_TAGS'          : [],
    'THEME_TAGS'          : [],
    'B3D_VER_MIN'         : "",
    'B3D_VER_MAX'         : "",
    'LICENSE'             : [],
    'COPYRIGHT'           : [],
    'PLATFORMS'           : [],
    'WHEELS'              : [],
    'PERMISSIONS'         : [],
    'EXCLUDE_PATTERNS'    : [],
}

########################•########################
"""                 VALIDATORS                """
########################•########################

check_string     = lambda item: isinstance(item, str) and bool(item.strip())
check_integer    = lambda item: isinstance(item, int)
check_float      = lambda item: isinstance(item, float)
check_tuple_type = lambda item: isinstance(item, tuple)
check_iterable   = lambda item: isinstance(item, Iterable) and not isinstance(item, (str, bytes))
check_path_exist = lambda item: isinstance(item, (str, Path)) and Path(item).exists()
check_file_exist = lambda item: isinstance(item, (str, Path)) and Path(item).is_file()
check_executable = lambda item: check_file_exist(item) and os.access(item, os.X_OK)


def validate_data_keys(keys=[]):
    global DATA
    for key in keys:
        if key not in DATA:
            return False
        if key == 'ADDON_NAME':
            if not check_string(item=key):
                return False
        elif key == 'ADDON_PARENT_DIR':
            if not check_path_exist(item=key):
                return False
        elif key == 'ADDON_DIR':
            if not check_path_exist(item=key):
                return False
        elif key == 'BUILD_FOLDER_NAME':
            if not check_string(item=key):
                return False
        elif key == 'BUILD_DIR':
            if not check_path_exist(item=key):
                return False
        elif key == 'EXTENSION_FILE_PATH':
            if not check_file_exist(item=key):
                return False
    return True


def make_safe_folder_name(name=""):
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*.]', '_', name)
    name = re.sub(r'[\x00-\x1f\x7f]', '', name)
    name = name[:255]
    return name

########################•########################
"""                 DIRECTORIES               """
########################•########################

def set_build_folder():

    # Errors
    if not validate_path_keys(keys=['ADDON_NAME', 'ADDON_PARENT_DIR']):
        return False

    # Path
    global PATH_DATA
    addon_name = PATH_DATA['ADDON_NAME']
    addon_parent_dir = PATH_DATA['ADDON_PARENT_DIR']
    build_folder_name = make_safe_folder_name(name=f"{addon_name}_build")
    build_dir = Path.joinpath(addon_parent_dir, build_folder_name)

    # Create
    if not build_dir.exists():
        os.makedirs(build_dir)

    # Errors
    if not build_dir.exists():
        return False

    # Assign
    PATH_DATA['BUILD_DIR'] = build_dir
    PATH_DATA['BUILD_FOLDER_NAME'] = build_folder_name
    return True


def set_manifest_file():
    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()

########################•########################
"""                  COMMANDS                 """
########################•########################

def build_extension():
    global BLENDER_EXE_PATH, PATH_DATA, MANIFEST_DATA

    # Error
    if not validate_path_keys(keys=PATH_DATA.keys()):
        return False


    source_dir = PATH_DATA['ADDON_PARENT_DIR']
    output_dir = PATH_DATA['BUILD_DIR']

    command = [
        BLENDER_EXE_PATH,
        "--command", "extension build",
        "--source-dir", source_dir,
        "--output-dir", output_dir,
        "--output-filepath", OUTPUT_FILEPATH,
        "--valid-tags", VALID_TAGS_JSON,
        "--split-platforms",
        "--verbose",
    ]

    try:
        completed_process = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Command succeeded with output: {completed_process.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")


def validate_extension():
    global PATH_DATA

    if not validate_path_keys(keys=PATH_DATA.keys()):
        return False

    command = [
        BLENDER_EXE,
        "--command", "extension validate",
        "--valid-tags", VALID_TAGS_JSON,
        SOURCE_PATH,
    ]

    try:
        completed_process = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Command succeeded with output: {completed_process.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")


########################•########################
"""                 INTERFACE                 """
########################•########################

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
