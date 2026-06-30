import tkinter as tk
from tkinter import messagebox

MAIN_BG = "#ffffff"
MAIN_FG = "#333333"
BUTTON_BG = "#454853"
BUTTON_FG = "#b0a5a5"
TEXT_BG = "#f0f0f0"
TEXT_FG = "#333333"
TEXT_FONT = ("Arial", 12)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Party Hire Shop")
        self.root.geometry("400x300")
        self.root.configure(bg=MAIN_BG)
        self.create_widgets()
        self.show_welcome_message()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    def create_widgets(self):
        self.label = tk.Label(self.root, text="Welcome to the Party Hire Shop!", bg=MAIN_BG, fg=MAIN_FG, font=("Arial", 16))
        self.label.pack(pady=20)
        self.hire_button = tk.Button(self.root, text="Hire Equipment", bg=BUTTON_BG, fg=BUTTON_FG, font=TEXT_FONT, command=self.hire_equipment)
        self.hire_button.pack(pady=10)
        self.exit_button = tk.Button(self.root, text="Quit", bg=BUTTON_BG, fg=BUTTON_FG, font=TEXT_FONT, command=self.on_closing)
        self.exit_button.pack(pady=10)