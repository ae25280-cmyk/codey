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
DROPDOWN_BG = "#2E004E"

class MainApp:
    def __init__(self, root):
        # Initialization
        self.root = root
        self.root.title("Party Hire Shop")
        self.root.geometry("420x680")
        self.root.configure(bg=MAIN_BG)
        self.hired_data = [] 
        self.load_data()
        self.create_widgets()
        self.update_listbox()
        self.root.after(100, self.show_welcome_message)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Return>', lambda event: self.handle_submit())

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text="Party Hire System", bg=MAIN_BG, fg=MAIN_FG, font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        # Name Input
        self.name_label = tk.Label(self.root, text="Customer Name:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.name_entry.pack(pady=5)
        
        # Item Dropdown Menu
        self.selected = tk.StringVar(self.root)
        self.selected.set("Choose an item")
        
        
        dropdown = tk.OptionMenu(self.root, self.selected, "Party Hat", "Bouncy Castle", "Table", "Chair", "Cake")
        dropdown.config(bg=TEXT_BG, fg=TEXT_FG, activebackground=TEXT_BG, activeforeground=TEXT_FG)
        dropdown["menu"].config(bg=DROPDOWN_BG, fg=MAIN_BG, activebackground=MAIN_BG, activeforeground=MAIN_FG)
        dropdown.pack(pady=15) 

        # Item Amount Input
        self.item_amount_label = tk.Label(self.root, text="Amount of Items:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.item_amount_label.pack()
        self.item_amount_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.item_amount_entry.pack(pady=5)
        
        # Submit Button
        self.submit_button = tk.Button(self.root, text="Submit Hire", command=self.handle_submit, bg=BUTTON_BG, fg=BUTTON_FG, font=BUTTON_FONT)
        self.submit_button.pack(pady=10)

        # Current Hires Display Label
        tk.Label(self.root, text="Current Hires (Receipt: Name - Item x Qty):", bg=MAIN_BG, font=("Arial", 10, "bold")).pack()
        
        # Listbox & Scrollbar Frame
        listbox_frame = tk.Frame(self.root)
        listbox_frame.pack(pady=5)
        
        self.hired_listbox = tk.Listbox(listbox_frame, width=45, height=6, font=("Arial", 10))
        self.scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.hired_listbox.yview)
        self.hired_listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.hired_listbox.pack(side=tk.LEFT)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Return Item Section
        tk.Label(self.root, text="Return by Receipt Number:", bg=MAIN_BG, font=TEXT_FONT).pack(pady=(10, 0))
        self.remove_item_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT)
        self.remove_item_entry.pack(pady=5)
        self.remove_item_button = tk.Button(self.root, text="Return Item", command=self.handle_delete, bg=BUTTON_BG, fg=BUTTON_FG, font=BUTTON_FONT)
        self.remove_item_button.pack(pady=5)

    def load_data(self):
        # Loads data from the csv file
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            try:
                with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    if reader.fieldnames and 'receipt' in reader.fieldnames:
                        self.hired_data = []
                        for row in reader:
                            if all(key in row for key in ['receipt', 'name', 'item', 'amount']):
                                self.hired_data.append({
                                    'receipt': int(row['receipt']), 
                                    'name': row['name'],
                                    'item': row['item'], 
                                    'amount': int(row['amount']),
                                })
            except (ValueError, KeyError):
                self.hired_data = []
        else:
            self.hired_data = []

    def save_data(self):
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['receipt', 'name', 'item', 'amount'])
            writer.writeheader()
            writer.writerows(self.hired_data)

    def update_listbox(self):
        # Refreshes UI listbox
        self.hired_listbox.delete(0, tk.END)
        for hire in self.hired_data:
            self.hired_listbox.insert(tk.END, f"{hire['receipt']}: {hire['name']} - {hire['item']} ({hire['amount']})")

    def handle_submit(self):
        name = self.name_entry.get().strip()
        item_amount_raw = self.item_amount_entry.get().strip()
        option = self.selected.get().strip() 

        # Validation
        if not name or not item_amount_raw or option == "Choose an item":
            messagebox.showwarning("Validation Error", "Please complete all fields before submitting.")
            return
        if len(name) > NAME_LENGTH_LIMIT:
            messagebox.showwarning("Validation Error", f"Name exceeds limit (Max {NAME_LENGTH_LIMIT} characters).")
            return
        if not item_amount_raw.isdigit() or int(item_amount_raw) <= 0:
            messagebox.showwarning("Validation Error", "Amount must be a positive whole number.")
            return
        
        item_amount = int(item_amount_raw)
        if item_amount > ITEM_AMOUNT_LIMIT:
            messagebox.showwarning("Validation Error", f"Amount cannot exceed {ITEM_AMOUNT_LIMIT} units.")
            return
            
        # Generate unique receipt number
        while True:
            receipt = random.randint(1000000000, 9999999999)
            if not any(h['receipt'] == receipt for h in self.hired_data):
                break
                
       
        self.hired_data.append({'receipt': receipt, 'name': name, 'item': option, 'amount': item_amount})
        
        self.save_data()
        self.update_listbox()
        
        # Clear fields
        self.name_entry.delete(0, tk.END)
        self.item_amount_entry.delete(0, tk.END)
        self.selected.set("Choose an item") 
        
        # Pluralization
        suffix = "s" if item_amount > 1 else ""
        messagebox.showinfo("Success", f"Successfully hired {item_amount} {option}{suffix}.\nReceipt Number: {receipt}")

    def handle_delete(self):
        # Cleans and handles deletions
        receipt_to_remove = self.remove_item_entry.get().strip()
        if not receipt_to_remove.isdigit():
            messagebox.showwarning("Error", "Please enter a valid numeric receipt number.")
            return
        
        receipt_int = int(receipt_to_remove)
        new_data = [h for h in self.hired_data if h['receipt'] != receipt_int]
        
        if len(new_data) == len(self.hired_data):
            messagebox.showwarning("Not Found", "The provided receipt number could not be found.")
        else:
            self.hired_data = new_data
            self.save_data()
            self.update_listbox()
            self.remove_item_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Item has been successfully returned.")

    def show_welcome_message(self):
        messagebox.showinfo("Welcome", "Welcome to the Party Hire Store.\nUse The interface to take out or return hires.")

    def on_closing(self):
        if messagebox.askokcancel("Exit Application", "Are you sure you want to close the store?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()