
import traceback
import tkinter as tk
from tkinter import ttk


def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"ERROR : {func.__name__}()")
            traceback.print_exc()
    return wrapper


APP_ROOT = None
APP_NAME = "Blender Extension Creator"
APP_WIDTH = 600
APP_HEIGHT = 800
APP_RESIZABLE = True


@try_except_decorator
def create_app():
    global APP_ROOT
    APP_ROOT = tk.Tk()
    APP_ROOT.title(APP_NAME)
    APP_ROOT.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
    if APP_RESIZABLE:
        APP_ROOT.resizable(True, True)
    else:
        APP_ROOT.resizable(False, False)


@try_except_decorator
def create_sections():
    global APP_ROOT
    if not APP_ROOT:
        return

    # Configure main grid
    APP_ROOT.grid_columnconfigure(0, weight=1)
    APP_ROOT.grid_rowconfigure(0, weight=1)

    # Colors
    color_a = "lightgray"
    color_b = "white"

    # Create frames
    frame_1 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_a).grid(row=0, column=0, sticky="nsew")
    frame_2 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_b).grid(row=1, column=0, sticky="nsew")
    frame_3 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_a).grid(row=2, column=0, sticky="nsew")
    frame_4 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_b).grid(row=3, column=0, sticky="nsew")
    frame_5 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_a).grid(row=4, column=0, sticky="nsew")
    frame_6 = tk.Frame(APP_ROOT, padx=2, pady=2, bg=color_b).grid(row=5, column=0, sticky="nsew")

    # Configure Frames
    APP_ROOT.grid_rowconfigure(0, weight=1)
    APP_ROOT.grid_rowconfigure(1, weight=6)
    APP_ROOT.grid_rowconfigure(2, weight=4)
    APP_ROOT.grid_rowconfigure(3, weight=1)
    APP_ROOT.grid_rowconfigure(4, weight=1)
    APP_ROOT.grid_rowconfigure(5, weight=1)

    # # Sections
    # build_section_1_PATHS(frame_1)
    # build_section_2_INFO(frame_2)
    # build_section_3_PREVIEWS(frame_3)
    # build_section_4_UTILS(frame_4)
    # build_section_5_STATUS(frame_5)
    # build_section_6_ACTIONS(frame_6)


if __name__ == "__main__":
    create_app()
    create_sections()
    if APP_ROOT:
        APP_ROOT.mainloop()
    else:
        print("Setup Failed")
