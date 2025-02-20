import tkinter as tk
from tkinter.simpledialog import Dialog



class EntryPopup(Dialog):
    def __init__(self, parent, width=100, height=100, label_text="", prompt_text=""):
        self.parent = parent
        self.width = width
        self.height = height
        self.label_text = label_text
        self.prompt_text = prompt_text
        self.result = ""
        self.label = None
        self.entry = None
        super().__init__(parent, label_text)
    def body(self, frame):
        self.geometry(f"{self.width}x{self.height}")
        self.label = tk.Label(frame, text=self.prompt_text)
        self.label.pack(pady=5)
        self.entry = tk.Entry(frame, width=self.width)
        self.entry.pack(pady=5)
        return self.entry
    def apply(self):
        if self.entry:
            self.result = self.entry.get()


    @staticmethod
    def invoke(parent, width=100, height=100, label_text="", prompt_text=""):
        popup = EntryPopup(parent, width, height, label_text, prompt_text)
        return popup.result


root = tk.Tk()
root.title("Treeview in Tk")

result = EntryPopup.invoke(root, width=500, height=100, label_text="LABEL", prompt_text="PROMPT")

print(result)


root.mainloop()