import tkinter as tk

root = tk.Tk()

# Create a Text widget
text_box = tk.Text(root, height=10, width=50)
text_box.pack(side=tk.LEFT, fill=tk.Y)

# Insert some text
text_box.insert(tk.END, "This is some read-only text.\n" * 20)  # Add multiple lines for scrolling

# Make the text box read-only
text_box.config(state=tk.DISABLED)

# Create a Scrollbar widget and link it to the Text widget
scrollbar = tk.Scrollbar(root, command=text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the scrollbar to the Text widget
text_box.config(yscrollcommand=scrollbar.set)

root.mainloop()