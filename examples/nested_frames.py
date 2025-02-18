import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Nested Frames with Grid")

# Create parent frames
frame_top = tk.Frame(window, bg="lightgray", height=100)
frame_bottom = tk.Frame(window, bg="white", height=200)

# Use grid to position parent frames
frame_top.grid(row=0, column=0, sticky="ew")
frame_bottom.grid(row=1, column=0, sticky="nsew")

# Configure row weights so bottom frame expands
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

# Create child frames within the top frame
frame_top_left = tk.Frame(frame_top, bg="lightblue")
frame_top_right = tk.Frame(frame_top, bg="lightgreen")

# Use grid to position child frames within the top frame
frame_top_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
frame_top_right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Configure column weights for the top frame
frame_top.grid_columnconfigure(0, weight=1)
frame_top.grid_columnconfigure(1, weight=1)

# Add widgets to child frames
label_top_left = tk.Label(frame_top_left, text="Top Left", bg="lightblue")
label_top_right = tk.Label(frame_top_right, text="Top Right", bg="lightgreen")
label_bottom = tk.Label(frame_bottom, text="Bottom", bg="white")

# Use grid to position widgets within child frames
label_top_left.grid(row=0, column=0, padx=10, pady=10)
label_top_right.grid(row=0, column=0, padx=10, pady=10)
label_bottom.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Run the Tkinter event loop
window.mainloop()