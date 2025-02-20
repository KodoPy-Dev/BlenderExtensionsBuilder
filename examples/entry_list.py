import tkinter as tk
from tkinter import messagebox, simpledialog


class EntryListWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.add_button = tk.Button(self, text="Add", command=self.add_entry)
        self.add_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        self.listbox = tk.Listbox(self)
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_entry)
        self.delete_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        self.listbox.bind("<Double-Button-1>", self.edit_entry)

    def add_entry(self):
        entry_text = self.entry_var.get().strip()
        if entry_text and entry_text not in self.listbox.get(0, tk.END):
            self.listbox.insert(tk.END, entry_text)
            self.entry_var.set("")
        else:
            messagebox.showwarning("Warning", "Invalid or duplicate entry.")

    def delete_entry(self):
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            self.listbox.delete(index)

    def edit_entry(self, event):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        index = selected_index[0]
        current_text = self.listbox.get(index)
        
        new_text = simpledialog.askstring("Edit Entry", "Modify entry:", initialvalue=current_text)
        if new_text:
            self.listbox.delete(index)
            self.listbox.insert(index, new_text)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Entry List Widget")
    root.geometry("300x400")
    app = EntryListWidget(master=root)
    app.mainloop()
