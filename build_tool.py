########################•########################
"""                   NOTES                   """
########################•########################

'''
______LICENSE______
GNU GENERAL PUBLIC LICENSE

______DISCLAIMER______
This software is provided "as is" without any warranties, express or implied. 
Use at your own risk. The author is not responsible for any damage, data loss, 
or issues arising from the use of this code.

______USAGE______
Run python script from system terminal
>python build_tool.py
Use the GUI interface to set the Directories and Extension Settings
Press Build to generate the build folder, write the manifest file and process the build commands

______LEGEND______
PATH = Full file path with extension
DIR  = Directory only
EXE  = Executable File
MANI = Manifest
VER  = Version
'''

########################•########################
"""                  IMPORTS                  """
########################•########################

import os
import re
import sys
import json
import shutil
import traceback
import subprocess
import tkinter as tk
from pathlib import Path
from collections.abc import Iterable
from tkinter import filedialog, messagebox

########################•########################
"""                   OPTIONS                 """
########################•########################

LICENSES = [
    "SPDX:GPL-3.0-or-later",
    "SPDX:CC0-1.0",
]

EXTENSION_TYPES = [
    "add-on",
    "theme",
]

ADDON_TAGS = [
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
"""                   UTILS                   """
########################•########################

def make_safe_folder_name(name=""):
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*.]', '', name)
    name = re.sub(r'[\x00-\x1f\x7f]', '', name)
    name = name.replace(" ", "_")
    name = name[:255]
    return name

########################•########################
"""                 VALIDATORS                """
########################•########################

is_integer     = lambda item: isinstance(item, int)
is_string      = lambda item: isinstance(item, str) and bool(item.strip())
is_float       = lambda item: isinstance(item, float)
is_tuple       = lambda item: isinstance(item, tuple)
is_path        = lambda item: isinstance(item, (str, Path)) and Path(item).is_file()
is_dir         = lambda item: isinstance(item, (str, Path)) and Path(item).exists()
is_exe         = lambda item: is_path(item) and os.access(item, os.X_OK)
is_folder_name = lambda item: is_string(item) and item == make_safe_folder_name(name=item)
is_iterable    = lambda item: isinstance(item, Iterable) and not isinstance(item, (str, bytes))
is_all_strs    = lambda item: is_iterable(item) and all(is_string(sub) for sub in item)
is_ver_str     = lambda item: is_string(item) and len(item.split(".")) == 3 and all(sub.isdigit() for sub in item.split("."))

########################•########################
"""                 DATA BASE                 """
########################•########################

class DB:
    # --- BLENDER --- #
    BLENDER_EXE_PATH = ""

    # --- SOURCE --- #
    SRC_DIR = ""
    SRC_PARENT_DIR = ""

    # --- BUILD --- #
    BUILD_FOLDER_NAME = ""
    BUILD_DIR = ""

    # --- MANIFEST --- #
    MANI_CREATED = False
    MANI_FILE_NAME  = "blender_manifest.toml"
    MANI_FILE_PATH  = ""
    MANI_SCHEMA_VER = "1.0.0"

    # --- EXTENSION --- #
    EXT_FILE_PATH   = ""
    EXT_ID          = ""
    EXT_NAME        = ""
    EXT_TYPE        = ""
    EXT_ADDON_TAGS  = []
    EXT_THEME_TAGS  = []
    EXT_VERSION     = ""
    EXT_TAG_LINE    = ""
    EXT_MAINTAINER  = ""
    EXT_WEBSITE     = ""
    EXT_B3D_VER_MIN = ""
    EXT_B3D_VER_MAX = ""
    EXT_LICENSE     = ""
    EXT_COPYRIGHT   = []
    EXT_PLATFORMS   = []
    EXT_WHEELS      = []
    EXT_PERMISSIONS = []
    EXT_EXCLUDES    = []

    @classmethod
    def validate_attributes(cls, attrs=[]):
        # Error : Nothing
        if not attrs:
            return False
        # Error : Type
        if not isinstance(attrs, (list, tuple, set)):
            return False
        # Test
        for attr in attrs:
            # Error : Type
            if not isinstance(attr, str):
                return False
            # Error : Non Existent
            if not hasattr(cls, attr):
                return False
            # Validate Attributes
            valid = True
            if attr == 'BLENDER_EXE_PATH':    valid = is_exe(cls.BLENDER_EXE_PATH)
            elif attr == 'SRC_DIR':           valid = is_dir(cls.SRC_DIR)
            elif attr == 'SRC_PARENT_DIR':    valid = is_dir(cls.SRC_PARENT_DIR)
            elif attr == 'BUILD_FOLDER_NAME': valid = is_folder(cls.BUILD_FOLDER_NAME)
            elif attr == 'BUILD_DIR':         valid = is_dir(cls.BUILD_DIR)
            elif attr == 'MANI_FILE_NAME':    valid = is_string(cls.MANI_FILE_NAME)
            elif attr == 'MANI_FILE_PATH':    valid = is_path(cls.MANI_FILE_PATH)
            elif attr == 'MANI_SCHEMA_VER':   valid = is_ver_str(cls.MANI_SCHEMA_VER)
            elif attr == 'EXT_FILE_PATH':     valid = is_path(cls.EXT_FILE_PATH)
            elif attr == 'EXT_ID':            valid = is_string(cls.EXT_ID)
            elif attr == 'EXT_NAME':          valid = is_string(cls.EXT_NAME)
            elif attr == 'EXT_TYPE':          valid = is_string(cls.EXT_TYPE)
            elif attr == 'EXT_ADDON_TAGS':    valid = is_all_strs(cls.EXT_ADDON_TAGS)
            elif attr == 'EXT_THEME_TAGS':    valid = is_all_strs(cls.EXT_THEME_TAGS)
            elif attr == 'EXT_VERSION':       valid = is_ver_str(cls.EXT_VERSION)
            elif attr == 'EXT_TAG_LINE':      valid = is_string(cls.EXT_TAG_LINE)
            elif attr == 'EXT_MAINTAINER':    valid = is_string(cls.EXT_MAINTAINER)
            elif attr == 'EXT_WEBSITE':       valid = is_string(cls.EXT_WEBSITE)
            elif attr == 'EXT_B3D_VER_MIN':   valid = is_ver_str(cls.EXT_B3D_VER_MIN)
            elif attr == 'EXT_B3D_VER_MAX':   valid = is_ver_str(cls.EXT_B3D_VER_MAX)
            elif attr == 'EXT_LICENSE':       valid = is_ver_str(cls.EXT_LICENSE)
            elif attr == 'EXT_COPYRIGHT':     valid = is_all_strs(cls.EXT_COPYRIGHT)
            elif attr == 'EXT_PLATFORMS':     valid = is_all_strs(cls.EXT_PLATFORMS)
            elif attr == 'EXT_WHEELS':        valid = is_all_strs(cls.EXT_WHEELS)
            elif attr == 'EXT_PERMISSIONS':   valid = is_all_strs(cls.EXT_PERMISSIONS)
            elif attr == 'EXT_EXCLUDES':      valid = is_all_strs(cls.EXT_EXCLUDES)
            if not valid:
                return False
        # Valid
        return True

########################•########################
"""                   FOLDERS                 """
########################•########################

def setup_build_folder():
    # Error : Requirements
    if not DB.validate_attributes(attrs=['EXT_ID', 'SRC_PARENT_PATH']):
        return False
    # Path
    DB.BUILD_FOLDER_NAME = make_safe_folder_name(name=f"{DB.EXT_ID}_build")
    DB.BUILD_DIR = Path.joinpath(DB.SRC_PARENT_PATH, DB.BUILD_FOLDER_NAME)
    # Create
    if not DB.BUILD_DIR.exists():
        os.makedirs(DB.BUILD_DIR)
    # Error : Nonexistent
    if not DB.BUILD_DIR.exists():
        return False
    # Valid
    return True

########################•########################
"""                   FILES                   """
########################•########################

def write_manifest_file():
    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()

    DB.MANI_CREATED = True

########################•########################
"""                  COMMANDS                 """
########################•########################

def build_extension():
    # Error : Requirements
    if not DB.validate_attributes(attrs=['BLENDER_EXE_PATH', 'SRC_PATH', 'BUILD_DIR']):
        return False
    if not DB.MANI_CREATED:
        return False


    # Error
    if not validate_data_keys(keys=['BLENDER_EXE_PATH', 'ADDON_PARENT_DIR', 'BUILD_DIR']):
        return False

    global DATA
    blender = DATA['BLENDER_EXE_PATH']
    source_dir = DATA['ADDON_PARENT_DIR']
    output_dir = DATA['BUILD_DIR']

    command = [
        blender,
        "--command", "extension build",
        "--source-dir", source_dir,
        "--output-dir", output_dir,
        "--output-filepath", None,
        "--valid-tags", None,
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

    # Error
    if not validate_data_keys(keys=['BLENDER_EXE_PATH', 'ADDON_DIR', 'ADDON_TYPE', 'ADDON_TAGS', 'THEME_TAGS']):
        return False

    global DATA
    blender = DATA['BLENDER_EXE_PATH']
    addon_dir = DATA['ADDON_DIR']
    addon_type = DATA['ADDON_TYPE']
    addon_tags = DATA['ADDON_TAGS']
    theme_tags = DATA['THEME_TAGS']

    valid_tags_arg = ""
    if addon_type == "add-on":
        tags = [tag for tag in addon_tags if tag in ADDON_TAGS]
        if tags:
            valid_tags_arg = json.dump({"add-on":tags})
    elif addon_type == "theme":
        tags = [tag for tag in theme_tags if tag in THEME_TAGS]
        if tags:
            valid_tags_arg = json.dump({"theme":tags})

    command = [
        blender,
        "--command", "extension validate",
        "--valid-tags", valid_tags_arg,
        addon_dir,
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
