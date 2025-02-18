
import tkinter as tk
from tkinter import filedialog

class FilePickController:
    def __init__(self, parent, label="Blender", file_types=(("All Files", "*.*"),)):
        self.frame = tk.Frame(parent, padx=2, pady=2, borderwidth=1, relief="solid")
        self.frame.pack(fill=tk.X)
        self.file_types = file_types

        # Label
        self.label = tk.Label(self.frame, text=label)
        self.label.pack(side=tk.LEFT, padx=5)

        # Entry
        self.entry = tk.Entry(self.frame)
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Button to open file dialog
        self.button = tk.Button(self.frame, text="Open Executable", command=self.open_file_dialog)
        self.button.pack(side=tk.LEFT, padx=5)

    def open_file_dialog(self):
        # Open a file dialog and filter for executable files
        file_path = filedialog.askopenfilename(title="Select an Executable File", filetypes=self.file_types)
        
        if file_path:
            # Insert the selected file path into the entry widget
            self.entry.delete(0, tk.END)  # Clear the current content of the entry
            self.entry.insert(0, file_path)  # Insert the selected file path
        else:
            print("No file selected")

# App class for demonstrating usage
class App:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)

        # Blender File Picker
        self.blender_file_picker = FilePickController(
            self.frame, 
            label="Blender Executable", 
            file_types=(("Executable Files", "*.exe"), ("All Files", "*.*"))
        )

# Set up the main window
root = tk.Tk()
app = App(root)
root.mainloop()