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
LABEL_WIDTH = 175
PADX = 4
PADY = 4

########################•########################
"""                  GUI HELPERS              """
########################•########################

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


class Observers:
    def __init__(self):
        self.listeners = []


    def add_callback(self, callback=None):
        if callback is None: return
        if not callable(callback): return
        if callback in self.listeners: return
        self.listeners.append(callback)


    def remove_callback(self, callback=None):
        if callback in self.listeners:
            self.listeners.remove(callback)


    def update(self, value=None):
        if self.listeners:
            for listener in self.listeners:
                if callable(listener):
                    listener(value)


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


class RELIEF:
    FLAT = "flat"
    RAISED = "raised"
    SUNKEN = "sunken"
    RIDGE = "ridge"
    SOLID = "solid"
    GROOVE = "groove"


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
                "background": COLORS.BG4,  # Default background color for the tabs
                "foreground": COLORS.WHITE  # Default text color for tabs
            },
            "map": {
                "background": [
                    ("selected", COLORS.VALID)  # Selected tab background color
                ],
                "foreground": [
                    ("selected", COLORS.BG4)  # Selected tab text color
                ],
                "expand": [
                    ("selected", [1, 1, 1, 0])
                ]
            }
        }
    }

    style.theme_create("KodoTabs", parent="alt", settings=style_settings)
    style.theme_use("KodoTabs")

    # Apply styles to widgets
    for widget, settings in style_settings.items():
        for setting, value in settings.items():
            getattr(style, setting)(widget, **value)


def config_widget(widget):
    if isinstance(widget, tk.Frame):
        widget.config(padx=PADX, pady=PADY, background=COLORS.BLACK, borderwidth=1, relief=RELIEF.RAISED, highlightcolor=COLORS.BG4, highlightbackground=COLORS.BG4, highlightthickness=1)
    elif isinstance(widget, tk.Label):
        widget.config(background=COLORS.BLACK, fg=COLORS.WHITE)
    elif isinstance(widget, tk.Entry):
        widget.config(background=COLORS.WHITE, fg=COLORS.BLACK, borderwidth=1, relief=RELIEF.RAISED, highlightcolor=COLORS.BG1, highlightbackground=COLORS.BG1, highlightthickness=2)
    elif isinstance(widget, tk.Button):
        widget.config(background=COLORS.BG4, fg=COLORS.WHITE)
    elif isinstance(widget, tk.Checkbutton):
        widget.config(background=COLORS.BLACK, fg=COLORS.ERROR)

########################•########################
"""                  WIDGETS                  """
########################•########################

class FolderPickerWidget:
    def __init__(self, parent, row=0, column=0, label_text="Select Path", pick_mode='DIR'):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky="we")
        config_widget(self.frame)

        # Configure Layout
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, minsize=75)
        self.frame.rowconfigure(0, weight=1)

        # Props
        self.observers = Observers()
        self.pick_mode = pick_mode

        # Create Widgets
        self.label  = tk.Label(self.frame, text=label_text)
        self.entry  = tk.Entry(self.frame)
        self.button = tk.Button(self.frame, text="Open", command=self.browse)
        config_widget(self.label)
        config_widget(self.entry)
        config_widget(self.button)

        # Add Widgets
        self.label.grid( row=0, column=0, sticky="we", padx=PADX)
        self.entry.grid( row=0, column=1, sticky="we", padx=PADX)
        self.button.grid(row=0, column=2, sticky="we", padx=PADX)

        # Bind
        self.entry.bind("<FocusOut>", self.callback_validator)
        self.entry.bind("<Return>", self.callback_validator)

        # Init Styles
        self.callback_validator()


    def get_value(self):
        return self.entry.get()


    def callback_validator(self, event=None):
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
        self.observers.update(value)


    def browse(self):
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
        self.callback_validator()


class TabsWidget:
    def __init__(self, frame, row=0, column=0, tab_names=[]):
        self.frame = frame
        self.tabs = {}

        # Notebook
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=row, column=column, sticky="nsew", padx=PADX)

        for tab_name in tab_names:
            tab_frame = tk.Frame(self.notebook)
            tab_frame.columnconfigure(0, weight=1)
            tab_frame.rowconfigure(0, weight=1)
            config_widget(tab_frame)
            self.notebook.add(tab_frame, text=tab_name)
            self.tabs[tab_name] = tab_frame


    def get_tab_frame(self, tab_name=""):
        return self.tabs.get(tab_name, None)


class EntryWidget:
    def __init__(self, parent, row=0, column=0, label_text="Entry", char_modifiers=[]):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky="we")
        config_widget(self.frame)

        # Configure Layout
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Props
        self.observers = Observers()
        self.char_modifiers = char_modifiers

        # Create Widgets
        self.label = tk.Label(self.frame, text=label_text)
        self.entry = tk.Entry(self.frame)
        config_widget(self.label)
        config_widget(self.entry)

        # Add Widgets
        self.label.grid(row=0, column=0, sticky="w", padx=PADX)
        self.entry.grid(row=0, column=1, sticky="we", padx=PADX)

        # Bind
        self.entry.bind("<FocusOut>", self.entry_callback)
        self.entry.bind("<Return>", self.entry_callback)
        self.entry.bind("<KeyPress>", self.entry_callback)


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
        self.observers.update(value)


class DropdownWidget:
    def __init__(self, parent, row=0, column=0, label_text="Dropdown", options=[], default=""):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky="we")
        config_widget(self.frame)

        # Configure Layout
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Props
        self.observers = Observers()
        self.options = options

        # Create Widgets
        self.label = tk.Label(self.frame, text=label_text)
        self.dropdown = ttk.Combobox(self.frame, values=self.options, state="readonly")
        config_widget(self.label)

        # Add Widgets
        self.label.grid(row=0, column=0, sticky="w", padx=PADX)
        self.dropdown.grid(row=0, column=1, sticky="w", padx=PADX)

        # Values
        if default and default in self.options:
            self.dropdown.set(default)
        elif self.options:
            self.dropdown.set(self.options[0])

        # Binds
        self.dropdown.bind("<<ComboboxSelected>>", self.dropdown_callback)


    def get_value(self):
        return self.dropdown.get()


    def dropdown_callback(self, event):
        value = self.get_value()
        self.observers.update(value)


class VersionWidget:
    def __init__(self, parent, row=0, column=0, label_text="Version", min_ver=(0, 0, 0), allow_ignore=False):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky="we")
        config_widget(self.frame)

        # Configure Layout
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        if allow_ignore:
            self.frame.columnconfigure(1, weight=1)
            self.frame.columnconfigure(2, weight=1)
            self.frame.columnconfigure(3, weight=2)
            self.frame.columnconfigure(4, weight=1)
            self.frame.columnconfigure(5, weight=2)
            self.frame.columnconfigure(6, weight=1)
        else:
            self.frame.columnconfigure(1, weight=1)
            self.frame.columnconfigure(2, weight=2)
            self.frame.columnconfigure(3, weight=1)
            self.frame.columnconfigure(4, weight=2)
            self.frame.columnconfigure(5, weight=1)

        # Props
        self.observers = Observers()
        self.ignore_var = tk.BooleanVar()
        self.var_major = tk.IntVar(value=min_ver[0])
        self.var_minor = tk.IntVar(value=min_ver[1])
        self.var_patch = tk.IntVar(value=min_ver[2])

        # Create Label
        self.label = tk.Label(self.frame, text=label_text)
        self.label.grid(row=0, column=0, sticky="w", padx=PADX)
        config_widget(self.label)

        # Create Version Labels
        self.label_major = tk.Label(self.frame, text="Major")
        self.label_minor = tk.Label(self.frame, text="Minor")
        self.label_patch = tk.Label(self.frame, text="Patch")
        config_widget(self.label_major)
        config_widget(self.label_minor)
        config_widget(self.label_patch)

        # Register Validator
        validate_cmd = self.frame.register(is_str_int)

        # Create Spin Boxes
        self.spin_major = tk.Spinbox(self.frame, from_=min_ver[0], to=sys.maxsize, textvariable=self.var_major, command=self.spinbox_callback, validate="key", validatecommand=(validate_cmd, "%P"))
        self.spin_minor = tk.Spinbox(self.frame, from_=min_ver[1], to=sys.maxsize, textvariable=self.var_minor, command=self.spinbox_callback, validate="key", validatecommand=(validate_cmd, "%P"))
        self.spin_patch = tk.Spinbox(self.frame, from_=min_ver[2], to=sys.maxsize, textvariable=self.var_patch, command=self.spinbox_callback, validate="key", validatecommand=(validate_cmd, "%P"))

        column = 1

        # Ignore Checkbox
        self.ignore_checkbox = None
        if allow_ignore:
            self.ignore_checkbox = tk.Checkbutton(self.frame, text="Ignore", command=self.ignore_checkbox_callback, variable=self.ignore_var)
            self.ignore_checkbox.grid(row=0, column=1, sticky="w", padx=PADX)
            config_widget(self.ignore_checkbox)
            self.disable()
            self.ignore_var.set(True)
            column += 1

        # Add Major
        self.label_major.grid(row=0, column=column + 0, sticky="w", padx=PADX)
        self.spin_major.grid( row=0, column=column + 1, sticky="w", padx=PADX)

        # Add Minor
        self.label_minor.grid(row=0, column=column + 2, sticky="w", padx=PADX)
        self.spin_minor.grid( row=0, column=column + 3, sticky="w", padx=PADX)

        # Add Patch
        self.label_patch.grid(row=0, column=column + 4, sticky="w", padx=PADX)
        self.spin_patch.grid( row=0, column=column + 5, sticky="w", padx=PADX)


    def get_value(self):
        if isinstance(self.ignore_checkbox, tk.Checkbutton):
            if self.ignore_var.get():
                return None
        return self.var_major.get(), self.var_minor.get(), self.var_patch.get()


    def spinbox_callback(self):
        value = self.get_value()
        self.observers.update(value)


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


    def enable(self):
        self.spin_major.config(state="normal", background=COLORS.WHITE)
        self.spin_minor.config(state="normal", background=COLORS.WHITE)
        self.spin_patch.config(state="normal", background=COLORS.WHITE)


class ListPickWidget:
    def __init__(self, parent, row=0, column=0, label_text="Item Picker", items=[]):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky="we")
        config_widget(self.frame)

        # Configure Layout
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH) # LABEL
        self.frame.columnconfigure(1, weight=1)            # SEARCH LABEL
        self.frame.columnconfigure(2, weight=1)            # SEARCH ENTRY
        self.frame.columnconfigure(3, weight=1)            # SEARCH CLEAR
        self.frame.columnconfigure(4, weight=1)            # LIST RESET SELECT

        # Props
        self.observers = Observers()
        self.items = items

        # Label
        self.label = tk.Label(self.frame, text=label_text)
        self.label.grid(row=0, column=0, sticky="w", padx=PADX)
        config_widget(self.label)

        # Label
        self.search_label = tk.Label(self.frame, text="Search")
        self.search_label.grid(row=0, column=1, sticky="e", padx=PADX)
        config_widget(self.search_label)

        # Entry
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=0, column=2, sticky="we", padx=PADX)
        self.search_entry.bind("<KeyPress>", self.filter_list_callback)
        config_widget(self.search_entry)

        # Reset Button
        self.clear_search_btn = tk.Button(self.frame, text="Clear Search", command=self.clear_search)
        self.clear_search_btn.grid(row=0, column=3, sticky="w")
        config_widget(self.clear_search_btn)

        # Clear Button
        self.clear_selection_btn = tk.Button(self.frame, text="Clear Selection", command=self.deselect_all)
        self.clear_selection_btn.grid(row=0, column=4, sticky="e")
        config_widget(self.clear_selection_btn)

        # List Box
        self.listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, width=50, height=8)
        self.listbox.grid(row=1, column=1, columnspan=4, sticky="snew")
        self.listbox.bind("<<ListboxSelect>>", self.listbox_callback)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=4, sticky="ens")

        # Link scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Populate Listbox
        self.update_listbox(items)


    def get_value(self):
        selected_indices = self.listbox.curselection()
        return [self.listbox.get(i) for i in selected_indices]


    def listbox_callback(self, event=None):
        value = self.get_value()
        self.observers.update(value)


    def color_rows(self):
        for i in range(self.listbox.size()):
            color = COLORS.BG1 if i % 2 == 0 else COLORS.BG2
            self.listbox.itemconfig(i, {'bg':color})


    def update_listbox(self, items):
        self.items = items
        self.listbox.delete(0, tk.END)
        for item in items:
            if isinstance(item, str):
                self.listbox.insert(tk.END, item)
        self.color_rows()
        self.listbox_callback()


    def deselect_all(self):
        self.listbox.selection_clear(0, tk.END)


    def filter_list_callback(self, event=None):
        search_term = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)

        # Search Box Cleared
        if not search_term:
            for item in self.items:
                self.listbox.insert(tk.END, item)
            self.color_rows()
            return

        # Refine Items
        for item in self.items:
            splits = search_term.split()
            if all(split.lower() in item.lower() for split in splits):
                self.listbox.insert(tk.END, item)
        self.color_rows()


    def clear_search(self, event=None):
        selected_indices = self.listbox.curselection()
        self.search_entry.delete(0, tk.END)
        self.update_listbox(items=self.items)
        for index in selected_indices:
            self.listbox.select_set(index)


class TextBoxWidget:
    def __init__(self, parent, row=0, column=0, label_text="Text Box"):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=row, column=column, sticky="we")
        config_widget(self.frame)

        # Configure layout
        self.frame.columnconfigure(0, minsize=LABEL_WIDTH)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=4)
        self.frame.columnconfigure(3, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Label
        self.label = tk.Label(self.frame, text=label_text)
        self.label.grid(row=0, column=0, sticky="wn", padx=PADX)
        config_widget(self.label)

        # Sub-frame for text & numbers
        self.text_frame = tk.Frame(self.frame)
        self.text_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")

        # Line numbers
        self.line_numbers = tk.Text(self.text_frame, width=4, height=10, bg=COLORS.BG4, fg=COLORS.WHITE, state=tk.DISABLED, relief=RELIEF.GROOVE, padx=PADX)
        self.line_numbers.pack(side="left", fill="y")

        # Text Box
        self.text_box = tk.Text(self.text_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.text_box.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self._sync_scroll)
        self.scrollbar.grid(row=0, column=3, sticky="ns", padx=PADX)

        # Link scrollbar properly
        self.text_box.config(yscrollcommand=self.scrollbar.set)
        self.line_numbers.config(yscrollcommand=self.scrollbar.set)

        # Scroll event binding
        self.text_box.bind("<MouseWheel>", self._on_mouse_wheel)
        self.line_numbers.bind("<MouseWheel>", self._on_mouse_wheel)
        self.text_box.bind("<<Modified>>", self._on_text_changed)


    def _sync_scroll(self, *args):
        """ Syncs the scrollbar with both text boxes """
        self.text_box.yview(*args)
        self.line_numbers.yview(*args)


    def _on_mouse_wheel(self, event):
        """ Sync mouse scrolling for both text areas """
        if event.num == 5 or event.delta < 0:
            self.text_box.yview_scroll(1, "units")
            self.line_numbers.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.text_box.yview_scroll(-1, "units")
            self.line_numbers.yview_scroll(-1, "units")
        return "break"


    def get_value(self):
        text = self.text_box.get(1.0, tk.END).strip()
        return text.split("\n")


    def set_value(self, lines=[]):
        """ Set text box content and update line numbers """
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        for line in lines:
            self.text_box.insert(tk.END, line + "\n")
        self.text_box.config(state=tk.DISABLED)
        self.update_line_numbers()


    def update_line_numbers(self):
        """ Updates the left-side line numbers """
        num_lines = int(self.text_box.index('end-1c').split('.')[0])
        line_numbers = '\n'.join(str(i) for i in range(1, num_lines + 1))
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        self.line_numbers.insert(tk.END, line_numbers)
        self.line_numbers.config(state=tk.DISABLED)


    def _on_text_changed(self, event):
        """ Updates line numbers when text changes """
        self.update_line_numbers()
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
        root.title(APP_NAME)
        root.resizable(APP_RESIZABLE, APP_RESIZABLE)

    @try_except_decorator
    def setup(self):
        root = self
        # Styles
        setup_styles()
        # Configure Layout
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        # Create frames
        frame_1 = tk.Frame(root, padx=PADX, pady=PADY, background=COLORS.BLACK)
        frame_2 = tk.Frame(root, padx=PADX, pady=PADY, background=COLORS.BLACK)
        frame_3 = tk.Frame(root, padx=PADX, pady=PADY, background=COLORS.BLACK)
        # Add Frames
        frame_1.grid(row=0, column=0, sticky="nsew")
        frame_2.grid(row=1, column=0, sticky="nsew")
        frame_3.grid(row=2, column=0, sticky="nsew")
        # Build
        self.build_frame_1(frame=frame_1)
        self.build_frame_2(frame=frame_2)
        self.build_frame_3(frame=frame_3)


    def build_frame_1(self, frame):
        # Configure Layout
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)

        # Widgets
        self.blender_picker = FolderPickerWidget(frame, row=0, column=0, label_text="Blender Exe Path", pick_mode='EXE')
        self.source_picker  = FolderPickerWidget(frame, row=1, column=0, label_text="Source Directory", pick_mode='DIR')
        self.build_picker   = FolderPickerWidget(frame, row=2, column=0, label_text="Build Directory" , pick_mode='DIR')


    def build_frame_2(self, frame):
        # Configure Frame
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
    
        # Tabs
        self.info_tabs = TabsWidget(frame, row=0, column=0, tab_names=["Required", "Optional", "Build"])

        # ------ [Required] ------ #
        # schema_version | id | name | version | tagline | maintainer | type | blender_version_min | license

        # Configure
        tab_1 = self.info_tabs.get_tab_frame(tab_name="Required")
        tab_1.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab_1.rowconfigure(0, weight=1)
        tab_1.rowconfigure(1, weight=1)
        tab_1.rowconfigure(2, weight=1)
        tab_1.rowconfigure(3, weight=1)
        tab_1.rowconfigure(4, weight=1)
        tab_1.rowconfigure(5, weight=1)
        tab_1.rowconfigure(6, weight=1)
        tab_1.rowconfigure(7, weight=1)
        tab_1.rowconfigure(8, weight=1)

        # Widgets
        self.schema_version = VersionWidget (tab_1, row=0, column=0, label_text="Schema Version"   , min_ver=(1,0,0))
        self.id_entry       = EntryWidget   (tab_1, row=1, column=0, label_text="Extension ID"     , char_modifiers=[CharsReplacer(filter_map={" ":"_"})])
        self.name_entry     = EntryWidget   (tab_1, row=2, column=0, label_text="Extension Name"   )
        self.ext_version    = VersionWidget (tab_1, row=3, column=0, label_text="Extension Version", min_ver=(0,0,0))
        self.tagline_entry  = EntryWidget   (tab_1, row=4, column=0, label_text="Extension Tagline", char_modifiers=[CharsLimiter(limit=64)])
        self.dev_name_entry = EntryWidget   (tab_1, row=5, column=0, label_text="Maintainer Name"  )
        self.type_dropdown  = DropdownWidget(tab_1, row=6, column=0, label_text="Extension Type"   , options=EXTENSION_TYPES, default="add-on")
        self.blender_min    = VersionWidget (tab_1, row=7, column=0, label_text="Blender Ver Min"  , min_ver=(4,2,0))
        self.license_pick   = ListPickWidget(tab_1, row=8, column=0, label_text="License(s)"       , items=LICENSES.keys())
    
        # Configure
        self.schema_version.disable()

        # ------ [Optional] ------ #
        # blender_version_max | website | copyright | tags | platforms | wheels | permissions

        # Configure
        tab_2 = self.info_tabs.get_tab_frame(tab_name="Optional")
        tab_2.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab_2.rowconfigure(0, weight=1)
        tab_2.rowconfigure(1, weight=1)
        tab_2.rowconfigure(2, weight=1)

        # Widgets
        self.blender_max     = VersionWidget (tab_2, row=0, column=0, label_text="Blender Ver Max"   , min_ver=(4,2,0), allow_ignore=True)
        self.dev_email_entry = EntryWidget   (tab_2, row=1, column=0, label_text="Maintainer Email"  )
        self.dev_web_entry   = EntryWidget   (tab_2, row=2, column=0, label_text="Maintainer Website")
        self.tags_pick       = ListPickWidget(tab_2, row=3, column=0, label_text="Extension Tags"    , items=ADDON_TAGS)
        self.platforms_pick  = ListPickWidget(tab_2, row=4, column=0, label_text="Platform Specs"    , items=PLATFORMS)

        # ------ [Build] ------ #
        # paths | paths_exclude_pattern

        # Configure
        tab_3 = self.info_tabs.get_tab_frame(tab_name="Build")
        tab_3.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab_3.rowconfigure(0, weight=1)

        # Widgets
        self.exclude_patterns_pick = ListPickWidget(tab_3, row=4, column=0, label_text="Exclude Patterns", items=PATH_EXCLUDE_PATTERNS)

        # ------ [Callbacks] ------ #

        self.type_dropdown.observers.add_callback(callback=self.callback_extension_type_change)


    def build_frame_3(self, frame):

        # Configure Frame
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Widgets
        self.info_tabs = TabsWidget(frame, row=0, column=0, tab_names=["Manifest", "Validate Command", "Build Command"])

        # ------ [Manifest] ------ #

        # Configure
        tab_1 = self.info_tabs.get_tab_frame(tab_name="Manifest")
        tab_1.columnconfigure(0, weight=1, minsize=LABEL_WIDTH)
        tab_1.rowconfigure(0, weight=1)

        # Widgets
        self.manifest_textbox = TextBoxWidget(tab_1, row=0, column=0, label_text="Manifest Preview")
        lines = [f"This is a line {i}" for i in range(100)]
        self.manifest_textbox.set_value(lines)

        # ------ [Callbacks] ------ #

        # self.type_dropdown.observers.add_callback(callback=self.callback_extension_type_change)


    def callback_extension_type_change(self, value):
        if value == "add-on":
            self.tags_pick.update_listbox(items=ADDON_TAGS)
        elif value == "theme":
            self.tags_pick.update_listbox(items=THEME_TAGS)


if __name__ == "__main__":
    set_licenses()
    app = App()
    app.setup()
    app.mainloop()
