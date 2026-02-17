import os
import csv
import hashlib
import uuid
import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import defaultdict
import platform

# ==============================
# MoBiz Manager v19.1
# Secure Mobile Freemium Edition
# Author: Moses Obaro Agbahowe
# Year: 2026
# ==============================

INCOME_FILE = "income_log_v19.txt"
EXPENSE_FILE = "expense_log_v19.txt"
EXPORT_FILE = "mobiz_export_v19.csv"
LICENSE_FILE = "license_v19.key"

# ==============================
# Device ID Generator
# ==============================
def get_device_id():
    raw_id = str(uuid.getnode())
    return hashlib.sha256(raw_id.encode()).hexdigest()[:16].upper()

# ==============================
# Premium License Logic
# ==============================
def _hidden_secret():
    p1 = "M0B"
    p2 = "1Z_"
    p3 = "S3C"
    p4 = "R3T"
    p5 = "_20"
    p6 = "26X"
    return p1 + p2 + p3 + p4 + p5 + p6

def generate_license(device_id):
    system_info = platform.system() + platform.machine()
    raw_string = device_id + system_info + _hidden_secret()
    hash_value = hashlib.sha256(raw_string.encode()).hexdigest().upper()
    formatted = f"{hash_value[:5]}-{hash_value[5:10]}-{hash_value[10:15]}-{hash_value[15:20]}"
    return formatted

def check_license():
    if not os.path.exists(LICENSE_FILE):
        return False
    with open(LICENSE_FILE, "r") as f:
        saved_key = f.read().strip()
    device_id = get_device_id()
    return saved_key == generate_license(device_id)

def save_license(key):
    with open(LICENSE_FILE, "w") as f:
        f.write(key)

# ==============================
# Activate Premium Popup
# ==============================
def activate_license():
    device_id = get_device_id()

    win = tk.Toplevel()
    win.title("Upgrade to Premium")

    # -----------------------------
    # Auto-resize for mobile screens
    # -----------------------------
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    popup_width = int(screen_width * 0.95)
    popup_height = int(screen_height * 0.90)
    win.geometry(f"{popup_width}x{popup_height}+10+10")
    win.resizable(False, False)

    font_small = ("Arial", 6)

    instructions = f"""
MoBiz Manager v19.1 Premium Upgrade

Price:
₦15,000
$10 USD

Device ID:
{device_id}

Payment Methods:
GTBank: 0139721323 (Agbahowe Moses Obaro)
Zenith Bank: 2263287035 (Agbahowe Moses Obaro)
Opay: 9027860267 (Agbahowe Moses Obaro)
PayPal: mosesobiy@gmail.com

After payment:
1. Send proof of payment and include your Device ID to the contact address. (check README)
2. You will receive your License Key.
"""

    text_box = tk.Text(win, font=font_small, wrap="word")
    text_box.pack(fill="both", expand=True, padx=15, pady=15)
    text_box.insert("1.0", instructions)
    text_box.config(state="disabled")

    # COPY DEVICE ID BUTTON
    def copy_device_id():
        win.clipboard_clear()
        win.clipboard_append(device_id)
        messagebox.showinfo("Copied", "Device ID copied successfully!")

    tk.Button(win, text="Copy Device ID", command=copy_device_id).pack(pady=10)

    # LICENSE ENTRY
    tk.Label(win, text="Enter License Key:", font=font_small).pack(pady=(20,5))
    license_entry = tk.Entry(win, font=font_small, width=50)
    license_entry.pack(pady=5)

    def verify_license():
        entered_key = license_entry.get().strip()
        device_id = get_device_id()
        expected_key = generate_license(device_id)
        if entered_key == expected_key:
            save_license(entered_key)
            messagebox.showinfo("Success", "Premium Activated Successfully!")
            win.destroy()
        else:
            messagebox.showerror("Error", "Invalid License Key")

    tk.Button(win, text="Activate Premium", command=verify_license).pack(pady=15)
    tk.Button(win, text="Cancel", command=win.destroy).pack(pady=5)

# ==============================
# Show Premium Info
# ==============================
def show_premium_info(master):
    messagebox.showinfo("Premium Feature", "Upgrade to Premium to access this feature.")

# ==============================
# Main App
# ==============================
class MoBizApp:

    def __init__(self, master):
        self.master = master
        self.master.title("MoBiz Manager v19.1 - Secure Mobile Freemium")
        self.premium = check_license()
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.master, text="Add Income", command=self.add_income).pack(fill="x")
        tk.Button(self.master, text="Add Expense", command=self.add_expense).pack(fill="x")
        tk.Button(self.master, text="Profit Summary", command=self.profit_summary).pack(fill="x")
        tk.Button(self.master, text="Export CSV", command=self.export_csv).pack(fill="x")

        tk.Label(self.master, text="--- PREMIUM FEATURES ---").pack()

        if self.premium:
            tk.Button(self.master, text="Monthly Summary", command=self.monthly_summary).pack(fill="x")
            tk.Button(self.master, text="Expense Category Breakdown", command=self.category_summary).pack(fill="x")
            tk.Button(self.master, text="Project Calculator", command=self.project_calculator).pack(fill="x")
        else:
            tk.Button(self.master, text="🔒 Monthly Summary", command=lambda: show_premium_info(self.master)).pack(fill="x")
            tk.Button(self.master, text="🔒 Expense Category Breakdown", command=lambda: show_premium_info(self.master)).pack(fill="x")
            tk.Button(self.master, text="🔒 Project Calculator", command=lambda: show_premium_info(self.master)).pack(fill="x")

        tk.Button(self.master, text="Upgrade to Premium", command=activate_license, fg="blue").pack(fill="x", pady=(5,2))
        tk.Button(self.master, text="README / Info", command=self.show_readme, fg="green").pack(fill="x", pady=(2,2))
        tk.Button(self.master, text="Exit", command=self.master.destroy, fg="red").pack(fill="x", pady=(5,5))

    # Free Features
    def write_record(self, filename, record):
        with open(filename, "a") as f:
            f.write(record + "\n")

    def read_records(self, filename):
        if not os.path.exists(filename):
            return []
        with open(filename, "r") as f:
            return [line.strip().split(",") for line in f.readlines()]

    def add_income(self):
        amount = simpledialog.askfloat("Income", "Enter amount:")
        date = simpledialog.askstring("Date", "Enter date (YYYY-MM-DD):")
        if amount and date:
            self.write_record(INCOME_FILE, f"{date},{amount}")
            messagebox.showinfo("Saved", "Income recorded.")

    def add_expense(self):
        amount = simpledialog.askfloat("Expense", "Enter amount:")
        category = simpledialog.askstring("Category", "Enter category:")
        date = simpledialog.askstring("Date", "Enter date (YYYY-MM-DD):")
        if amount and category and date:
            self.write_record(EXPENSE_FILE, f"{date},{category},{amount}")
            messagebox.showinfo("Saved", "Expense recorded.")

    def profit_summary(self):
        incomes = sum(float(r[1]) for r in self.read_records(INCOME_FILE)) if self.read_records(INCOME_FILE) else 0
        expenses = sum(float(r[2]) for r in self.read_records(EXPENSE_FILE)) if self.read_records(EXPENSE_FILE) else 0
        profit = incomes - expenses
        messagebox.showinfo("Profit Summary", f"Total Income: {incomes}\nTotal Expense: {expenses}\nNet Profit: {profit}")

    def export_csv(self):
        incomes = self.read_records(INCOME_FILE)
        expenses = self.read_records(EXPENSE_FILE)

        with open(EXPORT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Date", "Category", "Amount"])
            for inc in incomes:
                writer.writerow(["Income", inc[0], "-", inc[1]])
            for exp in expenses:
                writer.writerow(["Expense", exp[0], exp[1], exp[2]])

        messagebox.showinfo("Exported", f"Data exported to {EXPORT_FILE}")

    # Premium Features
    def monthly_summary(self):
        if not self.premium:
            messagebox.showwarning("Premium Required", "Upgrade to Premium to use this feature.")
            return
        monthly = defaultdict(float)
        for r in self.read_records(INCOME_FILE):
            month = r[0][:7]
            monthly[month] += float(r[1])
        for r in self.read_records(EXPENSE_FILE):
            month = r[0][:7]
            monthly[month] -= float(r[2])
        result = "\n".join([f"{m}: {monthly[m]}" for m in monthly])
        messagebox.showinfo("Monthly Summary", result)

    def category_summary(self):
        if not self.premium:
            messagebox.showwarning("Premium Required", "Upgrade to Premium to use this feature.")
            return
        categories = defaultdict(float)
        for r in self.read_records(EXPENSE_FILE):
            categories[r[1]] += float(r[2])
        result = "\n".join([f"{c}: {categories[c]}" for c in categories])
        messagebox.showinfo("Category Breakdown", result)

    def project_calculator(self):
        if not self.premium:
            messagebox.showwarning("Premium Required", "Upgrade to Premium to use this feature.")
            return
        base = simpledialog.askfloat("Project Calculator", "Enter base cost:")
        profit_percent = simpledialog.askfloat("Project Calculator", "Enter profit percentage:")
        tax_percent = simpledialog.askfloat("Project Calculator", "Enter tax percentage:")
        if base is None or profit_percent is None or tax_percent is None:
            return
        profit_amount = base * (profit_percent / 100)
        tax_amount = base * (tax_percent / 100)
        final_price = base + profit_amount + tax_amount
        messagebox.showinfo("Project Calculator",
                            f"Base Cost: {base}\nProfit: {profit_amount}\nTax: {tax_amount}\nFinal Price: {final_price}")

    # README / Info Popup with CLOSE button
    def show_readme(self):
        readme_win = tk.Toplevel(self.master)
        readme_win.title("MoBiz Manager v19.1 - Info / README")

        # Auto-resize
        readme_win.update_idletasks()
        screen_width = readme_win.winfo_screenwidth()
        screen_height = readme_win.winfo_screenheight()
        popup_width = int(screen_width * 0.95)
        popup_height = int(screen_height * 0.90)
        readme_win.geometry(f"{popup_width}x{popup_height}+10+10")
        readme_win.resizable(False, False)

        font_small = ("Arial", 6)
        text_box = tk.Text(readme_win, font=font_small, wrap="word")
        text_box.pack(fill="both", expand=True, padx=15, pady=10)

        readme_content = f"""
MoBiz Manager v19.1 - Secure Mobile Freemium Edition

📌 Free Features
- Add Income
- Add Expense
- Profit Summary
- Export CSV

🔒 Premium Features
- Monthly Summary
- Expense Category Breakdown
- Project Calculator

💳 Premium Price
- ₦15,000 / $10 USD

Payment Methods:
GTBank: 0139721323 (Agbahowe Moses Obaro)
Zenith Bank: 2263287035 (Agbahowe Moses Obaro)
Opay: 9027860267 (Agbahowe Moses Obaro)
PayPal: mosesobiy@gmail.com

📝 How to Upgrade
- Click Upgrade to Premium
- Copy your Device ID
- Send proof of ID to the contact address below to get your License Key

📧 Contact
- Email: mosesobiy@gmail.com
- Email: mosesagbahowe@gmail.com
- WhatsApp: +2349027860267
"""
        text_box.insert("1.0", readme_content)
        text_box.config(state="disabled")  # not editable

        # CLOSE BUTTON
        tk.Button(readme_win, text="Close", command=readme_win.destroy, font=("Arial",6)).pack(pady=10)

# ==============================
# Run App
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = MoBizApp(root)
    root.mainloop()
