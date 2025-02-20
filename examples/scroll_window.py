import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Main container
container = ttk.Frame(root)
container.pack(fill="both", expand=True)

# Canvas for scrollable region
canvas = tk.Canvas(container)
canvas.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure canvas scrolling
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Frame to hold scrollable content
scrollable_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Add content to the scrollable frame
for i in range(50):
    ttk.Label(scrollable_frame, text=f"Label {i}").pack()

root.mainloop()