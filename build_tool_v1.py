########################•########################
"""                   NOTES                   """
########################•########################

'''
    ___ LICENSE ___
        GNU GENERAL PUBLIC LICENSE

    ___ DISCLAIMER ___
        This software is provided "as is" without any warranties, express or implied. 
        Use at your own risk. The author is not responsible for any damage, data loss, 
        or issues arising from the use of this code.

    ___ USAGE ___
        Run python script from system terminal
        >python build_tool.py
        Use the GUI interface to set the Directories and Extension Settings
        Press Build to generate the build folder, write the manifest file and process the build commands

    ___ Tkinter ___
        ttk = "Themed" Tk
        ttk widgets = Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale, Scrollbar, Spinbox, Combobox, Notebook, Progressbar, Separator, Sizegrip, Treeview

    ___ Manifest File Layout ___
        |--------------------------------------------------------------------------------------------------------------------------------------------
        |        Blender         | Required |    TAB    |        Notes
        |--------------------------------------------------------------------------------------------------------------------------------------------
        | schema_version         | O        |           | Internal version of the file format - use 1.0.0
        | id                     | O        | Extension | Unique identifier for the extension
        | type                   | O        | Extension | “add-on” or “theme”
        | name                   | O        | Extension | Complete name of the extension
        | tagline                | O        | Extension | One-line short description, up to 64 characters - cannot end with punctuation
        | tags                   | X        | Extension | Pick tags based on type
        | maintainer             | O        | Developer | Developer name <email@address.com>
        | website                | X        | Developer | Website for the extension
        | license                | O        | License   | List of licenses, use SPDX license identifier
        | copyright              | X        | License   | Some licenses require a copyright, copyrights must be “Year Name” or “Year-Year Name”
        | version                | O        | Version   | Version of the extension
        | blender_version_min    | O        | Version   | Minimum supported Blender version - use at least 4.2.0
        | blender_version_max    | X        | Version   | Blender version that the extension does not support, earlier versions are supported
        | permissions            | X        | Build     | Options : files, network, clipboard, camera, microphone. Each permission followed by explanation (short single-sentence, up to 64 characters, with no end punctuation)
        | platforms              | X        | Build     | List of supported platforms. If omitted, the extension will be available in all operating systems
        | wheels                 | X        | Build     | List of relative file-paths Python Wheels
        | paths                  | X        | Build     | A list of file-paths relative to the manifest to include when building the package
        | paths_exclude_pattern  | X        | Build     | List of string, the pattern matching is compatible with gitignore
        |--------------------------------------------------------------------------------------------------------------------------------------------
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
from pathlib import Path
from collections.abc import Iterable
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup

########################•########################
"""                 DECORATORS                """
########################•########################

def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"ERROR : {func.__name__}()")
            traceback.print_exc()
    return wrapper

########################•########################
"""                   OPTIONS                 """
########################•########################

LICENSES = {}

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
"""                 VALIDATORS                """
########################•########################

def create_safe_name(name=""):
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*.]', '', name)
    name = re.sub(r'[\x00-\x1f\x7f]', '', name)
    name = name.replace(" ", "_")
    name = name[:255]
    return name


def get_file_extension(file_path):
    return Path(file_path).suffix.lower()


is_integer     = lambda item: isinstance(item, int)
is_string      = lambda item: isinstance(item, str) and bool(item.strip())
is_float       = lambda item: isinstance(item, float)
is_tuple       = lambda item: isinstance(item, tuple)
is_path        = lambda item: isinstance(item, (str, Path)) and Path(item).is_file()
is_dir         = lambda item: isinstance(item, (str, Path)) and Path(item).exists()
is_exe         = lambda item: is_path(item) and os.access(item, os.X_OK)
is_folder_name = lambda item: is_string(item) and item == create_safe_name(name=item)
is_file_name   = lambda item: is_string(item) and len(os.path.splitext(item)) == 2 and all(is_string(sub) for sub in os.path.splitext(item))
is_iterable    = lambda item: isinstance(item, Iterable) and not isinstance(item, (str, bytes))
is_all_strs    = lambda item: is_iterable(item) and all(is_string(sub) for sub in item)
is_ver_str     = lambda item: is_string(item) and len(item.split(".")) == 3 and all(sub.isdigit() for sub in item.split("."))
is_email       = lambda item: is_string(item) and bool(re.match(r"[^@]+@[^@]+\.[^@]+", item))
is_website     = lambda item: is_string(item) and bool(re.match(r'^(http[s]?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(/[\w\-._~:/?#[\]@!$&\'()*+,;=]*)?$', item))

does_file_ext_match           = lambda file_path, file_ext : is_path(file_path) and is_string(file_ext) and get_file_extension(file_path) == file_ext.lower()
does_file_name_match_no_ext   = lambda file_path, file_name: is_path(file_path) and is_string(file_name) and Path(file_path).name == file_name
does_file_name_match_with_ext = lambda file_path, file_name: is_path(file_path) and is_file_name(file_name) and Path(file_path).name.lower() == file_name.lower()

########################•########################
"""                 VARIABLES                 """
########################•########################

# --- Section 1 --- #

VAR__BLENDER_EXE = None
WIG__BLENDER_EXE = None

VAR__SOURCE_DIR = None
WIG__SOURCE_DIR = None

VAR__BUILD_DIR = None
WIG__BUILD_DIR = None

# --- Section 2 --- #

VAR_ADDON_TAGS = None
VAR_THEME_TAGS = None

# --- Section 3 --- #
# --- Section 4 --- #
# --- Section 5 --- #
# --- Section 6 --- #


########################•########################
"""                  BUILDERS                 """
########################•########################

@try_except_decorator
def set_licenses():
    global LICENSES
    url = 'https://spdx.org/licenses/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    licenses = {}
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) >= 2:
            full_name = columns[0].get_text(strip=True).replace('\"', '')
            identifier = columns[1].get_text(strip=True).replace('\"', '')
            if full_name and identifier:
                licenses[full_name] = identifier
    for key, value in licenses.items():
        LICENSES[key] = f"SPDX:{value}"


@try_except_decorator
def setup_build_folder():
    # Error : Requirements
    if not DB.validate_attributes(attrs=['EXT_ID', 'SRC_PARENT_DIR']):
        return False
    # Path
    DB.BUILD_FOLDER_NAME = create_safe_name(name=f"{DB.EXT_ID}_build")
    DB.BUILD_DIR = Path.joinpath(DB.SRC_PARENT_DIR, DB.BUILD_FOLDER_NAME)
    # Create
    if not DB.BUILD_DIR.exists():
        os.makedirs(DB.BUILD_DIR)
    # Error : Nonexistent
    if not DB.BUILD_DIR.exists():
        return False
    # Valid
    return True


@try_except_decorator
def write_manifest_file():
    # Error : Source Dir
    if not DB.validate_attributes(attrs=['SRC_DIR']):
        return False
    # Error : Required
    if not DB.validate_attributes(attrs=['MANI_SCHEMA_VER', 'DEV_AUTHOR', 'EXT_ID', 'EXT_TYPE', 'EXT_NAME', 'EXT_VERSION', 'EXT_TAG_LINE', 'EXT_LICENSES', 'BLENDER_VER_MIN']):
        return False
    # Mani File Path
    DB.MANI_FILE_PATH = Path.joinpath(DB.SRC_DIR, DB.MANI_FILE_NAME)
    # Write File Content
    with open(DB.MANI_FILE_PATH, "w") as file:
        write = file.write
        write(f'schema_version = "{DB.MANI_SCHEMA_VER}"\n')
        if DB.validate_attribute(attr='DEV_EMAIL'):
            write(f'maintainer = {DB.DEV_AUTHOR} <{DB.DEV_EMAIL}>\n')
        else:
            write(f'maintainer = {DB.DEV_AUTHOR}\n')
        write(f'id = "{DB.EXT_ID}"\n')
        write(f'type = "{DB.EXT_TYPE}"\n')
        write(f'name = "{DB.EXT_NAME}"\n')
        write(f'version = "{DB.EXT_VERSION}"\n')
        write(f'tagline = "{DB.EXT_TAG_LINE[:64]}"\n')
        if DB.validate_attributes(attrs=['EXT_ADDON_TAGS', 'EXT_THEME_TAGS']):
            tags = DB.EXT_ADDON_TAGS if DB.EXT_TYPE == 'add-on' else DB.EXT_THEME_TAGS
            write("tags = [\n")
            for item in tags:
                write(f'\t"{item}",\n')
            write("]\n")
        if DB.validate_attribute(attr='EXT_WEBSITE'):
            add(f'website = "{DB.EXT_WEBSITE}"')
        write("license = [\n")
        for item in DB.EXT_LICENSES:
            write(f'\t"{item}",\n')
        write("]\n")
        if DB.EXT_COPYRIGHT and DB.validate_attribute(attr='EXT_COPYRIGHT'):
            write("copyright = [\n")
            for item in DB.EXT_COPYRIGHT:
                write(f'\t"{item}",\n')
            write("]\n")
        write(f'blender_version_min = "{DB.BLENDER_VER_MIN}"\n')
        if DB.validate_attribute(attr='BLENDER_VER_MAX'):
            write(f'blender_version_max = "{DB.BLENDER_VER_MAX}"\n')
        if any(bool(reason_msg) for reason_msg in DB.EXT_PERMISSIONS.values()):
            write('[permissions]\n')
            for permission_type, reason_msg in DB.EXT_PERMISSIONS.items():
                if reason_msg:
                    write(f'{permission_type} = "{reason_msg}"\n')
        if DB.EXT_PLATFORMS and DB.validate_attribute(attr='EXT_PLATFORMS'):
            write("platforms = [\n")
            for item in DB.EXT_PLATFORMS:
                write(f'\t"{item}",\n')
            write("]\n")
        if DB.EXT_WHEELS and DB.validate_attribute(attr='EXT_WHEELS'):
            write("wheels = [\n")
            for item in DB.EXT_WHEELS:
                write(f'\t"{item}",\n')
            write("]\n")
        if DB.EXT_PATH_INCLUDES and DB.validate_attribute(attr='EXT_PATH_INCLUDES'):
            write("[build]")
            write("paths = [\n")
            for item in DB.EXT_PATH_INCLUDES:
                write(f'\t"{item}",\n')
            write("]\n")
        elif DB.EXT_PATH_EXCLUDES and DB.validate_attribute(attr='EXT_PATH_EXCLUDES'):
            write("[build]")
            write("paths_exclude_pattern = [\n")
            for item in DB.EXT_PATH_EXCLUDES:
                write(f'\t"{item}",\n')
            write("]\n")
    # Error : Mani File
    if not is_path(DB.MANI_FILE_PATH):
        return False
    # Valid
    return True

########################•########################
"""                  COMMANDS                 """
########################•########################

@try_except_decorator
def validate_manifest():
    # Error : Requirements
    if not DB.validate_attributes(attrs=['BLENDER_EXE_PATH', 'SRC_DIR']):
        return False

    command = [
        DB.BLENDER_EXE_PATH,
        "--command", "extension validate",
        DB.SRC_DIR,
    ]
    try:
        completed_process = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Command succeeded with output: {completed_process.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")


@try_except_decorator
def build_extension():
    # Error : Requirements
    if not DB.validate_attributes(attrs=['BLENDER_EXE_PATH', 'SRC_DIR', 'BUILD_DIR']):
        return False

    command = [
        DB.BLENDER_EXE_PATH,
        "--command", "extension build",
        "--source-dir", DB.SRC_DIR,
        "--output-dir", DB.BUILD_DIR,
        "--output-filepath", f"{DB.EXT_ID}-{DB.EXT_VERSION}.zip",
        "--valid-tags", "",
    ]
    if DB.BUILD_SPLIT_PLATS:
        command.append("--split-platforms")
    if DB.BUILD_VERBOSE:
        command.append("--verbose")
    try:
        completed_process = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Command succeeded with output: {completed_process.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")

########################•########################
"""                 CALLBACKS                 """
########################•########################

# --- Section 1 --- #

def blender_exe_entry_CB(event):
    value = VAR__BLENDER_EXE.get()
    widget = WIG__BLENDER_EXE
    if value:
        if os.path.isfile(value) and os.access(value, os.X_OK):
            print(f"Valid executable : {value}")
        else:
            print(f"Invalid executable : {value}")
            widget.delete(0, tk.END)
            widget.insert(0, "Invalid")
    else:
        print("No path entered.")
        widget.delete(0, tk.END)
        widget.insert(0, "Invalid")


def blender_exe_btn_CB():
    widget = WIG__BLENDER_EXE
    file_types = (("All Files", "*.*"),)
    file_path = filedialog.askopenfilename(title="Select Blender Executable", filetypes=file_types)
    print(f"Selected Path : {file_path}")
    if file_path and is_exe(file_path):
        widget.delete(0, tk.END)
        widget.insert(0, file_path)


def source_dir_entry_CB(event):
    value = VAR__SOURCE_DIR.get()
    widget = WIG__SOURCE_DIR
    if value:
        if is_dir(value):
            print(f"Valid Path : {value}")
        else:
            print(f"Invalid Path : {value}")
            widget.delete(0, tk.END)
            widget.insert(0, "Invalid")
    else:
        print("No path entered.")
        widget.delete(0, tk.END)
        widget.insert(0, "Invalid")


def source_dir_btn_CB():
    widget = WIG__SOURCE_DIR
    folder_dir = filedialog.askdirectory(title="Select Source Folder")
    print(f"Selected Directory : {folder_dir}")
    if folder_dir and is_dir(folder_dir):
        widget.delete(0, tk.END)
        widget.insert(0, folder_dir)


def build_dir_entry_CB(event):
    value = VAR__BUILD_DIR.get()
    widget = WIG__BUILD_DIR
    if value:
        if is_dir(value):
            print(f"Valid Path : {value}")
        else:
            print(f"Invalid Path : {value}")
            widget.delete(0, tk.END)
            widget.insert(0, "Invalid")
    else:
        print("No path entered.")
        widget.delete(0, tk.END)
        widget.insert(0, "Invalid")


def build_dir_btn_CB():
    widget = WIG__BUILD_DIR
    folder_dir = filedialog.askdirectory(title="Select Source Folder")
    print(f"Selected Directory : {folder_dir}")
    if folder_dir and is_dir(folder_dir):
        widget.delete(0, tk.END)
        widget.insert(0, folder_dir)

# --- Section 2 --- #
# --- Section 3 --- #
# --- Section 4 --- #
# --- Section 5 --- #
# --- Section 6 --- #

########################•########################
"""                 SECTIONS                  """
########################•########################

@try_except_decorator
def build_section_1_PATHS(frame):
    ''' Blender.exe | Source | Build '''

    # Configure Frame
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=5)
    frame.grid_columnconfigure(2, weight=1)

    # Blender Exe
    global VAR__BLENDER_EXE, WIG__BLENDER_EXE
    # Var
    VAR__BLENDER_EXE = tk.StringVar(value="")
    # Label
    label = tk.Label(frame, text="Blender Path")
    label.grid(row=0, column=0, sticky="w", padx=5)
    # Entry
    WIG__BLENDER_EXE = tk.Entry(frame, textvariable=VAR__BLENDER_EXE)
    WIG__BLENDER_EXE.grid(row=0, column=1, sticky="we", padx=5)
    WIG__BLENDER_EXE.bind("<Return>", blender_exe_entry_CB)
    # Button
    button = tk.Button(frame, text="Open", command=blender_exe_btn_CB)
    button.grid(row=0, column=2, sticky="e", padx=5)

    # Soure Directory
    global VAR__SOURCE_DIR, WIG__SOURCE_DIR
    # Var
    VAR__SOURCE_DIR = tk.StringVar(value="")
    # Label
    label = tk.Label(frame, text="Source Directory")
    label.grid(row=1, column=0, sticky="w", padx=5)
    # Entry
    WIG__SOURCE_DIR = tk.Entry(frame, textvariable=VAR__SOURCE_DIR)
    WIG__SOURCE_DIR.grid(row=1, column=1, sticky="we", padx=5)
    WIG__SOURCE_DIR.bind("<Return>", source_dir_entry_CB)
    # Button
    button = tk.Button(frame, text="Open", command=source_dir_btn_CB)
    button.grid(row=1, column=2, sticky="e", padx=5)

    # Build Directory
    global VAR__BUILD_DIR, WIG__BUILD_DIR
    # Var
    VAR__BUILD_DIR = tk.StringVar(value="")
    # Label
    label = tk.Label(frame, text="Build Directory")
    label.grid(row=2, column=0, sticky="w", padx=5)
    # Entry
    WIG__BUILD_DIR = tk.Entry(frame, textvariable=VAR__BUILD_DIR)
    WIG__BUILD_DIR.grid(row=2, column=1, sticky="we", padx=5)
    WIG__BUILD_DIR.bind("<Return>", source_dir_entry_CB)
    # Button
    button = tk.Button(frame, text="Open", command=source_dir_btn_CB)
    button.grid(row=2, column=2, sticky="e", padx=5)


@try_except_decorator
def build_section_2_INFO(frame):
    ''' Extension | Versions | Developer | License | Build '''

    # Configure
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Notebook
    notebook = ttk.Notebook(frame)
    notebook.grid(row=0, column=0, sticky="nsew", padx=10)

    # --- Extension --- #
    tab_1 = tk.Frame(notebook)
    global VAR_ADDON_TAGS, VAR_THEME_TAGS

    label = tk.Label(tab_1, text="Extension Tags")
    label.grid(row=0, column=0, sticky="w")

    VAR_ADDON_TAGS = tk.StringVar(value=ADDON_TAGS)
    VAR_THEME_TAGS = tk.StringVar(value=THEME_TAGS)
    tags_box = tk.Listbox(tab_1, listvariable=VAR_ADDON_TAGS, selectmode=tk.MULTIPLE, height=len(ADDON_TAGS))
    tags_box.grid(row=1, column=0, sticky="w")

    # --- Version --- #
    tab_2 = tk.Frame(notebook)

    # --- Developer --- #
    tab_3 = tk.Frame(notebook)

    # --- License --- #
    tab_4 = tk.Frame(notebook)

    # --- Build --- #
    tab_5 = tk.Frame(notebook)


    # Add Tabs
    notebook.add(tab_1, text="Extension")
    notebook.add(tab_2, text="Version")
    notebook.add(tab_3, text="Developer")
    notebook.add(tab_4, text="License")
    notebook.add(tab_5, text="Build")


@try_except_decorator
def build_section_3_PREVIEWS(frame):
    ''' Manifest | Validate | Build '''

    # Configure
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Notebook
    notebook = ttk.Notebook(frame)
    notebook.grid(row=0, column=0, sticky="nsew", padx=10)

    # Manifest
    tab_1 = tk.Frame(notebook)
    tools_var = tk.StringVar(value="None")
    for tool in ["Resizing", "Rotating"]:
        radio_btn = tk.Radiobutton(tab_1, text=tool, variable=tools_var, value=tool)
        radio_btn.pack(anchor="w", padx=20, pady=5)

    # Validate Command
    tab_2 = tk.Frame(notebook)
    tools_var = tk.StringVar(value="None")
    for tool in ["Resizing", "Rotating"]:
        radio_btn = tk.Radiobutton(tab_2, text=tool, variable=tools_var, value=tool)
        radio_btn.pack(anchor="w", padx=20, pady=5)

    # Build Command
    tab_3 = tk.Frame(notebook)
    tools_var = tk.StringVar(value="None")
    for tool in ["Resizing", "Rotating"]:
        radio_btn = tk.Radiobutton(tab_3, text=tool, variable=tools_var, value=tool)
        radio_btn.pack(anchor="w", padx=20, pady=5)

    # Add Tabs
    notebook.add(tab_1, text="Manifest")
    notebook.add(tab_2, text="Validate Command")
    notebook.add(tab_3, text="Build Command")


@try_except_decorator
def build_section_4_UTILS(frame):
    ''' Docs | Extensions '''

    # Configure Frame
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=1)

    # Docs
    button = tk.Button(frame, text="Docs", command=None)
    button.grid(row=0, column=0, sticky="we", padx=5)

    # Extensions
    button = tk.Button(frame, text="Extensions", command=None)
    button.grid(row=0, column=1, sticky="we", padx=5)

    # Notes
    button = tk.Button(frame, text="Notes", command=None)
    button.grid(row=0, column=2, sticky="we", padx=5)

    # Loader
    button = tk.Button(frame, text="Loader", command=None)
    button.grid(row=0, column=3, sticky="we", padx=5)


@try_except_decorator
def build_section_5_STATUS(frame):
    ''' Valid | Built '''

    # Configure Frame
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Valid
    label = tk.Label(frame, text="Valid : False")
    label.grid(row=0, column=0, sticky="we", padx=5)

    # Built
    label = tk.Label(frame, text="Built : False")
    label.grid(row=0, column=1, sticky="we", padx=5)


@try_except_decorator
def build_section_6_ACTIONS(frame):
    ''' Validate | Build '''

    # Configure Frame
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Docs
    button = tk.Button(frame, text="Validate", command=None)
    button.grid(row=0, column=0, sticky="we", padx=5)

    # Extensions
    button = tk.Button(frame, text="Build", command=None)
    button.grid(row=0, column=1, sticky="we", padx=5)

########################•########################
"""                APPLICATION                """
########################•########################

APP_ROOT = None
APP_NAME = "Blender Extension Creator"
APP_WIDTH = 600
APP_HEIGHT = 800
APP_RESIZABLE = True


@try_except_decorator
def create_app():
    global APP_ROOT
    APP_ROOT = tk.Tk()
    APP_ROOT.title(APP_NAME)
    APP_ROOT.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
    if APP_RESIZABLE:
        APP_ROOT.resizable(True, True)
    else:
        APP_ROOT.resizable(False, False)


@try_except_decorator
def create_sections():
    # Configure main grid
    APP_ROOT.grid_columnconfigure(0, weight=1)
    APP_ROOT.grid_rowconfigure(0, weight=1)

    # Create frames
    frame_1 = tk.Frame(APP_ROOT, padx=5, pady=2)
    frame_2 = tk.Frame(APP_ROOT, padx=5, pady=2)
    frame_3 = tk.Frame(APP_ROOT, padx=5, pady=2)
    frame_4 = tk.Frame(APP_ROOT, padx=5, pady=2)
    frame_5 = tk.Frame(APP_ROOT, padx=5, pady=2)
    frame_6 = tk.Frame(APP_ROOT, padx=5, pady=2)

    # Rows
    frame_1.grid(row=0, column=0, sticky="nsew")
    frame_2.grid(row=1, column=0, sticky="nsew")
    frame_3.grid(row=2, column=0, sticky="nsew")
    frame_4.grid(row=3, column=0, sticky="nsew")
    frame_5.grid(row=4, column=0, sticky="nsew")
    frame_6.grid(row=5, column=0, sticky="nsew")

    # Configure Frames
    APP_ROOT.grid_rowconfigure(0, weight=1)
    APP_ROOT.grid_rowconfigure(1, weight=30)
    APP_ROOT.grid_rowconfigure(2, weight=10)
    APP_ROOT.grid_rowconfigure(3, weight=1)
    APP_ROOT.grid_rowconfigure(4, weight=1)
    APP_ROOT.grid_rowconfigure(5, weight=1)

    # Sections
    build_section_1_PATHS(frame_1)
    build_section_2_INFO(frame_2)
    build_section_3_PREVIEWS(frame_3)
    build_section_4_UTILS(frame_4)
    build_section_5_STATUS(frame_5)
    build_section_6_ACTIONS(frame_6)


if __name__ == "__main__":
    # set_licenses()
    create_app()
    create_sections()
    if APP_ROOT:
        APP_ROOT.mainloop()
    else:
        print("Setup Failed")

