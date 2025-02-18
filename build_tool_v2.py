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
"""                  WIDGETS                  """
########################•########################

class FolderPickerWidget():
    def __init__(self, frame, row=0, column=0, label_text="Select Path", pick_folder=True):
        self.frame = frame
        self.pick_folder = pick_folder

        # Components
        self.label  = tk.Label(self.frame, text=label_text)
        self.entry  = tk.Entry(self.frame)
        self.button = tk.Button(self.frame, text="Open", command=self.browse)

        # Position
        col = column
        self.label.grid(row=row, column=col, sticky="w", padx=5)
        self.entry.grid(row=row, column=col+1, sticky="we", padx=5)
        self.button.grid(row=row, column=col+2, sticky="e", padx=5)


    def browse(self):
        if self.pick_folder:
            path = filedialog.askdirectory()
        else:
            path = filedialog.askopenfilename()
        if path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, path)


    def get_value(self):
        return self.entry.get()


class TabsWidget():
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


class EntryWidget():
    def __init__(self, frame, row=0, column=0, label_text="Entry", filter_map=dict(), char_limit=0):
        self.frame = frame
        self.filter_map = filter_map
        self.char_limit = char_limit

        # Components
        self.label = tk.Label(self.frame, text=label_text)
        self.entry = tk.Entry(self.frame)

        # Position
        col = column
        self.label.grid(row=row, column=col, sticky="w", padx=5)
        self.entry.grid(row=row, column=col+1, sticky="we", padx=5)

        # Events
        if self.filter_map:
            self.entry.bind("<KeyPress>", self.process_filter, add="+")
        if self.char_limit:
            self.entry.bind("<KeyPress>", self.process_char_limit, add="+")


    def get_value(self):
        return self.entry.get()


    def process_filter(self, event):
        current = self.get_value()
        composed = [self.filter_map.get(char, char) for char in current]
        new_value = "".join(composed)
        if current != new_value:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, new_value)


    def process_char_limit(self, event):
        current = self.get_value()
        if current and len(current) > self.char_limit:
            new_value = current[:self.char_limit]
            self.entry.delete(0, tk.END)
            self.entry.insert(0, new_value)


class DropdownWidget():
    def __init__(self, frame, row=0, column=0, label_text="Dropdown", options=[], default=""):
        self.frame = frame
        self.options = options

        # Components
        self.label = tk.Label(self.frame, text=label_text)
        self.dropdown = ttk.Combobox(self.frame, values=self.options, state="readonly")

        # Position
        col = column
        self.label.grid(row=row, column=col, sticky="w", padx=5)
        self.dropdown.grid(row=row, column=col+1, sticky="we", padx=5)

        # Values
        if default and default in self.options:
            self.dropdown.set(default)
        elif self.options:
            self.dropdown.set(self.options[0])


    def get_value(self):
        return self.dropdown.get()


    def set_value(self, value):
        if value in self.options:
            self.dropdown.set(value)


class VersionWidget:
    def __init__(self, frame, row=0, column=0, label_text="Version", min_ver=(0, 0, 0), add_use_check=False):
        self.frame = frame

        # Props
        self.var_major = tk.IntVar(value=min_ver[0])
        self.var_minor = tk.IntVar(value=min_ver[1])
        self.var_patch = tk.IntVar(value=min_ver[2])
        self.var_use = None


        # self.check_box = None
        # # Checkbutton variable (optional)
        # if add_use_check:
        #     self.var_use = tk.BooleanVar(value=False)
        # # Check Box
        # if add_use_check:
        #     self.check_box = tk.Checkbutton(self.frame, text="Use", variable=self.var_use, command=self.com_check_box)
        #     self.check_box.grid(row=row, column=column, sticky="w", padx=5)

        # # Initially hide spinboxes if "Use" checkbox exists and is unchecked
        # if add_use_check:
        #     self.com_check_box()


        # Label
        self.label = tk.Label(self.frame, text=label_text)
        self.label.grid(row=row, column=column, sticky="w", padx=5)

        # Spin Frame
        self.spin_frame = tk.Frame(self.frame)
        self.spin_frame.grid(row=row+1, column=column+1, sticky="nsew")
        self.spin_frame.grid_rowconfigure(0, weight=1)
        self.spin_frame.grid_columnconfigure(0, weight=1)
        self.spin_frame.grid_columnconfigure(1, weight=1)
        self.spin_frame.grid_columnconfigure(2, weight=1)

        self.spin_major = tk.Spinbox(self.spin_frame, from_=min_ver[0], to=sys.maxsize, textvariable=self.var_major)
        self.spin_minor = tk.Spinbox(self.spin_frame, from_=min_ver[1], to=sys.maxsize, textvariable=self.var_minor)
        self.spin_patch = tk.Spinbox(self.spin_frame, from_=min_ver[2], to=sys.maxsize, textvariable=self.var_patch)
        self.spin_major.grid(row=0, column=0, sticky="w" , padx=2)
        self.spin_minor.grid(row=0, column=1, sticky="we", padx=2)
        self.spin_patch.grid(row=0, column=2, sticky="e" , padx=2)



    def com_check_box(self):
        """Enable/Disable the version spinboxes based on checkbox state."""
        state = tk.NORMAL if self.var_use.get() else tk.DISABLED
        self.spin_major.config(state=state)
        self.spin_minor.config(state=state)
        self.spin_patch.config(state=state)

    def get_version(self):
        """Return the version tuple if enabled, else None."""
        if self.check_box and self.var_use and not self.var_use.get():
            return None
        return self.var_major.get(), self.var_minor.get(), self.var_patch.get()


########################•########################
"""                APPLICATION                """
########################•########################

APP_NAME = "Blender Extension Creator"
APP_WIDTH = 600
APP_HEIGHT = 800
APP_RESIZABLE = True

COL_WHITE = 'white'
COL_GREY  = '#f0f0f0'


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        root = self
        root.title(APP_NAME)
        root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        root.resizable(APP_RESIZABLE, APP_RESIZABLE)

        # Configure main grid
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Create frames
        frame_1 = tk.Frame(root, padx=5, pady=5, borderwidth=1, relief="solid")
        frame_2 = tk.Frame(root, padx=5, pady=5, borderwidth=1, relief="solid")
        frame_3 = tk.Frame(root, padx=5, pady=5, borderwidth=1, relief="solid")
        frame_4 = tk.Frame(root, padx=5, pady=5, borderwidth=1, relief="solid")
        frame_5 = tk.Frame(root, padx=5, pady=5, borderwidth=1, relief="solid")
        frame_6 = tk.Frame(root, padx=5, pady=5, borderwidth=1, relief="solid")

        # Rows
        frame_1.grid(row=0, column=0, sticky="nsew")
        frame_2.grid(row=1, column=0, sticky="nsew")
        frame_3.grid(row=2, column=0, sticky="nsew")
        frame_4.grid(row=3, column=0, sticky="nsew")
        frame_5.grid(row=4, column=0, sticky="nsew")
        frame_6.grid(row=5, column=0, sticky="nsew")

        # Position Frames
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=30)
        root.grid_rowconfigure(2, weight=10)
        root.grid_rowconfigure(3, weight=1)
        root.grid_rowconfigure(4, weight=1)
        root.grid_rowconfigure(5, weight=1)

        # --- Frame 1 --- #

        # Configure Frame
        frame_1.grid_columnconfigure(0, weight=1)
        frame_1.grid_columnconfigure(1, weight=5)
        frame_1.grid_columnconfigure(2, weight=1)

        # Widgets
        self.blender_picker = FolderPickerWidget(frame_1, row=0, column=0, label_text="Choose Blender Exe", pick_folder=False)
        self.source_picker  = FolderPickerWidget(frame_1, row=1, column=0, label_text="Choose Source Dir", pick_folder=True)
        self.build_picker   = FolderPickerWidget(frame_1, row=2, column=0, label_text="Choose Build Dir:", pick_folder=True)

        # --- Frame 2 --- #

        # Configure Frame
        frame_2.grid_rowconfigure(0, weight=1)
        frame_2.grid_columnconfigure(0, weight=1)

        # Tabs
        self.info_tabs = TabsWidget(frame_2, row=0, column=0, tab_names=["Extension", "Version", "Developer", "License", "Build"])

        # Tab 1 - Extension -
        tab_1 = self.info_tabs.get_tab_frame(tab_name="Extension")
        tab_1.grid_columnconfigure(0, weight=1)
        tab_1.grid_columnconfigure(1, weight=4)

        # Widgets
        self.id_entry      = EntryWidget(tab_1   , row=0, column=0, label_text="Extension ID"     , filter_map={' ':'_'})
        self.name_entry    = EntryWidget(tab_1   , row=1, column=0, label_text="Extension Name"   , filter_map=None)
        self.ext_version   = VersionWidget(tab_1 , row=2, column=0, label_text="Extension Version", min_ver=(0,0,0), add_use_check=False)
        self.tagline_entry = EntryWidget(tab_1   , row=3, column=0, label_text="Extension Tagline", filter_map=None, char_limit=64)
        self.type_dropdown = DropdownWidget(tab_1, row=4, column=0, label_text="Extension Type"   , options=EXTENSION_TYPES, default="add-on")



        # | tags                   | X        | Extension | Pick tags based on type


        # --- Frame 3 --- #

        # Configure Frame
        frame_3.grid_rowconfigure(0, weight=1)
        frame_3.grid_columnconfigure(0, weight=1)

        # Widgets
        self.info_tabs = TabsWidget(frame_3, row=0, column=0, tab_names=["Manifest", "Validate Command", "Build Command"])


if __name__ == "__main__":
    app = App()
    app.mainloop()
