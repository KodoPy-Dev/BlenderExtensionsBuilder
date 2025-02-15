import tkinter as tk
from tkinter import ttk

def create_general_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="General")
    
    ttk.Label(frame, text="Maintainer:").grid(row=0, column=0, sticky="w")
    maintainer_entry = ttk.Entry(frame)
    maintainer_entry.grid(row=0, column=1, sticky="ew")
    
    ttk.Label(frame, text="Website:").grid(row=1, column=0, sticky="w")
    website_entry = ttk.Entry(frame)
    website_entry.grid(row=1, column=1, sticky="ew")
    
    ttk.Label(frame, text="Name:").grid(row=2, column=0, sticky="w")
    name_entry = ttk.Entry(frame)
    name_entry.grid(row=2, column=1, sticky="ew")
    
    return frame

def create_compatibility_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Compatibility")
    
    ttk.Label(frame, text="Blender Version Min:").grid(row=0, column=0, sticky="w")
    blender_min_entry = ttk.Entry(frame)
    blender_min_entry.grid(row=0, column=1, sticky="ew")
    
    ttk.Label(frame, text="Blender Version Max:").grid(row=1, column=0, sticky="w")
    blender_max_entry = ttk.Entry(frame)
    blender_max_entry.grid(row=1, column=1, sticky="ew")
    
    return frame

def create_legal_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Legal")
    
    ttk.Label(frame, text="License:").grid(row=0, column=0, sticky="w")
    license_entry = ttk.Entry(frame)
    license_entry.grid(row=0, column=1, sticky="ew")
    
    ttk.Label(frame, text="Copyright:").grid(row=1, column=0, sticky="w")
    copyright_entry = ttk.Entry(frame)
    copyright_entry.grid(row=1, column=1, sticky="ew")
    
    return frame

def create_build_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Build")
    
    ttk.Label(frame, text="Paths:").grid(row=0, column=0, sticky="w")
    paths_entry = ttk.Entry(frame)
    paths_entry.grid(row=0, column=1, sticky="ew")
    
    ttk.Label(frame, text="Exclude Patterns:").grid(row=1, column=0, sticky="w")
    exclude_entry = ttk.Entry(frame)
    exclude_entry.grid(row=1, column=1, sticky="ew")
    
    return frame

def create_main_window():
    root = tk.Tk()
    root.title("Blender Extension Manifest Tool")
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)
    
    create_general_tab(notebook)
    create_compatibility_tab(notebook)
    create_legal_tab(notebook)
    create_build_tab(notebook)
    
    root.mainloop()

if __name__ == "__main__":
    create_main_window()
