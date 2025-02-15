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
        | Blender                | Required | Notes
        |--------------------------------------------------------------------------------------------------------------------------------------------
        | schema_version         | O        | Internal version of the file format - use 1.0.0
        | maintainer             | O        | Developer name <email@address.com>
        | id                     | O        | Unique identifier for the extension
        | type                   | O        | “add-on” or “theme”
        | name                   | O        | Complete name of the extension
        | version                | O        | Version of the extension
        | tagline                | O        | One-line short description, up to 64 characters - cannot end with punctuation
        | tags                   | X        | Pick tags based on type
        | website                | X        | Website for the extension
        | license                | O        | List of licenses, use SPDX license identifier
        | copyright              | X        | Some licenses require a copyright, copyrights must be “Year Name” or “Year-Year Name”
        | blender_version_min    | O        | Minimum supported Blender version - use at least 4.2.0
        | blender_version_max    | X        | Blender version that the extension does not support, earlier versions are supported
        | permissions            | X        | Options : files, network, clipboard, camera, microphone. Each permission followed by explanation (short single-sentence, up to 64 characters, with no end punctuation)
        | platforms              | X        | List of supported platforms. If omitted, the extension will be available in all operating systems
        | wheels                 | X        | List of relative file-paths Python Wheels
        | paths                  | X        | A list of file-paths relative to the manifest to include when building the package
        | paths_exclude_pattern  | X        | List of string, the pattern matching is compatible with gitignore
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
from tkinter import filedialog, messagebox
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

WIG__BLENDER_EXE = None
VAR__BLENDER_EXE = None


# --- Section 2 --- #
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

    # Blender Exe Path
    global WIG__BLENDER_EXE, VAR__BLENDER_EXE
    # Var
    VAR__BLENDER_EXE = tk.StringVar(value="")
    # Label
    label = tk.Label(frame, text="Blender")
    label.pack(side=tk.LEFT, padx=5)
    # Entry
    WIG__BLENDER_EXE = tk.Entry(frame, textvariable=VAR__BLENDER_EXE)
    WIG__BLENDER_EXE.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    WIG__BLENDER_EXE.bind("<Return>", blender_exe_entry_CB)
    # Button
    button = tk.Button(frame, text="Open Executable", command=blender_exe_btn_CB)
    button.pack(side=tk.LEFT, padx=5)




@try_except_decorator
def build_section_2_INFO(frame):
    ''' Extension | Versions | Developer | License | Build '''

    # Notebook
    notebook = ttk.Notebook(frame)
    notebook.grid(row=0, column=0, sticky="nsew")

    # Configure
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Extension
    ext_tab = tk.Frame(notebook)
    tools_var = tk.StringVar(value="None")
    for tool in ["Resizing", "Rotating"]:
        radio_btn = tk.Radiobutton(ext_tab, text=tool, variable=tools_var, value=tool)
        radio_btn.pack(anchor="w", padx=20, pady=5)

    # Version
    ver_tab = tk.Frame(notebook)
    tools_var = tk.StringVar(value="None")
    for tool in ["Resizing", "Rotating"]:
        radio_btn = tk.Radiobutton(ver_tab, text=tool, variable=tools_var, value=tool)
        radio_btn.pack(anchor="w", padx=20, pady=5)

    # Developer
    dev_tab = tk.Frame(notebook)
    tools_var = tk.StringVar(value="None")
    for tool in ["Resizing", "Rotating"]:
        radio_btn = tk.Radiobutton(dev_tab, text=tool, variable=tools_var, value=tool)
        radio_btn.pack(anchor="w", padx=20, pady=5)

    # License
    lic_tab = tk.Frame(notebook)
    tools_var = tk.StringVar(value="None")
    for tool in ["Resizing", "Rotating"]:
        radio_btn = tk.Radiobutton(lic_tab, text=tool, variable=tools_var, value=tool)
        radio_btn.pack(anchor="w", padx=20, pady=5)

    # Build
    bld_tab = tk.Frame(notebook)
    tools_var = tk.StringVar(value="None")
    for tool in ["Resizing", "Rotating"]:
        radio_btn = tk.Radiobutton(bld_tab, text=tool, variable=tools_var, value=tool)
        radio_btn.pack(anchor="w", padx=20, pady=5)

    # Add Tabs
    notebook.add(ext_tab, text="Extension")
    notebook.add(ver_tab, text="Version")
    notebook.add(dev_tab, text="Developer")
    notebook.add(lic_tab, text="License")
    notebook.add(bld_tab, text="Build")


@try_except_decorator
def build_section_3_PREVIEWS(frame):
    ''' Manifest | Validate | Build '''
    pass


@try_except_decorator
def build_section_4_UTILS(frame):
    ''' Docs | Extensions '''
    pass


@try_except_decorator
def build_section_5_STATUS(frame):
    ''' Valid | Built '''
    pass


@try_except_decorator
def build_section_6_ACTIONS(frame):
    ''' Validate | Build '''
    pass

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

    # Colors
    color_a = "lightgray"
    color_b = "white"

    # Create frames
    frame_1 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_a)
    frame_2 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_b)
    frame_3 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_a)
    frame_4 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_b)
    frame_5 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_a)
    frame_6 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_b)

    # Rows
    frame_1.grid(row=0, column=0, sticky="nsew")
    frame_2.grid(row=1, column=0, sticky="nsew")
    frame_3.grid(row=2, column=0, sticky="nsew")
    frame_4.grid(row=3, column=0, sticky="nsew")
    frame_5.grid(row=4, column=0, sticky="nsew")
    frame_6.grid(row=5, column=0, sticky="nsew")

    # Configure Frames
    APP_ROOT.grid_rowconfigure(0, weight=1)
    APP_ROOT.grid_rowconfigure(1, weight=6)
    APP_ROOT.grid_rowconfigure(2, weight=4)
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


class FilePickController:
    def __init__(self, parent, label="Blender", file_types=(("All Files", "*.*"),)):
        self.frame = tk.Frame(parent, padx=2, pady=2, borderwidth=1, relief="solid")
        self.frame.pack(fill=tk.X)
        self.file_types = file_types
        
        # Label
        self.label = tk.Label(self.frame, text=label)
        self.label.pack(side=tk.LEFT, padx=5)
        
        # Entry field
        self.entry = tk.Entry(self.frame)
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Button to open file dialog
        self.button = tk.Button(self.frame, text="Open Executable", command=self.open_file_dialog)
        self.button.pack(side=tk.LEFT, padx=5)

        # Bind the FocusOut event to check validity
        self.entry.bind("<FocusOut>", self.on_focus_out)

    def open_file_dialog(self):
        # Open file dialog to select an executable file
        file_path = filedialog.askopenfilename(title="Select an Executable File", filetypes=self.file_types)
        
        if file_path:
            # Insert selected file path into the entry
            self.entry.delete(0, tk.END)
            self.entry.insert(0, file_path)

    def on_focus_out(self, event):
        # Get the value from the entry field
        entered_value = self.entry.get()
        
        # Check if the entered value is a valid executable file (basic check)
        if entered_value:
            if os.path.isfile(entered_value) and os.access(entered_value, os.X_OK):
                print(f"Valid executable: {entered_value}")
            else:
                print("Invalid executable file!")
                self.entry.delete(0, tk.END)  # Optionally clear the entry if invalid
                self.entry.insert(0, "Invalid executable")
        else:
            print("No path entered.")
            self.entry.delete(0, tk.END)  # Optionally clear the entry if no path entered
            self.entry.insert(0, "No path entered")


class VerController:
    def __init__(self, parent, label="Version", min_ver=(0,0,0), add_use_check=False):
        self.frame = tk.Frame(parent, padx=2, pady=2, borderwidth=1, relief="solid")
        self.frame.pack(fill=tk.X)

        self.var_major = tk.IntVar(value=min_ver[0])
        self.var_minor = tk.IntVar(value=min_ver[1])
        self.var_patch = tk.IntVar(value=min_ver[2])
        self.var_use   = None
        if add_use_check:
            self.var_use = tk.BooleanVar(value=False)

        self.label = tk.Label(self.frame, text=label)
        self.spin_major = tk.Spinbox(self.frame, from_=min_ver[0], to=sys.maxsize, textvariable=self.var_major, width=5)
        self.spin_minor = tk.Spinbox(self.frame, from_=min_ver[1], to=sys.maxsize, textvariable=self.var_minor, width=5)
        self.spin_patch = tk.Spinbox(self.frame, from_=min_ver[2], to=sys.maxsize, textvariable=self.var_patch, width=5)
        self.check_box = None
        if add_use_check:
            self.check_box = tk.Checkbutton(self.frame, text='Use', variable=self.var_use, command=self.com_check_box, width=5)

        self.label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        if add_use_check:
            self.check_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        else:
            self.spin_major.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
            self.spin_minor.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
            self.spin_patch.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)


    def com_check_box(self):
        if self.var_use.get():
            self.spin_major.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            self.spin_minor.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            self.spin_patch.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        else:
            self.spin_major.pack_forget()
            self.spin_minor.pack_forget()
            self.spin_patch.pack_forget()


    def get_version(self):
        # Check box is not used
        if self.check_box and self.var_use and not self.var_use.get():
            return None
        # Valid
        return (self.var_major.get(), self.var_minor.get(), self.var_patch.get())


class App:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)

        # Blender Path
        self.blender_file_picker = FilePickController(
            self.frame, 
            label="Blender Executable", 
            file_types=(("Executable Files", "*.exe"), ("All Files", "*.*"))
        )

        # Versions
        self.ext_version = VerController(self.frame, label="Extension Version")
        self.b3d_ver_min = VerController(self.frame, label="Blender Version Min", min_ver=(4,2,0))
        self.b3d_ver_max = VerController(self.frame, label="Blender Version Max", min_ver=(4,2,0), add_use_check=True)