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
from tkinter.simpledialog import Dialog
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

# Key : Full License Name
# Val : SPDX: + Shorter Name
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
    "__pycache__/",
    "*.py[cod]",
    "*$py.class",
    "*.so",
    ".Python",
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "wheels/",
    "share/python-wheels/",
    "*.egg-info/",
    ".installed.cfg",
    "*.egg",
    "MANIFEST",
    "*.manifest",
    "*.spec",
    "pip-log.txt",
    "pip-delete-this-directory.txt",
    "htmlcov/",
    ".tox/",
    ".nox/",
    ".coverage",
    ".coverage.*",
    ".cache",
    "nosetests.xml",
    "coverage.xml",
    "*.cover",
    "*.py,cover",
    ".hypothesis/",
    ".pytest_cache/",
    "cover/",
    "*.mo",
    "*.pot",
    "*.log",
    "local_settings.py",
    "db.sqlite3",
    "db.sqlite3-journal",
    "instance/",
    ".webassets-cache",
    ".scrapy",
    "docs/_build/",
    ".pybuilder/",
    "target/",
    ".ipynb_checkpoints",
    "profile_default/",
    "ipython_config.py",
    ".pdm.toml",
    "__pypackages__/",
    "celerybeat-schedule",
    "celerybeat.pid",
    "*.sage.py",
    ".env",
    ".venv",
    "env/",
    "venv/",
    "ENV/",
    "env.bak/",
    "venv.bak/",
    ".spyderproject",
    ".spyproject",
    ".ropeproject",
    "/site",
    ".mypy_cache/",
    ".dmypy.json",
    "dmypy.json",
    ".pyre/",
    ".pytype/",
    "cython_debug/",
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
is_str_int     = lambda item: is_string(item) and item.isdigit()

does_file_ext_match           = lambda file_path, file_ext : is_path(file_path) and is_string(file_ext) and get_file_extension(file_path) == file_ext.lower()
does_file_name_match_no_ext   = lambda file_path, file_name: is_path(file_path) and is_string(file_name) and Path(file_path).name == file_name
does_file_name_match_with_ext = lambda file_path, file_name: is_path(file_path) and is_file_name(file_name) and Path(file_path).name.lower() == file_name.lower()

########################•########################
"""                  SETTINGS                 """
########################•########################

APP_NAME = "Blender Extension Creator"
APP_RESIZABLE = False
LABEL_WIDTH = 150
PADX = 4
PADY = 4
WSTICKY = "nsew"

########################•########################
"""                  GUI HELPERS              """
########################•########################

class EntryPopup(Dialog):
    def __init__(self, parent, width=100, height=100, label_text="", prompt_text="", entry_text=""):
        self.parent = parent
        self.width = width
        self.height = height
        self.label_text = label_text
        self.prompt_text = prompt_text
        self.entry_text = entry_text
        self.result = ""
        self.label = None
        self.entry = None
        super().__init__(parent, label_text)
    def body(self, frame):
        self.geometry(f"{self.width}x{self.height}")
        self.label = tk.Label(frame, text=self.prompt_text)
        self.label.pack(padx=PADX, pady=PADY)
        self.entry = tk.Entry(frame, width=self.width)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.entry_text)
        self.entry.pack(padx=PADX, pady=PADY)
        return self.entry
    def apply(self):
        if self.entry:
            self.result = self.entry.get()


    @staticmethod
    def invoke(parent, width=100, height=100, label_text="", prompt_text="", entry_text=""):
        popup = EntryPopup(parent, width, height, label_text, prompt_text, entry_text)
        return popup.result


class CharsReplacer:
    def __init__(self, filter_map=dict()):
        self.filter_map = filter_map

    def process(self, chars=""):
        if not chars: return ""
        if not isinstance(chars, str): return ""
        if not self.filter_map: return chars
        chars = "".join([self.filter_map.get(char, char) for char in chars])
        return chars


class CharsLimiter:
    def __init__(self, limit=64):
        self.limit = limit

    def process(self, chars=""):
        if not chars: return ""
        if not isinstance(chars, str): return ""
        return chars[:self.limit]


class COLORS:
    BG1    = "#EEEEEE" # Light Grey
    BG2    = "#CCCCCC" # Medium Grey
    BG3    = "#AAAAAA" # Dark Grey
    BG4    = "#351163" # Dark Purple
    BG5    = "#1e0938" # Darker Purple
    BLACK  = "#050D0F" # Black
    WHITE  = "#F3F3F3" # White
    VALID  = "#4ceb34" # Green
    ERROR  = "#E56B6F" # Red
    REQ    = "#faef28" # Yellow


class RELIEF:
    FLAT = "flat"
    RAISED = "raised"
    SUNKEN = "sunken"
    RIDGE = "ridge"
    SOLID = "solid"
    GROOVE = "groove"

# TTK
def setup_styles():
    style = ttk.Style()

    style_settings = {
        "TNotebook": {
            "configure": {
                "tabmargins": [2, 5, 2, 0],
                "background": COLORS.BG5
            }
        },
        "TNotebook.Tab": {
            "configure": {
                "padding": [4, 4],
                "background": COLORS.BG4,
                "foreground": COLORS.WHITE
            },
            "map": {
                "background": [("selected", COLORS.VALID)],
                "foreground": [("selected", COLORS.BG4)],
                "expand": [("selected", [1, 1, 1, 0])]
            }
        }
    }
    style.theme_create("KodoTabs", parent="alt", settings=style_settings)
    style.theme_use("KodoTabs")

# TK
def config_widget(widget, required=False):
    if isinstance(widget, tk.Frame):
        widget.config(padx=PADX, pady=PADY, background=COLORS.BLACK, borderwidth=1, relief=RELIEF.RAISED, highlightcolor=COLORS.BG4, highlightbackground=COLORS.BG4, highlightthickness=1)
    elif isinstance(widget, tk.Label):
        if required:
            widget.config(background=COLORS.BLACK, fg=COLORS.REQ)
        else:
            widget.config(background=COLORS.BLACK, fg=COLORS.WHITE)
    elif isinstance(widget, tk.Entry):
        widget.config(background=COLORS.WHITE, fg=COLORS.BLACK, borderwidth=1, relief=RELIEF.RAISED, highlightcolor=COLORS.BG1, highlightbackground=COLORS.BG1, highlightthickness=2)
    elif isinstance(widget, tk.Button):
        widget.config(background=COLORS.BG4, fg=COLORS.WHITE)
    elif isinstance(widget, tk.Checkbutton):
        widget.config(background=COLORS.BLACK, fg=COLORS.ERROR)


def color_rows(listbox, selected_items=set()):
    if isinstance(listbox, tk.Listbox):
        for i in range(listbox.size()):
            if listbox.get(i) in selected_items:
                listbox.itemconfig(i, {'bg':COLORS.BG4})
            else:
                color = COLORS.BG1 if i % 2 == 0 else COLORS.BG2
                listbox.itemconfig(i, {'bg':color})


########################•########################
"""                  DATABASE                 """
########################•########################

class DB:
    # ___ File ___ #
    MANI_FILE_NAME = "blender_manifest.toml"
    MANI_FILE_PATH = ""
    MANIFEST_LINES = []
    # ___ Commands ___ #
    VALIDATE_LINES = []
    BUILD_LINES = []
    # ___ Paths ___ #
    BLENDER_EXE_PATH = None
    SOURCE_DIR = None
    BUILD_DIR = None
    # ___ Extension ___ #
    ID = None
    NAME = None
    TAGLINE = None
    TYPE = None
    TAGS = None
    # ___ Versions ___ #
    SCHEMA_VERSION = None
    VERSION = None
    BLENDER_VERSION_MIN = None
    BLENDER_VERSION_MAX = None
    # ___ Developer ___ #
    MAINTAINER = None
    EMAIL = None
    WEBSITE = None
    # ___ Legal ___ #
    LICENSE = None
    COPYRIGHT = None
    # ___ Platform ___ #
    PERMISSIONS = None
    PLATFORMS = None
    # ___ Dependencies ___ #
    WHEELS = None
    INCLUDE_PATHS = None
    PATHS_EXCLUDE_PATTER = None

    @classmethod
    def set_value(cls, key='', val=None):
        if hasattr(cls, key):
            setattr(cls, key, val)

    @classmethod
    def update_lines(cls):
        cls.MANIFEST_LINES.clear()
        cls.VALIDATE_LINES.clear()
        cls.BUILD_LINES.clear()

        # Manifest File Path
        if is_path(cls.SOURCE_DIR):
            cls.MANI_FILE_PATH = Path.joinpath(cls.SOURCE_DIR, cls.MANI_FILE_NAME)
        else:
            cls.MANI_FILE_PATH = ""

        # # Write File Content
        # write(f'schema_version = "{DB.MANI_SCHEMA_VER}"\n')
        # if DB.validate_attribute(attr='DEV_EMAIL'):
        #     write(f'maintainer = {DB.DEV_AUTHOR} <{DB.DEV_EMAIL}>\n')
        # else:
        #     write(f'maintainer = {DB.DEV_AUTHOR}\n')
        # write(f'id = "{DB.EXT_ID}"\n')
        # write(f'type = "{DB.EXT_TYPE}"\n')
        # write(f'name = "{DB.EXT_NAME}"\n')
        # write(f'version = "{DB.EXT_VERSION}"\n')
        # write(f'tagline = "{DB.EXT_TAG_LINE[:64]}"\n')
        # if DB.validate_attributes(attrs=['EXT_ADDON_TAGS', 'EXT_THEME_TAGS']):
        #     tags = DB.EXT_ADDON_TAGS if DB.EXT_TYPE == 'add-on' else DB.EXT_THEME_TAGS
        #     write("tags = [\n")
        #     for item in tags:
        #         write(f'\t"{item}",\n')
        #     write("]\n")
        # if DB.validate_attribute(attr='EXT_WEBSITE'):
        #     add(f'website = "{DB.EXT_WEBSITE}"')
        # write("license = [\n")
        # for item in DB.EXT_LICENSES:
        #     write(f'\t"{item}",\n')
        # write("]\n")
        # if DB.EXT_COPYRIGHT and DB.validate_attribute(attr='EXT_COPYRIGHT'):
        #     write("copyright = [\n")
        #     for item in DB.EXT_COPYRIGHT:
        #         write(f'\t"{item}",\n')
        #     write("]\n")
        # write(f'blender_version_min = "{DB.BLENDER_VER_MIN}"\n')
        # if DB.validate_attribute(attr='BLENDER_VER_MAX'):
        #     write(f'blender_version_max = "{DB.BLENDER_VER_MAX}"\n')
        # if any(bool(reason_msg) for reason_msg in DB.EXT_PERMISSIONS.values()):
        #     write('[permissions]\n')
        #     for permission_type, reason_msg in DB.EXT_PERMISSIONS.items():
        #         if reason_msg:
        #             write(f'{permission_type} = "{reason_msg}"\n')
        # if DB.EXT_PLATFORMS and DB.validate_attribute(attr='EXT_PLATFORMS'):
        #     write("platforms = [\n")
        #     for item in DB.EXT_PLATFORMS:
        #         write(f'\t"{item}",\n')
        #     write("]\n")
        # if DB.EXT_WHEELS and DB.validate_attribute(attr='EXT_WHEELS'):
        #     write("wheels = [\n")
        #     for item in DB.EXT_WHEELS:
        #         write(f'\t"{item}",\n')
        #     write("]\n")
        # if DB.EXT_PATH_INCLUDES and DB.validate_attribute(attr='EXT_PATH_INCLUDES'):
        #     write("[build]")
        #     write("paths = [\n")
        #     for item in DB.EXT_PATH_INCLUDES:
        #         write(f'\t"{item}",\n')
        #     write("]\n")
        # elif DB.EXT_PATH_EXCLUDES and DB.validate_attribute(attr='EXT_PATH_EXCLUDES'):
        #     write("[build]")
        #     write("paths_exclude_pattern = [\n")
        #     for item in DB.EXT_PATH_EXCLUDES:
        #         write(f'\t"{item}",\n')
        #     write("]\n")


########################•########################
"""                  WIDGETS                  """
########################•########################

class Base:
    def __init__(self, parent, key='', required=False):
        self.parent = parent
        self.key = key
        self.required = required
        self.callbacks = []


    def invoke_update(self, value=None):
        for callback in self.callbacks:
            if callable(callback):
                callback(value)
        DB.set_value(key=self.key, val=value)
        DB.update_lines()


class TabsWidget:
    def __init__(self, frame, row=0, column=0, tab_names=[]):
        self.frame = frame
        self.tabs = {}

        # Notebook
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=row, column=column, sticky=WSTICKY, padx=PADX)

        for tab_name in tab_names:
            tab_frame = tk.Frame(self.notebook)
            tab_frame.columnconfigure(0, weight=1)
            tab_frame.rowconfigure(0, weight=1)
            config_widget(tab_frame)
            self.notebook.add(tab_frame, text=tab_name)
            self.tabs[tab_name] = tab_frame


    def get_tab_frame(self, tab_name=""):
        return self.tabs.get(tab_name, None)

# BLENDER_EXE_PATH | SOURCE_DIR | BUILD_DIR
class FolderPickerWidget(Base):
    def __init__(self, parent, key='', required=False, row=0, column=0, label_text="Select Path", pick_mode='DIR'):
        super().__init__(parent, key=key, required=required)

        # Props
        self.pick_mode = pick_mode

        # Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky=WSTICKY)

        # Layout
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, minsize=75)
        self.frame.rowconfigure(0, weight=1)

        # Widgets
        self.label  = tk.Label(self.frame, text=label_text)
        self.entry  = tk.Entry(self.frame)
        self.button = tk.Button(self.frame, text="Open", command=self.__browse_command)

        # Position
        self.label.grid( row=0, column=0, sticky="we", padx=PADX)
        self.entry.grid( row=0, column=1, sticky="we", padx=PADX)
        self.button.grid(row=0, column=2, sticky="we", padx=PADX)

        # Bind
        self.entry.bind("<FocusOut>", self.__entry_callback)
        self.entry.bind("<Return>", self.__entry_callback)

        # Config
        config_widget(self.frame)
        config_widget(self.label, self.required)
        config_widget(self.entry)
        config_widget(self.button)

        # Init
        self.__entry_callback()


    def get_value(self):
        return self.entry.get()


    def __entry_callback(self, event=None):
        value = self.get_value()
        if not value:
            self.entry.config(highlightthickness=2, highlightbackground=COLORS.WHITE, highlightcolor=COLORS.WHITE, relief=RELIEF.SOLID)
            return
        valid = False
        if self.pick_mode == 'DIR': valid = is_dir(value)
        elif self.pick_mode == 'EXE': valid = is_exe(value)
        elif self.pick_mode == 'FILE': valid = is_path(value)
        if valid:
            self.entry.config(highlightthickness=2, highlightbackground=COLORS.VALID, highlightcolor=COLORS.VALID, relief=RELIEF.SOLID)
        else:
            self.entry.config(highlightthickness=2, highlightbackground=COLORS.ERROR, highlightcolor=COLORS.ERROR, relief=RELIEF.SOLID)
        # Base
        self.invoke_update(value=self.get_value())


    def __browse_command(self):
        value = None
        # Folder
        if self.pick_mode == 'DIR':
            value = filedialog.askdirectory()
            value = value if is_dir(value) else None
        # Exe
        elif self.pick_mode == 'EXE':
            filetypes = []
            if sys.platform == "win32":
                filetypes.append(("Executable files", "*.exe"))
            filetypes.append(("All files", "*.*"))
            value = filedialog.askopenfilename(title="Select Executable", filetypes=filetypes)
            value = value if is_exe(value) else None
        # File
        elif self.pick_mode == 'FILE':
            filetypes = [("All files", "*.*")]
            value = filedialog.askopenfilename(title="Select Executable", filetypes=filetypes)
            value = value if is_path(value) else None
        # Assign
        if value:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, value)
        # Validate
        self.__entry_callback()

# ID | NAME | TAGLINE | MAINTAINER | EMAIL | WEBSITE
class EntryWidget(Base):
    def __init__(self, parent, key='', required=False, row=0, column=0, label_text="Entry", char_modifiers=[]):
        super().__init__(parent, key=key, required=required)

        # Props
        self.char_modifiers = char_modifiers

        # Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky=WSTICKY)

        # Layout
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Widgets
        self.label = tk.Label(self.frame, text=label_text)
        self.entry = tk.Entry(self.frame)

        # Position
        self.label.grid(row=0, column=0, sticky="w", padx=PADX)
        self.entry.grid(row=0, column=1, sticky="we", padx=PADX)

        # Bind
        self.entry.bind("<FocusOut>", self.entry_callback)
        self.entry.bind("<Return>", self.entry_callback)
        self.entry.bind("<KeyPress>", self.entry_callback)

        # Config
        config_widget(self.frame)
        config_widget(self.label, self.required)
        config_widget(self.entry)


    def get_value(self):
        return self.entry.get()


    def entry_callback(self, event):
        value = self.get_value()
        if self.char_modifiers:
            for modifier in self.char_modifiers:
                if isinstance(modifier, (CharsReplacer, CharsLimiter)):
                    value = modifier.process(chars=value)
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, value)
        # Base
        self.invoke_update(value=self.get_value())

# TYPE
class DropdownWidget(Base):
    def __init__(self, parent, key='', required=False, row=0, column=0, label_text="Dropdown", options=[], default=""):
        super().__init__(parent, key=key, required=required)

        # Props
        self.options = options

        # Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky=WSTICKY)

        # Layout
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Widgets
        self.label    = tk.Label(self.frame, text=label_text)
        self.dropdown = ttk.Combobox(self.frame, values=self.options, state="readonly")

        # Position
        self.label.grid   (row=0, column=0, sticky="w", padx=PADX)
        self.dropdown.grid(row=0, column=1, sticky="w", padx=PADX)

        # Binds
        self.dropdown.bind("<<ComboboxSelected>>", self.dropdown_callback)

        # Config
        config_widget(self.frame)
        config_widget(self.label, self.required)

        # Init
        if default and default in self.options:
            self.dropdown.set(default)
        elif self.options:
            self.dropdown.set(self.options[0])


    def get_value(self):
        return self.dropdown.get()


    def dropdown_callback(self, event):
        # Base
        self.invoke_update(value=self.get_value())

# SCHEMA_VERSION | VERSION | BLENDER_VERSION_MIN | BLENDER_VERSION_MAX
class VersionWidget(Base):
    def __init__(self, parent, key='', required=False, row=0, column=0, label_text="Version", min_ver=(0, 0, 0), allow_ignore=False):
        super().__init__(parent, key=key, required=required)

        # Props
        self.ignore_var = tk.BooleanVar()
        self.var_major = tk.IntVar(value=min_ver[0])
        self.var_minor = tk.IntVar(value=min_ver[1])
        self.var_patch = tk.IntVar(value=min_ver[2])

        # Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky=WSTICKY)

        # Layout
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=2)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=2)
        self.frame.columnconfigure(5, weight=1)
        self.frame.columnconfigure(6, weight=1)
        if allow_ignore:
            self.frame.columnconfigure(7, weight=1)

        # Register Validator
        validate_cmd = self.frame.register(is_str_int)

        # Widgets
        self.label       = tk.Label(self.frame, text=label_text)
        self.label_major = tk.Label(self.frame, text="Major")
        self.label_minor = tk.Label(self.frame, text="Minor")
        self.label_patch = tk.Label(self.frame, text="Patch")
        self.spin_major  = tk.Spinbox(self.frame, from_=min_ver[0], to=sys.maxsize, textvariable=self.var_major, command=self.spinbox_callback, validate="key", validatecommand=(validate_cmd, "%P"), justify="center")
        self.spin_minor  = tk.Spinbox(self.frame, from_=min_ver[1], to=sys.maxsize, textvariable=self.var_minor, command=self.spinbox_callback, validate="key", validatecommand=(validate_cmd, "%P"), justify="center")
        self.spin_patch  = tk.Spinbox(self.frame, from_=min_ver[2], to=sys.maxsize, textvariable=self.var_patch, command=self.spinbox_callback, validate="key", validatecommand=(validate_cmd, "%P"), justify="center")
        self.ignore_checkbox = None
        if allow_ignore:
            self.ignore_checkbox = tk.Checkbutton(self.frame, text="Ignore", command=self.ignore_checkbox_callback, variable=self.ignore_var)

        # Position
        self.label.grid      (row=0, column=0, sticky="w", padx=PADX)
        self.label_major.grid(row=0, column=1, sticky="w", padx=PADX)
        self.spin_major.grid (row=0, column=2, sticky="w", padx=PADX)
        self.label_minor.grid(row=0, column=3, sticky="w", padx=PADX)
        self.spin_minor.grid (row=0, column=4, sticky="w", padx=PADX)
        self.label_patch.grid(row=0, column=5, sticky="w", padx=PADX)
        self.spin_patch.grid (row=0, column=6, sticky="w", padx=PADX)
        if allow_ignore:
            self.ignore_checkbox.grid(row=0, column=7, sticky="ew", padx=PADX)

        # Config
        config_widget(self.frame)
        config_widget(self.label, self.required)
        config_widget(self.label_major)
        config_widget(self.label_minor)
        config_widget(self.label_patch)
        if allow_ignore:
            config_widget(self.ignore_checkbox)

        # Init
        if allow_ignore:
            self.ignore_var.set(True)
            self.disable()


    def get_value(self):
        if isinstance(self.ignore_checkbox, tk.Checkbutton):
            if self.ignore_var.get():
                return None
        return self.var_major.get(), self.var_minor.get(), self.var_patch.get()


    def spinbox_callback(self):
        # Base
        self.invoke_update(value=self.get_value())


    def ignore_checkbox_callback(self):
        if isinstance(self.ignore_checkbox, tk.Checkbutton):
            if self.ignore_var.get():
                self.disable()
            else:
                self.enable()
            self.spinbox_callback()


    def disable(self):
        self.spin_major.config(state="disabled", disabledbackground=COLORS.ERROR, disabledforeground=COLORS.BG5)
        self.spin_minor.config(state="disabled", disabledbackground=COLORS.ERROR, disabledforeground=COLORS.BG5)
        self.spin_patch.config(state="disabled", disabledbackground=COLORS.ERROR, disabledforeground=COLORS.BG5)
        self.spinbox_callback()


    def enable(self):
        self.spin_major.config(state="normal", background=COLORS.WHITE)
        self.spin_minor.config(state="normal", background=COLORS.WHITE)
        self.spin_patch.config(state="normal", background=COLORS.WHITE)
        self.spinbox_callback()

# TAGS | LICENSE | COPYRIGHT | PERMISSIONS | PLATFORMS | EXCLUDE_PATTERNS
class ListPickWidget(Base):
    def __init__(self, parent, key='', required=False, row=0, column=0, label_text="Item Picker", items=[]):
        super().__init__(parent, key=key, required=required)

        # Props
        self.items = items
        self.selected_indices = set()

        # Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky=WSTICKY)

        # Layout
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH) # LABEL
        self.frame.columnconfigure(1, weight=1)            # SEARCH LABEL
        self.frame.columnconfigure(2, weight=1)            # SEARCH ENTRY
        self.frame.columnconfigure(3, weight=1)            # SEARCH CLEAR
        self.frame.columnconfigure(4, weight=1)            # LIST RESET SELECT

        # Widgets
        self.label          = tk.Label(self.frame, text=label_text)
        self.search_label   = tk.Label(self.frame, text="Search")
        self.search_entry   = tk.Entry(self.frame)
        self.clr_search_btn = tk.Button(self.frame, text="Clear Search", command=self.__clear_search_command)
        self.clr_sel_btn    = tk.Button(self.frame, text="Deselect All", command=self.__clear_selection_command)
        self.listbox        = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, exportselection=0, selectbackground=COLORS.BG4, selectforeground=COLORS.WHITE, height=6)
        self.scrollbar      = tk.Scrollbar(self.frame, orient=tk.VERTICAL)

        # Position
        self.label.grid         (row=0, column=0, sticky="w", padx=PADX)
        self.search_label.grid  (row=0, column=1, sticky="e", padx=PADX)
        self.search_entry.grid  (row=0, column=2, sticky="we", padx=PADX)
        self.clr_search_btn.grid(row=0, column=3, sticky="w")
        self.clr_sel_btn.grid   (row=0, column=4, sticky="e")
        self.listbox.grid       (row=1, column=1, columnspan=4, sticky="snew")
        self.scrollbar.grid     (row=1, column=4, sticky="ens")

        # Binds
        self.search_entry.bind("<KeyRelease>", self.__search_key_callback)
        self.listbox.bind("<<ListboxSelect>>", self.__listbox_select_callback)

        # Link scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Config
        config_widget(self.frame)
        config_widget(self.label, self.required)
        config_widget(self.search_label)
        config_widget(self.search_entry)
        config_widget(self.clr_search_btn)
        config_widget(self.clr_sel_btn)

        # Init
        self.__rebuild_list()


    def get_value(self):
        return [item for i, item in enumerate(self.items) if i in self.selected_indices]


    def external_update_list(self, items=[]):
        self.items = items
        self.selected_indices = set()
        self.__rebuild_list()


    def __rebuild_list(self):
        # Rebuild
        self.listbox.delete(0, tk.END)
        for i, item in enumerate(self.items):
            self.listbox.insert(tk.END, item)
            if i in self.selected_indices:
                self.listbox.selection_set(i)
        color_rows(self.listbox)


    def __clear_search_command(self):
        self.search_entry.delete(0, tk.END)
        self.__rebuild_list()


    def __clear_selection_command(self):
        self.selected_indices.clear()
        self.listbox.selection_clear(0, tk.END)
        color_rows(self.listbox)
        # Base
        self.invoke_update(value=self.get_value())


    def __search_key_callback(self, event=None):
        # Search Chars
        search_term = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)

        # Search Box Cleared
        if not search_term:
            self.__rebuild_list()
        # Refine Items
        else:
            current_index = 0
            for i, item in enumerate(self.items):
                splits = search_term.split()
                if all(split.lower() in item.lower() for split in splits):
                    self.listbox.insert(tk.END, item)
                    if i in self.selected_indices:
                        self.listbox.selection_set(current_index)
                    current_index += 1

        selected_items = [item for i, item in enumerate(self.items) if i in self.selected_indices]
        color_rows(self.listbox, selected_items)


    def __listbox_select_callback(self, event=None):
        # Current
        selected_items = {self.listbox.get(i) for i in self.listbox.curselection()}
        listed_items = set(self.listbox.get(0, tk.END))

        # Selected Indices
        for i, item in enumerate(self.items):
            if item in selected_items:
                self.selected_indices.add(i)
            elif i in self.selected_indices:
                self.selected_indices.remove(i)
        
        selected_items = [item for i, item in enumerate(self.items) if i in self.selected_indices]
        color_rows(self.listbox, selected_items)
        # Base
        self.invoke_update(value=self.get_value())

# WHEELS | INCLUDE_PATHS
class EntryListWidget(Base):
    def __init__(self, parent, key='', required=False, row=0, column=0, label_text="Text Box"):
        super().__init__(parent, key=key, required=required)

        # Props
        self.entry_var = tk.StringVar()

        # Create Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky=WSTICKY)

        # Layout
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=2)
        self.frame.rowconfigure(1, weight=1)

        # Widgets
        self.label     = tk.Label(self.frame, text=label_text, padx=PADX)
        self.entry     = tk.Entry(self.frame, textvariable=self.entry_var)
        self.add_btn   = tk.Button(self.frame, text="Add", command=self.add_entry)
        self.del_btn   = tk.Button(self.frame, text="Delete", command=self.delete_entry)
        self.listbox   = tk.Listbox(self.frame, height=6)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)

        # Position
        self.label.grid(row=0, column=0, sticky="w")
        self.entry.grid(row=0, column=1, sticky="we")
        self.add_btn.grid(row=0, column=2, sticky="w")
        self.del_btn.grid(row=0, column=3, sticky="w")
        self.listbox.grid(row=1, column=1, columnspan=3, sticky="nsew")
        self.scrollbar.grid(row=1, column=3, sticky="ens")

        # Link scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Binds
        self.listbox.bind("<Double-Button-1>", self.edit_entry)

        # Config
        config_widget(self.frame)
        config_widget(self.label, self.required)
        config_widget(self.entry)
        config_widget(self.add_btn)
        config_widget(self.del_btn)
        config_widget(self.listbox)


    def get_value(self):
        result = self.listbox.get(0, tk.END)
        if not result:
            return []
        return result


    def add_entry(self):
        entry_text = self.entry_var.get().strip()
        if entry_text and entry_text not in self.listbox.get(0, tk.END):
            self.listbox.insert(tk.END, entry_text)
            self.entry_var.set("")
            color_rows(self.listbox)
        else:
            messagebox.showwarning("Warning", "Invalid or duplicate entry.")


    def delete_entry(self):
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            self.listbox.delete(index)


    def edit_entry(self, event):
        selected_index = self.listbox.curselection()
        if not selected_index: return

        index = selected_index[0]
        current_text = self.listbox.get(index)
        current_text = current_text if current_text else ""
        
        result = EntryPopup.invoke(parent=self.frame, width=350, height=100, label_text="Entry", prompt_text="Edit", entry_text=current_text)
        if not result: return

        self.listbox.delete(index)
        self.listbox.insert(index, result)

        # Base
        self.invoke_update(value=self.get_value())

# MANIFEST | VALIDATE | BUILD
class TextBoxWidget(Base):
    def __init__(self, parent, key='', required=False, row=0, column=0, label_text="Text Box"):
        super().__init__(parent, key=key, required=required)

        # Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky=WSTICKY)

        # Sub Frame
        self.text_frame = tk.Frame(self.frame)
        self.text_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")

        # layout
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=4)
        self.frame.columnconfigure(3, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Widgets
        self.label        = tk.Label(self.frame, text=label_text)
        self.line_numbers = tk.Text(self.text_frame, width=3, bg=COLORS.BG4, fg=COLORS.WHITE, state=tk.DISABLED, relief=RELIEF.GROOVE, padx=PADX)
        self.text_box     = tk.Text(self.text_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.scrollbar    = tk.Scrollbar(self.frame, orient="vertical", command=self.__sync_scroll_command)

        # Position Main
        self.label.grid(row=0, column=0, sticky="wn", padx=PADX)
        self.scrollbar.grid(row=0, column=3, sticky="ns", padx=PADX)

        # Position Sub
        self.line_numbers.pack(side="left", fill="y")
        self.text_box.pack(side="left", fill="both", expand=True)

        # Link Scrollbar
        self.text_box.config(yscrollcommand=self.scrollbar.set)
        self.line_numbers.config(yscrollcommand=self.scrollbar.set)

        # Bind
        self.text_box.bind("<MouseWheel>", self.__on_mouse_wheel_callback)
        self.line_numbers.bind("<MouseWheel>", self.__on_mouse_wheel_callback)
        self.text_box.bind("<<Modified>>", self.__on_text_changed_callback)

        # Config
        config_widget(self.frame)
        config_widget(self.text_frame)
        config_widget(self.label, self.required)


    def get_value(self):
        text = self.text_box.get(1.0, tk.END).strip()
        return text.split("\n")


    def set_value(self, lines=[]):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        for line in lines:
            self.text_box.insert(tk.END, line + "\n")
        self.text_box.config(state=tk.DISABLED)
        self.__update_line_numbers()


    def __sync_scroll_command(self, *args):
        self.text_box.yview(*args)
        self.line_numbers.yview(*args)


    def __on_mouse_wheel_callback(self, event):
        if event.num == 5 or event.delta < 0:
            self.text_box.yview_scroll(1, "units")
            self.line_numbers.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.text_box.yview_scroll(-1, "units")
            self.line_numbers.yview_scroll(-1, "units")
        return "break"


    def __update_line_numbers(self):
        num_lines = int(self.text_box.index('end-1c').split('.')[0])
        line_numbers = '\n'.join(str(i) for i in range(1, num_lines + 1))
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        self.line_numbers.insert(tk.END, line_numbers)
        self.line_numbers.config(state=tk.DISABLED)
        # Base
        self.invoke_update(value=self.get_value())


    def __on_text_changed_callback(self, event):
        self.__update_line_numbers()
        self.text_box.edit_modified(False)

########################•########################
"""                 COMMANDERS                """
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

########################•########################
"""                APPLICATION                """
########################•########################

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        root = self
        # Window
        root.title(APP_NAME)
        root.resizable(APP_RESIZABLE, APP_RESIZABLE)
        # Styles
        setup_styles()
        # Configure Layout
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        # Create frames
        frame_1 = tk.Frame(root, padx=PADX, pady=PADY, background=COLORS.BLACK)
        frame_2 = tk.Frame(root, padx=PADX, pady=PADY, background=COLORS.BLACK)
        # Add Frames
        frame_1.grid(row=0, column=0, sticky="nsew")
        frame_2.grid(row=1, column=0, sticky="nsew")
        # Configure
        frame_1.columnconfigure(0, weight=1)
        frame_1.rowconfigure(0, weight=1)
        frame_2.columnconfigure(0, weight=1)
        frame_2.rowconfigure(0, weight=1)
        # Build
        self.build_frame_1(frame_1)
        self.build_frame_2(frame_2)
        self.build_callbacks()


    def build_frame_1(self, frame):
        # Tabs
        self.info_tabs = TabsWidget(frame, row=0, column=0, tab_names=["Paths", "Extension", "Versions", "Developer", "Legal", "Platform", "Dependencies"])

        # Paths
        tab = self.info_tabs.get_tab_frame(tab_name="Paths")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        tab.rowconfigure(2, weight=1)
        self.blender_picker = FolderPickerWidget(tab, key='BLENDER_EXE_PATH', required=True, row=0, column=0, label_text="Blender Exe Path", pick_mode='EXE')
        self.source_picker  = FolderPickerWidget(tab, key='SOURCE_DIR'      , required=True, row=1, column=0, label_text="Source Directory", pick_mode='DIR')
        self.build_picker   = FolderPickerWidget(tab, key='BUILD_DIR'       , required=True, row=2, column=0, label_text="Build Directory" , pick_mode='DIR')

        # Extension
        tab = self.info_tabs.get_tab_frame(tab_name="Extension")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        tab.rowconfigure(2, weight=1)
        tab.rowconfigure(3, weight=1)
        tab.rowconfigure(4, weight=1)
        self.id_entry      = EntryWidget    (tab, key='ID'     , required=True , row=0, column=0, label_text="ID", char_modifiers=[CharsReplacer(filter_map={" ":"_"})])
        self.name_entry    = EntryWidget    (tab, key='NAME'   , required=True , row=1, column=0, label_text="Name")
        self.tagline_entry = EntryWidget    (tab, key='TAGLINE', required=True , row=2, column=0, label_text="Tagline", char_modifiers=[CharsLimiter(limit=64)])
        self.type_dropdown = DropdownWidget (tab, key='TYPE'   , required=True , row=3, column=0, label_text="Type", options=EXTENSION_TYPES, default="add-on")
        self.tags_pick     = ListPickWidget (tab, key='TAGS'   , required=False, row=4, column=0, label_text="Tags", items=ADDON_TAGS)

        # Versions
        tab = self.info_tabs.get_tab_frame(tab_name="Versions")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        tab.rowconfigure(2, weight=1)
        tab.rowconfigure(3, weight=1)
        self.schema_version = VersionWidget(tab, key='SCHEMA_VERSION'     , required=True , row=0, column=0, label_text="Schema Version", min_ver=(1,0,0))
        self.ext_version    = VersionWidget(tab, key='VERSION'            , required=True , row=1, column=0, label_text="Extension Version", min_ver=(0,0,0))
        self.blender_min    = VersionWidget(tab, key='BLENDER_VERSION_MIN', required=True , row=2, column=0, label_text="Blender Ver Min", min_ver=(4,2,0))
        self.blender_max    = VersionWidget(tab, key='BLENDER_VERSION_MAX', required=False, row=3, column=0, label_text="Blender Ver Max", min_ver=(4,2,0), allow_ignore=True)
        # Config
        self.schema_version.disable()

        # Developer
        tab = self.info_tabs.get_tab_frame(tab_name="Developer")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        tab.rowconfigure(2, weight=1)
        self.dev_name_entry  = EntryWidget(tab, key='MAINTAINER', required=True , row=0, column=0, label_text="Maintainer Name")
        self.dev_email_entry = EntryWidget(tab, key='EMAIL'     , required=False, row=1, column=0, label_text="Maintainer Email"  )
        self.dev_web_entry   = EntryWidget(tab, key='WEBSITE'   , required=False, row=2, column=0, label_text="Maintainer Website")

        # Legal
        tab = self.info_tabs.get_tab_frame(tab_name="Legal")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        self.license_pick    = ListPickWidget(tab, key='LICENSE'  , required=True , row=0, column=0, label_text="License(s)", items=LICENSES.keys())
        self.copyright_entry = ListPickWidget(tab, key='COPYRIGHT', required=False, row=1, column=0, label_text="Copyright", items=LICENSES.keys())

        # Platform
        tab = self.info_tabs.get_tab_frame(tab_name="Platform")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        self.permission     = ListPickWidget (tab, key='PERMISSIONS', required=False, row=0, column=0, label_text="Permissions", items=PLATFORMS)
        self.platforms_pick = ListPickWidget (tab, key='PLATFORMS'  , required=False, row=1, column=0, label_text="Platform Specs", items=PLATFORMS)

        # Dependencies
        tab = self.info_tabs.get_tab_frame(tab_name="Dependencies")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        tab.rowconfigure(2, weight=1)
        self.wheels           = EntryListWidget(tab, key='WHEELS'          , required=False, row=0, column=0, label_text="Wheels")
        self.include_paths    = EntryListWidget(tab, key='INCLUDE_PATHS'   , required=False, row=1, column=0, label_text="Include Paths")
        self.exclude_patterns = ListPickWidget (tab, key='EXCLUDE_PATTERNS', required=False, row=2, column=0, label_text="Exclude Patterns", items=PATH_EXCLUDE_PATTERNS)


    def build_frame_2(self, frame):
        # Tabs
        self.builder_tabs = TabsWidget(frame, row=0, column=0, tab_names=["Manifest", "Validate", "Build"])

        # Manifest
        tab = self.builder_tabs.get_tab_frame(tab_name="Manifest")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        self.manifest_textbox = TextBoxWidget(tab, row=0, column=0, label_text="Preview")
        self.manifest_textbox.set_value([f"This is a line {i}" for i in range(100)])

        # Validate Command
        tab = self.builder_tabs.get_tab_frame(tab_name="Validate")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        self.manifest_textbox = TextBoxWidget(tab, row=0, column=0, label_text="Command")
        self.manifest_textbox.set_value([f"This is a line {i}" for i in range(100)])

        # Build Command
        tab = self.builder_tabs.get_tab_frame(tab_name="Build")
        tab.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab.rowconfigure(0, weight=1)
        self.manifest_textbox = TextBoxWidget(tab, row=0, column=0, label_text="Command")
        self.manifest_textbox.set_value([f"This is a line {i}" for i in range(100)])


    def build_callbacks(self):

        def switch_tags(value):
            if isinstance(value, str):
                if value == "add-on":
                    self.tags_pick.external_update_list(items=ADDON_TAGS)
                elif value == "theme":
                    self.tags_pick.external_update_list(items=THEME_TAGS)
        self.type_dropdown.callbacks.append(switch_tags)


if __name__ == "__main__":
    set_licenses()
    app = App()
    app.mainloop()
