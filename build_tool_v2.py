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
is_str_int     = lambda item: is_string(item) and item.isdigit()

does_file_ext_match           = lambda file_path, file_ext : is_path(file_path) and is_string(file_ext) and get_file_extension(file_path) == file_ext.lower()
does_file_name_match_no_ext   = lambda file_path, file_name: is_path(file_path) and is_string(file_name) and Path(file_path).name == file_name
does_file_name_match_with_ext = lambda file_path, file_name: is_path(file_path) and is_file_name(file_name) and Path(file_path).name.lower() == file_name.lower()

########################•########################
"""                  WIDGETS                  """
########################•########################

class COLORS:
    BLACK = "#050D0F" # Black
    WHITE = "#F3F3F3" # White
    BG1 = "#EEEEEE" # Light Grey
    BG2 = "#CCCCCC" # Medium Grey
    BG3 = "#AAAAAA" # Dark Grey
    VALID = "#4ceb34" # Gren
    ERROR = "#E56B6F" # Red


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


class FolderPickerWidget:
    def __init__(self, parent, row=0, column=0, padx=0, pady=0, label_text="Select Path", label_min_w=150, bg=COLORS.BG1, pick_mode='DIR'):
        '''
        pick_mode : DIR (folder), FILE (file), EXE (executable)
        '''
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent, padx=padx, pady=pady, bg=bg)

        # Add Frame
        self.frame.grid(row=row, column=column, sticky="we")

        # Configure Layout
        self.frame.grid_columnconfigure(0, minsize=label_min_w)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, minsize=75)
        self.frame.grid_rowconfigure(0, weight=1)

        # Props
        self.observers = Observers()
        self.pick_mode = pick_mode

        # Create Widgets
        self.label  = tk.Label(self.frame, text=label_text, bg=bg)
        self.entry  = tk.Entry(self.frame)
        self.button = tk.Button(self.frame, text="Open", command=self.browse, bg=COLORS.BLACK, fg=COLORS.WHITE)

        # Add Widgets
        self.label.grid( row=0, column=0, sticky="we", padx=5)
        self.entry.grid( row=0, column=1, sticky="we", padx=5)
        self.button.grid(row=0, column=2, sticky="we", padx=5)

        # Style
        self.entry.config(highlightthickness=1, highlightbackground=COLORS.BLACK, highlightcolor=COLORS.BLACK)

        # Bind
        self.entry.bind("<FocusOut>", self.callback_validator)
        self.entry.bind("<Return>", self.callback_validator)


    def get_value(self):
        return self.entry.get()


    def callback_validator(self, event=None):
        value = self.get_value()
        if not value:
            self.entry.config(highlightthickness=1, highlightbackground=COLORS.BLACK, highlightcolor=COLORS.BLACK)
            return
        valid = False
        if self.pick_mode == 'DIR': valid = is_dir(value)
        elif self.pick_mode == 'EXE': valid = is_exe(value)
        elif self.pick_mode == 'FILE': valid = is_path(value)
        if valid:
            self.entry.config(highlightthickness=1, highlightbackground=COLORS.VALID, highlightcolor=COLORS.VALID)
        else:
            self.entry.config(highlightthickness=1, highlightbackground=COLORS.ERROR, highlightcolor=COLORS.ERROR)
        # Observers
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
        self.notebook.grid(row=row, column=column, sticky="nsew", padx=10)

        # Tabs
        for tab_name in tab_names:
            tab_frame = tk.Frame(self.notebook)
            self.notebook.add(tab_frame, text=tab_name)
            self.tabs[tab_name] = tab_frame


    def get_tab_frame(self, tab_name=""):
        if tab_name in self.tabs:
            frame = self.tabs[tab_name]
            if isinstance(frame, tk.Frame):
                return frame
        return None


class EntryWidget:
    def __init__(self, parent, row=0, column=0, padx=0, pady=0, label_text="Entry", label_min_w=150, bg=COLORS.BG1, filter_map=dict(), char_limit=0):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent, padx=padx, pady=pady, bg=bg)

        # Add Frame
        self.frame.grid(row=row, column=column, sticky="we")

        # Configure Layout
        self.frame.grid_columnconfigure(0, minsize=label_min_w)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # Props
        self.observers = Observers()
        self.filter_map = filter_map
        self.char_limit = char_limit

        # Create Widgets
        self.label = tk.Label(self.frame, text=label_text)
        self.entry = tk.Entry(self.frame)

        # Add Widgets
        self.label.grid(row=0, column=0, sticky="w", padx=5)
        self.entry.grid(row=0, column=1, sticky="we", padx=5)

        # Bind
        self.entry.bind("<FocusOut>", self.entry_callback)
        self.entry.bind("<Return>", self.entry_callback)
        self.entry.bind("<KeyPress>", self.entry_callback)


    def get_value(self):
        return self.entry.get()


    def entry_callback(self, event):
        value = self.get_value()

        # Filter
        if value and self.filter_map:
            value = "".join([self.filter_map.get(char, char) for char in value])
            self.entry.delete(0, tk.END)
            self.entry.insert(0, value)

        # Limit
        if value and self.char_limit > 0:
            if len(value) > self.char_limit:
                value = value[:self.char_limit]
                self.entry.delete(0, tk.END)
                self.entry.insert(0, value)

        # Observers
        self.observers.update(value)


class DropdownWidget:
    def __init__(self, parent, row=0, column=0, padx=0, pady=0, label_text="Dropdown", label_min_w=150, bg=COLORS.BG1, options=[], default=""):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent, padx=padx, pady=pady, bg=bg)

        # Add Frame
        self.frame.grid(row=row, column=column, sticky="we")

        # Configure Layout
        self.frame.grid_columnconfigure(0, minsize=label_min_w)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # Props
        self.observers = Observers()
        self.options = options

        # Create Widgets
        self.label = tk.Label(self.frame, text=label_text)
        self.dropdown = ttk.Combobox(self.frame, values=self.options, state="readonly")

        # Add Widgets
        self.label.grid(row=0, column=0, sticky="w", padx=5)
        self.dropdown.grid(row=0, column=1, sticky="w", padx=5)

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
    def __init__(self, parent, row=0, column=0, padx=0, pady=0, label_text="Version", label_min_w=150, bg=COLORS.BG1, min_ver=(0, 0, 0), allow_ignore=False):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent, padx=padx, pady=pady, bg=bg)

        # Add Frame
        self.frame.grid(row=row, column=column, sticky="we")

        # Configure Layout
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, minsize=label_min_w)
        if allow_ignore:
            self.frame.grid_columnconfigure(1, weight=1)
            self.frame.grid_columnconfigure(2, weight=1)
            self.frame.grid_columnconfigure(3, weight=2)
            self.frame.grid_columnconfigure(4, weight=1)
            self.frame.grid_columnconfigure(5, weight=2)
            self.frame.grid_columnconfigure(6, weight=1)
        else:
            self.frame.grid_columnconfigure(1, weight=1)
            self.frame.grid_columnconfigure(2, weight=2)
            self.frame.grid_columnconfigure(3, weight=1)
            self.frame.grid_columnconfigure(4, weight=2)
            self.frame.grid_columnconfigure(5, weight=1)

        # Props
        self.observers = Observers()
        self.var_major = tk.IntVar(value=min_ver[0])
        self.var_minor = tk.IntVar(value=min_ver[1])
        self.var_patch = tk.IntVar(value=min_ver[2])

        # Create Label
        self.label = tk.Label(self.frame, text=label_text)

        # Add Label
        self.label.grid(row=0, column=0, sticky="w", padx=5)

        # Create Version Labels
        self.label_major = tk.Label(self.frame, text="Major")
        self.label_minor = tk.Label(self.frame, text="Minor")
        self.label_patch = tk.Label(self.frame, text="Patch")

        # Register Validator
        validate_cmd = self.frame.register(is_str_int)

        # Create Spin Boxes
        self.spin_major = tk.Spinbox(self.frame, from_=min_ver[0], to=sys.maxsize, textvariable=self.var_major, command=self.spinbox_callback, validate="key", validatecommand=(validate_cmd, "%P"))
        self.spin_minor = tk.Spinbox(self.frame, from_=min_ver[1], to=sys.maxsize, textvariable=self.var_minor, command=self.spinbox_callback, validate="key", validatecommand=(validate_cmd, "%P"))
        self.spin_patch = tk.Spinbox(self.frame, from_=min_ver[2], to=sys.maxsize, textvariable=self.var_patch, command=self.spinbox_callback, validate="key", validatecommand=(validate_cmd, "%P"))

        column = 1

        # Ignore Checkbox
        self.ignore_var = tk.BooleanVar()
        self.ignore_checkbox = None
        if allow_ignore:
            self.ignore_checkbox = tk.Checkbutton(self.frame, text="Ignore", command=self.ignore_checkbox_callback)
            self.ignore_checkbox.grid(row=0, column=1, sticky="w", padx=1)
            column += 1

        # Add Major
        self.label_major.grid(row=0, column=column + 0, sticky="w", padx=1)
        self.spin_major.grid( row=0, column=column + 1, sticky="w", padx=1)

        # Add Minor
        self.label_minor.grid(row=0, column=column + 2, sticky="w", padx=1)
        self.spin_minor.grid( row=0, column=column + 3, sticky="w", padx=1)

        # Add Patch
        self.label_patch.grid(row=0, column=column + 4, sticky="w", padx=1)
        self.spin_patch.grid( row=0, column=column + 5, sticky="w", padx=1)


    def get_value(self):
        if isinstance(self.ignore_checkbox, tk.Checkbutton):
            if self.ignore_checkbox.get():
                return None
        return self.var_major.get(), self.var_minor.get(), self.var_patch.get()


    def spinbox_callback(self):
        value = self.get_value()
        self.observers.update(value)


    def ignore_checkbox_callback(self):
        if isinstance(self.ignore_checkbox, tk.Checkbutton):
            if self.ignore_checkbox.cget():
                self.var_major.config(state="disabled")
                self.var_minor.config(state="disabled")
                self.var_patch.config(state="disabled")
            else:
                self.var_major.config(state="normal")
                self.var_minor.config(state="normal")
                self.var_patch.config(state="normal")
            self.spinbox_callback()


class ListPickWidget:
    def __init__(self, parent, row=0, column=0, padx=0, pady=0, label_text="Item Picker", label_min_w=150, bg=COLORS.BG1, items=None):
        # Parent
        self.parent = parent

        # Create Frame
        self.frame = tk.Frame(self.parent, padx=padx, pady=pady, bg=bg)

        # Add Frame
        self.frame.grid(row=row, column=column, sticky="we")

        # Configure Layout
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, minsize=label_min_w)
        self.frame.grid_columnconfigure(1, weight=1)

        # Props
        self.observers = Observers()

        # Create Label
        self.label = tk.Label(self.frame, text=label_text, bg=bg, fg=COLORS.BLACK)

        # Add Label
        self.label.grid(row=0, column=0, sticky="w", padx=5)

        # Create Scrollbar
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)

        # Create List Box
        self.listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, width=50, height=10, yscrollcommand=self.scrollbar.set)

        # Add Scrollbar
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=2, sticky="ns")

        # Add Listbox
        self.listbox.grid(row=1, column=1, sticky="we")

        # Populate Listbox
        self.update_listbox(items)

        # Bind
        self.listbox.bind("<<ListboxSelect>>", self.listbox_callback)


    def get_value(self):
        selected_indices = self.listbox.curselection()
        return [self.listbox.get(i) for i in selected_indices]


    def listbox_callback(self, event=None):
        value = self.get_value()
        self.observers.update(value)


    def update_listbox(self, items):
        self.listbox.delete(0, tk.END)
        for item in items:
            if isinstance(item, str):
                self.listbox.insert(tk.END, item)
        self.listbox_callback()

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

APP_NAME = "Blender Extension Creator"
LABEL_WIDTH = 150

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        root = self
        root.title(APP_NAME)
        root.resizable(False, False)

    @try_except_decorator
    def setup(self):
        root = self
        # Configure Layout
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=10)
        root.grid_rowconfigure(2, weight=10)
        root.grid_rowconfigure(3, weight=1)
        root.grid_rowconfigure(4, weight=1)
        root.grid_rowconfigure(5, weight=1)
        # Create frames
        frame_1 = tk.Frame(root, padx=5, pady=5, borderwidth=2, relief="groove", background=COLORS.BG3)
        frame_2 = tk.Frame(root, padx=5, pady=5, borderwidth=2, relief="groove", background=COLORS.BG2)
        frame_3 = tk.Frame(root, padx=5, pady=5, borderwidth=2, relief="groove", background=COLORS.BG1)
        frame_4 = tk.Frame(root, padx=5, pady=5, borderwidth=2, relief="groove", background=COLORS.BG2)
        frame_5 = tk.Frame(root, padx=5, pady=5, borderwidth=2, relief="groove", background=COLORS.BG1)
        frame_6 = tk.Frame(root, padx=5, pady=5, borderwidth=2, relief="groove", background=COLORS.BG2)
        # Add Frames
        frame_1.grid(row=0, column=0, sticky="nsew")
        frame_2.grid(row=1, column=0, sticky="nsew")
        frame_3.grid(row=2, column=0, sticky="nsew")
        frame_4.grid(row=3, column=0, sticky="nsew")
        frame_5.grid(row=4, column=0, sticky="nsew")
        frame_6.grid(row=5, column=0, sticky="nsew")
        # Build
        self.build_frame_1(frame=frame_1)
        self.build_frame_2(frame=frame_2)
        self.build_frame_3(frame=frame_3)
        self.build_frame_4(frame=frame_4)
        self.build_frame_5(frame=frame_5)
        self.build_frame_6(frame=frame_6)


    def build_frame_1(self, frame):
        # Configure Layout
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        # Widgets
        self.blender_picker = FolderPickerWidget(frame, row=0, column=0, padx=5, pady=5, label_text="Blender Exe Path", label_min_w=LABEL_WIDTH, bg=COLORS.BG3, pick_mode='EXE')
        self.source_picker  = FolderPickerWidget(frame, row=1, column=0, padx=5, pady=5, label_text="Source Directory", label_min_w=LABEL_WIDTH, bg=COLORS.BG3, pick_mode='DIR')
        self.build_picker   = FolderPickerWidget(frame, row=2, column=0, padx=5, pady=5, label_text="Build Directory" , label_min_w=LABEL_WIDTH, bg=COLORS.BG3, pick_mode='DIR')


    def build_frame_2(self, frame):
        # Configure Frame
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        # Tabs
        self.info_tabs = TabsWidget(frame, row=0, column=0, tab_names=["Extension", "Developer", "License", "Build"])

        # --- [Extension] -- #

        # Configure Tab
        tab_1 = self.info_tabs.get_tab_frame(tab_name="Extension")
        tab_1.grid_columnconfigure(0, weight=1, minsize=100)
        tab_1.grid_columnconfigure(1, weight=1)
        tab_1.grid_rowconfigure(0, weight=1)
        tab_1.grid_rowconfigure(1, weight=1)
        tab_1.grid_rowconfigure(2, weight=1)
        tab_1.grid_rowconfigure(3, weight=1)
        tab_1.grid_rowconfigure(4, weight=1)
        tab_1.grid_rowconfigure(5, weight=1)

        # Widgets
        self.id_entry      = EntryWidget(   tab_1, row=0, column=0, padx=5, pady=5, label_text="ID"             , label_min_w=LABEL_WIDTH, filter_map={' ':'_'})
        self.name_entry    = EntryWidget(   tab_1, row=1, column=0, padx=5, pady=5, label_text="Name"           , label_min_w=LABEL_WIDTH, filter_map=None)
        self.ext_version   = VersionWidget( tab_1, row=2, column=0, padx=5, pady=5, label_text="Version"        , label_min_w=LABEL_WIDTH, min_ver=(0,0,0))
        self.tagline_entry = EntryWidget(   tab_1, row=3, column=0, padx=5, pady=5, label_text="Tagline"        , label_min_w=LABEL_WIDTH, filter_map=None, char_limit=64)
        self.type_dropdown = DropdownWidget(tab_1, row=4, column=0, padx=5, pady=5, label_text="Type"           , label_min_w=LABEL_WIDTH, options=EXTENSION_TYPES, default="add-on")
        self.tags_picker   = ListPickWidget(tab_1, row=5, column=0, padx=5, pady=5, label_text="Tags"           , label_min_w=LABEL_WIDTH, bg=COLORS.BG1, items=ADDON_TAGS)
        self.blender_min   = VersionWidget( tab_1, row=6, column=0, padx=5, pady=5, label_text="Blender Min Ver", label_min_w=LABEL_WIDTH, min_ver=(4,2,0))
        self.blender_max   = VersionWidget( tab_1, row=7, column=0, padx=5, pady=5, label_text="Blender Max Ver", label_min_w=LABEL_WIDTH, min_ver=(4,2,0), allow_ignore=True)

        # Callbacks
        self.type_dropdown.observers.add_callback(callback=self.callback_extension_type_change)


    def build_frame_3(self, frame):

        # Configure Frame
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        # Widgets
        self.info_tabs = TabsWidget(frame, row=0, column=0, tab_names=["Manifest", "Validate Command", "Build Command"])


    def build_frame_4(self, frame=None):
        pass


    def build_frame_5(self, frame=None):
        pass


    def build_frame_6(self, frame=None):
        pass


    def callback_extension_type_change(self, value):
        if value == "add-on":
            self.tags_picker.update_listbox(items=ADDON_TAGS)
        elif value == "theme":
            self.tags_picker.update_listbox(items=THEME_TAGS)


if __name__ == "__main__":
    set_licenses()
    app = App()
    app.setup()
    app.mainloop()
