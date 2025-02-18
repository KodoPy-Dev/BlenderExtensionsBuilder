import tkinter as tk

# Initialize main window
root = tk.Tk()
root.title("Tkinter Grid Layout")

# Configure main grid
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create frames
top_frame = tk.Frame(root, bg="lightgray")
top_frame.grid(row=0, column=0, sticky="nsew")

bottom_frame = tk.Frame(root, bg="white")
bottom_frame.grid(row=1, column=0, sticky="nsew")

# Configure weight so frames resize properly
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)

# Add widgets to frames
label = tk.Label(top_frame, text="Top Frame", bg="lightgray")
label.grid(row=0, column=0, padx=10, pady=10)

button = tk.Button(bottom_frame, text="Click Me")
button.grid(row=0, column=0, padx=10, pady=10)

# Run the application
root.mainloop()