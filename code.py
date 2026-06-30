import tkinter as tk
from tkinter import messagebox

# Styling Constants
MAIN_BG = "#ffffff"
MAIN_FG = "#333333"
BUTTON_BG = "#454853"
BUTTON_FG = "#ffffff" 
TEXT_BG = "#f0f0f0"
TEXT_FG = "#333333"
TEXT_FONT = ("Arial", 12)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Party Hire Shop")
        self.root.geometry("400x380")  
        self.root.configure(bg=MAIN_BG)
        self.create_widgets()
        self.show_welcome_message()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Welcome to the Party Hire Shop!", bg=MAIN_BG, fg=MAIN_FG, font=("Arial", 16, "bold"))
        self.title_label.pack(pady=20)
        
        self.name_label = tk.Label(self.root, text="Please enter your name to continue:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.name_entry.pack(pady=5)
        
        self.age_label = tk.Label(self.root, text="Please also enter your age:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.age_label.pack(pady=5)
        self.age_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.age_entry.pack(pady=5)
        
        self.email_label = tk.Label(self.root, text="Please also enter your email:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.email_entry.pack(pady=5)

        self.submit_button = tk.Button(
            self.root, 
            text="Submit", 
            command=self.handle_submit, 
            bg=BUTTON_BG, 
            fg=BUTTON_FG, 
            font=TEXT_FONT,
            padx=10,
            pady=5
        )
        self.submit_button.pack(pady=20)