import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("Version Picker")
root.geometry("400x400")

major_var = tk.IntVar(value=1)
minor_var = tk.IntVar(value=0)
patch_var = tk.IntVar(value=0)

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Spinboxes for version selection
ttk.Label(frame, text="Major:").grid(row=0, column=0)
major_spin = ttk.Spinbox(frame, from_=0, to=99, textvariable=major_var, width=5)
major_spin.grid(row=0, column=1)

ttk.Label(frame, text="Minor:").grid(row=0, column=1)
minor_spin = ttk.Spinbox(frame, from_=0, to=99, textvariable=minor_var, width=5)
minor_spin.grid(row=1, column=1)

ttk.Label(frame, text="Patch:").grid(row=0, column=2)
patch_spin = ttk.Spinbox(frame, from_=0, to=99, textvariable=patch_var, width=5)
patch_spin.grid(row=2, column=1)

# Button to get version
select_button = ttk.Button(frame, text="Select Version", command=get_version)
select_button.grid(row=3, column=0, columnspan=2, pady=10)

# Output label
output_label = ttk.Label(frame, text="Selected Version: 1.0.0")
output_label.grid(row=4, column=0, columnspan=2)

root.mainloop()


def get_version():
    version = f"{major_var.get()}.{minor_var.get()}.{patch_var.get()}"
    output_label.config(text=f"Selected Version: {version}")
