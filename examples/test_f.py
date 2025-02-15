import tkinter as tk

root = tk.Tk()

# Create widgets
label1 = tk.Label(root, text="Column 0")
label2 = tk.Label(root, text="Column 1 - Wider")

# Place widgets in the grid
label1.grid(row=0, column=0)
label2.grid(row=0, column=1)

# Configure column 1 to be wider
root.columnconfigure(1, weight=1)

root.mainloop()