import tkinter as tk
from tkinter import messagebox
import csv
import os
import random

# Constants
MAIN_BG = "#ffe600"
MAIN_FG = "#000000"
BUTTON_BG = "#E6981A"
BUTTON_FG = "#000000" 
TEXT_BG = "#fffb00"
TEXT_FG = "#000000"
TEXT_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 13)
ITEM_AMOUNT_LIMIT = 500
NAME_LENGTH_LIMIT = 30
DATA_FILE = "party_hire_data.csv"

class MainApp:
    def __init__(self, root):
        # Initialization
        self.root = root
        self.root.title("Party Hire Shop")
        self.root.geometry("400x650")  
        self.root.configure(bg=MAIN_BG)
        self.hired_data = [] 
        self.load_data()
        self.create_widgets()
        self.update_listbox()
        self.root.after(100, self.show_welcome_message)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Return>', lambda event: self.handle_submit())
 

    def create_widgets(self):
        # Creates the labels and buttons and dropdowns and input areas aswell as the area with previous hires
        self.title_label = tk.Label(self.root, text="Welcome.", bg=MAIN_BG, fg=MAIN_FG, font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        self.name_label = tk.Label(self.root, text="Name:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.name_entry.pack(pady=5)
        
        self.selected_option = tk.StringVar(self.root, value="Choose an item")
        self.items = ["Party Hat", "Bouncy Castle", "Chair", "Table"]
        self.item_choice = tk.OptionMenu(self.root, self.selected_option, *self.items)
        self.item_choice.pack(pady=5)

        self.item_amount_label = tk.Label(self.root, text="Amount of Items:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.item_amount_label.pack()
        self.item_amount_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.item_amount_entry.pack(pady=5)
        
        self.submit_button = tk.Button(self.root, text="Submit", command=self.handle_submit, bg=BUTTON_BG, fg=BUTTON_FG, font=BUTTON_FONT)
        self.submit_button.pack(pady=10)

        tk.Label(self.root, text="Current Hires (Receipt: Item):", bg=MAIN_BG).pack()
        self.hired_listbox = tk.Listbox(self.root, width=50, height=6)
        self.hired_listbox.pack(pady=5)
        
        tk.Label(self.root, text="Return by Receipt Number:", bg=MAIN_BG).pack()
        self.remove_item_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.remove_item_entry.pack(pady=5)
        self.remove_item_button = tk.Button(self.root, text="Return", command=self.handle_delete, bg=BUTTON_BG, fg=BUTTON_FG, font=BUTTON_FONT)
        self.remove_item_button.pack(pady=5)

    def load_data(self):
        # Loads the data in the csv file
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            try:
                with open(DATA_FILE, mode='r', newline='') as file:
                    reader = csv.DictReader(file)
                    if reader.fieldnames and 'receipt' in reader.fieldnames:
                        self.hired_data = []
                        for row in reader:
                            if all(key in row for key in ['receipt', 'item', 'amount']):
                                self.hired_data.append({
                                    'receipt': int(row['receipt']), 
                                    'item': row['item'], 
                                    'amount': int(row['amount']),
                                })
            except (ValueError, KeyError):
                self.hired_data = []
        else:
            self.hired_data = []

    def save_data(self):
        # adds data to csv file
        with open(DATA_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['receipt', 'item', 'amount'])
            writer.writeheader()
            writer.writerows(self.hired_data)

    def update_listbox(self):
        # show hired items
        self.hired_listbox.delete(0, tk.END)
        for hire in self.hired_data:
            self.hired_listbox.insert(tk.END, f"{hire['receipt']}: {hire['item']} ({hire['amount']})")

    def handle_submit(self):
        name = self.name_entry.get().strip()
        item_amount_raw = self.item_amount_entry.get().strip()
        option = self.selected_option.get().strip()

        # Validation
        if not name or not item_amount_raw or option == "Choose an item":
            messagebox.showwarning("Error", "Please fill in all fields.")
            return
        if len(name) > NAME_LENGTH_LIMIT:
            messagebox.showwarning("Error", f"Name too long (Max {NAME_LENGTH_LIMIT} characters).")
            return
        if not item_amount_raw.isdigit() or int(item_amount_raw) <= 0:
            messagebox.showwarning("Error", "Amount must be a positive number.")
            return
        
        item_amount = int(item_amount_raw)
        if item_amount > ITEM_AMOUNT_LIMIT:
            messagebox.showwarning("Error", f"Amount cannot exceed {ITEM_AMOUNT_LIMIT}.")
            return
        # Get reciept number
        receipt = random.randint(1000000000, 9999999999)
        self.hired_data.append({'receipt': receipt, 'item': option, 'amount': item_amount})
        
        self.save_data()
        self.update_listbox()
        
        # Clear fields
        self.name_entry.delete(0, tk.END)
        self.item_amount_entry.delete(0, tk.END)
        self.selected_option.set("Choose an item")
        if item_amount == 1:
            messagebox.showinfo("Success", f"Hired {item_amount} {option}. Receipt: {receipt}")
        elif item_amount > 1:
            messagebox.showinfo("Success", f"Hired {item_amount} {option}s. Receipt: {receipt}")

    def handle_delete(self):
        # Deletes chosen reciept number
        receipt_to_remove = self.remove_item_entry.get().strip()
        if not receipt_to_remove.isdigit():
            messagebox.showwarning("Error", "That aint correct.")
            return
        
        receipt_int = int(receipt_to_remove)
        new_data = [h for h in self.hired_data if h['receipt'] != receipt_int]
        
        if len(new_data) == len(self.hired_data):
            messagebox.showwarning("Not Found", "That number aint there or ya code broken.")
        else:
            self.hired_data = new_data
            self.save_data()
            self.update_listbox()
            self.remove_item_entry.delete(0, tk.END)
            messagebox.showinfo("Deleted", "item gone ya did ya code gooooood.")

    def show_welcome_message(self):
        #Welcome people
        messagebox.showinfo("Welcome", "Welcome and bla bla bla ya know change when actually turn in.")

    def on_closing(self):
        # if they want to close need confirmation
        if messagebox.askokcancel("Quit", "Please dont delete me man i promise ill be good."):
            self.root.destroy()

if __name__ == "__main__":
    #Runs the code
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()