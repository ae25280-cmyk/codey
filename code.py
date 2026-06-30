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
ITEM_AMOUNT_LIMIT = 500
RECEIPT_LIMIT = 99999999999999999999
NAME_LENGTH_LIMIT = 30

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Party Hire Shop")
        self.root.geometry("400x550")  
        self.root.configure(bg=MAIN_BG)
        self.create_widgets()
        self.root.after(100, self.show_welcome_message)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Welcome!", bg=MAIN_BG, fg=MAIN_FG, font=("Arial", 16, "bold"))
        self.title_label.pack(pady=15)
        
        self.name_label = tk.Label(self.root, text="Name:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.name_entry.pack(pady=5)
        
        self.receipt_number_label = tk.Label(self.root, text="Receipt Number:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.receipt_number_label.pack(pady=5)
        self.receipt_number_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.receipt_number_entry.pack(pady=5)

        self.selected_option = tk.StringVar(self.root, value="Choose an item")
        self.items = ["Party Hats", "Bouncy Castle", "Chairs", "Tables"]
        self.item_choice = tk.OptionMenu(self.root, self.selected_option, *self.items)
        self.item_choice.pack(pady=10)

        self.item_amount_label = tk.Label(self.root, text="Amount of Items:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.item_amount_label.pack(pady=5)
        self.item_amount_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.item_amount_entry.pack(pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.handle_submit, bg=BUTTON_BG, fg=BUTTON_FG, font=TEXT_FONT, padx=10, pady=5)
        self.submit_button.pack(pady=15)

    def show_welcome_message(self):
        messagebox.showinfo("Notification", "Thank you for opening the Party Hire Shop app!")
    
    def handle_submit(self):
        name = self.name_entry.get().strip().capitalize()
        receipt_raw = self.receipt_number_entry.get().strip()
        item_amount_raw = self.item_amount_entry.get().strip()
        option = self.selected_option.get().strip()

        # Validation Logic
        if not name or not receipt_raw or not item_amount_raw:
            messagebox.showwarning("Missing Information", "Please fill in all boxes.")
            return
            
        if option == "Choose an item":
            messagebox.showwarning("Missing Information", "Please select an item.")
            return
            
        if not name.replace(" ", "").isalpha():
            messagebox.showwarning("Invalid Input", "Name must contain letters only.")
            return

        if not receipt_raw.isdigit() or not item_amount_raw.isdigit():
            messagebox.showwarning("Invalid Input", "Receipt and Amount must be numbers.")
            return

        receipt = int(receipt_raw)
        item_amount = int(item_amount_raw)

        if item_amount <= 0 or item_amount > ITEM_AMOUNT_LIMIT:
            messagebox.showwarning("Invalid Input", f"Amount must be between 1 and {ITEM_AMOUNT_LIMIT}.")
            return
        
        if len(name) > NAME_LENGTH_LIMIT:
            messagebox.showwarning("Invalid Input", f"Name must be under {NAME_LENGTH_LIMIT} characters.")
            return

        # Success Process
        self.save_to_csv(name, receipt, option, item_amount)
        messagebox.showinfo("Success!", f"Saved data for {name}.")

        # Clear fields
        self.name_entry.delete(0, tk.END)
        self.receipt_number_entry.delete(0, tk.END)
        self.item_amount_entry.delete(0, tk.END)
        self.selected_option.set("Choose an item")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to close?"):
            self.root.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
    