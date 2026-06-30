import tkinter as tk
from tkinter import *
from tkinter import messagebox
import csv
import os
import random

DROPDOWN_BG = "#52455D"
MAIN_BG = "#FEF9E9"       
MAIN_FG = "#1A1A1A"       
BUTTON_BG = "#D9A05B"     
BUTTON_FG = "#FFFFFF"     
TEXT_BG = "#FFFFFF"       
TEXT_FG = "#1A1A1A"       
TEXT_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 13, "bold")
ITEM_AMOUNT_LIMIT = 500
NAME_LENGTH_LIMIT = 30
DATA_FILE = "party_hire_data.csv"

class MainApp:
    def __init__(self, root):
        # Initialization
        self.root = root
        self.root.title("Party Hire Shop")
        self.root.iconbitmap("favicon.ico")
        self.root.geometry("420x680")
        self.root.resizable(False, False) 
        self.root.configure(bg=MAIN_BG)
        self.hired_data = [] 
        self.load_data()
        self.create_widgets()
        self.update_listbox()
        self.root.after(100, self.show_welcome_message)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.hired_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text="🎈 Party Hire Shop 🎈", bg=MAIN_BG, fg=MAIN_FG, font=("Arial", 18, "bold"))
        self.title_label.pack(pady=15)
        
        # Name
        self.name_label = tk.Label(self.root, text="Customer Name:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT, relief=tk.SOLID, bd=1)
        self.name_entry.pack(pady=5, ipady=3)
        self.name_entry.bind('<Return>', self.handle_submit)
        
        # Dropdown
        self.selected = tk.StringVar(self.root)
        self.selected.set("Choose an item")
        
        dropdown = tk.OptionMenu(self.root, self.selected, "Party Hat", "Bouncy Castle", "Table", "Chair", "Cake", "Plate", "Fork", "Knife", "Gas Canister", "Pinata")
        dropdown.config(bg=TEXT_BG, fg=TEXT_FG, activebackground=TEXT_BG, activeforeground=TEXT_FG, relief=tk.SOLID, bd=1)
        dropdown["menu"].config(bg=DROPDOWN_BG, fg=MAIN_BG, activebackground=BUTTON_BG, activeforeground=TEXT_BG)
        dropdown.pack(pady=15) 

        # Item Amount
        self.item_amount_label = tk.Label(self.root, text="Amount of Items:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT)
        self.item_amount_label.pack()
        self.item_amount_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT, relief=tk.SOLID, bd=1)
        self.item_amount_entry.pack(pady=5, ipady=3)
        self.item_amount_entry.bind('<Return>', self.handle_submit) 
        
        # Submit
        self.submit_button = tk.Button(self.root, text="Submit Hire", command=self.handle_submit, bg=BUTTON_BG, fg=BUTTON_FG, font=BUTTON_FONT, cursor="hand1")
        self.submit_button.pack(pady=15, ipadx=10)

        # Current Hires
        tk.Label(self.root, text="Current Hires (Click to auto-fill return):", bg=MAIN_BG, fg=MAIN_FG, font=("Arial", 10, "bold")).pack()
        
        # Listbox & Scrollbar 
        listbox_frame = tk.Frame(self.root, bg=MAIN_BG)
        listbox_frame.pack(pady=5)
        
        self.hired_listbox = tk.Listbox(listbox_frame, width=50, height=10, font=("Arial", 10), relief=tk.SOLID, bd=5)
        self.scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.hired_listbox.yview)
        self.hired_listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.hired_listbox.pack(side=tk.LEFT)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Return Item
        tk.Label(self.root, text="Return by Receipt Number:", bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT).pack(pady=(15, 0))
        self.remove_item_entry = tk.Entry(self.root, bg=TEXT_BG, fg=TEXT_FG, font=TEXT_FONT, relief=tk.SOLID, bd=1)
        self.remove_item_entry.pack(pady=5, ipady=3)
        self.remove_item_entry.bind('<Return>', self.handle_delete) 
        
        self.remove_item_button = tk.Button(self.root, text="Return Item", command=self.handle_delete, bg=BUTTON_BG, fg=BUTTON_FG, font=BUTTON_FONT, cursor="hand1")
        self.remove_item_button.pack(pady=5, ipadx=10)

    def load_data(self):
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
        try:
            with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['receipt', 'name', 'item', 'amount'])
                writer.writeheader()
                writer.writerows(self.hired_data)
            return True
        except IOError as e:
            messagebox.showerror("File Error", f"Could not save data to database.\nReason: {e}")
            return False

    def update_listbox(self):
        self.hired_listbox.delete(0, tk.END)
        for hire in self.hired_data:
            self.hired_listbox.insert(tk.END, f"  {hire['receipt']}: {hire['name']} - {hire['item']} ({hire['amount']})")

    def on_listbox_select(self, event):
        selection = self.hired_listbox.curselection()
        if not selection:
            return
            
        listbox_text = self.hired_listbox.get(selection[0])
        if ":" in listbox_text:
            receipt_num = listbox_text.split(":")[0]
            self.remove_item_entry.delete(0, tk.END)
            self.remove_item_entry.insert(0, receipt_num)

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.item_amount_entry.delete(0, tk.END)
        self.remove_item_entry.delete(0, tk.END)
        self.selected.set("Choose an item")

    def handle_submit(self, event=None):
        name = self.name_entry.get().strip()
        item_amount_raw = self.item_amount_entry.get().strip()
        option = self.selected.get().strip() 

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
            
        existing_receipts = {h['receipt'] for h in self.hired_data}
        attempts = 0
        while attempts < 100:
            receipt = random.randint(1000000000, 9999999999)
            if receipt not in existing_receipts:
                break
            attempts += 1
        else:
            messagebox.showerror("Error", "Failed to generate a unique receipt number. Please try again.")
            return
                
        self.hired_data.append({'receipt': receipt, 'name': name, 'item': option, 'amount': item_amount})
        
        if self.save_data():
            self.update_listbox()
            self.clear_form()
            messagebox.showinfo("Success", f"Successfully hired {option} (x{item_amount}).\nReceipt Number: {receipt}")

    def handle_delete(self, event=None):
        receipt_to_remove = self.remove_item_entry.get().strip()
        if not receipt_to_remove.isdigit():
            messagebox.showwarning("Error", "Please enter a valid numeric receipt number.")
            return
        
        receipt_int = int(receipt_to_remove)
        target_item = next((h for h in self.hired_data if h['receipt'] == receipt_int), None)
        
        if target_item is None:
            messagebox.showwarning("Not Found", "The provided receipt number could not be found.")
        else:
            self.hired_data.remove(target_item) 
            
            if self.save_data():
                self.update_listbox()
                self.clear_form()
                messagebox.showinfo("Success", "Item has been successfully returned.")
            else:
                self.hired_data.append(target_item)

    def show_welcome_message(self):
        messagebox.showinfo("Welcome", "Welcome to the Party Hire Store.\nUse the interface to take out or return hires.")

    def on_closing(self):
        if messagebox.askokcancel("Exit Application", "Are you sure you want to close the store?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()