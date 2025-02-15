import tkinter as tk

def on_enter_pressed(event):
    entry_widget = event.widget  # Get the Entry widget from the event
    print("Entry content:", entry_widget.get())

root = tk.Tk()

entry = tk.Entry(root)
entry.pack()

# Bind the Enter key (Return) to the callback function
entry.bind("<Return>", on_enter_pressed)

root.mainloop()