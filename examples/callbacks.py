import tkinter as tk

class DropdownWidget:
    def __init__(self, parent, update_callback):
        self.dropdown_var = tk.StringVar()
        self.dropdown = tk.OptionMenu(parent, self.dropdown_var, 'Option 1', 'Option 2', 'Option 3')
        self.dropdown.pack(pady=10)
        
        # Set the callback to be triggered on value change
        self.dropdown_var.trace_add("write", lambda *args: update_callback(self.dropdown_var.get()))

class ListboxWidget:
    def __init__(self, parent):
        self.listbox = tk.Listbox(parent)
        self.listbox.pack(pady=10)
    
    def update_listbox(self, items):
        self.listbox.delete(0, tk.END)  # Clear existing items
        for item in items:
            self.listbox.insert(tk.END, item)

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dropdown and Listbox Example")

        # Create the Listbox widget
        self.listbox_widget = ListboxWidget(root)
        
        # Create the Dropdown widget and pass a callback to update the listbox
        self.dropdown_widget = DropdownWidget(root, self.update_listbox)

    def update_listbox(self, selected):
        if selected == 'Option 1':
            items = ['Item 1A', 'Item 1B', 'Item 1C']
        elif selected == 'Option 2':
            items = ['Item 2A', 'Item 2B', 'Item 2C']
        elif selected == 'Option 3':
            items = ['Item 3A', 'Item 3B', 'Item 3C']
        else:
            items = []
        
        # Call the ListboxWidget to update the list
        self.listbox_widget.update_listbox(items)

# Run the application
root = tk.Tk()
app = MyApp(root)
root.mainloop()
